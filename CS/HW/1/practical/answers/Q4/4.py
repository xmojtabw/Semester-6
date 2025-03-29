from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PIL import Image
import numpy as np


data = "40131383-40125933"
sha256_hash = SHA256.new(data=data.encode()).hexdigest()

key = bytes.fromhex(sha256_hash[: int(128 / 4)])
iv = bytes.fromhex(sha256_hash[int(128 / 4) :])

img = Image.open("image.png").convert("RGB")
pixels = np.array(img)
original_shape = pixels.shape
data = pixels.tobytes()

ecb_cipher = AES.new(key=key, mode=AES.MODE_ECB)
data_ecb_enc = ecb_cipher.encrypt(data)

ecb_encrypted_array = np.frombuffer(data_ecb_enc, dtype=np.uint8)
ecb_encrypted_array = ecb_encrypted_array.reshape(original_shape)
ecb_encrypted_img = Image.fromarray(ecb_encrypted_array, mode="RGB")
ecb_encrypted_img.save("image_ecb_encrypted.png")

cbc_cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
data_cbc_enc = cbc_cipher.encrypt(data)

cbc_encrypted_array = np.frombuffer(data_cbc_enc, dtype=np.uint8).reshape(
    original_shape
)
cbc_encrypted_img = Image.fromarray(cbc_encrypted_array, mode="RGB")
cbc_encrypted_img.save("image_cbc_encrypted.png")


data_cbc_dec = AES.new(key=key, mode=AES.MODE_CBC, iv=iv).decrypt(data_cbc_enc)

cbc_decrypted_array = np.frombuffer(data_cbc_dec, dtype=np.uint8).reshape(
    original_shape
)
cbc_decrypted_img = Image.fromarray(cbc_decrypted_array, mode="RGB")
cbc_decrypted_img.save("image_cbc_decrypted.png")


print("Match!") if SHA256.new(data=data).digest() == SHA256.new(
    data=data_cbc_dec
).digest() else print("not match!")
