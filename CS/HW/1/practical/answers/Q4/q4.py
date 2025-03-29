from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from PIL import Image
import numpy as np

# Step 1: Derive key from string
data = "40131383-40125933"
sha256_hash = SHA256.new(data=data.encode()).hexdigest()
key = sha256_hash[:32]  # 128-bit key = 32 hex characters

# Step 2: Load PNG and extract RGB data
img = Image.open("image.png").convert("RGB")
pixels = np.array(img)
original_shape = pixels.shape  # Save shape for reshaping later

# Step 3: Flatten pixel data to 1D bytes
flat_pixels = pixels.tobytes()

# Step 4: Encrypt pixel data using ECB
cipher = AES.new(key.encode(), AES.MODE_ECB)
padded_pixels = pad(flat_pixels, AES.block_size)
encrypted_pixels = cipher.encrypt(padded_pixels)

# Step 5: Truncate extra bytes and reshape back
encrypted_pixels = encrypted_pixels[:len(flat_pixels)]
encrypted_array = np.frombuffer(encrypted_pixels, dtype=np.uint8)
encrypted_array = encrypted_array.reshape(original_shape)

# Step 6: Save the encrypted image
encrypted_img = Image.fromarray(encrypted_array, mode="RGB")
encrypted_img.save("image_ecb_encrypted.png")
