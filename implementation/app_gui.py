"""
Tkinter Graphical User Interface for Reversible Data Hiding (RDH) via Histogram Shifting.
Designed for high-impact academic project demonstrations (viva/evaluation).
Features:
- Side-by-side visual comparison (Original vs Stego vs Restored)
- 1-Click Demonstration mode (Instant load, embed, save to /encoded, extract, verify)
- Step-by-step Tabs (Manual Embed, Manual Extract)
- Interactive Histogram visualizer (Peak & Zero bin visualization)
- Real-time MSE = 0.000 and PSNR = inf proof badge
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
from PIL import Image, ImageTk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

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

class RDHApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reversible Data Hiding in Medical Scans | B.Tech Project")
        self.root.geometry("1180x820")
        self.root.minsize(1050, 750)

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Colors
        self.c_bg = "#F8FAFC"
        self.c_primary = "#1E3A8A" # Navy
        self.c_success = "#059669" # Emerald green
        self.c_card = "#FFFFFF"
        self.c_border = "#E2E8F0"
        
        self.root.configure(bg=self.c_bg)

        # State variables
        self.current_cover_path = ""
        self.current_cover_img = None
        self.current_stego_img = None
        self.current_restored_img = None
        self.current_meta = {}

        # PhotoImage references to prevent garbage collection
        self.photo_orig = None
        self.photo_stego = None
        self.photo_rest = None

        self._build_header()
        self._build_tabs()

    def _build_header(self):
        header_frame = tk.Frame(self.root, bg=self.c_primary, padx=20, pady=12)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title_lbl = tk.Label(
            header_frame,
            text="Reversible Data Hiding in Medical Scans Using Histogram Shifting",
            font=("Helvetica", 16, "bold"),
            fg="white",
            bg=self.c_primary
        )
        title_lbl.pack(anchor="w")

        info_lbl = tk.Label(
            header_frame,
            text="Team: Eshan Jogwar (BT24CSD012) | Tushar Sign (BT24CSD001) | Rudravignesh (BT24CSD019)  •  3rd Year Term Project",
            font=("Helvetica", 10),
            fg="#93C5FD",
            bg=self.c_primary
        )
        info_lbl.pack(anchor="w", pady=(2, 0))

    def _build_tabs(self):
        tab_control = ttk.Notebook(self.root)
        
        self.tab_live = tk.Frame(tab_control, bg=self.c_bg, padx=15, pady=10)
        self.tab_embed = tk.Frame(tab_control, bg=self.c_bg, padx=15, pady=10)
        self.tab_extract = tk.Frame(tab_control, bg=self.c_bg, padx=15, pady=10)
        self.tab_hist = tk.Frame(tab_control, bg=self.c_bg, padx=15, pady=10)

        tab_control.add(self.tab_live, text="  ⭐ 1-Click Professor Demo  ")
        tab_control.add(self.tab_embed, text="  Step 1: Embed to /encoded  ")
        tab_control.add(self.tab_extract, text="  Step 2: Extract & Restore  ")
        tab_control.add(self.tab_hist, text="  📊 Histogram Analysis  ")
        
        tab_control.pack(expand=True, fill=tk.BOTH)

        self._init_live_demo_tab()
        self._init_embed_tab()
        self._init_extract_tab()
        self._init_hist_tab()

    # -------------------------------------------------------------
    # TAB 1: 1-CLICK PROFESSOR DEMO (High-impact side-by-side view)
    # -------------------------------------------------------------
    def _init_live_demo_tab(self):
        # Top preset selection bar
        preset_frame = tk.LabelFrame(self.tab_live, text="Quick Presets (For instant demonstration)", bg=self.c_card, font=("Helvetica", 10, "bold"), padx=12, pady=8)
        preset_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(preset_frame, text="Select Medical Scan:", bg=self.c_card, font=("Helvetica", 10)).pack(side=tk.LEFT, padx=(0, 8))

        btn_brain = tk.Button(preset_frame, text="🧠 Brain MRI", bg="#E0E7FF", fg="#3730A3", font=("Helvetica", 9, "bold"), command=lambda: self._load_preset("brain_mri.png", "CONFIDENTIAL: Patient #89021 - MRI Normal. No acute intracranial hemorrhage."))
        btn_brain.pack(side=tk.LEFT, padx=4)

        btn_chest = tk.Button(preset_frame, text="🫁 Chest X-Ray", bg="#E0E7FF", fg="#3730A3", font=("Helvetica", 9, "bold"), command=lambda: self._load_preset("chest_xray.png", "DIAGNOSIS: Clear bilateral lung fields. Cardiothoracic ratio within normal limits."))
        btn_chest.pack(side=tk.LEFT, padx=4)

        btn_knee = tk.Button(preset_frame, text="🦵 Knee Joint", bg="#E0E7FF", fg="#3730A3", font=("Helvetica", 9, "bold"), command=lambda: self._load_preset("knee_scan.png", "SURGICAL NOTE: Femur and tibia alignment normal. Joint space preserved."))
        btn_knee.pack(side=tk.LEFT, padx=4)

        btn_custom = tk.Button(preset_frame, text="📂 Browse Custom Image...", bg="#F1F5F9", font=("Helvetica", 9), command=self._browse_custom_demo)
        btn_custom.pack(side=tk.LEFT, padx=8)

        # Message input row
        msg_frame = tk.Frame(self.tab_live, bg=self.c_bg)
        msg_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(msg_frame, text="Secret Patient Record to Embed:", bg=self.c_bg, font=("Helvetica", 10, "bold")).pack(side=tk.LEFT, padx=(0, 8))
        self.live_msg_var = tk.StringVar(value="CONFIDENTIAL: Patient #89021 - MRI Normal. No acute pathology observed.")
        self.live_msg_entry = tk.Entry(msg_frame, textvariable=self.live_msg_var, font=("Helvetica", 10), width=65)
        self.live_msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        btn_run = tk.Button(
            msg_frame,
            text=" ▶ RUN FULL DEMO (Embed & Lossless Extract) ",
            bg="#10B981",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=12,
            pady=4,
            command=self._execute_live_demo
        )
        btn_run.pack(side=tk.RIGHT)

        # 3 Side-by-Side Images Display Frame
        imgs_frame = tk.Frame(self.tab_live, bg=self.c_card, bd=1, relief=tk.SOLID, padx=10, pady=10)
        imgs_frame.pack(fill=tk.BOTH, expand=True)

        # Column 1: Original
        c1 = tk.Frame(imgs_frame, bg=self.c_card)
        c1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        tk.Label(c1, text="1. Original Medical Scan", font=("Helvetica", 11, "bold"), bg=self.c_card, fg="#1E293B").pack(anchor="center", pady=(0, 4))
        self.lbl_img_orig = tk.Label(c1, bg="#CBD5E1", width=34, height=16, text="[Select or Click Preset]")
        self.lbl_img_orig.pack(expand=True, fill=tk.BOTH)
        self.lbl_info_orig = tk.Label(c1, text="Original Dimension: 512x512", font=("Helvetica", 9), bg=self.c_card, fg="#64748B")
        self.lbl_info_orig.pack(pady=(4, 0))

        # Column 2: Stego (Modified)
        c2 = tk.Frame(imgs_frame, bg=self.c_card)
        c2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        tk.Label(c2, text="2. Stego Scan (Data Hidden)", font=("Helvetica", 11, "bold"), bg=self.c_card, fg="#1E293B").pack(anchor="center", pady=(0, 4))
        self.lbl_img_stego = tk.Label(c2, bg="#CBD5E1", width=34, height=16, text="[Pending Run]")
        self.lbl_img_stego.pack(expand=True, fill=tk.BOTH)
        self.lbl_info_stego = tk.Label(c2, text="Stego Quality: Waiting...", font=("Helvetica", 9), bg=self.c_card, fg="#64748B")
        self.lbl_info_stego.pack(pady=(4, 0))

        # Column 3: Restored (Recovered)
        c3 = tk.Frame(imgs_frame, bg=self.c_card)
        c3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        tk.Label(c3, text="3. Restored Scan (Post-Extraction)", font=("Helvetica", 11, "bold"), bg=self.c_card, fg="#1E293B").pack(anchor="center", pady=(0, 4))
        self.lbl_img_rest = tk.Label(c3, bg="#CBD5E1", width=34, height=16, text="[Pending Run]")
        self.lbl_img_rest.pack(expand=True, fill=tk.BOTH)
        self.lbl_info_rest = tk.Label(c3, text="Restoration: Waiting...", font=("Helvetica", 9), bg=self.c_card, fg="#64748B")
        self.lbl_info_rest.pack(pady=(4, 0))

        # Bottom Results Banner (Big Lossless Verification Banner)
        self.banner_frame = tk.Frame(self.tab_live, bg="#F1F5F9", bd=1, relief=tk.SOLID, padx=12, pady=10)
        self.banner_frame.pack(fill=tk.X, pady=(10, 0))

        self.lbl_banner_status = tk.Label(
            self.banner_frame,
            text="⚡ Status: Ready. Click any preset above and click 'RUN FULL DEMO' to demonstrate.",
            font=("Helvetica", 11, "bold"),
            bg="#F1F5F9",
            fg="#334155"
        )
        self.lbl_banner_status.pack(anchor="w")

        self.lbl_banner_extracted = tk.Label(
            self.banner_frame,
            text="Extracted Record: (none yet)",
            font=("Helvetica", 10),
            bg="#F1F5F9",
            fg="#475569"
        )
        self.lbl_banner_extracted.pack(anchor="w", pady=(3, 0))

        # Auto-load the Brain MRI preset on startup
        self._load_preset("brain_mri.png", "CONFIDENTIAL: Patient #89021 - MRI Normal. No acute intracranial hemorrhage.")

    def _load_preset(self, filename, default_text):
        target_path = os.path.join(SAMPLES_DIR, filename)
        if os.path.exists(target_path):
            self.current_cover_path = target_path
            self.current_cover_img = np.array(Image.open(target_path).convert("L"), dtype=np.uint8)
            self.live_msg_var.set(default_text)
            self._display_thumbnail(self.current_cover_img, self.lbl_img_orig, "orig")
            self.lbl_info_orig.config(text=f"Loaded: {filename} (512x512 Grayscale)")
            self.lbl_banner_status.config(text=f"Loaded {filename}. Click 'RUN FULL DEMO' to run the test.", fg="#334155")
        else:
            messagebox.showwarning("File Missing", f"Could not find sample at {target_path}")

    def _browse_custom_demo(self):
        file_selected = filedialog.askopenfilename(
            title="Select Cover Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff"), ("All files", "*.*")]
        )
        if file_selected:
            self.current_cover_path = file_selected
            self.current_cover_img = np.array(Image.open(file_selected).convert("L"), dtype=np.uint8)
            self._display_thumbnail(self.current_cover_img, self.lbl_img_orig, "orig")
            self.lbl_info_orig.config(text=f"Loaded: {os.path.basename(file_selected)}")

    def _execute_live_demo(self):
        if self.current_cover_img is None:
            messagebox.showwarning("No Image", "Please select or load a medical image first.")
            return
            
        secret_text = self.live_msg_var.get().strip()
        if not secret_text:
            messagebox.showwarning("Empty Message", "Please enter a secret message to embed.")
            return

        try:
            # 1. Encrypt payload
            payload_bytes = encrypt_payload(secret_text, password="")
            secret_bits = bytes_to_bits(payload_bytes)

            # 2. Embed via Histogram Shifting
            stego, meta = embed_global_histogram_shifting(self.current_cover_img, secret_bits)
            self.current_stego_img = stego
            self.current_meta = meta

            # 3. Calculate Stego Fidelity
            stego_psnr = calculate_psnr(self.current_cover_img, stego)
            stego_ssim = calculate_ssim(self.current_cover_img, stego)

            # 4. Save to /encoded folder
            base_name = os.path.splitext(os.path.basename(self.current_cover_path))[0]
            out_path = os.path.join(ENCODED_DIR, f"stego_{base_name}")
            saved_png, saved_json = save_stego_object(stego, meta, out_path)

            # 5. Extract & Reversible Restoration
            loaded_stego, loaded_meta = load_stego_object(saved_png)
            extracted_bits, restored_img = extract_and_restore_global(loaded_stego, loaded_meta)
            self.current_restored_img = restored_img

            # 6. Decrypt extracted payload
            extracted_bytes = bits_to_bytes(extracted_bits)
            recovered_text = decrypt_payload(extracted_bytes, password="")

            # 7. Verify Lossless Restoration Proof
            results = verify_losslessness(self.current_cover_img, restored_img)
            text_matches = (recovered_text == secret_text)

            # Update UI Visuals
            self._display_thumbnail(stego, self.lbl_img_stego, "stego")
            self._display_thumbnail(restored_img, self.lbl_img_rest, "rest")

            self.lbl_info_stego.config(text=f"Stego PSNR: {stego_psnr:.2f} dB | SSIM: {stego_ssim:.5f}")
            self.lbl_info_rest.config(text=f"MSE: {results['mse']:.4f} | PSNR: {results['psnr']}")

            # Update Banner with bold green proof
            if results["exact_match"] and text_matches:
                self.banner_frame.config(bg="#DCFCE7") # Light green
                self.lbl_banner_status.config(
                    text="✓ 100% LOSSLESS RECOVERY CONFIRMED:  MSE = 0.000000  |  Restored PSNR = ∞  |  Bit-for-bit Exact Match!",
                    fg="#166534",
                    bg="#DCFCE7"
                )
                self.lbl_banner_extracted.config(
                    text=f"Extracted Secret Record: \"{recovered_text}\"  (Saved to {os.path.relpath(saved_png, BASE_DIR)})",
                    fg="#14532D",
                    bg="#DCFCE7"
                )
            else:
                self.banner_frame.config(bg="#FEE2E2")
                self.lbl_banner_status.config(text="❌ Verification mismatch detected.", fg="#991B1B", bg="#FEE2E2")

            # Update Histogram Tab
            self._plot_histograms(self.current_cover_img, stego, meta)

        except Exception as e:
            messagebox.showerror("Execution Error", str(e))

    def _display_thumbnail(self, img_array, label_widget, slot_name):
        # Resize to thumbnail maintaining aspect ratio
        thumb_size = (310, 310)
        img_pil = Image.fromarray(img_array).resize(thumb_size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img_pil)
        
        # Keep reference to prevent GC
        if slot_name == "orig":
            self.photo_orig = photo
        elif slot_name == "stego":
            self.photo_stego = photo
        elif slot_name == "rest":
            self.photo_rest = photo

        label_widget.config(image=photo, text="")

    # -------------------------------------------------------------
    # TAB 2: STEP 1 - EMBEDDING TOOL
    # -------------------------------------------------------------
    def _init_embed_tab(self):
        frame = self.tab_embed
        
        # Select Cover Image
        row1 = tk.Frame(frame, bg=self.c_bg)
        row1.pack(fill=tk.X, pady=8)
        tk.Label(row1, text="Cover Image:", font=("Helvetica", 10, "bold"), bg=self.c_bg, width=15, anchor="w").pack(side=tk.LEFT)
        self.embed_path_var = tk.StringVar(value="")
        tk.Entry(row1, textvariable=self.embed_path_var, font=("Helvetica", 10), width=60).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        tk.Button(row1, text="Browse...", command=self._browse_embed_image).pack(side=tk.LEFT)

        # Secret Message Box
        row2 = tk.Frame(frame, bg=self.c_bg)
        row2.pack(fill=tk.BOTH, expand=True, pady=8)
        tk.Label(row2, text="Secret Message:", font=("Helvetica", 10, "bold"), bg=self.c_bg, width=15, anchor="nw").pack(side=tk.LEFT)
        self.embed_text_box = tk.Text(row2, font=("Helvetica", 10), height=6)
        self.embed_text_box.insert("1.0", "Patient ID: #449102\nDiagnosis: Normal pulmonary parenchyma. No consolidation or effusion.")
        self.embed_text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Optional Password
        row3 = tk.Frame(frame, bg=self.c_bg)
        row3.pack(fill=tk.X, pady=8)
        tk.Label(row3, text="Optional Password:", font=("Helvetica", 10, "bold"), bg=self.c_bg, width=15, anchor="w").pack(side=tk.LEFT)
        self.embed_pass_var = tk.StringVar(value="")
        tk.Entry(row3, textvariable=self.embed_pass_var, show="*", font=("Helvetica", 10), width=30).pack(side=tk.LEFT, padx=5)
        tk.Label(row3, text="(Leaves plaintext if empty, or uses AES-GCM if set)", font=("Helvetica", 9), fg="#64748B", bg=self.c_bg).pack(side=tk.LEFT)

        # Embed Action Button
        row4 = tk.Frame(frame, bg=self.c_bg)
        row4.pack(fill=tk.X, pady=15)
        btn_embed = tk.Button(
            row4,
            text=" 🔒 Embed and Save Stego Image to /encoded ",
            bg=self.c_primary,
            fg="white",
            font=("Helvetica", 11, "bold"),
            padx=15,
            pady=8,
            command=self._do_manual_embed
        )
        btn_embed.pack(side=tk.LEFT)

        # Results area
        self.embed_results_var = tk.StringVar(value="Waiting to embed...")
        tk.Label(frame, textvariable=self.embed_results_var, font=("Helvetica", 10), bg="#F1F5F9", fg="#1E293B", justify=tk.LEFT, padx=10, pady=10, bd=1, relief=tk.SOLID).pack(fill=tk.X, pady=10)

    def _browse_embed_image(self):
        f = filedialog.askopenfilename(initialdir=SAMPLES_DIR, filetypes=[("Images", "*.png *.jpg *.bmp")])
        if f:
            self.embed_path_var.set(f)

    def _do_manual_embed(self):
        img_path = self.embed_path_var.get().strip()
        if not img_path or not os.path.exists(img_path):
            messagebox.showwarning("Missing Image", "Please select a valid image file.")
            return
            
        text = self.embed_text_box.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Empty Message", "Please type a secret message to embed.")
            return

        password = self.embed_pass_var.get().strip()

        try:
            cover = np.array(Image.open(img_path).convert("L"), dtype=np.uint8)
            payload_bytes = encrypt_payload(text, password)
            bits = bytes_to_bits(payload_bytes)

            stego, meta = embed_global_histogram_shifting(cover, bits)
            psnr = calculate_psnr(cover, stego)
            ssim = calculate_ssim(cover, stego)

            base_name = os.path.splitext(os.path.basename(img_path))[0]
            out_file = os.path.join(ENCODED_DIR, f"stego_{base_name}")
            saved_png, saved_json = save_stego_object(stego, meta, out_file)

            msg = (
                f"✓ Successfully embedded {len(bits)} bits into stego image!\n"
                f"• Saved Stego Image: {saved_png}\n"
                f"• Saved Metadata: {saved_json}\n"
                f"• Peak Bin P: {meta['peak_bin']} | Zero Bin Z: {meta['zero_bin']}\n"
                f"• Stego Image Fidelity: PSNR = {psnr:.2f} dB | SSIM = {ssim:.5f}"
            )
            self.embed_results_var.set(msg)
            messagebox.showinfo("Success", f"Stego image successfully generated and saved to:\n{saved_png}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # -------------------------------------------------------------
    # TAB 3: STEP 2 - EXTRACTION & RESTORATION TOOL
    # -------------------------------------------------------------
    def _init_extract_tab(self):
        frame = self.tab_extract
        
        # Select Stego Image
        row1 = tk.Frame(frame, bg=self.c_bg)
        row1.pack(fill=tk.X, pady=8)
        tk.Label(row1, text="Stego Image:", font=("Helvetica", 10, "bold"), bg=self.c_bg, width=15, anchor="w").pack(side=tk.LEFT)
        self.extract_path_var = tk.StringVar(value="")
        tk.Entry(row1, textvariable=self.extract_path_var, font=("Helvetica", 10), width=60).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        tk.Button(row1, text="Browse from /encoded...", command=self._browse_extract_image).pack(side=tk.LEFT)

        # Password
        row2 = tk.Frame(frame, bg=self.c_bg)
        row2.pack(fill=tk.X, pady=8)
        tk.Label(row2, text="Password (if set):", font=("Helvetica", 10, "bold"), bg=self.c_bg, width=15, anchor="w").pack(side=tk.LEFT)
        self.extract_pass_var = tk.StringVar(value="")
        tk.Entry(row2, textvariable=self.extract_pass_var, show="*", font=("Helvetica", 10), width=30).pack(side=tk.LEFT, padx=5)

        # Extract Button
        row3 = tk.Frame(frame, bg=self.c_bg)
        row3.pack(fill=tk.X, pady=15)
        btn_extract = tk.Button(
            row3,
            text=" 🔓 Extract Secret & Losslessly Restore Image ",
            bg=self.c_success,
            fg="white",
            font=("Helvetica", 11, "bold"),
            padx=15,
            pady=8,
            command=self._do_manual_extract
        )
        btn_extract.pack(side=tk.LEFT)

        # Extracted Text Display Box
        tk.Label(frame, text="Extracted Secret Message:", font=("Helvetica", 10, "bold"), bg=self.c_bg).pack(anchor="w", pady=(10, 2))
        self.extract_text_box = tk.Text(frame, font=("Helvetica", 10), height=5, bg="#F8FAFC", bd=1, relief=tk.SOLID)
        self.extract_text_box.pack(fill=tk.X, pady=(0, 10))

        # Verification metrics output
        self.extract_results_var = tk.StringVar(value="Waiting to extract...")
        tk.Label(frame, textvariable=self.extract_results_var, font=("Helvetica", 10), bg="#F1F5F9", fg="#1E293B", justify=tk.LEFT, padx=10, pady=10, bd=1, relief=tk.SOLID).pack(fill=tk.X)

    def _browse_extract_image(self):
        f = filedialog.askopenfilename(initialdir=ENCODED_DIR, filetypes=[("PNG Images", "*.png")])
        if f:
            self.extract_path_var.set(f)

    def _do_manual_extract(self):
        stego_path = self.extract_path_var.get().strip()
        if not stego_path or not os.path.exists(stego_path):
            messagebox.showwarning("Missing Image", "Please select a valid stego image from the /encoded folder.")
            return

        password = self.extract_pass_var.get().strip()

        try:
            stego, meta = load_stego_object(stego_path)
            extracted_bits, restored_img = extract_and_restore_global(stego, meta)
            
            raw_bytes = bits_to_bytes(extracted_bits)
            decrypted_text = decrypt_payload(raw_bytes, password)

            self.extract_text_box.delete("1.0", tk.END)
            self.extract_text_box.insert("1.0", decrypted_text)

            # Check if original exists to verify losslessness
            base_name = os.path.basename(stego_path).replace("stego_", "")
            orig_candidate = os.path.join(SAMPLES_DIR, base_name)
            
            verification_note = ""
            if os.path.exists(orig_candidate):
                orig_img = np.array(Image.open(orig_candidate).convert("L"), dtype=np.uint8)
                res = verify_losslessness(orig_img, restored_img)
                if res["exact_match"]:
                    verification_note = (
                        f"\n✓ REVERSIBILITY VERIFIED AGAINST ORIGINAL:\n"
                        f"• Exact Match: True (Bit-for-bit identical)\n"
                        f"• Mean Squared Error (MSE): 0.000000\n"
                        f"• Restored PSNR: INFINITY (Lossless Recovery)"
                    )
                else:
                    verification_note = f"\nMSE mismatch: {res['mse']}"

            status = (
                f"✓ Extraction complete!\n"
                f"• Total Bits Extracted: {len(extracted_bits)}\n"
                f"• Decryption Status: Successful\n"
                f"• Peak Bin Reversed: {meta['peak_bin']} | Direction: {meta['direction']}"
                f"{verification_note}"
            )
            self.extract_results_var.set(status)

        except Exception as e:
            messagebox.showerror("Extraction Error", str(e))

    # -------------------------------------------------------------
    # TAB 4: HISTOGRAM & REVERSIBILITY VISUALIZER
    # -------------------------------------------------------------
    def _init_hist_tab(self):
        self.hist_frame = tk.Frame(self.tab_hist, bg=self.c_bg)
        self.hist_frame.pack(fill=tk.BOTH, expand=True)

        self.fig = Figure(figsize=(9, 5), dpi=100)
        self.ax1 = self.fig.add_subplot(121)
        self.ax2 = self.fig.add_subplot(122)
        self.fig.tight_layout(pad=3.0)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.hist_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Initial placeholder plot
        self.ax1.set_title("Original Image Histogram")
        self.ax2.set_title("Stego Image Histogram (Shifted)")
        self.canvas.draw()

    def _plot_histograms(self, cover_img, stego_img, meta):
        self.ax1.clear()
        self.ax2.clear()

        # Compute histograms
        h_orig, bins = np.histogram(cover_img.ravel(), bins=256, range=[0, 256])
        h_stego, _ = np.histogram(stego_img.ravel(), bins=256, range=[0, 256])

        peak = meta.get("peak_bin", 0)
        zero = meta.get("zero_bin", 255)

        # Plot Original
        self.ax1.bar(range(256), h_orig, color="#3B82F6", width=1.0, alpha=0.8)
        self.ax1.axvline(peak, color="#10B981", linestyle="--", linewidth=1.5, label=f"Peak P ({peak})")
        self.ax1.axvline(zero, color="#EF4444", linestyle="--", linewidth=1.5, label=f"Zero Z ({zero})")
        self.ax1.set_title("1. Original Histogram", fontsize=11, fontweight="bold")
        self.ax1.set_xlabel("Pixel Value (0 - 255)")
        self.ax1.set_ylabel("Pixel Frequency")
        self.ax1.legend(loc="upper right", fontsize=9)
        self.ax1.grid(True, linestyle=":", alpha=0.5)

        # Plot Stego (Shifted)
        self.ax2.bar(range(256), h_stego, color="#8B5CF6", width=1.0, alpha=0.8)
        self.ax2.axvline(peak, color="#10B981", linestyle="--", linewidth=1.5, label=f"Embedded P ({peak})")
        self.ax2.set_title("2. Stego Histogram (Shifted & Embedded)", fontsize=11, fontweight="bold")
        self.ax2.set_xlabel("Pixel Value (0 - 255)")
        self.ax2.set_ylabel("Pixel Frequency")
        self.ax2.legend(loc="upper right", fontsize=9)
        self.ax2.grid(True, linestyle=":", alpha=0.5)

        self.fig.tight_layout(pad=3.0)
        self.canvas.draw()

def main():
    root = tk.Tk()
    app = RDHApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
