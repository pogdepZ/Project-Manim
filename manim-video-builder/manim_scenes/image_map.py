import os

# Base directory for images
IMAGE_BASE = "images"

def get_image_path(category, item_name):
    """
    Returns the path to a photorealistic image.
    Attempts to find it in the specific scene folder first, then a global assets folder.
    """
    # Example: images/scene_001/user.png
    scene_path = os.path.join(IMAGE_BASE, category, f"{item_name}.png")
    if os.path.exists(scene_path):
        return scene_path
    
    # Fallback or general assets
    general_path = os.path.join(IMAGE_BASE, "general", f"{item_name}.png")
    
    # For now, return the scene_path even if it doesn't exist, 
    # as FlowchartBlock handles missing files with placeholders.
    return scene_path

# Common mappings for the project
KEYWORD_TO_IMAGE = {
    "người": "person",
    "người dùng": "user",
    "chúng ta": "person",
    "robot": "ai_robot",
    "ai": "ai_robot",
    "máy tính": "computer",
    "bàn": "table",
    "ghế": "chair",
    "ly": "cup",
    "cốc": "cup",
    "xe": "car",
    "ô tô": "car",
    "đèn đỏ": "traffic_light",
    "cửa": "door",
    "phòng": "room",
    "pích xơ": "pixels",
    "điểm ảnh": "pixels",
}

def map_keyword_to_path(keyword, scene_id="general"):
    keyword = keyword.lower()
    item_name = KEYWORD_TO_IMAGE.get(keyword, keyword)
    return get_image_path(scene_id, item_name)
