import os
import re
import requests

# Minta input nama file dari user
txt_file = input("Masukkan nama file txt (contoh: drama_links.txt): ")

if not os.path.exists(txt_file):
    raise FileNotFoundError(f"File '{txt_file}' tidak ditemukan.")

# Baca isi file
with open(txt_file, "r", encoding="utf-8") as f:
    content = f.read()

# Ambil nama drama
drama_name_match = re.search(r"Drama:\s*(.+)", content)
if not drama_name_match:
    raise ValueError("Nama drama tidak ditemukan di file.")
drama_name = drama_name_match.group(1).strip()

# Buat folder sesuai nama drama
folder_name = drama_name.replace(":", "").replace("/", "-")
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Ambil semua URL video
urls = re.findall(r"https?://\S+", content)
if not urls:
    raise ValueError("Tidak ada URL video ditemukan.")

# Download satu per satu
for i, url in enumerate(urls, start=1):
    episode_filename = f"episode_{i}.mp4"
    save_path = os.path.join(folder_name, episode_filename)

    print(f"Mengunduh Episode {i}...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Selesai: {save_path}")
    else:
        print(f"Gagal mengunduh Episode {i}: {response.status_code}")
