# %% [markdown]
# # Parameters

# %%
from sklearn.metrics import confusion_matrix
from torch.optim.lr_scheduler import OneCycleLR
import torch.nn.functional as F
import torch.nn as nn
from sklearn.preprocessing import StandardScaler
from torch.utils.data import Dataset, DataLoader
import torch
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from ucimlrepo import fetch_ucirepo
BATCH_SIZE = 128
NUM_EPOCHS = 40
LR = 0.001  # learning rate

# %% [markdown]
# # Part 1: Load the Covertype Dataset

# %%
# Install the required package
!pip install ucimlrepo

# Import the dataset fetcher

# Fetch the dataset
covertype = fetch_ucirepo(id=31)

# Get features and target
X = covertype.data.features
y = covertype.data.targets

# Display dataset metadata
print("Dataset Overview:")
display(covertype.metadata)

# Check class distribution
print("\nTarget Distribution:")
print(y.value_counts())


# %% [markdown]
# #Part 2: Basic Data Cleaning & EDA

# %%
# Check for missing values
print("Missing values in each column:")
print(X.isnull().sum())

# Check for duplicate rows
print(f"\nNumber of duplicate rows: {X.duplicated().sum()}")

# Basic statistics
print("\nFeature summary:")
display(X.describe())


# %% [markdown]
# Dataset is clean! but needs to be normalized

# %% [markdown]
# #Part 3: Split the Dataset (Train/Validation/Test)

# %%

# First split: 90% train, 10% temp (which will be split into val and test)
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.10, stratify=y, random_state=42
)

# Second split: 5% val, 5% test from temp (which is 10% of original)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
)

# Check sizes
print(f"Train size: {len(X_train)}")
print(f"Validation size: {len(X_val)}")
print(f"Test size: {len(X_test)}")


# %% [markdown]
# #Part 4: Data Visualization

# %% [markdown]
# ##Visualize Class Distribution

# %%
# Plot class distribution in train, val, and test


def plot_class_distribution(y_data, title):
    # Convert to 1D Series if it's a DataFrame
    if isinstance(y_data, pd.DataFrame):
        y_data = y_data.squeeze()

    plt.figure(figsize=(8, 4))
    sns.countplot(x=y_data)
    plt.title(title)
    plt.xlabel("Cover Type")
    plt.ylabel("Count")
    plt.show()


plot_class_distribution(y_train, "Class Distribution - Training Set")
plot_class_distribution(y_val, "Class Distribution - Validation Set")
plot_class_distribution(y_test, "Class Distribution - Test Set")


# %% [markdown]
# The class distribution is heavily imbalanced across the training, development, and test sets, with cover types 1 and 2 being the most frequent. Cover types 3 to 7, especially type 4, have significantly fewer samples.

# %% [markdown]
#  ## Feature Distribution (e.g., Elevation, Slope)

# %%
# Plot histogram for a few numeric features
numeric_features = ["Elevation", "Slope", "Aspect"]

for feature in numeric_features:
    plt.figure(figsize=(6, 4))
    sns.histplot(X_train[feature], kde=True, bins=30)
    plt.title(f"Distribution of {feature}")
    plt.xlabel(feature)
    plt.ylabel("Frequency")
    plt.show()


# %% [markdown]
# ## Feature Correlation Heatmap

# %%
# Compute correlation matrix of numerical features
plt.figure(figsize=(12, 10))
sns.heatmap(X_train.corr(), cmap='coolwarm', annot=False)
plt.title("Feature Correlation Heatmap")
plt.show()

# %% [markdown]
#  # Part5: Convert Data to PyTorch Dataset

# %% [markdown]
# ## Convert features and labels to NumPy

# %%

# Convert to NumPy arrays
X_train_np = X_train.to_numpy()
X_val_np = X_val.to_numpy()
X_test_np = X_test.to_numpy()

y_train_np = y_train.squeeze().to_numpy()
y_val_np = y_val.squeeze().to_numpy()
y_test_np = y_test.squeeze().to_numpy()


# %% [markdown]
# ## Fix label values

# %%
# Fix label values: convert from [1, 7] to [0, 6]
y_train_np -= 1
y_val_np -= 1
y_test_np -= 1


# %% [markdown]
# ## Define a Custom Dataset Class

# %%
class CovertypeDataset(Dataset):
    def __init__(self, features, labels):
        self.features = torch.tensor(features, dtype=torch.float32)
        self.labels = torch.tensor(labels, dtype=torch.long)

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]


# %% [markdown]
# ## Create DataLoaders

# %%
# Create datasets
train_dataset = CovertypeDataset(X_train_np, y_train_np)
val_dataset = CovertypeDataset(X_val_np, y_val_np)
test_dataset = CovertypeDataset(X_test_np, y_test_np)

# Create dataloaders
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)


# %% [markdown]
# # Normalize the Features

# %%

# Fit on training data, apply to all sets
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# Replace it
X_train_np = X_train_scaled
X_val_np = X_val_scaled
X_test_np = X_test_scaled


# %% [markdown]
# # Part 6: Define the Neural Network Architecture

# %% [markdown]
# ## Define the Model

# %%


class CovertypeNet(nn.Module):
    def __init__(self):
        super(CovertypeNet, self).__init__()
        self.fc1 = nn.Linear(54, 256)
        self.bn1 = nn.BatchNorm1d(256)
        self.dropout1 = nn.Dropout(0.4)

        self.fc2 = nn.Linear(256, 128)
        self.bn2 = nn.BatchNorm1d(128)
        self.dropout2 = nn.Dropout(0.4)

        self.fc3 = nn.Linear(128, 64)
        self.bn3 = nn.BatchNorm1d(64)
        self.dropout3 = nn.Dropout(0.3)

        self.output = nn.Linear(64, 7)

    def forward(self, x):
        x = F.relu(self.bn1(self.fc1(x)))
        x = self.dropout1(x)

        x = F.relu(self.bn2(self.fc2(x)))
        x = self.dropout2(x)

        x = F.relu(self.bn3(self.fc3(x)))
        x = self.dropout3(x)

        # No softmax needed (CrossEntropyLoss expects raw logits)
        x = self.output(x)
        return x


# %% [markdown]
# ## Instantiate the Model

# %%
model = CovertypeNet()
print(model)


# %% [markdown]
#  # Part 7: Use CUDA for Faster Training

# %% [markdown]
# ##  Set the Device

# %%
# Set device to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")


# %% [markdown]
# ## Move the Model to the Device

# %%
model = model.to(device)

# %% [markdown]
# ## Make Sure Data is Moved to the Device During Training

# %%


# %% [markdown]
# # Part 8: Set Up the Optimizer, Loss Function, and LR Scheduler

# %% [markdown]
# ## Define the Loss Function

# %%
criterion = nn.CrossEntropyLoss()


# %% [markdown]
# ##  Define the Optimizer

# %%
optimizer = torch.optim.Adam(model.parameters(), lr=LR, weight_decay=1e-4)

# %% [markdown]
# ## Add a Learning Rate Scheduler

# %%
scheduler = OneCycleLR(
    optimizer,
    max_lr=0.005,                  # try between 0.003–0.01
    steps_per_epoch=len(train_loader),
    epochs=NUM_EPOCHS
)


# %% [markdown]
# # Part 9: Training and Validation Loops

# %% [markdown]
# ## Accuracy Function (Helper)

# %%
def calculate_accuracy(outputs, labels):
    _, preds = torch.max(outputs, dim=1)
    correct = (preds == labels).sum().item()
    return correct / len(labels)


# %% [markdown]
# ## Train for One Epoch

# %%
def train_one_epoch(model, loader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    running_acc = 0.0

    for features, labels in loader:
        features = features.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        outputs = model(features)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        running_acc += calculate_accuracy(outputs, labels)

    return running_loss / len(loader), running_acc / len(loader)


# %% [markdown]
# ## Validation Function

# %%
def validate(model, loader, criterion, device):
    model.eval()
    running_loss = 0.0
    running_acc = 0.0

    with torch.no_grad():
        for features, labels in loader:
            features = features.to(device)
            labels = labels.to(device)

            outputs = model(features)
            loss = criterion(outputs, labels)

            running_loss += loss.item()
            running_acc += calculate_accuracy(outputs, labels)

    return running_loss / len(loader), running_acc / len(loader)


# %% [markdown]
# # Part 10: Full Training Loop

# %% [markdown]
# ## Training Loop

# %%
print(device)

# %%

train_losses = []
val_losses = []
train_accuracies = []
val_accuracies = []

for epoch in range(NUM_EPOCHS):
    train_loss, train_acc = train_one_epoch(
        model, train_loader, criterion, optimizer, device)
    val_loss, val_acc = validate(model, val_loader, criterion, device)

    # Step the scheduler
    scheduler.step()

    # Save metrics
    train_losses.append(train_loss)
    val_losses.append(val_loss)
    train_accuracies.append(train_acc)
    val_accuracies.append(val_acc)

    print(f"Epoch {epoch+1}/{NUM_EPOCHS}")
    print(f"  Train Loss: {train_loss:.4f}, Accuracy: {train_acc:.4f}")
    print(f"  Val   Loss: {val_loss:.4f}, Accuracy: {val_acc:.4f}")


# %% [markdown]
# ## Plot Loss and Accuracy Curves

# %%

# Plot Loss
plt.figure(figsize=(10, 4))
plt.plot(train_losses, label="Train Loss")
plt.plot(val_losses, label="Val Loss")
plt.title("Loss over Epochs")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.grid(True)
plt.show()

# Plot Accuracy
plt.figure(figsize=(10, 4))
plt.plot(train_accuracies, label="Train Accuracy")
plt.plot(val_accuracies, label="Val Accuracy")
plt.title("Accuracy over Epochs")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(True)
plt.show()


# %% [markdown]
# # Part 11: Final Model Evaluation

# %% [markdown]
# ## Evaluate Accuracy on Test Set

# %%
model.eval()
test_loss = 0.0
test_acc = 0.0
all_preds = []
all_labels = []

with torch.no_grad():
    for features, labels in test_loader:
        features = features.to(device)
        labels = labels.to(device)

        outputs = model(features)
        loss = criterion(outputs, labels)

        test_loss += loss.item()
        test_acc += calculate_accuracy(outputs, labels)

        # Store predictions and true labels for confusion matrix
        preds = torch.argmax(outputs, dim=1)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

test_loss /= len(test_loader)
test_acc /= len(test_loader)

print(f"\nTest Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_acc:.4f}")


# %% [markdown]
# ## Plot Confusion Matrix

# %%

# Create confusion matrix
cm = confusion_matrix(all_labels, all_preds)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=range(1, 8), yticklabels=range(1, 8))
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix on Test Set")
plt.show()
