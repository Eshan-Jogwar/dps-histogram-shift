"""
Flask backend for Reversible Data Hiding (Histogram Shifting) Web GUI.
Provides REST endpoints for:
- Preset loading (brain_mri, chest_xray, knee_scan)
- Embedding (cover -> stego with histogram shift)
- Extraction & Restoration (stego -> restored image + extracted plaintext)
- 1-Click live demonstration (end-to-end with MSE=0 and PSNR=inf proof)
- Histogram generation (original vs stego JSON for Chart.js)
"""

import os
import io
import base64
import json
from flask import Flask, render_template, request, jsonify, send_file
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

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SAMPLES_DIR = os.path.join(BASE_DIR, "sample_images")
ENCODED_DIR = os.path.join(BASE_DIR, "encoded")

app = Flask(__name__, template_folder="templates", static_folder="static")

PRESETS = {
    "brain_mri.png": {
        "title": "Brain MRI Scan",
        "description": "512x512 Grayscale T1 Axial Slice",
        "default_message": "CONFIDENTIAL: Patient #89021 - MRI Normal. No acute intracranial hemorrhage or mass effect observed."
    },
    "chest_xray.png": {
        "title": "Chest X-Ray Radiograph",
        "description": "512x512 Grayscale AP Chest Projection",
        "default_message": "DIAGNOSIS: Clear bilateral lung fields. Cardiothoracic ratio within normal limits. Bones intact."
    },
    "knee_scan.png": {
        "title": "Knee Joint Radiograph",
        "description": "512x512 Grayscale Lateral Knee Radiograph",
        "default_message": "SURGICAL NOTE: Femur and tibia alignment normal. Medial joint space well-preserved. No fracture."
    }
}

def img_to_b64(arr: np.ndarray) -> str:
    img = Image.fromarray(arr.astype(np.uint8))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")

def b64_to_img(b64_str: str) -> np.ndarray:
    if "," in b64_str:
        b64_str = b64_str.split(",", 1)[1]
    raw = base64.b64decode(b64_str)
    img = Image.open(io.BytesIO(raw)).convert("L")
    return np.array(img, dtype=np.uint8)

def compute_histogram(arr: np.ndarray) -> list:
    counts = np.bincount(arr.ravel(), minlength=256)
    return counts.tolist()

@app.route("/")
def index():
    return render_template("index.html", presets=PRESETS)

@app.route("/api/preset/<filename>")
def get_preset(filename):
    if filename not in PRESETS:
        return jsonify({"error": "Unknown preset"}), 404
    path = os.path.join(SAMPLES_DIR, filename)
    if not os.path.exists(path):
        return jsonify({"error": "File not found"}), 404
    arr = np.array(Image.open(path).convert("L"), dtype=np.uint8)
    return jsonify({
        "filename": filename,
        "info": PRESETS[filename],
        "image_b64": img_to_b64(arr),
        "histogram": compute_histogram(arr),
        "shape": list(arr.shape)
    })

@app.route("/api/run_demo", methods=["POST"])
def run_demo():
    """1-Click end-to-end execution: load, embed, save, extract, verify lossless."""
    data = request.json or {}
    filename = data.get("filename", "brain_mri.png")
    message = data.get("message", PRESETS.get(filename, {}).get("default_message", "CONFIDENTIAL RECORD"))

    path = os.path.join(SAMPLES_DIR, filename)
    if not os.path.exists(path):
        return jsonify({"error": "Cover image not found"}), 404

    cover = np.array(Image.open(path).convert("L"), dtype=np.uint8)

    # 1. Prepare payload
    payload_bytes = encrypt_payload(message, password="")
    bits = bytes_to_bits(payload_bytes)

    # 2. Embed via histogram shift
    try:
        stego, meta = embed_global_histogram_shifting(cover, bits)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    stego_psnr = calculate_psnr(cover, stego)
    stego_ssim = calculate_ssim(cover, stego)

    # 3. Save to /encoded folder
    base_name = os.path.splitext(filename)[0]
    out_prefix = os.path.join(ENCODED_DIR, f"stego_{base_name}")
    saved_png, saved_json = save_stego_object(stego, meta, out_prefix)

    # 4. Extract and restore
    extracted_bits, restored = extract_and_restore_global(stego, meta)
    extracted_bytes = bits_to_bytes(extracted_bits)
    decrypted_text = decrypt_payload(extracted_bytes, password="")

    # 5. Lossless verification
    metrics = verify_losslessness(cover, restored)
    text_matches = (decrypted_text == message)

    return jsonify({
        "success": True,
        "original_b64": img_to_b64(cover),
        "stego_b64": img_to_b64(stego),
        "restored_b64": img_to_b64(restored),
        "original_hist": compute_histogram(cover),
        "stego_hist": compute_histogram(stego),
        "restored_hist": compute_histogram(restored),
        "extracted_text": decrypted_text,
        "text_matches": text_matches,
        "meta": meta,
        "metrics": {
            "stego_psnr": round(stego_psnr, 2) if stego_psnr != float("inf") else "inf",
            "stego_ssim": round(stego_ssim, 5),
            "restored_mse": float(metrics["mse"]),
            "restored_psnr": "inf" if metrics["psnr"] == float("inf") else round(metrics["psnr"], 2),
            "exact_match": metrics["exact_match"]
        },
        "saved_files": {
            "png": os.path.relpath(saved_png, BASE_DIR),
            "json": os.path.relpath(saved_json, BASE_DIR)
        }
    })

@app.route("/api/embed", methods=["POST"])
def manual_embed():
    """Embed arbitrary payload into uploaded or preset image."""
    data = request.json or {}
    img_b64 = data.get("image_b64")
    message = data.get("message", "").strip()
    if not img_b64 or not message:
        return jsonify({"error": "Missing image or message"}), 400

    try:
        cover = b64_to_img(img_b64)
        payload_bytes = encrypt_payload(message, password="")
        bits = bytes_to_bits(payload_bytes)
        stego, meta = embed_global_histogram_shifting(cover, bits)
        psnr = calculate_psnr(cover, stego)
        ssim = calculate_ssim(cover, stego)

        out_prefix = os.path.join(ENCODED_DIR, "stego_custom")
        saved_png, saved_json = save_stego_object(stego, meta, out_prefix)

        return jsonify({
            "success": True,
            "stego_b64": img_to_b64(stego),
            "meta": meta,
            "psnr": round(psnr, 2) if psnr != float("inf") else "inf",
            "ssim": round(ssim, 5),
            "original_hist": compute_histogram(cover),
            "stego_hist": compute_histogram(stego),
            "saved_png": os.path.relpath(saved_png, BASE_DIR)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/extract", methods=["POST"])
def manual_extract():
    """Extract payload from uploaded stego image and metadata."""
    data = request.json or {}
    stego_b64 = data.get("stego_b64")
    meta = data.get("meta")
    if not stego_b64 or not meta:
        return jsonify({"error": "Missing stego image or metadata"}), 400

    try:
        stego = b64_to_img(stego_b64)
        extracted_bits, restored = extract_and_restore_global(stego, meta)
        raw_bytes = bits_to_bytes(extracted_bits)
        text = decrypt_payload(raw_bytes, password="")

        return jsonify({
            "success": True,
            "extracted_text": text,
            "restored_b64": img_to_b64(restored),
            "restored_hist": compute_histogram(restored)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
