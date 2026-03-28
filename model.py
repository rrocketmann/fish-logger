"""
Fish Classification CNN Model using PyTorch
"""
import torch
import torch.nn as nn
import torch.nn.functional as F

class FishCNN(nn.Module):
    """Convolutional Neural Network for fish species classification"""
    
    def __init__(self, num_classes=9):
        super(FishCNN, self).__init__()
        
        # Convolutional layers
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        self.conv4 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.bn4 = nn.BatchNorm2d(256)
        self.conv5 = nn.Conv2d(256, 512, kernel_size=3, padding=1)
        self.bn5 = nn.BatchNorm2d(512)
        
        # Pooling layer
        self.pool = nn.MaxPool2d(2, 2)
        
        # Dropout for regularization
        self.dropout = nn.Dropout(0.5)
        
        # Fully connected layers
        # After 5 pooling layers, 224x224 -> 7x7
        self.fc1 = nn.Linear(512 * 7 * 7, 1024)
        self.fc2 = nn.Linear(1024, 512)
        self.fc3 = nn.Linear(512, num_classes)
        
    def forward(self, x):
        # Block 1
        x = self.pool(F.relu(self.bn1(self.conv1(x))))
        
        # Block 2
        x = self.pool(F.relu(self.bn2(self.conv2(x))))
        
        # Block 3
        x = self.pool(F.relu(self.bn3(self.conv3(x))))
        
        # Block 4
        x = self.pool(F.relu(self.bn4(self.conv4(x))))
        
        # Block 5
        x = self.pool(F.relu(self.bn5(self.conv5(x))))
        
        # Flatten
        x = x.view(-1, 512 * 7 * 7)
        
        # Fully connected layers
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        
        return x


class FishResNet(nn.Module):
    """
    Alternative model using transfer learning with ResNet-18
    Generally achieves better results with less training time
    """
    def __init__(self, num_classes=9, pretrained=True):
        super(FishResNet, self).__init__()
        
        # Load pretrained ResNet-18
        from torchvision import models
        self.resnet = models.resnet18(pretrained=pretrained)
        
        # Replace the final fully connected layer
        num_features = self.resnet.fc.in_features
        self.resnet.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(num_features, num_classes)
        )
    
    def forward(self, x):
        return self.resnet(x)


def get_model(model_type='resnet', num_classes=9, pretrained=True):
    """
    Factory function to get the desired model
    
    Args:
        model_type: 'cnn' or 'resnet'
        num_classes: Number of fish species to classify
        pretrained: Whether to use pretrained weights (for ResNet)
    
    Returns:
        PyTorch model
    """
    if model_type == 'cnn':
        return FishCNN(num_classes=num_classes)
    elif model_type == 'resnet':
        return FishResNet(num_classes=num_classes, pretrained=pretrained)
    else:
        raise ValueError(f"Unknown model type: {model_type}")


if __name__ == "__main__":
    # Test the models
    print("Testing FishCNN...")
    model_cnn = FishCNN(num_classes=9)
    x = torch.randn(1, 3, 224, 224)
    output = model_cnn(x)
    print(f"Output shape: {output.shape}")
    print(f"Total parameters: {sum(p.numel() for p in model_cnn.parameters()):,}")
    
    print("\nTesting FishResNet...")
    model_resnet = FishResNet(num_classes=9, pretrained=False)
    output = model_resnet(x)
    print(f"Output shape: {output.shape}")
    print(f"Total parameters: {sum(p.numel() for p in model_resnet.parameters()):,}")
