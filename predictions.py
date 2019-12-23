from __future__ import print_function, division

import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms

# Load the pre-trained model from pytorch
vgg16 = models.vgg16_bn()
class_index = {0: 'CNV', 1: 'DME', 2: 'DRUSEN', 3: 'NORMAL', 4: 'CSR', 5: 'MH'}

num_features = vgg16.classifier[6].in_features
features = list(vgg16.classifier.children())[:-1]  # Remove last layer
features.extend([nn.Linear(num_features, 6)])  # Add our layer with 6 outputs

vgg16.classifier = nn.Sequential(*features)  # Replace the model classifier
print("Loading pretrained model..")
vgg16.load_state_dict(torch.load('/Users/a112233/Downloads/VGG16_v2-OCT_Retina_CSR_MH.pt', map_location=torch.device('cpu')))
print("Loaded!")
vgg16.eval()


def transform_image(image_path):
    my_transforms = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    image = Image.open(image_path).convert('RGB')
    return my_transforms(image).unsqueeze(0)


def get_prediction(image_path):
    tensor = transform_image(image_path=image_path)
    outputs = vgg16(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = y_hat.item()
    return class_index[predicted_idx]


class_name = get_prediction(image_path='/Users/a112233/Downloads/kermany2018/DEC2019-half-dataset/test/CSR/CSR97.jpeg')
print(class_name)
