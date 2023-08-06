#!/usr/bin/env python3
# coding=utf-8
# Copyright 2018 Google AI, Google Brain and Carnegie Mellon University Authors and the HuggingFace Inc. team.
# Copyright (c) 2018, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" Conditional text generation with the auto-regressive models of the library (GPT/GPT-2/Transformer-XL/XLNet)
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
import torch
import torch.nn.functional as F
from pytorch_transformers import GPT2Config

from models.model import GPT2VisionAttentiveLMHead
from models.detector_feature import SimpleDetector
from models.object_detector import ObjectDetector

from dataloaders.tokenizers import VCRAtomicGpt2Tokenizer
from dataloaders.box_utils import load_image, to_tensor_and_normalize, resize_image


NUM_MAX_BOXES = 15
MAX_IMAGE = 17
MAX_EVENT = 28
MAX_PLACE= 22
MAX_RELATION = 18
MAX_SEQ_LEN = 192
        

def set_seed(seed):
    n_gpu = torch.cuda.device_count()
    np.random.seed(seed)
    torch.manual_seed(seed)
    if n_gpu > 0:
        torch.cuda.manual_seed_all(seed)

def sample_sequence(model, length, context, img_feats, boxes, boxes_mask, objects, segments, person_ids, subject_ids,
                    do_sample=True, num_samples=5, temperature=1, top_k=0, top_p=0.9):

    img_feats = img_feats.repeat(num_samples, 1, 1, 1)
    boxes = boxes.repeat(num_samples, 1, 1)
    boxes_mask = boxes_mask.repeat(num_samples, 1)
    objects = objects.repeat(num_samples, 1)
    person_ids = person_ids.repeat(num_samples, 1)
    subject_ids = subject_ids.repeat(num_samples, 1)

    generated = context

    with torch.no_grad():
        for tok_idx in range(length):

            inputs = {'input_ids': generated}

            if img_feats is not None:
                inputs = {
                    'input_ids': generated,
                    'img_feats': img_feats,
                    'boxes': boxes,
                    'boxes_mask': boxes_mask,
                    'objects': objects,
                    'segments': segments,
                    'person_ids': person_ids,
                    'subject_ids': subject_ids
                }

            outputs = model(
                **inputs)  # Note: we could also use 'past' with GPT-2/Transfo-XL/XLNet (cached hidden-states)
            next_token_logits = outputs[0][:, -1, :] / temperature
            if do_sample:
                filtered_logits = top_k_top_p_filtering(next_token_logits, top_k=top_k, top_p=top_p)
                next_token = torch.multinomial(F.softmax(filtered_logits, dim=-1),
                                               num_samples=1)
            else:
                next_token = torch.argmax(next_token_logits, dim=-1).unsqueeze(-1)

            generated = torch.cat((generated, next_token), dim=-1)
    return generated

def top_k_top_p_filtering(logits, top_k=0, top_p=0.0, filter_value=-float('Inf')):
    """ Filter a distribution of logits using top-k and/or nucleus (top-p) filtering
        Args:
            logits: logits distribution shape (vocabulary size)
            top_k > 0: keep only top k tokens with highest probability (top-k filtering).
            top_p > 0.0: keep the top tokens with cumulative probability >= top_p (nucleus filtering).
                Nucleus filtering is described in Holtzman et al. (http://arxiv.org/abs/1904.09751)
        From: https://gist.github.com/thomwolf/1a5a29f6962089e871b94cbd09daf317
    """
    # assert logits.dim() == 1  # batch size 1 for now - could be updated for more but the code would be less clear
    top_k = min(top_k, logits.size(-1))  # Safety check
    if top_k > 0:
        # Remove all tokens with a probability less than the last token of the top-k
        indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
        logits[indices_to_remove] = filter_value

    if top_p > 0.0:
        # sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        # cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)
        #
        # # Remove tokens with cumulative probability above the threshold
        # sorted_indices_to_remove = cumulative_probs > top_p
        #
        # # Shift the indices to the right to keep also the first token above the threshold
        # sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
        # sorted_indices_to_remove[..., 0] = 0

        # indices_to_remove = sorted_indices[sorted_indices_to_remove].scatter(1, sorted_indices, sorted_indices_to_remove)
        # logits[indices_to_remove] = filter_value

        probs = F.softmax(logits, dim=1)
        sorted_probs, sorted_indices = torch.sort(probs, descending=True, dim=1)

        _cumsum = sorted_probs.cumsum(1)
        mask = _cumsum < top_p
        mask = torch.cat([torch.ones_like(mask[:, :1]), mask[:, :-1]], 1)
        sorted_probs = sorted_probs * mask.float()
        sorted_probs = sorted_probs / sorted_probs.sum(1, keepdim=True)

        logits.scatter_(1, sorted_indices, sorted_probs.log())

    return logits

def _pad_ids(ids, max_len):
    if len(ids) >= max_len:
        return ids[:max_len]
    else:
        return ids + [0] * (max_len - len(ids))

def _combine_and_pad_tokens(tokenizer: VCRAtomicGpt2Tokenizer, tokens,
                            max_image, max_event, max_place, max_relation, max_seq_len):
    """
    :param tokenizer: tokenizer for the model
    :param tokens: [[image_tokens], [event_tokens], [place_tokens], [relation_tokens] ]
    :param max_seq_len: maximum sequence for concatenated tokens
    :return: Padded tokens to max length for each set (image, event, place, relation) and concatenated version of the set
    """
    new_tokens = []
    max_lens = [max_image, max_event, max_place, max_relation]
    assert len(tokens) == len(max_lens)
    for i, t in enumerate(tokens):
        max_len = max_lens[i]
        if len(t) > max_len:
            if i < 3:
                if i == 0:
                    end_token = tokenizer.end_img
                elif i == 1:
                    end_token = tokenizer.end_event
                elif i == 2:
                    end_token = tokenizer.end_place
                t = t[:max_len - 1] + [end_token]
        else:
            t.extend([tokenizer.unk_token] * (max_len - len(t)))
        new_tokens.extend(t)

    if len(new_tokens) > max_seq_len:
        new_tokens = new_tokens[:max_seq_len - 1] + [tokenizer.end_relation]
    else:
        new_tokens.extend([tokenizer.unk_token] * (max_seq_len - len(new_tokens)))

    return new_tokens

def _to_boxes_and_masks(boxes, obj_labels, num_max_boxes):
    num_boxes = len(boxes)
    if num_boxes > num_max_boxes:
        return boxes[:num_max_boxes,: ], obj_labels[:num_max_boxes], [1] * num_max_boxes
    padded_boxes = np.concatenate((boxes, np.zeros((num_max_boxes - num_boxes, 4))))
    padded_obj_labels = np.concatenate((obj_labels, np.zeros(num_max_boxes - num_boxes)), axis=0)

    mask = np.concatenate((np.ones(num_boxes), np.zeros(num_max_boxes - num_boxes)), axis=0)

    return padded_boxes, padded_obj_labels, mask

def _get_example_token(tokenizer: VCRAtomicGpt2Tokenizer,
                         relation='intent',
                         num_max_boxes=15,
                         ):
    event = 'event'
    place = 'place'
    relation = relation
    inference = 'inference'

    training_instance = [[tokenizer.begin_img] + [tokenizer.unk_token] * num_max_boxes + [tokenizer.end_img]]
    training_instance.append([tokenizer.begin_event,event,tokenizer.end_event])
    training_instance.append([tokenizer.begin_place,place,tokenizer.end_place])
    training_instance.append([tokenizer.begin_relations[relation],inference,tokenizer.end_relation])

    return training_instance

# create context input for generation
def _get_context(tokenizer, relation='intent'):
    tokens = _get_example_token(tokenizer, relation)
    tokens = [tokenizer.tokenize(" ".join(vt)) for vt in tokens]
    assert len(tokens) == 4

    padded_tokens = _combine_and_pad_tokens(tokenizer, tokens,
                                            MAX_IMAGE, MAX_EVENT, MAX_PLACE, MAX_RELATION, MAX_SEQ_LEN)
    tokenized_text = tokenizer.convert_tokens_to_ids(padded_tokens)
    return tokenized_text

def _insert_seq(tokenizer, tokenized_text, sentence, start_insert, end_insert, max_len):

    start_token = tokenizer.convert_tokens_to_ids([start_insert])[0]
    start_idx = tokenized_text.index(start_token)
    end_token = tokenizer.convert_tokens_to_ids([end_insert])[0]
    end_idx = tokenized_text.index(end_token)
    assert end_idx > start_idx

    sentence_token = tokenizer.tokenize(sentence)
    sentence_token = tokenizer.convert_tokens_to_ids(sentence_token)[:max_len-2]
    l = len(sentence_token)
    tokenized_text[start_idx+1: start_idx+1+l] = sentence_token
    tokenized_text[start_idx+1+l] = end_token

    return tokenized_text

def _remove_seq(tokenizer, tokenized_text, start_remove, end_remove):

    start_token = tokenizer.convert_tokens_to_ids([start_remove])[0]
    start_idx = tokenized_text.index(start_token)
    end_token = tokenizer.convert_tokens_to_ids([end_remove])[0]
    end_idx = tokenized_text.index(end_token)
    assert end_idx > start_idx

    unk_id = tokenizer.convert_tokens_to_ids([tokenizer.unk_token])[0]
    tokenized_text[start_idx: end_idx + 1] = [unk_id] * (end_idx - start_idx + 1)

    return tokenized_text

def _clean_up_end(out, end_token, pad_token):
    ending_idx = (out == end_token).nonzero()
    processed = []
    for i in range(ending_idx.size(0)):
        sample_idx = ending_idx[i][0].item()
        if sample_idx not in processed:
            processed.append(sample_idx)
            end_idx = ending_idx[i][1].item()
            if end_idx < out.size(1) - 1:
                out[sample_idx, end_idx + 1:] = pad_token
    return out

class VisualCOMET:
    def __init__(self, model_name_or_path):

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        config = GPT2Config.from_pretrained(model_name_or_path)
        self.tokenizer = VCRAtomicGpt2Tokenizer.from_pretrained(model_name_or_path)
        self.sd = SimpleDetector(pretrained=True, final_dim=config.n_embd).cuda().eval()
        self.model = GPT2VisionAttentiveLMHead.from_pretrained(model_name_or_path)
        self.model.to(device)
        self.model.eval()

        self.object_detector = ObjectDetector()

    def tokenize_sentence(self, sentence):
        return self.tokenizer.tokenize(sentence)

    def convert_tokens_to_ids(self, tokens):
        return self.tokenizer.convert_tokens_to_ids(tokens)

    def detect_objects(self, image_path):
        return self.object_detector.detect_objects(image_path)

    def detect_people_bounding_boxes(self, image_path):
        vis_info = self.detect_objects(image_path)
        boxes = np.array([b for i,b in enumerate(vis_info['boxes']) if vis_info['classes'][i] == 1])

        return boxes

    def get_global_visual_features_for_person(self, image_path, person_id):
        image, boxes, window = self.__get_boxes(image_path)

        obj_labels, person_ids = self.__get_object_labels_and_person_ids(boxes)
        if person_id < 1 or person_id > len(obj_labels) or person_id > len(person_ids):
            raise ValueError('person_id must be a valid id for the image')
            
        i = person_id - 1
        if obj_labels[i] == 1:
            person_ids[i] = self.tokenizer.convert_tokens_to_ids(['<|det%d|>' % person_id])[0]

        boxes, boxes_mask, objects, person_ids = self.__get_global_visual_features(boxes, window, obj_labels, person_ids)

        return image, boxes, boxes_mask, objects, person_ids

    def get_global_visual_features(self, image_path):
        image, boxes, window = self.__get_boxes(image_path)

        obj_labels, person_ids = self.__get_object_labels_and_person_ids(boxes)
        p_id = 0
        for i in range(len(person_ids)):
            if obj_labels[i] == 1:
                p_id +=1  # add 1 for person ids because it starts with 1
                person_ids[i] = self.tokenizer.convert_tokens_to_ids(['<|det%d|>' % p_id])[0]

        boxes, boxes_mask, objects, person_ids = self.__get_global_visual_features(boxes, window, obj_labels, person_ids)

        return image, boxes, boxes_mask, objects, person_ids

    def process_image(self, image):
        return self.sd(image)

    def get_subject_ids(self, num_subjects, subjects):
        subject_ids = [0] * num_subjects
        if type(subjects) == int:
            assert subjects <= num_subjects and subjects > 0, 'subject id (%d) should be between 1 and %d' % (subjects,num_subjects)
            subject_ids[subjects-1] = 1
        elif type(subjects) is list:
            for s in subjects:
                assert type(s) is int
                assert s <= num_subjects and s > 0, 'subject id (%d) should be between 1 and %d' % (s,num_subjects)
                subject_ids[s] = 1
        else :
            raise TypeError('subjects should be either an integer or list of integers')
        subject_ids = _pad_ids(subject_ids, NUM_MAX_BOXES)

        return torch.LongTensor(subject_ids)

    def generate_event(self, img_feats, boxes, boxes_mask, objects, person_ids, subject_ids):
        do_sample = False
        num_samples = 1

        # remove event tokens
        context = _get_context(self.tokenizer)
        context = torch.tensor(context).unsqueeze(0).repeat(num_samples, 1).cuda()

        prompt_token_idx = self.convert_tokens_to_ids([self.tokenizer.begin_event])[0]
        end_token = self.convert_tokens_to_ids([self.tokenizer.end_event])[0]
        pad_token = self.convert_tokens_to_ids([self.tokenizer.unk_token])[0]

        idx_of_prompt_token = (context == prompt_token_idx).nonzero()[0][1].item()
        context[:, idx_of_prompt_token] = prompt_token_idx
        context_input = context[:, :idx_of_prompt_token + 1]

        out = sample_sequence(
            model=self.model,
            context=context_input,
            img_feats=img_feats,
            boxes=boxes,
            boxes_mask=boxes_mask,
            objects=objects,
            segments=None,
            length=20,
            temperature=1,
            top_p=0.9,
            do_sample=do_sample,
            num_samples=num_samples,
            person_ids=person_ids,
            subject_ids=subject_ids
        )

        out = out[:, idx_of_prompt_token + 1:]
        out[:, -1] = end_token
        out = _clean_up_end(out, end_token, pad_token)

        text = [self.tokenizer.decode(o, skip_special_tokens=True, clean_up_tokenization_spaces=True) for o in
                out.tolist()]
        return text
        

    def generate_place(self, img_feats, boxes, boxes_mask, objects, person_ids, subject_ids):
        do_sample = False
        num_samples = 1

        # remove event tokens
        context = _get_context(self.tokenizer)
        context = _remove_seq(self.tokenizer,context,self.tokenizer.begin_event, self.tokenizer.end_event)
        context = torch.tensor(context).unsqueeze(0).repeat(num_samples, 1).cuda()

        prompt_token_idx = self.convert_tokens_to_ids([self.tokenizer.begin_place])[0]
        end_token = self.convert_tokens_to_ids([self.tokenizer.end_place])[0]
        pad_token = self.convert_tokens_to_ids([self.tokenizer.unk_token])[0]

        idx_of_prompt_token = (context == prompt_token_idx).nonzero()[0][1].item()
        context[:, idx_of_prompt_token] = prompt_token_idx
        context_input = context[:, :idx_of_prompt_token + 1]

        out = sample_sequence(
            model=self.model,
            context=context_input,
            img_feats=img_feats,
            boxes=boxes,
            boxes_mask=boxes_mask,
            objects=objects,
            segments=None,
            length=20,
            temperature=1,
            top_p=0.9,
            do_sample=do_sample,
            num_samples=num_samples,
            person_ids=person_ids,
            subject_ids=subject_ids
        )

        out = out[:, idx_of_prompt_token + 1:]
        out[:, -1] = end_token
        out = _clean_up_end(out, end_token, pad_token)

        text = [self.tokenizer.decode(o, skip_special_tokens=True, clean_up_tokenization_spaces=True) for o in
                out.tolist()]
        return text


    def generate_inference(self, img_feats, boxes, boxes_mask, objects, person_ids, subject_ids, relation, event=None, place=None):
        set_seed(42)
        num_samples = 5
        do_sample = True

        context = _get_context(self.tokenizer, relation=relation)
        if event:
            context = _insert_seq(self.tokenizer, context, event, self.tokenizer.begin_event, self.tokenizer.end_event, MAX_EVENT)
        else:
            context = _remove_seq(self.tokenizer, context, self.tokenizer.begin_event, self.tokenizer.end_event)
        if place:
            context = _insert_seq(self.tokenizer, context, place, self.tokenizer.begin_place, self.tokenizer.end_place, MAX_PLACE)
        else:
            context = _remove_seq(self.tokenizer, context, self.tokenizer.begin_place, self.tokenizer.end_place)

        context = torch.tensor(context).unsqueeze(0).repeat(num_samples, 1).cuda()

        prompt_token_idx = self.convert_tokens_to_ids([self.tokenizer.begin_relations[relation]])[0]
        end_token = self.convert_tokens_to_ids([self.tokenizer.end_relation])[0]
        pad_token = self.convert_tokens_to_ids([self.tokenizer.unk_token])[0]

        idx_of_prompt_token = (context == prompt_token_idx).nonzero()[0][1].item()
        context[:, idx_of_prompt_token] = prompt_token_idx
        context_input = context[:, :idx_of_prompt_token + 1]

        out = sample_sequence(
            model=self.model,
            context=context_input,
            img_feats=img_feats,
            boxes=boxes,
            boxes_mask=boxes_mask,
            objects=objects,
            segments=None,
            length=20,
            temperature=1,
            top_p=0.9,
            do_sample=do_sample,
            num_samples=num_samples,
            person_ids=person_ids,
            subject_ids=subject_ids
        )

        out = out[:, idx_of_prompt_token + 1:]
        out[:, -1] = end_token
        out = _clean_up_end(out, end_token, pad_token)

        text = [self.tokenizer.decode(o, skip_special_tokens=True, clean_up_tokenization_spaces=True) for o in
                out.tolist()]
        return text

    def __get_boxes(self, image_path):
        #######
        # Compute Image Features. Adapted from https://github.com/rowanz/r2c/blob/master/dataloaders/vcr.py
        #######
        image = load_image(image_path)
        image, window, img_scale, padding = resize_image(image, random_pad=False)
        image = to_tensor_and_normalize(image)
        c, h, w = image.shape

        # Detect all objects in the image using detectron2 https://github.com/facebookresearch/detectron2
        # Keep only person (indexed by 1)
        boxes = self.detect_people_bounding_boxes(image_path)

        # Possibly rescale them if necessary
        boxes *= img_scale
        boxes[:, :2] += np.array(padding[:2])[None]
        boxes[:, 2:] += np.array(padding[:2])[None]

        assert np.all((boxes[:, 0] >= 0.) & (boxes[:, 0] < boxes[:, 2]))
        assert np.all((boxes[:, 1] >= 0.) & (boxes[:, 1] < boxes[:, 3]))
        if not np.all((boxes[:, 2] <= w)):
            boxes[:,2] = np.clip(boxes[:,2],None,w)
        if not np.all((boxes[:, 3] <= h)):
            boxes[:, 3] = np.clip(boxes[:, 3], None, h)

        return image, boxes, window

    def __get_object_labels_and_person_ids(self, boxes): 
        obj_labels = [1] * len(boxes)
        person_ids = [0] * len(obj_labels)

        return (obj_labels, person_ids)

    def __get_global_visual_features(self, boxes, window, obj_labels, person_ids):
        # add entire image as another input
        boxes = np.row_stack((window, boxes))
        obj_labels = [0] + obj_labels
        person_ids = [self.tokenizer.convert_tokens_to_ids(['<|det0|>'])[0]] + person_ids

        # pad to max number of boxes
        padded_boxes, padded_obj_labels, box_masks = _to_boxes_and_masks(boxes, obj_labels, NUM_MAX_BOXES)
        person_ids = _pad_ids(person_ids, NUM_MAX_BOXES)

        boxes = torch.Tensor(padded_boxes)
        boxes_mask = torch.LongTensor(box_masks)
        objects = torch.LongTensor(padded_obj_labels)
        person_ids = torch.LongTensor(person_ids)

        return boxes, boxes_mask, objects, person_ids