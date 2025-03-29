import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from matplotlib import pyplot as plt

def load_image(image_path):
    """ Load and preprocess image (grayscale, 224x224). """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (224, 224))  # Ensure correct size
    return img

def encrypt_image_ecb(img, key):
    """ Encrypt the image using AES-128-ECB. """
    cipher = AES.new(key, AES.MODE_ECB)
    img_bytes = img.tobytes()
    encrypted_bytes = cipher.encrypt(pad(img_bytes, AES.block_size))
    encrypted_img = np.frombuffer(encrypted_bytes, dtype=np.uint8).reshape(224, 224)
    return encrypted_img

def decrypt_image_ecb(encrypted_img, key):
    """ Decrypt the image to show ECB mode reversibility. """
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_bytes = unpad(cipher.decrypt(encrypted_img.tobytes()), AES.block_size)
    decrypted_img = np.frombuffer(decrypted_bytes, dtype=np.uint8).reshape(224, 224)
    return decrypted_img

def show_images(original, encrypted):
    """ Display original and encrypted images. """
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(original, cmap='gray')
    plt.title("Original Image")
    plt.axis("off")
    
    plt.subplot(1, 2, 2)
    plt.imshow(encrypted, cmap='gray')
    plt.title("Encrypted Image (ECB Mode)")
    plt.axis("off")
    
    plt.show()

if __name__ == "__main__":
    image_path = "image.png"  # Replace with your image path
    key = b"1234567890abcdef"  # 16-byte AES key
    
    img = load_image(image_path)
    encrypted_img = encrypt_image_ecb(img, key)
    
    show_images(img, encrypted_img)
