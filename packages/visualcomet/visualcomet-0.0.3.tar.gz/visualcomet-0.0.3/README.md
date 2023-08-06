# vcg_demo

## Installation
```bash
pip install -r requirements.txt
```
Then, install [detectron2](https://github.com/facebookresearch/detectron2/blob/master/INSTALL.md) to have the object detectors ready.

Now, there is a chance that detectron2 might complain because of cuda error. If this is the case, try the following:
Uninstall `torch` and `torchvision`.
Reinstall them with the following command:
```bash
pip install torch==1.5.0+cu101 torchvision==0.6.0+cu101 -f https://download.pytorch.org/whl/torch_stable.html
```

Then run the following to make detectron2 compatible with the pytorch and cuda version.
``` bash
python -m pip install detectron2 -f \
  https://dl.fbaipublicfiles.com/detectron2/wheels/cu101/torch1.5/index.html
```

## Demo
Set the image to run in `$image_path` argument.
Then, the following script generates inference sentences for every person in the image.

```bash
python scripts/run_demo.py  --image_path sample_images/1010_TITANIC_02.34.42.828-02.34.43.864@0.jpg --model_name_or_path /net/nfs.corp/alexandria/jamesp/vgpt-ckpt/out_image_all_person_subject_9000_57000_lr5e-5
```

You should also look into `visualization.ipynb` for better visualization.
