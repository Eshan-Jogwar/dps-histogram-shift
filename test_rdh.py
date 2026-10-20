"""
Automated validation script to verify 100% lossless Reversible Data Hiding.
Tests all 3 sample images with both plain and encrypted payloads.
"""

import os
import numpy as np
from PIL import Image

from implementation.rdh_core import (
    bytes_to_bits,
    bits_to_bytes,
    embed_global_histogram_shifting,
    extract_and_restore_global,
    save_stego_object,
    load_stego_object
)
from implementation.crypto_utils import encrypt_payload, decrypt_payload
from implementation.metrics import calculate_psnr, calculate_ssim, calculate_mse, verify_losslessness

def run_test_suite():
    samples_dir = "sample_images"
    encoded_dir = "encoded"
    os.makedirs(encoded_dir, exist_ok=True)
    
    test_cases = [
        ("brain_mri.png", "CONFIDENTIAL: Patient #89021 - MRI Normal, No lesions.", "pass123"),
        ("chest_xray.png", "DIAGNOSIS: Clear bilateral lung fields. Cardiothoracic ratio normal.", ""),
        ("knee_scan.png", "SURGICAL RECORD: Joint spacing intact, minimal osteophyte presence.", "ortho2026")
    ]
    
    print("\n" + "=" * 78)
    print("      REVERSIBLE DATA HIDING (HISTOGRAM SHIFTING) - VALIDATION SUITE")
    print("=" * 78)
    
    all_passed = True
    
    for filename, message, password in test_cases:
        image_path = os.path.join(samples_dir, filename)
        if not os.path.exists(image_path):
            print(f"Skipping {filename} (not found)")
            continue
            
        print(f"\n[+] Testing Carrier: {filename}")
        print(f"    - Input Secret: \"{message}\"")
        print(f"    - Password Protection: {'YES' if password else 'NO (Plaintext)'}")
        
        # 1. Load cover image
        cover = np.array(Image.open(image_path).convert("L"), dtype=np.uint8)
        
        # 2. Encrypt & pack payload
        payload_bytes = encrypt_payload(message, password)
        secret_bits = bytes_to_bits(payload_bytes)
        
        # 3. Embed data
        stego, meta = embed_global_histogram_shifting(cover, secret_bits)
        stego_psnr = calculate_psnr(cover, stego)
        stego_ssim = calculate_ssim(cover, stego)
        
        print(f"    - Peak Bin P: {meta['peak_bin']} | Zero Bin Z: {meta['zero_bin']} ({meta['direction']})")
        print(f"    - Embedded Bits: {meta['embedded_bits']} bits | Pixels Shifted: {meta['pixels_shifted']}")
        print(f"    - Stego Image Fidelity: PSNR = {stego_psnr:.2f} dB, SSIM = {stego_ssim:.5f}")
        
        # 4. Save stego image and metadata to /encoded
        out_name = f"stego_{os.path.splitext(filename)[0]}"
        stego_png_path = os.path.join(encoded_dir, out_name)
        saved_png, saved_json = save_stego_object(stego, meta, stego_png_path)
        print(f"    - Saved Stego Object: {saved_png} & {saved_json}")
        
        # 5. Load and Extract
        loaded_stego, loaded_meta = load_stego_object(saved_png)
        extracted_bits, restored_image = extract_and_restore_global(loaded_stego, loaded_meta)
        
        # 6. Decrypt payload
        extracted_bytes = bits_to_bytes(extracted_bits)
        recovered_message = decrypt_payload(extracted_bytes, password)
        
        # 7. Verify Lossless Restoration
        results = verify_losslessness(cover, restored_image)
        msg_match = (recovered_message == message)
        
        print(f"    - Extracted Message: \"{recovered_message}\" (Match: {msg_match})")
        print(f"    - Reversibility Check: Exact Match = {results['exact_match']}")
        print(f"    - Reconstructed MSE: {results['mse']:.6f} | Restored PSNR: {results['psnr']}")
        
        if results['exact_match'] and msg_match:
            print("    --> STATUS: [PASSED] 100% LOSSLESS RECOVERY CONFIRMED")
        else:
            print("    --> STATUS: [FAILED]")
            all_passed = False
            
    print("\n" + "=" * 78)
    if all_passed:
        print("          ALL TEST CASES PASSED WITH 100% BIT-FOR-BIT EXACTNESS!")
    else:
        print("          SOME TEST CASES FAILED.")
    print("=" * 78 + "\n")

if __name__ == "__main__":
    run_test_suite()
