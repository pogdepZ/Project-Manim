import requests
from PIL import Image
import os
import io

# Project Keywords and their Search Terms
ASSETS = {
    "user": "person",
    "person": "man",
    "ai_robot": "robot",
    "ai": "intelligence",
    "robot": "android",
    "computer": "laptop",
    "car": "car",
    "table": "table",
    "chair": "chair",
    "cup": "cup",
    "camera": "camera",
    "pixels": "pixels",
    "world": "earth",
    "physical_world": "nature",
    "thế giới": "world",
    "đối tượng": "box",
    "quan hệ": "link",
    "nguyên nhân": "impact",
    "mô hình thế giới": "brain",
    "cửa": "door",
    "đèn đỏ": "traffic",
}

def fetch_and_process(name, query):
    print(f"Fetching raw image for: {name} ({query})...")
    urls = [
        f"https://loremflickr.com/800/800/{query}",
        f"https://picsum.photos/800/800"
    ]
    
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            img = Image.open(io.BytesIO(response.content))
            
            # Standardize size (512x512) and crop center
            width, height = img.size
            min_dim = min(width, height)
            left = (width - min_dim) / 2
            top = (height - min_dim) / 2
            right = (width + min_dim) / 2
            bottom = (height + min_dim) / 2
            
            img = img.crop((left, top, right, bottom))
            img = img.resize((512, 512), Image.Resampling.LANCZOS)
            
            os.makedirs("images/general", exist_ok=True)
            target_path = f"images/general/{name}.png"
            img.save(target_path, "PNG")
            print(f"Successfully saved: {target_path}")
            return # Exit after first success
        except Exception as e:
            print(f"  Failed URL {url}: {e}")
            continue
            
    print(f"Error: Could not fetch any image for {name}")

def main():
    for name, query in ASSETS.items():
        fetch_and_process(name, query)
    print("\nAll raw assets downloaded and processed successfully!")

if __name__ == "__main__":
    main()
