

import numpy as np
import cv2

# import some common detectron2 utilities
import torch

from detectron2.modeling.postprocessing import detector_postprocess
from detectron2.modeling.roi_heads.fast_rcnn import FastRCNNOutputLayers, FastRCNNOutputs, \
    fast_rcnn_inference_single_image
from detectron2.structures.boxes import Boxes

from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.data import MetadataCatalog


class ObjectDetector:
    def __init__(self):
        cfg = get_cfg()
        # add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
        cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_101_C4_3x.yaml"))
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.8  # set threshold for this model
        # Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
        cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_101_C4_3x.yaml")

        self.predictor = DefaultPredictor(cfg)
        coco_key = MetadataCatalog.get(cfg.DATASETS.TRAIN[0]).thing_dataset_id_to_contiguous_id
        self.coco_key = {coco_key[k]: k for k in coco_key}

    def detect_objects(self, raw_image):
        im = cv2.imread(raw_image)
        outputs = self.predictor(im)
        output = outputs["instances"].to("cpu")

        vis_info = {}
        vis_info['boxes'] = output.pred_boxes.tensor.numpy()
        vis_info['scores'] = output.scores.numpy()
        vis_info['classes'] = [self.coco_key[k] for k in output.pred_classes.numpy()]
        vis_info['num_boxes'] = len(vis_info['boxes'])
        h, w = output.image_size
        vis_info['height'] = h
        vis_info['width'] = w

        return vis_info


    def extract_features(self, raw_image, raw_boxes):
        # Process Boxes
        raw_boxes = Boxes(torch.from_numpy(raw_boxes).cuda())

        with torch.no_grad():
            raw_height, raw_width = raw_image.shape[:2]

            # Preprocessing
            image = self.predictor.transform_gen.get_transform(raw_image).apply_image(raw_image)

            # Scale the box
            new_height, new_width = image.shape[:2]
            scale_x = 1. * new_width / raw_width
            scale_y = 1. * new_height / raw_height

            boxes = raw_boxes.clone()
            boxes.scale(scale_x=scale_x, scale_y=scale_y)

            # ----
            image = torch.as_tensor(image.astype("float32").transpose(2, 0, 1))
            inputs = [{"image": image, "height": raw_height, "width": raw_width}]
            images = self.predictor.model.preprocess_image(inputs)

            # Run Backbone Res1-Res4
            features = self.predictor.model.backbone(images.tensor)

            # Run RoI head for each proposal (RoI Pooling + Res5)
            proposal_boxes = [boxes]
            features = [features[f] for f in self.predictor.model.roi_heads.in_features]
            box_features = self.predictor.model.roi_heads._shared_roi_transform(
                features, proposal_boxes
            )
            feature_pooled = box_features.mean(dim=[2, 3])  # pooled to 1x1
        return feature_pooled


