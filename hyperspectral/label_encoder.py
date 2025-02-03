import os
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Define paths
images_folder = "images/indoor"

# Dictionary to encode class labels
label_encoder = {}
current_label = 0

# Each subfolder contains a labelled img
for subfolder in os.listdir(images_folder):
    subfolder_path = os.path.join(images_folder, subfolder)

    # Skip if not a directory
    if not os.path.isdir(subfolder_path):
        continue

    # Load the label mask
    label_mask_path = os.path.join(subfolder_path, "label.png")

    # Load corresponding .npy file
    npy_path = os.path.join(images_folder, subfolder + ".npy")

    # The data
    label_mask = cv2.imread(label_mask_path, cv2.IMREAD_GRAYSCALE)
    hyperspectral_image = np.load(npy_path)  # Shape: (H, W, Bands)

    # Get unique labels and encode each of them
    unique_labels = np.unique(label_mask)
    for label in unique_labels:
        if label == 0:
            continue  # Skip background pxels

        # New label if not already assigned
        if label not in label_encoder:
            label_encoder[label] = current_label
            current_label += 1

        # Get pixels corresponding to this label
        mask = label_mask == label
        class_pixels = hyperspectral_image[mask]

        # Save data with encoded class labels
        save_path = os.path.join(
            subfolder_path, f"class_{label_encoder[label]}.npy"
        )
        np.save(save_path, class_pixels)
        print(
            f"Saved: {save_path} (Original Label: {label} -> Encoded as: {label_encoder[label]})"
        )

# Save label encoding for reference
encoding_path = os.path.join(images_folder, "label_encoding.npy")
np.save(encoding_path, label_encoder)
print(f"Label encoding saved at {encoding_path}")
