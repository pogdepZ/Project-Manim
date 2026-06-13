#!/usr/bin/env python3
"""
Generate Vietnamese narration for Part 6 & Part 7 using Microsoft Edge TTS.
Run: python generate_narration_part6_7.py

Requires: pip install edge-tts pydub
"""

import asyncio
import argparse
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    import edge_tts
except ImportError:
    print("❌ edge-tts not installed. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts"])
    import edge_tts


VOICE = "vi-VN-HoaiMyNeural"
RATE = "+0%"
SCRIPT_FILE = Path("merged_script_content.txt")

# ── Bảng phiên âm: từ tiếng Anh → cách đọc mà giọng Việt phát âm gần đúng ──
# Thứ tự match: cụm dài trước, ngắn sau (sorted by length desc)
PHONETIC_MAP = {
    "Slot Attention": "s-lót Ờ-ten-sình",
    "DINOSAUR": "Đái-nờ-suồ",
    "DINO": "Đai-nô",
    "MoCo-v3": "Mô-cô vi th-ri",
    "MSN": "em ét en",
    "MAE": "em ây i",
    "SLATE": "Xờ-lây",
    "OSRT": "âu ét a ti",
    "ObSuRF": "óp-sớp",
    "SysBinder": "Xít-bai-đơ",
    "AdaSlot": "Ây-đơ s-lót",
    "VideoSaur": "Vi-đeô soar",
    "DiffFAE": "Đíp ép ây i",
    "PaLM-E": "Pam i",
    "CoSA": "Cô-xa",
    "ISA": "ai ét ây",
    "MoToK": "Mô-tốc",
    "LSD": "eo ét đi",
    "DORSAL": "Đo-sồ", 
    "Neural Radiance Field": "Niu-rồ Ra-đi-ình Phiu",
    "NeRF": "Nớp",
    
    # ── Architecture ──
    "Vision Transformer": "Ví-sình Tren-xờ-pho-mơ",
    "ViT": "Vi-ai-ti",
    "ViT-B/16": "Vi ai ti bi síx-tin",
    "CNN": "xi en en",
    "ResNet34": "Rét-nét thơ-ti-pho",
    "ResNet": "Rét-nét",
    "MLP": "em-eo-pi",
    "Transformer": "Tren-xờ-pho-mơ",
    "Auto-Encoder": "Au-tu En-câu-đơ",
    "Multiview U-Net": "Mân-ti-viu Du-Nét",
    "Encoder": "En-câu-đơ",
    "encoder": "en-câu-đơ",
    "Decoder": "Đi-câu-đơ",
    "decoder": "đi-câu-đơ",
    "backbone": "bắc-bon",
    "self-attention": "xeo Ờ-ten-sình",
    "cross-attention": "cờ-róts Ờ-ten-sình",
    "Cross-Attention": "Cờ-róts Ờ-ten-sình",
    "attention map": "Ờ-ten-sình mép",
    "attention": "Ờ-ten-sình",
    "AdaIN": "Ây-đơ-in",
    
    # ── ML concepts ──
    "Self-Supervised Learning": "Xeo Su-pờ-vai Lơ-nìng",
    "SSL": "ét-ét-eo",
    "pre-training": "pri tren-nìng",
    "pre-trained": "pri trây-nờ",
    "frozen": "frô-zìn",
    "finetuned": "phái-tuỳnh",
    "finetune": "phái-tuỳnh",
    "Knowledge Distillation": "Nó-lịt Đít-xti-lây-sình",
    "Student-Teacher": "Xtiu-đình Tít-chờ",
    "object-centric representation learning": "Óp-tréc xen-trít re-pri-xen-tây-sình Lơ-nìng",
    "object-centric representation": "Óp-tréc xen-trít re-pri-xen-tây-sình",
    "object-centric learning": "Óp-tréc xen-trít Lơ-nìng",
    "object-centric": "Óp-tréc xen-trít",
    "unsupervised": "Ân-su-pờ-vais",
    "autoregressive": "Âu-tu-ri-grét-xìp",
    "loss function": "lót phánh-sình",
    "MSE loss": "em-ét-i lót",
    "MSE": "em-ét-i",
    "loss": "lót",
    "Gumbel Softmax": "Gâm-bồ Xóp-méc",
    "regularization loss": "Re-giu-lơ-rai-dây-sình lót",
    "regularization": "Re-giu-lơ-rai-dây-sình",
    "training signal": "Trây-nìng xít-nồ",
    
    # ── Data & datasets ──
    "CLEVR-3D": "Cờ-le-vờ thri đi",
    "CLEVR": "Cờ-le-vờ",
    "PASCAL VOC": "Pátx-can Vốc",
    "COCO": "Câu-câu",
    "Street View": "Xờ-xtrít Viu",
    "dataset": "đây-tơ-sét",
    "synthetic": "synthetic",
    
    # ── Segmentation & grouping ──
    "segmentation mask": "xéc-mần-tây-sình mátxc",
    "segmentation": "xéc-mần-tây-sình",
    "object grouping": "Óp-tréc grúp-ping",
    "semantic grouping": "xi-men-tíc grúp-ping",
    "face editing": "phây e-đít-tin",
    "facial editing": "phây-sồ e-đít-tin",
    "Mobile Manipulation": "Mâu-bai Mơ-níp-piu-lây-sình",
    "Task Planning": "Tát-xcờ Pờ-len-nìng",
    "embodied AI": "em-bó-địt ây ai",
    
    # ── Technical terms ──
    "feature maps": "Phí-trờ mép",
    "feature space": "Phí-trờ xờ-pây-xờ",
    "features": "Phí-trờ",
    "feature": "Phí-trờ",
    "patches": "pát-chịts",
    "patch": "pátch",
    "discrete tokens": "đít-sờcờ-rít tâu-kình",
    "VQ tokens": "vi-kiu tâu-kình",
    "tokens": "tâu-kình",
    "token": "tâu-kình",
    "latent space": "Lây-tình xờ-pây",
    "latent z0": "Lây-tình di de-râu",
    "latent": "Lây-tình",
    "global semantic consistency": "Gờlâu-bồ xi-men-tíc con-xít-tần-xi",
    "semantic consistency": "xi-men-tíc con-xít-tần-xi",
    "semantic space": "xi-men-tíc xờ-pây",
    "semantic": "xi-men-tíc",
    "global consistency": "Gờlâu-bồ con-xít-tình-xi",
    "pixel reconstruction": "Píc-xồ ri-cần-xtrắc-sình",
    "image reconstruction": "Í-mịt ri-cần-xtrắc-sình",
    "pixels": "Píc-xồs",
    "pixel": "Píc-xồ",
    "pixel-mixture decoder": "Píc-xồ mít-xtrờ đi-câu-đờ",
    "alpha compositing": "Eo-phờ cờm-po-sít-ting",
    "RGB": "a-gi-bi",
    "optical flow": "Óp-ti-cồ phờ-lâu",
    "depth": "đépt",
    "LiDAR": "Lai-đa",
    "volumetric rendering": "Vó-liu-mé-tríc rén-đơ-ring",
    "light-field rendering": "Lai phiu rén-đơ-ring",
    "novel views": "Nó-vồ vius",
    "multi-view": "Mân-ti vius",
    "DVAE": "đi-vi-ây-i",
    "Latent Diffusion Models": "Lây-tình Đi-phiu-sình Mâu-đồ",
    "Latent Diffusion": "Lây-tần Đi-phiu-sình",
    "diffusion denoising": "Đi-phiu-sình đi-noi-sìng",
    "video diffusion": "Vi-đio Đi-phiu-sình",
    "diffusion": "Đi-phiu-sình",
    "composition": "Cơm-pơ-dí-sình",
    "compose": "Cờmpâux",
    "disentanglement": "Đít-xen-tén-gồ-mình",
    "disentangle": "Đít-xen-tén-gồ",
    "low-level features": "Lâu-le-vồ Phí-trờ",
    "low-level": "Lâu-le-vồ",
    "object property": "Óp-tréc pró-pơ-ti",
    "object slots": "Óp-tréc s-lót",
    "slots": "s-lót",
    "slot": "s-lót",
    "reference frames": "Ré-phơ-rình phờ-rem",
    "3D Inductive Bias": "Thri đi In-đắc-típ bai-ợtx",
    "inductive bias": "In-đắc-típ bai-ợtx",
    "3D": "thri đi",
    "zero-shot generation": "Di-râu-sót gié-nơ-rây-sình",
    "zero-shot": "Di-râu-sót",
    "PSNR": "pi-ét-en-a",
    "FID score": "ép-ai-đi xờ-co",
    "FID": "ép-ai-đi",
    "CLIP": "Cờ-líp",
    "from scratch": "phờ-rom xờ-cờ-rátch",
    "scale": "xờ-kêu",
    "input": "in-pút",
    "output": "ao-pút",
    "Generative AI": "Gié-nờ-rây-típ ây-ai",
    "Generative Model": "Gié-nờ-rây-típ mâu-đồ",
    "Robotics": "Râu-bó-tíc",
    "Large Language Model": "Lát léng-guỵch mâu-đồ",
    "LLM": "eo-eo-em",
    
    # ── Scene-specific terms (SAVi, Waymo, etc.) ──
    "SAVi++": "Xa-vi cộng cộng",
    "SAVi": "Xa-vi",
    "Waymo Open Dataset": "quay-mô Âu-pình đây-tơ-sét",
    "autonomous driving": "Au-tó-nơ-mớt đờ-rai-vìng",
    "Multi-dSprites": "Mân-ti đi-xờ-pờ-rai",
    "MultiShapeNet": "Mân-ti-sép-nét",
    "ImageNet": "I-mịt-nét",
    "DALL-E": "Đa-li",
    "Image GPT": "I-mịt gi-pi-ti",
    "CVPR 2024": "xi-vi-pi-a 2024",
    "CVPR": "xi-vi-pi-a",
    "LDM": "eo-đi-em",
    "VQ-VAE": "vi-kiu vi-ây-i",
    "UNet": "Du-Nét",
    "Perceiver": "Pơ-xi-vơ",
    "PaLM": "Pam",
    
    # ── ML concepts (additions) ──
    "convolutional layer": "con-vơ-lu-sồ-nồ lây-ờ",
    "convolutional": "con-vơ-lu-sồ-nồ",
    "receptive field": "rì-xép-típ phiu",
    "self-distillation": "xeo đít-xti-lây-sình",
    "transfer learning": "tren-phờ Lơ-nìng",
    "Knowledge Distillation": "Nó-lịt Đít-xti-lây-sình",
    "Student-Teacher": "s-tiu-đình Tít-chờ",
    "competitive attention": "Cờm-pé-tí-tịp Ờ-ten-sình",
    "positional encoding": "Pâu-dít-sồ-nồ en-câu-đìn",
    "position encoding": "Pâu-dí-sình en-câu-đìn",
    "object discovery": "Óp-tréc đít-xcó-vơ-ri",
    "object disentanglement": "Óp-tréc Đít-xen-ten-gồ-mình",
    "subset selection": "xắp-xết xe-lếch-sình",
    "dynamic slot selection": "đái-na-mích s-lót xi-lếch-sình",
    "dynamic slot number": "đai-ná-mích s-lót nâm-bờ",
    "predefine": "pri-đi-phai",
    "differentiable": "đi-phe-ren-sờ-bồ",
    "end-to-end": "en-tu-en",
    "ARI": "ây-a-ai",
    "mBO": "em-bi-âu",
    "CorLoc": "co-lốc",
    "temporal feature similarity": "Tem-pô-rồ Phí-trờ xi-mi-la-ri-ti",
    "temporal similarity": "Tem-pô-rồ xi-mi-la-ri-ti",
    "temporal": "Tem-pô-rồ",
    "similarity matrix": "xi-mi-la-ri-ti mây-tríx",
    "cross-entropy loss": "cờ-rót en-trơ-pi lót",
    "cross-entropy": "cờ-rót en-trơ-pi",
    "cosine distance": "câu-xai đít-tần",
    "color statistics": "ca-lờ s-ta-tít-tịc",
    "key component": "ki Cờm-pâu-nình",
    "reconstruction loss": "ri-cần-s-trắc-sình lót",
    "reconstruction": "ri-cần-s-trắc-sình",
    "reconstruct": "ri-cần-s-trắc",
    "representations": "re-pri-xen-tây-sình",
    "representation": "re-pri-xen-tây-sình",
    
    # ── Decoder-specific terms ──
    "Slot-Decoding Dilemma": "s-lót đi-câu-đìn Đi-lê-mơ",
    "Pixel Independence": "Píc-xồ In-đi-pen-đình",
    "Spatial Broadcast Network": "s-pa-siồ bờ-rót-cát Nét-wước",
    "Spatial Broadcast": "s-pa-siồ bờ-rót-cát-xờ",
    "capacity": "Ca-pá-xi-ti",
    "concept modules": "Cón-xẹp mâu-điu",
    "word embedding": "wớt em-bét-đìn",
    "embedding": "em-bét-đìn",
    "superposition": "xu-pơ-zí-sình",
    "text supervision": "téch xu-pờ-vít-sình",
    "text embedding": "tếch em-bét-đìn",
    "camera pose": "Camera Pâu",
    "ray direction": "rây đai-réch-sình",
    "multiview diffusion": "Mân-ti-viu Đi-phiu-sình",
    "image generation": "I-mịt gié-nơ-rây-sình",
    "Visual Concept Library": "Ví-sù-ồ Cón-xẹp Lái-bơ-re-ri",
    "visual concepts": "Ví-sù-ồ Cón-xẹp",
    "learned dictionary": "lơn-đờ đít-sình-ne-ri",
    "clustering": "Cờ-lớt-tơ-rin",
    "clusters": "Cờ-lớt-tơ",
    "Gaussian noise": "Gâu-xi-ần noi",
    "denoising process": "đi-noi-sìng prâu-xết",
    "denoising": "đi-noi-sìng",
    "denoise": "đi-noi",
    "object removal": "Óp-tréc ri-mu-vồ",
    "insertion": "in-xơ-sình",
    "background swapping": "bắc-grao s-quáp-pìng",
    "background separation": "bắc-grao xe-pơ-rây-sình",
    "FiLM modulation": "Phim mâu-điu-lây-sình",
    "conditioning": "Cần-đít-sình-ning",
    "scene representation": "xin ri-pri-xen-tây-sình",
    "viewing direction": "viu-in đai-réch-sình",
    "volume density": "Vó-liu đen-xi-ti",
    "radiance": "Ra-đi-ình",
    "render": "rén-đờ",
    "composite": "Cờm-po-sít",
    "Allocation Transformer": "A-lô-kây-sình Tren-s-pho-mơ",
    "Mixing Block": "Mít-xìn b-lốc",
    "Render MLP": "Rén-đờ em-eo-pi",
    "weighted sum": "quây-tịt xâm",
    "weighted mean": "quây-tịt min",
    "alpha map": "Eo-phờ mép",
    "shared MLP": "xe-a em-eo-pi",
    
    # ── Properties & editing ──
    "systematic generalization": "xít-tơ-ma-tíc gié-nơ-rơ-lai-dây-sình",
    "modalities": "mâu-đa-li-ti",
    "motion segmentation": "mâu-sình xéc-mần-tây-sình",
    "pseudo segmentation masks": "xu-đâu xéc-mần-tây-sình mátxc",
    "pseudo": "pxu-đâu",
    "ground-truth": "Grao tru",
    "ground truth": "Grao tru",
    "spatial symmetry": "s-pa-siồ xi-mê-tri",
    "slot-centric": "s-lót xen-trít",
    "orientation": "au-ri-en-tây-sình",
    "compositionally": "Cờm-pơ-dít-sồ-nồ-li",
    "pose": "Pâu",
    "expression": "éch-s-pré-sình",
    "lighting": "lai-tìn",
    "identity": "ai-đén-ti-ti",
    "Control": "Con-trâu",
    "bridge": "Bờ-rít",
    "visual understanding": "Ví-sù-ồ ân-đờ-s-ten-đìn",
    "reasoning": "ri-sình-nình",
    "swap": "s-quáp",
    "provider": "prâu-vai-đờ",
    "scene": "xin",
    "bias": "bai-ợtx",
    
    # ── Misc ──
    "Grounded Slot Dictionary": "Gờ-rao-địt s-lót Đích-sình-ne-ri",
    "GSD Binding": "gi-ét-đi bai-đìn",
    "GSD": "gi-ét-đi",  
    "K-means clustering": "Kây-min Cờ-lớt-tờ-rìng",
    "K-means": "Kây minxờ",
    "Slot Mixer Decoder": "s-lót mít-xờ đi-câu-đờ",
    "Slot Mixer": "s-lót mít-xờ",
    "Frankenstein-like images": "Phờ-răng-kền-s-tâi í-mịt",
    "Frankenstein images": "Phờ-răng-kền-s-tâi í-mịt",
    "paradigms": "Pế-ra-đaim",
    "Paradigm": "Pế-ra-đaim",
    "Substituting": "Xắp-xti-tiu-tìn",
    "Manipulating": "Mờ-níp-piu-lây-tìn",
    "Moving": "Mú-vìn",
    "Invariant Slot Attention": "In-ve-ri-ình s-lót Ờ-ten-sình",
    "Invariant": "In-ve-ri-ình",
    "Decoupling Decoding": "Đi-cắp-p-lình Đi-câu-đin",
    "Decoupling": "Đi-cắp-plìn",
    "Student": "Sờ-tiu-đình",
    "Teacher": "Tít-chờ",
    "bottleneck": "bót-tồ-nếc",
    "signal": "xít-nồ",
    "target": "ta-gịt",
    "knowledge": "nó-lịt",
    "hidden": "hít-đình",
    "pipeline": "pai-plai",
    "UPGRADING": "úp-grey-đing",
    "DECODER": "đi-câu-đờ",
    "Pipeline": "pai-plai",
    "instance-level separation": "in-s-tần le-vồ xe-pơ-rây-sình",
    "instance-level": "in-s-tần le-vồ",
    "first choice": "Phớt chois",
    "out-perform": "aot pơphom",
    "powerful": "Pao-ờ-phu",
    "object": "Óp-tréc",
    "texture": "Tếch-trờ",
    "mask": "mátxc",
    "layer": "lây-ờ",
    "frame": "phờ-rem",
    "model": "mâu-đồ",
    "occlusion": "ốc-cờ-lu-sình",
    "diverge": "đai-vớ",
    "finetuning": "phái-t-ning",
    "Slot-Conditioned Diffusion": "s-lót cần-đít-sần Đi-phiu-sình",
    "slot-conditioned": "s-lót cần-đít-sần",
    "Denoising Network": "Đi-noi-sìng Nét-wước",
    "Linear layer": "Li-ni-ờ lây-ờ",
    "Linear": "Li-ni-ờ",
    "context views": "con-téch vius",
    "Slot Decoder": "s-lót đi-câu-đờ",
    
    # ── Missing Terms Added ──
    "AI": "ây ai",
    "Computer Vision": "Cầm-piu-tơ Ví-sình",
    "Autoregressive": "Âu-tu-ri-grét-xìp",
    "Context": "Con-téch",
    "DINO-trained": "Đai-nô trây-nờ",
    "Depth": "Đép-th",
    "Flow": "Phờ-lâu",
    "Gumbel-Softmax": "Gâm-bồ Xóp-méc",
    "Image": "I-mịt",
    "NeRF-based": "Nớp bây-xờ",
    "PASCAL": "Pát-xcan",
    "Pixel-mixture": "Píc-xồ mít-xtrờ",
    "Pre-trained": "Pri trây-nờ",
    "Reconstructed": "Ri-cần-xtrắc-tựt",
    "Tokenization": "Tâu-kìn-nai-zây-sình",
    "Tutorial": "Tu-tô-ri-ồ",
    "algorithm": "eo-gô-ri-dầm",
    "allocation": "a-lô-kây-sình",
    "broadcast": "bờ-rót-cát-xờ",
    "computational burden": "cầm-piu-tây-sồ-nồ bơ-đình",
    "discrete": "đít-sờcờ-rít",
    "editing": "e-đít-tin",
    "object-centricness": "óp-tréc xen-trít-nết",
    "robot": "râu-bót",
    "robotics": "râu-bó-tíc",
    "slot-based": "s-lót bây-xờ",
    "block": "bờ-lốc",
    "blocks": "bờ-lốc",
    "bind": "bai-đờ",
    "cheeks": "chích-xờ",
    "eyes": "ai-dờ",
    "forehead": "pho-hét",
    "hair": "he-ờ",
    "facial": "phây-sồ",
    "class": "cờ-lát-xờ",
    "color": "ca-lờ",
    "consistency": "con-xít-tần-xi",
    "control": "con-trâu",
    "convert": "con-vợt",
    "data": "đây-tờ",
    "decode": "đi-câu-đờ",
    "decoding": "đi-câu-đình",
    "demo": "đê-mô",
    "elements": "e-lê-mình",
    "encode": "en-câu-đờ",
    "excess": "ếch-xét",
    "freeze": "p-ri-zờ",
    "function": "phánh-sình",
    "general": "gié-nơ-rồ",
    "generative": "gié-nờ-rây-típ",
    "global": "gờlâu-bồ",
    "grab": "gờ-ráp",
    "group": "grúp",
    "integrate": "in-tờ-grây-tờ",
    "labels": "lây-bồ",
    "language-based": "léng-guỵch bây-xờ",
    "learned": "lơn-đờ",
    "learning": "lơ-nìng",
    "maps": "mép-xờ",
    "masks": "mát-xờ",
    "metric": "mê-tríc",
    "minimize": "mi-ni-mai",
    "multiple": "mân-ti-pồ",
    "novel": "nó-vồ",
    "overlay": "âu-vơ-lây",
    "position": "pâu-dí-sình",
    "predict": "pri-đích",
    "realistic": "ri-ồ-lít-tíc",
    "region": "ri-giình",
    "rendering": "rén-đơ-ring",
    "sample": "xem-pồ",
    "scores": "xờ-co",
    "sequence": "xi-quần",
    "shape": "sép",
    "space": "xờ-pây",
    "structure": "xờ-trắc-chờ",
    "subset": "xắp-xét",
    "task": "tát-xờ-cờ",
    "teacher": "tít-chờ",
    "train": "trên",
    "training": "trên-nìng",
    "transformer": "tren-xờ-pho-mơ",
    "types": "tai-pờ",
    "useful": "yếu-phùn",
    "video": "vi-đi-ô",
    "view": "viu",
    "views": "vius",
    "weight": "quết",
    "weights": "quết-xờ",
}

def phonetic_substitute(text):
    """Thay thế các từ tiếng Anh bằng phiên âm để giọng Việt đọc gần đúng."""
    # Sort by key length (longest first) để tránh match cụm con trước cụm dài
    sorted_terms = sorted(PHONETIC_MAP.keys(), key=len, reverse=True)

    # Dùng placeholder để tránh double-replace
    placeholders = {}

    for term in sorted_terms:
        pattern = re.escape(term)
        regex = re.compile(r"(?<![a-zA-ZÀ-ỹ0-9_-])" + pattern + r"(?![a-zA-ZÀ-ỹ0-9_-])", re.IGNORECASE)

        def replacer(m, t=term):
            key = f"__PH{len(placeholders)}__"
            placeholders[key] = PHONETIC_MAP[t]
            return key

        text = regex.sub(replacer, text)

    for key, val in placeholders.items():
        text = text.replace(key, val)

    return text




def load_narrations(script_file=SCRIPT_FILE):
    if not script_file.exists():
        raise FileNotFoundError(f"Missing narration script: {script_file}")

    content = script_file.read_text(encoding="utf-8")
    if "\\n" in content and "\n" not in content.replace("\\n", ""):
        content = content.replace("\\n", "\n")

    pattern = re.compile(
        r"^###\s+SCENE\s+(\d+):[^\n]*\n"
        r"\*\*Thời gian video:\s*TBD\*\*\n\n"
        r'"(.*?)"\n\n---',
        re.MULTILINE | re.DOTALL,
    )

    narrations = {}
    for match in pattern.finditer(content):
        scene_number = int(match.group(1))
        text = " ".join(match.group(2).split())
        narrations[f"scene{scene_number}"] = text

    return dict(sorted(narrations.items(), key=lambda item: int(item[0].replace("scene", ""))))


async def generate_narration(key, text, output_file, skip_existing=False):
    output_path = Path(output_file)
    if skip_existing and output_path.exists() and output_path.stat().st_size > 0:
        print(f"↷ Skipping existing: {output_file}")
        return "skipped"

    max_attempts = 10
    for attempt in range(1, max_attempts + 1):
        print(f"🎙️  Generating: {output_file}... attempt {attempt}/{max_attempts}")
        try:
            phonetic_text = phonetic_substitute(text)
            communicate = edge_tts.Communicate(text=phonetic_text, voice=VOICE, rate=RATE)
            await communicate.save(output_file)
            if Path(output_file).stat().st_size == 0:
                raise RuntimeError("TTS returned an empty file")
            print(f"✓ {output_file} created ({len(text)} chars)")
            return "generated"
        except Exception as exc:
            if attempt == max_attempts:
                print(f"❌ Failed to generate {output_file} after {max_attempts} attempts.")
                raise
            sleep_time = 3 + attempt * 2
            print(f"  retrying after TTS error: {exc}. Waiting {sleep_time}s...")
            await asyncio.sleep(sleep_time)


async def main():
    parser = argparse.ArgumentParser(
        description="Generate Vietnamese narration for Part 6 & Part 7 using Edge TTS."
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Do not regenerate mp3 files that already exist and are non-empty.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only parse and list narration scenes; do not call Edge TTS.",
    )
    parser.add_argument(
        "--test",
        type=str,
        help="Chỉ test đoạn text ngắn. Ví dụ: --test 'Slot Attention'",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Vietnamese Narration Generator — Part 6 & Part 7")
    print("=" * 60)
    
    if args.test:
        print(f"🧪 Đang test phát âm cho: '{args.test}'")
        output_file = "test_audio.mp3"
        await generate_narration("test", args.test, output_file)
        print(f"\n✅ Đã tạo file test tại: {output_file}")
        print("Hãy mở file này để nghe thử!")
        return

    output_dir = Path("narration_part6_7")
    output_dir.mkdir(exist_ok=True)
    narrations = load_narrations()
    if not narrations:
        raise RuntimeError(f"No narrations found in {SCRIPT_FILE}. Refusing to report success.")

    print(f"\n📁 Output directory: {output_dir}")
    print(f"🎤 Voice: {VOICE}\n")
    print(f"🧾 Loaded {len(narrations)} narration scenes from {SCRIPT_FILE}")

    if args.dry_run:
        for key, text in narrations.items():
            print(f"  {key}: {len(text)} chars")
        print("\nDry run only. No audio files were generated.")
        return

    generated_count = 0
    skipped_count = 0
    for key, text in narrations.items():
        output_file = output_dir / f"{key}.mp3"
        result = await generate_narration(key, text, str(output_file), skip_existing=args.skip_existing)
        if result == "generated":
            generated_count += 1
        elif result == "skipped":
            skipped_count += 1

    print("\n" + "=" * 60)
    print(f"✓ Done. Generated: {generated_count}, skipped existing: {skipped_count}")
    print("=" * 60)
    print("\nNext step: Run: python combine_part6_7.py")


if __name__ == "__main__":
    asyncio.run(main())
