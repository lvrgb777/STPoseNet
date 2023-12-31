# Ultralytics YOLO 🚀, AGPL-3.0 license

import torch

from ultralytics.data.augment import LetterBox
from ultralytics.engine.predictor import BasePredictor
from ultralytics.engine.results import Results
from ultralytics.utils import ops


class RTDETRPredictor(BasePredictor):
    """
    A class extending the BasePredictor class for prediction based on an RT-DETR detection model.

    Example:
        ```python
        from ultralytics.utils import ASSETS
        from ultralytics.models.rtdetr import RTDETRPredictor

        args = dict(model='rtdetr-l.pt', source=ASSETS)
        predictor = RTDETRPredictor(overrides=args)
        predictor.predict_cli()
        ```
    """

    def postprocess(self, preds, img, orig_imgs):
        """Postprocess predictions and returns a list of Results objects."""
        nd = preds[0].shape[-1]
        bboxes, scores = preds[0].split((4, nd - 4), dim=-1)
        results = []
        is_list = isinstance(orig_imgs, list)  # input images are a list, not a torch.Tensor
        for i, bbox in enumerate(bboxes):  # (300, 4)
            bbox = ops.xywh2xyxy(bbox)
            score, cls = scores[i].max(-1, keepdim=True)  # (300, 1)
            idx = score.squeeze(-1) > self.args.conf  # (300, )
            if self.args.classes is not None:
                idx = (cls == torch.tensor(self.args.classes, device=cls.device)).any(1) & idx
            pred = torch.cat([bbox, score, cls], dim=-1)[idx]  # filter
            orig_img = orig_imgs[i] if is_list else orig_imgs
            oh, ow = orig_img.shape[:2]
            if is_list:
                pred[..., [0, 2]] *= ow
                pred[..., [1, 3]] *= oh
            img_path = self.batch[0][i]
            results.append(Results(orig_img, path=img_path, names=self.model.names, boxes=pred, min_flag=self.min_flag))
        return results

        # """Postprocess predictions and returns a list of Results objects."""
        # nd = preds[0].shape[-1]
        # bboxes, scores = preds[0].split((4, nd - 4), dim=-1)
        # results = []
        # is_list = isinstance(orig_imgs, list)  # input images are a list, not a torch.Tensor
        # likelihood_ = 0
        # for i, bbox in enumerate(bboxes):  # (300, 4)
        #     bbox = ops.xywh2xyxy(bbox)
        #     score, cls = scores[i].max(-1, keepdim=True)  # (300, 1)
        #     idx = score.squeeze(-1) > self.args.conf  # (300, )
        #     if self.args.classes is not None:
        #         idx = (cls == torch.tensor(self.args.classes, device=cls.device)).any(1) & idx
        #     pred = torch.cat([bbox, score, cls], dim=-1)[idx]  # filter
        #     orig_img = orig_imgs[i] if is_list else orig_imgs
        #     oh, ow = orig_img.shape[:2]
        #     if is_list:
        #         pred[..., [0, 2]] *= ow
        #         pred[..., [1, 3]] *= oh
        #     img_path = self.batch[0][i]
        #     result = Results(orig_img, path=img_path, names=self.model.names, boxes=pred, min_flag=self.min_flag)
        #     likelihood = result.boxes[-2]
        #     if likelihood > likelihood_:
        #         likelihood_ = likelihood
        #         results = result
        # return results

    def pre_transform(self, im):
        """Pre-transform input image before inference.

        Args:
            im (List(np.ndarray)): (N, 3, h, w) for tensor, [(h, w, 3) x N] for list.

        Notes: The size must be square(640) and scaleFilled.

        Returns:
            (list): A list of transformed imgs.
        """
        return [LetterBox(self.imgsz, auto=False, scaleFill=True)(image=x) for x in im]