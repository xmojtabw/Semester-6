# %%
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# %%
data = "40131383-40125933"
sha256_hash = SHA256.new(data=data.encode()).hexdigest()
sha256_hash


# %%
key = sha256_hash[: int(128 / 4)]
iv = sha256_hash[int(128 / 4) :]
(key, iv)

# %%
with open("photo.jpg", "rb") as f:
    data = f.read()
padded_data = pad(data, AES.block_size, style="pkcs7")

# %%
cipher = AES.new(key=key.encode(), mode=AES.MODE_ECB)
data_ecb_enc = cipher.encrypt(padded_data)

# %%
with open("photo_ecb_enc.jpg", "wb") as f:
    f.write(data_ecb_enc)
