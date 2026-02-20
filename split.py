import os
import shutil
import random

# Paths
base_dir = "train"  # folder you downloaded from Roboflow
images_dir = os.path.join(base_dir, "images")
labels_dir = os.path.join(base_dir, "labels")

# Output folders
for folder in ["train", "val", "test"]:
    os.makedirs(f"dataset/images/{folder}", exist_ok=True)
    os.makedirs(f"dataset/labels/{folder}", exist_ok=True)

# List of images
all_images = [f for f in os.listdir(images_dir) if f.endswith(".jpg")]
random.shuffle(all_images)

# Split percentages
train_split = 0.8
val_split = 0.1
test_split = 0.1
n_total = len(all_images)
n_train = int(n_total * train_split)
n_val = int(n_total * val_split)

# Move files
for i, img_file in enumerate(all_images):
    label_file = img_file.replace(".jpg", ".txt")
    
    if i < n_train:
        folder = "train"
    elif i < n_train + n_val:
        folder = "val"
    else:
        folder = "test"
    
    shutil.copy(os.path.join(images_dir, img_file), f"dataset/images/{folder}/{img_file}")
    shutil.copy(os.path.join(labels_dir, label_file), f"dataset/labels/{folder}/{label_file}")

print("Dataset split completed!")
