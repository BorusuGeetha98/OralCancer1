import os
import shutil
import subprocess
from bing_image_downloader import downloader

def download_normal():
    print("Downloading 150 Healthy/Normal images to balance the dataset...")
    try:
        downloader.download("healthy human tongue photo", limit=150, output_dir='dataset/temp_normal', 
                            adult_filter_off=True, force_replace=False, timeout=60)
    except Exception as e:
        print(f"Error downloading normal images: {e}")

def organize_files(temp_dir_parent, train_target, val_target):
    if not os.path.exists(temp_dir_parent):
        print(f"Directory Empty: {temp_dir_parent}")
        return
        
    all_files = []
    for subdir in os.listdir(temp_dir_parent):
        subdir_path = os.path.join(temp_dir_parent, subdir)
        if os.path.isdir(subdir_path):
            files = [os.path.join(subdir_path, f) for f in os.listdir(subdir_path) 
                     if os.path.isfile(os.path.join(subdir_path, f))]
            all_files.extend(files)
            
    if not all_files:
        print(f"No files found in {temp_dir_parent}")
        return
        
    print(f"Found {len(all_files)} total images for {temp_dir_parent}")
    num_val = int(len(all_files) * 0.2)
    val_files = all_files[:num_val]
    train_files = all_files[num_val:]
    
    os.makedirs(train_target, exist_ok=True)
    os.makedirs(val_target, exist_ok=True)

    for f in train_files:
        try:
            shutil.copy(f, os.path.join(train_target, os.path.basename(f)))
        except Exception: pass
    for f in val_files:
        try:
            shutil.copy(f, os.path.join(val_target, os.path.basename(f)))
        except Exception: pass

if __name__ == '__main__':
    download_normal()
    print("Organizing files...")
    organize_files('dataset/temp_cancer', 'dataset/train/cancer', 'dataset/validation/cancer')
    organize_files('dataset/temp_normal', 'dataset/train/non_cancer', 'dataset/validation/non_cancer')
    
    # Cleanup temp
    if os.path.exists('dataset/temp_cancer'):
        shutil.rmtree('dataset/temp_cancer')
    if os.path.exists('dataset/temp_normal'):
        shutil.rmtree('dataset/temp_normal')
        
    print("Organizing complete! Running train_model.py...")
    subprocess.call(["python", "train_model.py"])
