from transformers import GPT2Tokenizer

import os
import json

class VCRGpt2Tokenizer(GPT2Tokenizer):
    def __init__(self,
                 vocab_file,
                 merges_file,
                 errors='replace',
                 unk_token="<|endoftext|>",
                 bos_token="<|endoftext|>",
                 eos_token="<|endoftext|>",
                 begin_img="<|b_img|>",
                 end_img="<|e_img|>",
                 begin_question="<|b_qn|>",
                 end_question="<|e_qn|>",
                 begin_rationale="<|b_rtnl|>",
                 end_rationale="<|e_rtnl|>",
                 **kwargs):
        super(VCRGpt2Tokenizer, self).__init__(
            vocab_file,
            merges_file,
            errors=errors,
            bos_token=bos_token,
            eos_token=eos_token,
            unk_token=unk_token,
            **kwargs
        )

        self.begin_img = begin_img
        self.end_img = end_img
        self.begin_question = begin_question
        self.end_question = end_question
        self.begin_rationale = begin_rationale
        self.end_rationale = end_rationale

        self.add_special_tokens({
            "additional_special_tokens": [self.begin_img, self.end_img, self.begin_question,
                                          self.end_question, self.begin_rationale, self.end_rationale]
        })

    def decode(self, token_ids, skip_special_tokens=False, clean_up_tokenization_spaces=True):
        text = super().decode(token_ids, skip_special_tokens, clean_up_tokenization_spaces)
        idx = text.find(self.end_rationale)
        if idx != -1:
            text = text[:idx]
        return text

class VCRAtomicGpt2Tokenizer(GPT2Tokenizer):
    def __init__(self,
                 vocab_file,
                 merges_file,
                 errors='replace',
                 unk_token="<|endoftext|>",
                 bos_token="<|endoftext|>",
                 eos_token="<|endoftext|>",
                 begin_img="<|b_img|>",
                 end_img="<|e_img|>",
                 begin_event="<|b_ev|>",
                 end_event="<|e_ev|>",
                 begin_place="<|b_pl|>",
                 end_place="<|e_pl|>",
                 begin_relations={'intent': "<|intent|>", 'need': "<|need|>", 'react': "<|react|>"},
                 end_relation="<|e_rn|>",
                 **kwargs):
        super(VCRAtomicGpt2Tokenizer, self).__init__(
            vocab_file,
            merges_file,
            errors=errors,
            bos_token=bos_token,
            eos_token=eos_token,
            unk_token=unk_token,
            **kwargs
        )

        self.begin_img = begin_img
        self.end_img = end_img
        self.begin_event = begin_event
        self.end_event = end_event
        self.begin_place = begin_place
        self.end_place = end_place
        self.begin_relations = begin_relations
        self.end_relation = end_relation
        self.det_tokens = ['<|det%d|>' % i for i in range(50)]
        self.add_special_tokens({
            "additional_special_tokens": [self.begin_img, self.end_img, self.begin_event, self.end_event,
                                          self.begin_place, self.end_place, self.end_relation]
                                         + list(self.begin_relations.values()) + self.det_tokens
        })

    def decode(self, token_ids, skip_special_tokens=False, clean_up_tokenization_spaces=True):
        text = super().decode(token_ids, False, clean_up_tokenization_spaces)
        tokens2remove = [self.begin_img, self.end_img, self.begin_event, self.end_event,
                         self.end_place, self.end_relation, self.unk_token] + list(self.begin_relations.values())
        if skip_special_tokens:
            for t in tokens2remove:
                text = text.replace(t, ' ')
        idx = text.find(self.end_relation)
        if idx != -1:
            text = text[:idx]
        return text.strip()


class VCRRationaleGpt2Tokenizer(GPT2Tokenizer):
    def __init__(self,
                 vocab_file,
                 merges_file,
                 errors='replace',
                 unk_token="<|endoftext|>",
                 bos_token="<|endoftext|>",
                 eos_token="<|endoftext|>",
                 begin_img="<|b_img|>",
                 end_img="<|e_img|>",
                 begin_question="<|b_qn|>",
                 end_question="<|e_qn|>",
                 begin_answer="<|b_an|>",
                 end_answer="<|e_an|>",
                 begin_aux="<|b_au|>",
                 end_aux="<|e_au|>",
                 begin_rationale="<|b_rtnl|>",
                 end_rationale="<|e_rtnl|>",
                 **kwargs):
        super(VCRRationaleGpt2Tokenizer, self).__init__(
            vocab_file,
            merges_file,
            errors=errors,
            bos_token=bos_token,
            eos_token=eos_token,
            unk_token=unk_token,
            **kwargs
        )

        self.begin_img = begin_img
        self.end_img = end_img
        self.begin_question = begin_question
        self.end_question = end_question
        self.begin_answer = begin_answer
        self.end_answer = end_answer
        self.begin_aux = begin_aux
        self.end_aux = end_aux
        self.begin_rationale = begin_rationale
        self.end_rationale = end_rationale
        self.det_tokens = ['<|det%d|>' % i for i in range(50)]

        self.add_special_tokens({
            "additional_special_tokens": [self.begin_img, self.end_img, self.begin_question, self.end_question,
                                          self.begin_answer, self.end_answer, self.begin_aux, self.end_aux,
                                          self.begin_rationale, self.end_rationale] + self.det_tokens
        })

        with open(os.path.join(os.path.dirname(__file__), 'cocoontology.json'), 'r') as f:
            coco = json.load(f)
        coco_objects = ['__background__'] + [x['name'] for k, x in sorted(coco.items(), key=lambda x: int(x[0]))]
        coco_obj_to_ind = {o: i for i, o in enumerate(coco_objects)}
        self.add_tokens(list(coco_obj_to_ind.keys()))

    def decode(self, token_ids, skip_special_tokens=False, clean_up_tokenization_spaces=True):
        text = super().decode(token_ids, False, clean_up_tokenization_spaces)
        tokens2remove = [self.begin_question, self.end_question, self.begin_answer, self.end_answer,
                         self.begin_aux, self.end_aux, self.begin_rationale, self.unk_token]
        if skip_special_tokens:
            for t in tokens2remove:
                text = text.replace(t, ' ')
        idx = text.find(self.end_rationale)
        if idx != -1:
            text = text[:idx]
        return text.strip()
