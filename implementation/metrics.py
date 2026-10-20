"""
Metrics and evaluation module for Reversible Data Hiding.
Computes MSE, PSNR, SSIM, and exact-array equality to demonstrate 100% losslessness.
"""

import numpy as np

def calculate_mse(img1: np.ndarray, img2: np.ndarray) -> float:
    """Mean Squared Error between two images."""
    if img1.shape != img2.shape:
        raise ValueError("Images must have identical dimensions.")
    return float(np.mean((img1.astype(np.float64) - img2.astype(np.float64)) ** 2))

def calculate_psnr(img1: np.ndarray, img2: np.ndarray, max_pixel: float = 255.0) -> float:
    """Peak Signal-to-Noise Ratio (PSNR) in decibels (dB). Returns infinity if identical."""
    mse = calculate_mse(img1, img2)
    if mse == 0.0:
        return float("inf")
    return float(20.0 * np.log10(max_pixel / np.sqrt(mse)))

def calculate_ssim(img1: np.ndarray, img2: np.ndarray) -> float:
    """
    Structural Similarity Index (SSIM) between two grayscale images.
    Implements standard Wang et al. formula.
    """
    if img1.shape != img2.shape:
        raise ValueError("Images must have identical dimensions.")
    
    x = img1.astype(np.float64)
    y = img2.astype(np.float64)
    
    k1 = 0.01
    k2 = 0.03
    L = 255.0
    c1 = (k1 * L) ** 2
    c2 = (k2 * L) ** 2
    
    mu_x = np.mean(x)
    mu_y = np.mean(y)
    
    sigma_x_sq = np.var(x)
    sigma_y_sq = np.var(y)
    sigma_xy = np.cov(x.ravel(), y.ravel())[0, 1]
    
    numerator = (2 * mu_x * mu_y + c1) * (2 * sigma_xy + c2)
    denominator = (mu_x**2 + mu_y**2 + c1) * (sigma_x_sq + sigma_y_sq + c2)
    
    if denominator == 0:
        return 1.0
    return float(numerator / denominator)

def verify_losslessness(original: np.ndarray, restored: np.ndarray) -> dict:
    """
    Evaluates restoration fidelity.
    Returns dictionary with exact boolean match, MSE, and PSNR.
    """
    is_exact = bool(np.array_equal(original, restored))
    mse = calculate_mse(original, restored)
    psnr = calculate_psnr(original, restored)
    return {
        "exact_match": is_exact,
        "mse": mse,
        "psnr": psnr
    }
