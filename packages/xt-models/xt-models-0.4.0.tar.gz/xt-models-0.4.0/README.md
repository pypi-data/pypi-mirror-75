# xt-models
  
## Description

This repo contains common models and utilities for working with ML tasks, developed by [Xtract AI](https://xtract.ai/).



More to come.

## Installation
From PyPi:
```bash
pip install xt-models
```

From source:
```bash
git clone https://github.com/XtractTech/xt-models.git
pip install ./xt-models
```

## Usage


#### Grabbing a segmentation model

```python
from xt_models.models import ModelBuilder, SegmentationModule
from torch import nn

deep_sup_scale = 0.4
fc_dim = 2048
n_class = 2
net_encoder = ModelBuilder.build_encoder(
    arch="resnet50dilated",
    fc_dim=fc_dim,
    weights="/nasty/scratch/common/smart_objects/model/ade20k/encoder_epoch_20.pth"
)
net_decoder = ModelBuilder.build_decoder(
    arch="ppm_deepsup",
    fc_dim=fc_dim,
    num_class=150,
    weights="/nasty/scratch/common/smart_objects/model/ade20k/decoder_epoch_20.pth"
)
in_channels = net_decoder.conv_last[-1].in_channels
net_decoder.conv_last[-1] = nn.Conv2d(in_channels, n_class, kernel_size=(1, 1), stride=(1, 1))
net_decoder.conv_last_deepsup = nn.Conv2d(in_channels, n_class, 1, 1, 0)


model = SegmentationModule(net_encoder, net_decoder, deep_sup_scale)
```

#### Grabbing a detection model

```
from xt_models.models import Model
import torch

# Load a fine-tuned model for inference
model_name = "yolov5x"
model = Model(model_name,nc=15)
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
weights = "/nasty/scratch/common/smart_objects/model/veh_detection/yolov5_ft/best_state_dict.pt"
ckpt = torch.load(weights, map_location=device)
model.load_state_dict(ckpt['model_state_dict'])

# Load pre-trained COCO model for finetuning/inference
model_name = "yolov5x"
model = Model(model_name,nc=80)
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
weights = "/nasty/scratch/common/smart_objects/model/veh_detection/yolov5_pretrain/yolov5x_state_dict.pt"
ckpt = torch.load(weights, map_location=device)
model.load_state_dict(ckpt['model_state_dict'])
# Fine-tuning number of classes
n_class = 15
model.nc = n_class

```
#### Implementing a new model

If you are having to always copy and paste the same model code for different projects, simply add the model code to the `models` directory, and import it in the `models/__init__.py` file.

## Data Sources

[descriptions and links to data]
  
## Dependencies/Licensing

[list of dependencies and their licenses, including data]

## References

[list of references]
