import os
import shutil
import subprocess

def install_downloader():
    try:
        from bing_image_downloader import downloader
    except ImportError:
        import sys
        print("Installing bing-image-downloader package inside VENV...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "bing-image-downloader"])

def download_images():
    from bing_image_downloader import downloader
    
    base_dir = 'dataset'
    cancer_dir = os.path.join(base_dir, 'train', 'cancer')
    non_cancer_dir = os.path.join(base_dir, 'train', 'non_cancer')
    val_cancer_dir = os.path.join(base_dir, 'validation', 'cancer')
    val_non_cancer_dir = os.path.join(base_dir, 'validation', 'non_cancer')

    # 1. Clean up only synthetic data for fresh start (preserves real images)
    if os.path.exists(base_dir):
        print("Cleaning up synthetic data, keeping real images...")
        num_deleted = 0
        for root, _, files in os.walk(base_dir):
            for file in files:
                if 'synth_' in file.lower():
                    try:
                        os.remove(os.path.join(root, file))
                        num_deleted += 1
                    except Exception:
                        pass
        print(f"Deleted {num_deleted} synthetic files.")
    else:
        print("Creating dataset directory structure...")

    os.makedirs(cancer_dir, exist_ok=True)
    os.makedirs(non_cancer_dir, exist_ok=True)
    os.makedirs(val_cancer_dir, exist_ok=True)
    os.makedirs(val_non_cancer_dir, exist_ok=True)

    # 2. Download Images (Multi-queries to reach ~2,000 images)
    cancer_queries = [
        "tongue squamous cell carcinoma photo",
        "tongue cancer lesion",
        "tongue tumor photo",
        "oral cancer tongue photo"
    ]
    
    normal_queries = [
        "healthy human tongue photo",
        "normal tongue image",
        "clean pink tongue photo",
        "healthy tongue texture"
    ]

    print("Downloading Cancer images from Bing...")
    for q in cancer_queries:
        print(f"Searching for: {q}")
        try:
            downloader.download(q, limit=500, output_dir='dataset/temp_cancer', 
                                adult_filter_off=True, force_replace=False, timeout=60)
        except Exception as e:
            print(f"Error downloading {q}: {e}")
    
    print("Downloading Non-Cancer images from Bing...")
    for q in normal_queries:
        print(f"Searching for: {q}")
        try:
            downloader.download(q, limit=500, output_dir='dataset/temp_normal', 
                                adult_filter_off=True, force_replace=False, timeout=60)
        except Exception as e:
            print(f"Error downloading {q}: {e}")

    # 3. Organize Files into train/validation lists
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
            print(f"No files found in subdirectories of {temp_dir_parent}")
            return
            
        print(f"Found {len(all_files)} total images for {temp_dir_parent}")
        # Split train/validation (80/20 ratio)
        num_val = int(len(all_files) * 0.2)
        val_files = all_files[:num_val]
        train_files = all_files[num_val:]
        
        for f in train_files:
            try:
                shutil.copy(f, os.path.join(train_target, os.path.basename(f)))
            except Exception:
                pass
        for f in val_files:
            try:
                shutil.copy(f, os.path.join(val_target, os.path.basename(f)))
            except Exception:
                pass

    organize_files('dataset/temp_cancer', cancer_dir, val_cancer_dir)
    organize_files('dataset/temp_normal', non_cancer_dir, val_non_cancer_dir)

    # Cleanup temp
    if os.path.exists('dataset/temp_cancer'):
        shutil.rmtree('dataset/temp_cancer')
    if os.path.exists('dataset/temp_normal'):
        shutil.rmtree('dataset/temp_normal')
        
    print("Dataset preparation from Bing complete!")

if __name__ == '__main__':
    install_downloader()
    download_images()
