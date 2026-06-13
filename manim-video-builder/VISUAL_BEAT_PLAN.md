# MASTER SCENE PLAN: FROM PIXELS TO CAUSAL WORLD MODELS

## 1. Bảng màu & Style Guide (Global)
- **Background:** #0F1117 (Dark Charcoal)
- **Primary Yellow (Titles):** #F2C94C
- **Teal (Objects/Structure):** #4ECDC4
- **Orange (Action/Force):** #FF6B4A
- **Blue (Data/Models):** #3A86FF
- **Red (Loss/Constraint):** #D76D77
- **Green (Success/Causality):** #6BCB77
- **Fonts:** Sans-serif (Manim default), Size 32 for titles, 24 for labels.

---

## 2. Scene Plan (31 Scenes)

| Scene | Ý tưởng cốt lõi (Core Idea) | Ẩn dụ hình ảnh (Visual Metaphor) | Đối tượng chính |
| :--- | :--- | :--- | :--- |
| **001** | AI vs Human Perception | **Room to Matrix Transformation** | Room shapes, Grid numbers |
| **002** | Tensor representation | **3D Tensor Block & RGB Split** | Cube, 3 Color layers, Camera optics |
| **003** | Representation/Compression | **Information Funnel/Compressor** | Image -> Funnel -> Vector |
| **004** | Entanglement Problem | **Soup vs. Ingredients** | Chaotic circle -> 3 Discrete icons |
| **005** | Unsupervised Learning | **Self-Glow Discovery** | Bounding boxes -> Glowing entities |
| **006** | Slot Invariance | **Swapping Trays** | Slots as containers, Ball/Box icons |
| **007** | Slot Attention | **Interactive Searchlights** | Rays from slots to image features |
| **008** | Competition | **Greedy Piece-picking** | Students icons, Jigsaw pieces |
| **009** | Reconstruction | **Layered Summation** | Object masks stacking to full image |
| **010** | Synthetic vs Real | **The Barrier Reef** | Simple 3D shapes vs Complex noisy photo |
| **011** | ViT & Semantic Features | **The Neural Filter Stack** | Image layers turning into heatmaps |
| **012** | Feature Reconstruction | **Structure over Detail** | Blurry textures vs Sharp silhouettes |
| **013** | Object Relations | **The Semantic Web/Graph** | Objects connected by labeled arrows |
| **014** | Statistical Correlation | **The Ghost Link** | Objects moving together without touch |
| **015** | Intervention (do-operator) | **The Hand of God/Control** | Interactive 'do' button, Direct push |
| **016** | Passive vs Active | **Observer vs Sign-maker** | Split screen: Binoculars vs Hand sign |
| **017** | SCM Equations | **The Mechanism Blueprint** | Nodes as gears/functions, Parent nodes |
| **018** | Physical Collision | **Momentum Transfer** | Ball rolling, Impact flash, Box sliding |
| **019** | Force & Mass | **Scale Calibration** | Large ball = Large slide, Vectors |
| **020** | Why Slots for Causality | **The Entity-Action Bridge** | Slots lighting up as causal nodes |
| **021** | Distribution Shift | **The Rain/Night Filter** | Sunny road -> Stormy road, Logic stays |
| **022** | Object Permanence | **The Shadow Proxy** | Ball behind board, Ghost dot continues |
| **023** | World Model | **The Mental Simulation (Ghost Frame)** | Real state -> Ghost future state |
| **024** | Robotics Planning | **The Force-Constraint HUD** | Robot arm, Fragile cup, Force labels |
| **025** | Self-Driving | **The Relational Safety HUD** | Cars with proximity bubbles & arrows |
| **026** | Embodied AI | **The Key-Door Logic Tree** | Character, Key icon, Logic decision tree |
| **027** | Medical Diagnosis | **The Saliency Spotlight** | X-ray with segmenting lung lesion |
| **028** | Smart City / Digital Twin | **From Video to Vector Dots** | Busy street -> Digital grid with dots |
| **029** | Multi-modal AI | **Text-to-Object Grounding** | Text "Red Cup" -> Arrow to Slot(Red) |
| **030** | Future Challenges | **The Fog of Ambiguity** | Blurry tree, Mystery 'U' node, Power graph |
| **031** | Conclusion | **The Causal World Brain** | Perception + Causality = Final Brain icon |

---

## 3. Mapping: Câu thoại → Visual (Scene 1-5)

| Câu thoại (Voice) | Visual | Animation |
| :--- | :--- | :--- |
| "Khi chúng ta nhìn vào một căn phòng..." | Vẽ căn phòng (bàn, ghế, ly). | `FadeIn` & `Create` objects. |
| "Nhưng đối với AI, mọi thứ bắt đầu từ điểm ảnh..." | Room biến thành lưới ma trận số. | `Transform` objects into a 2D Grid. |
| "Trong thị giác máy tính, ảnh là tensor..." | Lưới 2D xoay thành khối 3D. | `Rotate` & `Extrude` grid. |
| "Ta biến tensor thành véc tơ biểu diễn dê..." | Khối 3D đi qua phễu nén. | `MoveTo` funnel, output a column vector. |
| "Thông tin bị nén vào một véc tơ duy nhất... trộn lẫn." | Biểu tượng xe, người, đèn trong 1 vòng tròn. | `VGroup` rotation/jumbling. |
| "Chúng ta cần tách biệt thông tin... slot." | Vòng tròn lớn vỡ ra thành 3 slot độc lập. | `ReplacementTransform` (One to Many). |

---

## 4. Implementation (Phase 1: Scene 1-5)
*(Code will follow in the next turn)*
