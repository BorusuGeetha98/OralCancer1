from PIL import Image, ImageDraw
import random
import os

def generate_dataset(base_dir, num_images):
    cancer_dir = os.path.join(base_dir, 'cancer')
    non_cancer_dir = os.path.join(base_dir, 'non_cancer')
    os.makedirs(cancer_dir, exist_ok=True)
    os.makedirs(non_cancer_dir, exist_ok=True)
    
    print(f'Generating {num_images} images for {base_dir}...')
    for i in range(num_images):
        # Fake cancer image (has a dark/reddish lesion)
        r, g, b = random.randint(150, 255), random.randint(100, 150), random.randint(100, 150)
        img = Image.new('RGB', (224, 224), color=(r, g, b))
        draw = ImageDraw.Draw(img)
        x1, y1 = random.randint(20, 100), random.randint(20, 100)
        x2, y2 = x1 + random.randint(30, 80), y1 + random.randint(30, 80)
        draw.ellipse((x1, y1, x2, y2), fill=(random.randint(50, 120), 0, 0))
        img.save(os.path.join(cancer_dir, f'cancer_synth_{i}.jpg'))
        
        # Fake normal image (clear tongue texture)
        r_n, g_n, b_n = random.randint(200, 255), random.randint(150, 200), random.randint(150, 200)
        img_normal = Image.new('RGB', (224, 224), color=(r_n, g_n, b_n))
        img_normal.save(os.path.join(non_cancer_dir, f'normal_synth_{i}.jpg'))

if __name__ == '__main__':
    # Generate 3000 images per class for training
    generate_dataset('dataset/train', 3000)
    # Generate 600 images per class for validation
    generate_dataset('dataset/validation', 600)
    print('Synthetic dataset generated successfully!')
