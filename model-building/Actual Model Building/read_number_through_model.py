import torch
from torch import nn
from torchvision import transforms, models
from PIL import Image

def load_model(model_path="number_recognition_model.pth", num_classes=6):
    model = models.resnet18(pretrained=False)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    return model

def get_transforms():
    # this is the same transforms used during training
    data_transforms = transforms.Compose([
        transforms.Resize((640, 640)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])
    return data_transforms

def predict_number(model, image_path):
    # defining the class names (prediction possibilities) 
    classes = ['1', '2', '3', '4', '5', '6']

   
    img = Image.open(image_path).convert("RGB")

    # making sure it is transformed the same way as it was while being trained
    data_transforms = get_transforms()
    img_tensor = data_transforms(img).unsqueeze(0)  # this is a batch dimension, dw about it just leave it here

    with torch.no_grad():
        outputs = model(img_tensor)
        _, predicted = torch.max(outputs, 1)
        predicted_class = classes[predicted.item()]

    return predicted_class

if __name__ == "__main__":
    # Example usage:
    model = load_model("number_recognition_model.pth") # i will send you the number_recognition_model when i have finished running it 
    image_path = "number_dataset/4/4_2_45_0.jpg"
    prediction = predict_number(model, image_path)
    print(f"Predicted number on the dice: {prediction}")


#I briefly put this together by combining the important parts of my model, i am assuming that this should work though it hasnt been tested and you cant test it until my model is finished running, so far epoch 2 is at about 98% accuracy so we balling


