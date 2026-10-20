"""
Script to generate synthetic realistic medical images (Brain MRI, Chest X-ray, Knee Joint)
for testing Reversible Data Hiding.
All images are 512x512 8-bit grayscale PNGs.
"""

import os
import numpy as np
from PIL import Image

def generate_brain_mri(size=512):
    """Simulates an axial slice of a Brain MRI."""
    img = np.zeros((size, size), dtype=np.float32)
    cy, cx = size // 2, size // 2
    y, x = np.indices((size, size))
    
    # Outer skull ellipse
    dist_outer = ((x - cx) / 180.0)**2 + ((y - cy) / 220.0)**2
    skull_bone = (dist_outer <= 1.0) & (dist_outer > 0.90)
    img[skull_bone] = 180 + np.random.normal(0, 5, skull_bone.sum())
    
    # Brain tissue (parenchyma)
    dist_inner = ((x - cx) / 165.0)**2 + ((y - cy) / 200.0)**2
    parenchyma = dist_inner <= 1.0
    
    base_brain = 90 + 35 * np.cos(dist_inner * 3.14 * 2) + 15 * np.sin(x / 30.0) * np.cos(y / 30.0)
    img[parenchyma] = base_brain[parenchyma] + np.random.normal(0, 6, parenchyma.sum())
    
    # Ventricles (fluid cavities)
    ventricle_left = (((x - (cx - 25)) / 22.0)**2 + ((y - (cy - 10)) / 55.0)**2 <= 1.0)
    ventricle_right = (((x - (cx + 25)) / 22.0)**2 + ((y - (cy - 10)) / 55.0)**2 <= 1.0)
    ventricles = ventricle_left | ventricle_right
    img[ventricles] = 25 + np.random.normal(0, 3, ventricles.sum())
    
    # Scanner background noise
    bg = dist_outer > 1.0
    img[bg] = np.clip(np.random.normal(8, 3, bg.sum()), 0, 20)
    
    return np.clip(img, 0, 255).astype(np.uint8)

def generate_chest_xray(size=512):
    """Simulates an AP Chest Radiograph (X-ray)."""
    img = np.full((size, size), 220.0, dtype=np.float32)
    cy, cx = size // 2, size // 2
    y, x = np.indices((size, size))
    
    # Thoracic cage shape
    thorax = ((x - cx) / 220.0)**2 + ((y - (cy + 20)) / 220.0)**2 <= 1.0
    img[~thorax] = 20 + np.random.normal(0, 4, (~thorax).sum())
    
    # Lungs
    lung_l = (((x - (cx - 95)) / 75.0)**2 + ((y - (cy - 10)) / 140.0)**2 <= 1.0)
    lung_r = (((x - (cx + 95)) / 75.0)**2 + ((y - (cy - 10)) / 140.0)**2 <= 1.0)
    
    img[lung_l] = 60 + 20 * np.sin(y[lung_l] / 20.0) + np.random.normal(0, 5, lung_l.sum())
    img[lung_r] = 60 + 20 * np.sin(y[lung_r] / 20.0) + np.random.normal(0, 5, lung_r.sum())
    
    # Cardiac silhouette
    heart = (((x - (cx + 35)) / 85.0)**2 + ((y - (cy + 60)) / 80.0)**2 <= 1.0)
    img[heart] = 160 + np.random.normal(0, 5, heart.sum())
    
    # Spine column
    spine = (np.abs(x - cx) <= 22) & (y >= 40) & (y <= 460)
    img[spine] = 175 + 15 * np.sin(y[spine] / 8.0) + np.random.normal(0, 4, spine.sum())
    
    # Ribs
    for rib_y in range(100, 420, 32):
        rib_mask = (np.abs(y - (rib_y + 0.0006 * (x - cx)**2)) < 7) & thorax
        img[rib_mask] = np.clip(img[rib_mask] + 45, 0, 255)
        
    return np.clip(img, 0, 255).astype(np.uint8)

def generate_knee_scan(size=512):
    """Simulates a Knee Joint Radiograph."""
    img = np.full((size, size), 50.0, dtype=np.float32)
    cy, cx = size // 2, size // 2
    y, x = np.indices((size, size))
    
    # Soft tissue contour
    leg = np.abs(x - cx) <= (140 + 20 * np.sin(y / 80.0))
    img[leg] = 95 + np.random.normal(0, 4, leg.sum())
    
    # Femur (upper bone)
    femur = (y < (cy - 20)) & (np.abs(x - cx) <= (65 + 0.05 * (cy - y)))
    img[femur] = 195 + np.random.normal(0, 6, femur.sum())
    
    # Tibia (lower bone)
    tibia = (y > (cy + 20)) & (np.abs(x - cx) <= (60 + 0.04 * (y - cy)))
    img[tibia] = 190 + np.random.normal(0, 6, tibia.sum())
    
    # Patella
    patella = (((x - (cx - 75)) / 22.0)**2 + ((y - cy) / 45.0)**2 <= 1.0)
    img[patella] = 205 + np.random.normal(0, 5, patella.sum())
    
    # Joint gap
    joint_gap = (np.abs(y - cy) <= 12) & (np.abs(x - cx) <= 80)
    img[joint_gap] = 75 + np.random.normal(0, 4, joint_gap.sum())
    
    return np.clip(img, 0, 255).astype(np.uint8)

def main():
    target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../sample_images"))
    os.makedirs(target_dir, exist_ok=True)
    
    samples = {
        "brain_mri.png": generate_brain_mri(512),
        "chest_xray.png": generate_chest_xray(512),
        "knee_scan.png": generate_knee_scan(512)
    }
    
    for filename, img_data in samples.items():
        path = os.path.join(target_dir, filename)
        Image.fromarray(img_data).save(path)
        print(f"Generated test sample: {path} (512x512 Grayscale)")

if __name__ == "__main__":
    main()
