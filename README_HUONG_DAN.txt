TTT AI — BỘ DỰ ÁN FLASK
========================

TÍNH NĂNG
- Giao diện bảng điều khiển nền tối xanh neon, tiếng Việt.
- Trợ lý hologram ở góc dưới bên phải, có hiệu ứng vòng sáng/chuyển động và cửa sổ chat.
- Chọn ảnh, xem trước, kéo-thả, thông tin tệp và độ phân giải.
- Mô hình COCO-SSD chạy trên trình duyệt để khoanh khung một số lớp vật thể đã học.
- Gọi AI thị giác để mô tả ảnh và trả lời câu hỏi về ảnh (cần OPENAI_API_KEY và có thể phát sinh phí API).
- Xuất báo cáo TXT.
- Giới hạn chọn ảnh trên giao diện 500 MB.

LƯU Ý VỀ 500 MB
Giới hạn 500 MB là giới hạn chọn tệp trong trình duyệt. Ảnh gốc được giữ ở trình duyệt; khi gửi cho AI, trang sẽ thu nhỏ/nén thành ảnh JPEG nhỏ hơn. Thiết bị yếu có thể không đọc được ảnh rất lớn. Không gửi ảnh gốc 500 MB lên API; API có giới hạn kích thước riêng. COCO-SSD chỉ nhận diện các lớp trong mô hình, không phải mọi vật thể và không cam kết độ chính xác cố định.

CÀI ĐẶT WINDOWS
1. Sao lưu app.py cũ trong thư mục website_python (đổi thành app_backup.py).
2. Chép app.py và requirements.txt trong bộ này vào thư mục website_python.
3. Mở CMD tại đúng thư mục đó.
4. Chạy:
   python -m pip install -r requirements.txt
   python -m py_compile app.py
   python app.py
5. Mở http://127.0.0.1:5000/

AI MÔ TẢ ẢNH VÀ HỎI ĐÁP
Cần API key OpenAI có quyền sử dụng mô hình. Không ghi API key trực tiếp vào mã nguồn hoặc đẩy lên GitHub.
- Windows CMD (chỉ có hiệu lực ở cửa sổ CMD hiện tại):
  set OPENAI_API_KEY=YOUR_API_KEY_HERE
  python app.py
Thay YOUR_API_KEY_HERE bằng khóa thật của bạn, không chia sẻ khóa này.

ĐƯA LÊN RENDER
- Đẩy app.py, requirements.txt và render.yaml lên repository GitHub.
- Tạo/cập nhật Web Service trên Render dùng repository đó.
- Build Command: pip install -r requirements.txt
- Start Command: gunicorn app:app
- Trong Environment trên Render, thêm OPENAI_API_KEY bằng khóa riêng của bạn nếu cần AI thị giác/chat.
- Không đưa khóa vào README, app.py hoặc GitHub.
- Sau khi deploy, kiểm tra URL Render. Bản trong ZIP chưa tự động được đẩy lên GitHub/Render.

GIỚI HẠN VÀ KIỂM TRA
- COCO-SSD tải mô hình/thư viện từ CDN, nên cần Internet. Nếu không tải được, tải lại trang hoặc kiểm tra kết nối.
- Mô hình COCO-SSD không nhận diện tất cả vật thể; ví dụ cá không phải lớp chuẩn trong COCO-SSD.
- AI có thể mô tả sai. Kiểm tra lại thông tin quan trọng.
- Bản này dùng giao diện trang chủ / và /vision; chatbot cũ có các đường dẫn /tro-ly và /chatbot, endpoint /chat.
- Hãy chạy thử trên máy trước khi thay bản trực tuyến. Giữ app_backup.py để quay lại khi cần.
