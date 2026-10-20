"""
Cryptographic utility module for payload confidentiality in Reversible Data Hiding.
Supports plaintext passthrough and AES-GCM / PBKDF2 authenticated encryption with password.
"""

import os
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

MAGIC_HEADER = b"RDH_ENC:"

def encrypt_payload(plaintext: str, password: str = "") -> bytes:
    """
    Encrypts a plaintext string into bytes.
    If no password is provided, returns raw UTF-8 bytes.
    If a password is provided, encrypts using AES-GCM with a PBKDF2-derived 256-bit key.
    """
    raw_data = plaintext.encode("utf-8")
    if not password:
        return raw_data
    
    # Generate 12-byte nonce and 16-byte salt
    salt = os.urandom(16)
    nonce = os.urandom(12)
    
    # Derive 32-byte key using PBKDF2-HMAC-SHA256
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations=10000, dklen=32)
    
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, raw_data, None)
    
    # Format: MAGIC (8 bytes) + salt (16 bytes) + nonce (12 bytes) + ciphertext
    return MAGIC_HEADER + salt + nonce + ciphertext

def decrypt_payload(payload_bytes: bytes, password: str = "") -> str:
    """
    Decrypts payload bytes back to the original UTF-8 string.
    Raises ValueError on incorrect password or corrupted ciphertext.
    """
    if payload_bytes.startswith(MAGIC_HEADER):
        if not password:
            raise ValueError("This payload is encrypted. A password is required for decryption.")
        
        offset = len(MAGIC_HEADER)
        salt = payload_bytes[offset:offset + 16]
        nonce = payload_bytes[offset + 16:offset + 28]
        ciphertext = payload_bytes[offset + 28:]
        
        key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations=10000, dklen=32)
        aesgcm = AESGCM(key)
        
        try:
            decrypted = aesgcm.decrypt(nonce, ciphertext, None)
            return decrypted.decode("utf-8")
        except Exception as e:
            raise ValueError("Decryption failed. Incorrect password or data corrupted.") from e
    else:
        # Plain unencrypted text
        return payload_bytes.decode("utf-8", errors="replace")
