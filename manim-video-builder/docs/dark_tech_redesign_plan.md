# Dark-Tech Redesign Plan for Scenes 001-031

## Global Design System
- Background: #080D16 / #0A1118 navy-black.
- Title: centered top, #FFD700, bold sans-serif, one title per scene.
- Blocks: rounded rectangles with transparent fill, semantic border colors.
- Entity visuals: raster cutout-style semi-photoreal assets inside bordered blocks.
- Arrows: thick light-gray data arrows; orange-red double arrows for feedback/causal tension.
- Layout: main row occupies the central 60-70% usable width; formula/note stay in bottom annotation zone.
- Audio sync: scene audio starts at t=0; visuals reveal in order and are held until `manifest.duration`.

## Scene-by-scene Redesign Plan
### Scene 001: Mở đầu: A I có thật sự hiểu thế giới không?
- Core idea: Giúp người xem hiểu: Mở đầu: A I có thật sự hiểu thế giới không?.
- Voiceover summary: Pích xơ dẫn tới đối tượng, dẫn tới mối quan hệ, dẫn tới nguyên nhân, dẫn tới mô hình thế giới. Khi chúng ta nhìn vào một căn phòng, chúng ta không thấy một ma trận pích xơ. Chúng ta thấy cái bàn, cái ghế, cái ly, con ngư...
- Main entities/modules: Pixels -> real room objects -> relations -> causes -> world model.
- Formula panel: `Pixels -> Objects -> Relations -> Causes -> World Model`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 52.152s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 002: Pixel không phải là thế giới
- Core idea: Giúp người xem hiểu: Pixel không phải là thế giới.
- Voiceover summary: Ảnh ích thuộc không gian số thực chiều hát nhân vê kép nhân sê. Trong thị giác máy tính, một bức ảnh được biểu diễn dưới dạng một ten xơ ích. Nó có chiều cao hát, chiều rộng vê kép, và số kênh màu sê. Đối với một bức ảnh...
- Main entities/modules: real object -> camera -> RGB tensor -> pixel matrix.
- Formula panel: `X in R^{H x W x C}`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 48.288s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 003: Representation là gì?
- Core idea: Giúp người xem hiểu: Representation là gì?.
- Voiceover summary: Véc tơ dê bằng hàm ép chỉ số theta của ảnh ích. Để A I hiểu ảnh, ta biến ten xơ ích thành một véc tơ biểu diễn dê. Véc tơ biểu diễn này nén thông tin ảnh thành dạng dễ xử lý hơn. Hãy tưởng tượng một chiếc máy nén thông t...
- Main entities/modules: image tensor -> encoder -> compact representation vector.
- Formula panel: `z = f_theta(X)`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 37.752s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 004: Biểu diễn trộn lẫn và bài toán suy luận
- Core idea: Giúp người xem hiểu: Biểu diễn trộn lẫn và bài toán suy luận.
- Voiceover summary: Véc tơ dê chứa thông tin trộn lẫn của xe hơi, người đi bộ và đèn giao thông. Trong các mô hình cũ, tất cả thông tin trong cảnh bị nén vào một véc tơ duy nhất. Thông tin về xe, người và đèn giao thông bị trộn lẫn với nhau...
- Main entities/modules: car/person/traffic light split from one mixed vector.
- Formula panel: `z = [z_car, z_pedestrian, z_light]`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 39.600s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 005: Từ object detection đến học theo trung tâm đối tượng
- Core idea: Giúp người xem hiểu: Từ object detection đến học theo trung tâm đối tượng.
- Voiceover summary: Cảnh gồm tập hợp đối tượng một, đối tượng hai, cho đến đối tượng thứ ca. Nhiều người sẽ nghĩ đến bài toán phát hiện đối tượng trong thị giác máy tính. Bài toán này tìm vật thể và vẽ các khung chữ nhật quanh chúng. Nhưng ...
- Main entities/modules: street scene -> detection boxes -> object slots -> unsupervised structure.
- Formula panel: `Scene = {Object_1, Object_2, ..., Object_K}`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 38.160s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 006: Object slots là gì?
- Core idea: Giúp người xem hiểu: Object slots là gì?.
- Voiceover summary: Tập hợp dê bằng các phần tử dê một, dê hai, cho đến dê ca. Một khái niệm cốt lõi trong học theo trung tâm đối tượng là các slot. Chúng ta hãy tưởng tượng mỗi slot là một chiếc khay chứa thông tin. Nếu cảnh có quả bóng và...
- Main entities/modules: ball and box mapped into separate slots.
- Formula panel: `Z = {z_1, z_2, ..., z_K}`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 39.648s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 007: Cơ chế chú ý theo slot trực giác như thế nào?
- Core idea: Giúp người xem hiểu: Cơ chế chú ý theo slot trực giác như thế nào?.
- Voiceover summary: Hàm chú ý của truy vấn quy, khóa ca, giá trị vê bằng softmax của quy nhân ca chuyển vị chia căn bậc hai của đê, tất cả nhân vê. Cơ chế chú ý theo slot là một thuật toán vô cùng độc đáo. Đầu vào là các đặc trưng ảnh, đầu ...
- Main entities/modules: image features enter Slot Attention and leave as clean slots.
- Formula panel: `Attention(Q, K, V) = softmax(Q K^T / sqrt(d)) V`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 40.512s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 008: Quá trình cạnh tranh giữa các slot
- Core idea: Giúp người xem hiểu: Quá trình cạnh tranh giữa các slot.
- Voiceover summary: Quá trình cạnh tranh dẫn tới sự phân rã biểu diễn không trộn lẫn. Hãy tưởng tượng một nhóm học sinh đang tranh nhau các mảnh ghép của bức tranh. Mỗi học sinh chỉ được chọn một nhóm mảnh ghép liên quan. Nếu một mảnh ghép ...
- Main entities/modules: competition resolves mixed pieces into disentangled slots.
- Formula panel: `Competition -> Disentanglement`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 34.656s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 009: Reconstruction và mask: kiểm tra việc học
- Core idea: Giúp người xem hiểu: Reconstruction và mask: kiểm tra việc học.
- Voiceover summary: Ảnh ích mũ bằng tổng các tích của mặt nạ em ca nhân ảnh thành phần ích mũ ca. Làm thế nào để chúng ta biết các slot đã học đúng cấu trúc? Chúng ta bắt mô hình phải tái tạo lại bức ảnh ban đầu từ các slot. Mỗi slot sẽ tạo...
- Main entities/modules: slots -> decoder -> masks -> reconstruction.
- Formula panel: `x_hat = sum (m_k * x_hat_k)`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 37.416s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 010: Bài toán dữ liệu mô phỏng và thế giới thực
- Core idea: Giúp người xem hiểu: Bài toán dữ liệu mô phỏng và thế giới thực.
- Voiceover summary: Thế giới mô phỏng đơn giản dẫn tới thế giới thực phức tạp. Các nghiên cứu ban đầu thường chỉ chạy trên dữ liệu mô phỏng đơn giản. Dữ liệu này có nền trơn, ánh sáng hoàn hảo và vật thể đơn sắc. Nhưng thế giới thực phức tạ...
- Main entities/modules: synthetic world contrasted with real-world complexity.
- Formula panel: `Synthetic (Simple) -> Real World (Complex)`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 36.552s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 011: Vai trò của V I T và Đi nô trong biểu diễn ngữ nghĩa
- Core idea: Giúp người xem hiểu: Vai trò của V I T và Đi nô trong biểu diễn ngữ nghĩa.
- Voiceover summary: Ảnh gốc đi qua mạng biến đổi thị giác để tạo ra các đặc trưng ngữ nghĩa. Để giải quyết khoảng cách này, chúng ta không dùng điểm ảnh thô trực tiếp. Thay vào đó, ta sử dụng mạng biến đổi thị giác làm nền tảng. Các mô hình...
- Main entities/modules: image -> ViT -> DINO features -> semantic slots.
- Formula panel: `Image -> ViT -> Semantic Features`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 37.752s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 012: Đi nô sau và hướng tái tạo đặc trưng
- Core idea: Giúp người xem hiểu: Đi nô sau và hướng tái tạo đặc trưng.
- Voiceover summary: Sai số tái tạo đặc trưng bằng bình phương độ chuẩn hiệu véc tơ đặc trưng V I T và đặc trưng giải mã. Mô hình Đi nô sau là một bước tiến vô cùng quan trọng gần đây. Thay vì tái tạo điểm ảnh gốc, mô hình này tái tạo lại cá...
- Main entities/modules: slots reconstruct DINO features instead of raw pixels.
- Formula panel: `Feature Reconstruction Loss = ||F_ViT - F_decoded||^2`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 39.528s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 013: Học quan hệ giữa các đối tượng
- Core idea: Giúp người xem hiểu: Học quan hệ giữa các đối tượng.
- Voiceover summary: Mối quan hệ chỉ số i j bằng hàm rê của véc tơ dê i và véc tơ dê j. Sau khi tách được các đối tượng đơn lẻ, chúng ta cần học mối quan hệ. Thế giới không phải là những vật thể nằm tách biệt vô nghĩa. Chúng ta học hàm rê nh...
- Main entities/modules: object pair enters relation function.
- Formula panel: `r_ij = g(z_i, z_j)`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 37.344s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 014: Tương quan thống kê và hạn chế của mô hình truyền thống
- Core idea: Giúp người xem hiểu: Tương quan thống kê và hạn chế của mô hình truyền thống.
- Voiceover summary: Xác suất của biến cố y khi biết biến cố ích. Hầu hết các mô hình trí tuệ nhân tạo hiện nay chỉ học tương quan thống kê. Chúng học xác suất của kết quả y khi quan sát thấy điều kiện ích. Ví dụ, cứ khi thấy quả bóng ở gần ...
- Main entities/modules: observed condition -> correlation -> result, with warning role.
- Formula panel: `P(Y | X)`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 35.664s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 015: Nhân quả: câu hỏi về sự can thiệp
- Core idea: Giúp người xem hiểu: Nhân quả: câu hỏi về sự can thiệp.
- Voiceover summary: Xác suất của biến cố y khi thực hiện can thiệp ích nhận giá trị ích nhỏ. Nhân quả đặt ra một câu hỏi sâu sắc hơn rất nhiều. Nếu chúng ta chủ động can thiệp vào ích, kết quả y sẽ thay đổi như thế nào? Trong lý thuyết nhân...
- Main entities/modules: intervention hand changes physical system and outcome.
- Formula panel: `P(Y | do(X = x))`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 37.776s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 016: Sức mạnh của hành động can thiệp
- Core idea: Giúp người xem hiểu: Sức mạnh của hành động can thiệp.
- Voiceover summary: Sự khác biệt giữa việc quan sát thụ động và can thiệp chủ động. Quan sát thụ động giống như việc chúng ta ngồi nhìn dòng xe cộ chạy. Can thiệp chủ động giống như ta đặt thêm một biển báo dừng xe. Nếu chỉ quan sát, A I dễ...
- Main entities/modules: passive observation contrasted with active intervention.
- Formula panel: `Observation vs Intervention`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 37.368s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 017: Mô hình nhân quả cấu trúc S C M
- Core idea: Giúp người xem hiểu: Mô hình nhân quả cấu trúc S C M.
- Voiceover summary: Biến ích chỉ số i bằng hàm ép chỉ số i của các biến cha chỉ số i và nhiễu u chỉ số i. Mô hình nhân quả cấu trúc S C M mô tả thế giới qua các phương trình. Mỗi biến số ích i được tạo ra bởi một hàm số f i cụ thể. Đầu vào ...
- Main entities/modules: parents/noise feed SCM function to produce variable.
- Formula panel: `X_i = f_i(PA_i, U_i)`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 37.560s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 018: Ví dụ vật lý: quả bóng va chạm cái hộp
- Core idea: Giúp người xem hiểu: Ví dụ vật lý: quả bóng va chạm cái hộp.
- Voiceover summary: Đồ thị va chạm gồm bóng tác động lực dẫn tới hộp chuyển động. Chúng ta hãy phân tích một ví dụ vật lý vô cùng trực quan. Một quả bóng lăn trên mặt sàn phẳng và va chạm vào một chiếc hộp gỗ. Vận tốc của quả bóng chính là ...
- Main entities/modules: ball velocity causes impact force and box motion.
- Formula panel: `Collision Graph: Ball -> Force -> Box`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 36.240s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 019: Phân tích lực và động lượng dưới góc nhìn nhân quả
- Core idea: Giúp người xem hiểu: Phân tích lực và động lượng dưới góc nhìn nhân quả.
- Voiceover summary: Lực bằng khối lượng nhân gia tốc, độ biến thiên động lượng bằng lực nhân khoảng thời gian. Theo định luật vật lý, lực ép bằng khối lượng em nhân gia tốc a. Độ biến thiên động lượng bằng tích của lực ép và thời gian tác d...
- Main entities/modules: mass/acceleration create force, momentum and slide distance.
- Formula panel: `F = m * a, Delta p = F * Delta t`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 36.384s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 020: Tại sao học theo trung tâm đối tượng hỗ trợ nhân quả?
- Core idea: Giúp người xem hiểu: Tại sao học theo trung tâm đối tượng hỗ trợ nhân quả?.
- Voiceover summary: Các slot dẫn tới đồ thị nhân quả, dẫn tới kết quả dự đoán hành vi. Học theo trung tâm đối tượng và nhân quả hỗ trợ nhau rất tự nhiên. Bởi vì các mối quan hệ nhân quả thường xảy ra giữa các thực thể. Chúng ta không nói pí...
- Main entities/modules: slots become causal graph and behavior prediction.
- Formula panel: `Slots -> Causal Graph -> Prediction`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 38.064s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 021: Dịch chuyển phân phối và khả năng tổng quát hóa
- Core idea: Giúp người xem hiểu: Dịch chuyển phân phối và khả năng tổng quát hóa.
- Voiceover summary: Phân phối dữ liệu huấn luyện khác với phân phối dữ liệu thử nghiệm thực tế. Dịch chuyển phân phối xảy ra khi môi trường lúc thử nghiệm khác lúc huấn luyện. Ví dụ, xe tự lái học đi đường vào ban ngày nắng ráo. Nhưng khi c...
- Main entities/modules: sunny training shifts to rainy testing while stable rule remains.
- Formula panel: `P_train(X, Y) != P_test(X, Y)`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 37.704s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 022: Sự tồn tại vĩnh viễn của đối tượng
- Core idea: Giúp người xem hiểu: Sự tồn tại vĩnh viễn của đối tượng.
- Voiceover summary: Sự tồn tại vĩnh viễn duy trì biểu diễn đối tượng từ thời điểm tê sang tê cộng một. Trẻ em học được một quy luật quan trọng gọi là sự tồn tại vĩnh viễn. Khi một vật bị che khuất, nó không hề biến mất khỏi thế giới. Chúng ...
- Main entities/modules: visible ball, occluder, persistent slot, reappearance.
- Formula panel: `Object Permanence: z_t -> z_{t+1}`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 38.496s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 023: Mô hình thế giới trong trí tuệ nhân tạo
- Core idea: Giúp người xem hiểu: Mô hình thế giới trong trí tuệ nhân tạo.
- Voiceover summary: Trạng thái tiếp theo ét chỉ số tê cộng một bằng mô hình thế giới của trạng thái hiện tại ét chỉ số tê và hành động a chỉ số tê. Mô hình thế giới là một bộ não giả lập bên trong hệ thống trí tuệ nhân tạo. Nó dự đoán trạng...
- Main entities/modules: state/action feed world model to predict next state.
- Formula panel: `s_{t+1} = WorldModel(s_t, a_t)`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 41.328s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 024: Ứng dụng trong Robotics: lập kế hoạch hành động
- Core idea: Giúp người xem hiểu: Ứng dụng trong Robotics: lập kế hoạch hành động.
- Voiceover summary: Nhận thức dẫn tới phân tách slot, dẫn tới lập kế hoạch nhân quả, dẫn tới hành động thực tế. Trong ngành robot, robot cần hiểu rõ cấu trúc của môi trường xung quanh. Trên bàn có thể có chiếc cốc thủy tinh và bình nước nón...
- Main entities/modules: robot perception -> cup/bottle slots -> causal plan -> safe grasp.
- Formula panel: `Perception -> Slots -> Causal Plan -> Action`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 38.136s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 025: Xe tự lái: hiểu các mối quan hệ trên đường phố
- Core idea: Giúp người xem hiểu: Xe tự lái: hiểu các mối quan hệ trên đường phố.
- Voiceover summary: Các thực thể kết hợp mối quan hệ giúp lái xe an toàn tuyệt đối. Xe tự lái hoạt động trong một môi trường vô cùng phức tạp và nguy hiểm. Nó cần nhận biết xe hơi xung quanh, người đi bộ và vạch kẻ đường. Hệ thống phải liên...
- Main entities/modules: road entities -> relations -> brake decision -> safe driving.
- Formula panel: `Entities + Relations -> Safe Driving`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 37.080s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 026: A I hiện thân và agent trong môi trường game
- Core idea: Giúp người xem hiểu: A I hiện thân và agent trong môi trường game.
- Voiceover summary: Agent hiện thân thực hiện hành động tác động vào môi trường để nhận phần thưởng. A I hiện thân là những tác nhân thông minh hoạt động trong thế giới vật lý hoặc giả lập. Chúng cần học cách tương tác với đồ vật xung quanh...
- Main entities/modules: embodied agent uses key-door rule to obtain reward.
- Formula panel: `Embodied Agent: Action -> Environment -> Reward`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 38.640s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 027: Hỗ trợ chẩn đoán y tế dựa trên vùng có ý nghĩa
- Core idea: Giúp người xem hiểu: Hỗ trợ chẩn đoán y tế dựa trên vùng có ý nghĩa.
- Voiceover summary: Ảnh y khoa được phân vùng giúp chẩn đoán bệnh chính xác. Dữ liệu ảnh y khoa như chụp cắt lớp hay cộng hưởng từ thường vô cùng phức tạp. Bác sĩ cần tập trung vào các cấu trúc bất thường rất nhỏ. Học theo trung tâm đối tượ...
- Main entities/modules: medical image -> segments -> lesion highlight -> diagnosis.
- Formula panel: `Medical Image -> Segments -> Diagnosis`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 35.136s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 028: Thành phố thông minh và bản sao số
- Core idea: Giúp người xem hiểu: Thành phố thông minh và bản sao số.
- Voiceover summary: Thành phố vật lý ánh xạ sang bản sao số dưới dạng các thực thể có cấu trúc. Trong quản lý đô thị hiện đại, chúng ta xây dựng bản sao số của thành phố. Bản sao số này theo dõi dòng người và phương tiện giao thông. Thay vì...
- Main entities/modules: physical city and cameras map to digital twin and traffic control.
- Formula panel: `Physical City -> Digital Twin (Entities)`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 37.632s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 029: A I đa phương thức: kết nối ngôn ngữ và hình ảnh
- Core idea: Giúp người xem hiểu: A I đa phương thức: kết nối ngôn ngữ và hình ảnh.
- Voiceover summary: Lệnh văn bản được liên kết với đối tượng thực tế để thực thi hành động. A I đa phương thức có khả năng hiểu cả ngôn ngữ nói và hình ảnh thực tế. Hãy lấy ví dụ câu lệnh lấy chiếc cốc màu đỏ trên bàn. Để làm đúng, hệ thống...
- Main entities/modules: text command grounds to red cup slot and robot action.
- Formula panel: `Text Command -> Object Grounding -> Execution`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 37.464s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 030: Các thách thức lớn trong tương lai
- Core idea: Giúp người xem hiểu: Các thách thức lớn trong tương lai.
- Voiceover summary: Sự mơ hồ và các yếu tố gây nhiễu hạn chế việc khám phá quan hệ nhân quả. Mặc dù rất hứa hẹn, hướng đi này vẫn đối mặt với ba thách thức lớn. Đầu tiên là ranh giới của đối tượng thế giới thực rất mơ hồ. Thứ hai, các yếu t...
- Main entities/modules: ambiguity, hidden U, missing intervention and scaling cost.
- Formula panel: `Ambiguity + Confounding -> Causal Discovery Limits`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 38.736s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

### Scene 031: Kết luận: hướng tới mô hình thế giới nhân quả
- Core idea: Giúp người xem hiểu: Kết luận: hướng tới mô hình thế giới nhân quả.
- Voiceover summary: Nhận thức kết hợp nhân quả tạo nên mô hình thế giới nhân quả hoàn thiện. Tóm lại, học theo trung tâm đối tượng cung cấp các biến số biểu diễn độc lập. Học biểu diễn nhân quả kết nối chúng bằng quy luật tự nhiên. Sự kết h...
- Main entities/modules: perception plus causality forms a causal world model.
- Formula panel: `Perception + Causality = Causal World Model`.
- Flowchart layout: left-to-right central row, with bordered blocks and thick arrows.
- Color roles: entities blue, models purple/teal, outputs green, warnings/loss orange-red, math pale yellow.
- Timing notes: reveal title/formula first, then blocks, arrows, annotation; hold all visuals until 39.168s.
- Rule fit: every key idea is inside a bordered block; real nouns use cutout assets; no early fade-out.

## Voiceover / Visual Sync Map
- 0.0s: audio starts; title appears immediately with no future-scene content.
- 0.8-1.6s: formula panel appears only for the current scene formula.
- 1.6-4.8s: flow blocks appear left-to-right in the same order as the spoken concept chain.
- 4.8-7.0s: arrows are created after both connected blocks exist.
- 7.0s-end: note/highlight may appear, but the core visual remains visible until `manifest.duration`.
- Feedback scenes add orange-red double-arrow only after causal/comparison blocks are on screen.