import os
import subprocess
import glob
import sys
from pathlib import Path
import imageio_ffmpeg

def check_ffmpeg():
    """Kiểm tra xem ffmpeg đã được cài đặt chưa."""
    try:
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def main():
    print("=" * 60)
    print("🎬 TOOL GHÉP VIDEO NHÓM (KHÔNG GIẢM CHẤT LƯỢNG) 🎬")
    print("=" * 60)

    if not check_ffmpeg():
        print("❌ Lỗi: Không tìm thấy 'ffmpeg' trên hệ thống.")
        print("Vui lòng cài đặt ffmpeg và thêm vào PATH để tiếp tục.")
        sys.exit(1)

    # Thư mục chứa các video của các thành viên
    # Mặc định là thư mục hiện tại hoặc một thư mục cụ thể
    input_folder = input("\nNhập đường dẫn thư mục chứa các video của nhóm (nhấn Enter để dùng thư mục hiện tại): ").strip()
    if not input_folder:
        input_folder = "."

    if not os.path.isdir(input_folder):
        print(f"❌ Lỗi: Thư mục '{input_folder}' không tồn tại.")
        sys.exit(1)

    # Tự động tìm tất cả các file .mp4
    video_files = glob.glob(os.path.join(input_folder, "*.mp4"))
    
    # Loại trừ file kết quả nếu đã tồn tại từ trước để tránh loop
    output_filename = "FINAL_GROUP_PRESENTATION.mp4"
    if os.path.abspath(output_filename) in [os.path.abspath(f) for f in video_files]:
        video_files = [f for f in video_files if os.path.abspath(f) != os.path.abspath(output_filename)]

    if not video_files:
        print(f"❌ Không tìm thấy file .mp4 nào trong thư mục '{input_folder}'.")
        sys.exit(1)

    # Sắp xếp các video theo thứ tự tên file (VD: 1_part1.mp4, 2_part2.mp4, ...)
    video_files.sort()

    print("\nCác video sẽ được ghép theo thứ tự sau:")
    for i, vf in enumerate(video_files, 1):
        print(f"  {i}. {os.path.basename(vf)}")
    
    confirm = input("\nBạn có chắc chắn muốn ghép các video này không? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Đã hủy thao tác.")
        sys.exit(0)

    # Tạo file list cho ffmpeg (định dạng: file 'đường/dẫn/tới/file.mp4')
    list_filename = "concat_list.txt"
    with open(list_filename, "w", encoding="utf-8") as f:
        for vf in video_files:
            # ffmpeg yêu cầu escape ký tự đặc biệt hoặc dùng đường dẫn tương đối an toàn
            # Dùng absolute path và đổi \ thành / cho an toàn với ffmpeg trên windows
            safe_path = os.path.abspath(vf).replace("\\", "/")
            f.write(f"file '{safe_path}'\n")

    print("\nĐang tiến hành ghép video (copy stream, không re-encode để giữ nguyên chất lượng)...")
    
    # Lệnh ghép video sử dụng concat demuxer (nhanh và không giảm chất lượng)
    command = [
        imageio_ffmpeg.get_ffmpeg_exe(),
        "-y",               # Ghi đè file nếu đã tồn tại
        "-f", "concat",     # Sử dụng concat demuxer
        "-safe", "0",       # Cho phép dùng absolute path
        "-i", list_filename,
        "-c", "copy",       # Copy nguyên gốc (không re-render -> cực nhanh và giữ 100% chất lượng)
        output_filename
    ]

    try:
        subprocess.run(command, check=True)
        print("\n" + "=" * 60)
        print(f"✅ THÀNH CÔNG! Video hoàn chỉnh đã được lưu tại:")
        print(f"👉 {os.path.abspath(output_filename)}")
        print("=" * 60)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Có lỗi xảy ra trong quá trình ghép video: {e}")
    finally:
        # Dọn dẹp file list tạm
        if os.path.exists(list_filename):
            os.remove(list_filename)

if __name__ == "__main__":
    main()
