import os
import torch
from torch import nn, optim
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms, models
from tqdm import tqdm

def main():
    data_dir = "number_dataset"
    # Expected structure:
    # number_dataset/
    #     1/
    #         1_3_45_0.jpg, etc.
    #     2/
    #         ...
    #     ...
    #     6/
    #         ...

    data_transforms = transforms.Compose([
        transforms.Resize((640, 640)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])

    # Load the full dataset
    full_dataset = datasets.ImageFolder(data_dir, transform=data_transforms)
    print("Found classes:", full_dataset.classes)  # ['1', '2', '3', '4', '5', '6']

    # this is for sdeperating the train and validation stuff
    train_indices = []
    val_indices = []

    for idx, (path, class_idx) in enumerate(full_dataset.samples):
        filename = os.path.basename(path)   # ie: "1_3_45_0.jpg"
        parts = filename.split('_')
        # parts[0] = class, parts[1] = image_num, parts[2] = rotation, parts[3] = yap
        image_num_int = int(parts[1])
        
        # Assign shi to train or val
        if image_num_int == 9 or image_num_int == 10:
            val_indices.append(idx)
        else:
            train_indices.append(idx)

    train_dataset = Subset(full_dataset, train_indices)
    val_dataset = Subset(full_dataset, val_indices)

    # Create DataLoaders
    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False, num_workers=2)

    num_classes = 6
    model = models.resnet18(pretrained=True)
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    epochs = 10

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        running_corrects = 0

        for images, labels in tqdm(train_loader, desc=f"Epoch {epoch+1}/{epochs} [Training]", leave=False):
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            _, preds = torch.max(outputs, 1)
            running_loss += loss.item() * images.size(0)
            running_corrects += torch.sum(preds == labels)

        epoch_loss = running_loss / len(train_dataset)
        epoch_acc = running_corrects.double() / len(train_dataset)
        print(f"Epoch {epoch+1}/{epochs} - Train Loss: {epoch_loss:.4f}, Train Acc: {epoch_acc:.4f}")

        model.eval()
        val_loss = 0.0
        val_corrects = 0
        with torch.no_grad():
            for images, labels in tqdm(val_loader, desc=f"Epoch {epoch+1}/{epochs} [Validation]", leave=False):
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)

                _, preds = torch.max(outputs, 1)
                val_loss += loss.item() * images.size(0)
                val_corrects += torch.sum(preds == labels)

        val_loss = val_loss / len(val_dataset)
        val_acc = val_corrects.double() / len(val_dataset)
        print(f"Epoch {epoch+1}/{epochs} - Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}\n")

    print("Training complete!")

    # save the model's state yuh
    torch.save(model.state_dict(), "number_recognition_model.pth")
    print("Model saved as number_recognition_model.pth")

if __name__ == '__main__':
    main()
