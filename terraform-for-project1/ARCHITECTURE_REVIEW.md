# Đánh Giá Kiến Trúc Hệ Thống (Architecture Review)

Tài liệu này tổng hợp cấu trúc luồng hoạt động tổng thể của hệ thống AWS được triển khai thông qua dự án Terraform hiện tại, đồng thời tổng hợp số lượng tài nguyên máy chủ đang được cấu hình.

## 1. Số Lượng Máy Chủ Hiện Tại

Dựa trên cấu hình trong mã nguồn Terraform thư mục `environments/dev`:

*   **EC2 Instances: Hiện tại có 2 máy ảo (Instances)**
    *   *Chi tiết:* Hệ thống sử dụng Auto Scaling Group (ASG) quản lý các EC2 (`aws_autoscaling_group.app`). ASG đang được cấu hình với `desired_capacity = 2`, `min_size = 1`, và `max_size = 3`. Do đó, ở trạng thái bình thường chưa có hiện tượng quá tải, hệ thống sẽ luôn duy trì đúng **2 EC2 instances**. Các instance này dùng hệ điều hành Amazon Linux 2 (`t3.micro`).
*   **RDS Instances: Hiện tại có 1 cơ sở dữ liệu (Database)**
    *   *Chi tiết:* Một instance RDS PostgreSQL phiên bản 15 (`db.t3.micro`) duy nhất được cấu hình (`aws_db_instance.main`). Cấu hình `multi_az = false` (không chạy chế độ dự phòng ở nhiều zone) để tối ưu hóa chi phí cho môi trường Dev.

---

## 2. Luồng Hoạt Động Của Hệ Thống (Traffic Flow & Architecture)

Hệ thống được thiết kế hoàn chỉnh theo tiêu chuẩn **Kiến trúc 3 Lớp (3-Tier Architecture)** trên AWS, bảo mật rất tốt thông qua mạng chuyên biệt.

### Flow đi của một Request (Truy cập)

1.  **Internet -> Lớp Công Khai (Public Tier):** 
    Người dùng (End user) từ ngoài Internet gửi yêu cầu HTTP/HTTPS (Port 80/443). Yêu cầu này đi qua Internet Gateway (IGW) và tới **Application Load Balancer (ALB)**. ALB là tài nguyên duy nhất được phép giao tiếp trực tiếp với môi trường ngoài. ALB được gán vào 3 Public Subnet trên 3 Availability Zones (AZ).

2.  **Lớp Công Khai -> Lớp Ứng Dụng (Private Tier):**
    Từ ALB, các luồng request được phân tải đều đặn (Load Balancing) thông qua một Target Group (tại cổng 8080) và đẩy xuống các **máy ảo EC2** đang chạy bên trong mạng Private Subnet.
    *Bảo mật:* Các Security Group (SG) ngăn chặn mọi kết nối trực tiếp từ Internet vào máy ảo EC2. EC2 chỉ chấp nhận luồng giao tiếp bắt nguồn từ chính ALB (`p1-dev-apse1-sg-app` có Inbound Rule từ ALB SG). EC2 cũng không mở port SSH (22) mà thay vào đó sử dụng AWS Systems Manager (SSM) thông qua quyền IAM rẽ nhánh an toàn.

3.  **Lớp Ứng Dụng -> Lớp Dữ Liệu (Isolated Tier):**
    Khi ứng dụng (dự kiến Node.js/Python,... trên EC2) cần thao tác với dữ liệu, chúng sẽ mở kết nối từ EC2 trong Private Subnet tới máy chủ cơ sở dữ liệu **RDS PostgreSQL** ở vùng cô lập (DB Subnet / Isolated).
    *Bảo mật:* Tương tự như EC2, Security Group của DB (`p1-dev-apse1-sg-db`) cực kỳ khắt khe; nó từ chối tất cả kết nối ngoại trừ kết nối tại Port `5432` phát sinh từ chính các EC2 nói trên. DB này thậm chí không thể mở kết nối ra ngoài Internet (Outbound rule bị đóng).

4.  **Luồng Trả Về (Response):** 
    Dữ liệu lấy từ RDS trả ngược cho ứng dụng ở EC2. EC2 hoàn trả file HTML/JSON về cho ALB, và ALB điều phối về lại trình duyệt người dùng ngoài mạng Internet.

### Khả Năng Tự Phục Hồi & Co Giãn
*   Nếu 1 EC2 bị lỗi, ALB sẽ ngừng gửi traffic cho nó (sau khi Health Check thất bại). Đồng thời, ASG sẽ phát hiện tình trạng hụt số lượng lượng instance (yêu cầu là 2 nhưng chỉ còn 1), tự động "khởi tạo" và "bơm" 1 máy ảo EC2 mới bù vào một AZ khác để đảm bảo duy trì độ ổn định.

---

## Tổng Kết

*   Hệ thống thiết kế theo module cực kỳ chuẩn DevOps cho môi trường Dev.
*   **Chi Phí (Cost):** Tối giản (hiện tại EC2 `t3.micro` ASG(2), RDS `db.t3.micro` thuộc vùng Free-tier).
*   **An Ninh (Security):** Tính tách rời mạng lưới tốt (Public -> Private -> Isolated DB) và quy tắc "Least Privilege" qua cấu hình các File Security_Group chuyên nghiệp.
