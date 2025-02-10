import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Set paths
images_folder = "images/indoor"

# Load label encoding
label_encoding_path = os.path.join(images_folder, "label_encoding.npy")
if os.path.exists(label_encoding_path):
    label_encoder = np.load(label_encoding_path, allow_pickle=True).item()
else:
    raise FileNotFoundError("Label encoding file not found!")

# Reverse the label encoding for visualisation
label_decoder = {v: k for k, v in label_encoder.items()}

# Define valid spectral range (discard first and last 100 bands)
valid_band_start = 100
valid_band_end = 500
num_valid_bands = valid_band_end - valid_band_start  # 400 bands available

# Select 30 uniformly distributed bands from the valid 400 bands
num_selected_bands = 20
selected_bands = np.linspace(
    valid_band_start, valid_band_end - 1, num_selected_bands, dtype=int
)

# Prepare dataset
X = []
y = []

# Loop through subfolders
for subfolder in os.listdir(images_folder):
    subfolder_path = os.path.join(images_folder, subfolder)

    # Skip if not a directory
    if not os.path.isdir(subfolder_path):
        continue

    # Loop through saved class files
    for file in os.listdir(subfolder_path):
        if file.startswith("class_") and file.endswith(".npy"):
            class_label = int(
                file.split("_")[1].split(".")[0]
            )  # Extract encoded label
            data = np.load(os.path.join(subfolder_path, file))

            # Select the 30 chosen spectral bands (from valid range)
            data = data[:, selected_bands]

            # Append to dataset
            X.append(data)
            y.append(np.full(len(data), class_label))  # Assign labels

# Convert to numpy arrays
X = np.vstack(X)  # Stack all data points
y = np.hstack(y)  # Stack labels

# Define the number of training samples to use (subsample N random samples)
N = 500000
if X.shape[0] > N:
    idx = np.random.choice(X.shape[0], N, replace=False)
    X = X[idx]
    y = y[idx]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Dataset shape: {X.shape}, Labels shape: {y.shape}")
print(f"Train size: {X_train.shape}, Test size: {X_test.shape}")

# RF
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate model
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Random Forest Accuracy: {accuracy:.4f}")


# Function to classify an image and visualise results
def classify_and_visualise(image, labels, model):
    """
    Classifies an entire hyperspectral image at pixel level and visualises results.

    Args:
        image: Hyperspectral image (H, W, Bands)
        labels: Ground truth labels (H, W)
        model: Trained classifier
    """
    h, w, d = image.shape

    # Select only the 30 spectral bands (from valid range)
    image_selected = image[:, :, selected_bands]

    # Reshape for prediction
    image_reshaped = image_selected.reshape(-1, len(selected_bands))

    predictions = model.predict(image_reshaped)  # Predict pixel-wise labels
    predicted_labels = predictions.reshape(
        h, w
    )  # Reshape back to image format

    # Plot original labels vs predicted labels
    fig, axes = plt.subplots(1, 3, figsize=(12, 6))

    # Original labels
    ax = axes[0]
    ax.set_title("Original Labels")
    sns.heatmap(labels, cmap="jet", square=True, cbar=False, ax=ax)

    # Predicted labels
    ax = axes[1]
    ax.set_title("Predicted Labels")
    sns.heatmap(predicted_labels, cmap="jet", square=True, cbar=False, ax=ax)

    # Single-band image visualisation
    ax = axes[2]
    ax.set_title("Single Band Image")
    plt.imshow(image[:, :, selected_bands[5]], cmap="gray")

    plt.show()


if __name__ == "__main__":
    sample = "indoor_014"
    image_path = os.path.join(images_folder, sample + ".npy")
    label_path = os.path.join(images_folder, sample, "label.png")

    if os.path.exists(image_path) and os.path.exists(label_path):
        image = np.load(image_path)  # Load hyperspectral image
        labels = plt.imread(label_path)  # Load label mask

        # Convert to grayscale (temp solution for now - weird error reading labels.png)
        if len(labels.shape) == 3:
            labels = labels[:, :, 0]

        classify_and_visualise(image, labels, clf)
    else:
        print(f"{sample} not found.")
