# Bảng Kiểm Tra Tiến Độ Thực Hành (Hands-on Checklist)

Bảng kiểm tra này tổng hợp các bài lab thực hành cốt lõi từ `https://cloudjourney.awsstudygroup.com/` được sắp xếp theo thứ tự ưu tiên nhằm phục vụ trực tiếp cho kỳ thực tập và dự án **Agentic RAG**.

---

## 1. Giai đoạn 1: Thiết lập & Nền tảng cốt lõi (Bắt buộc)

- [ ] **Lab 000001**: Tạo tài khoản AWS cá nhân và bảo mật tài khoản root bằng MFA.
- [ ] **Lab 000007**: Cấu hình AWS Budgets với cảnh báo ngưỡng 5 USD và 10 USD gửi về email.
- [ ] **Lab 000002**: Quản lý truy cập IAM (Tạo IAM Group, IAM User cho công việc hàng ngày, áp dụng chính sách Least Privilege).
- [ ] **Lab 000003**: Xây dựng hệ thống mạng VPC (Public Subnet, Private Subnet, Internet Gateway, Route Tables).
- [ ] **Lab 000004**: Khởi tạo và kết nối máy chủ ảo Amazon EC2 (Linux/Ubuntu), cấu hình Security Group.
- [ ] **Lab 000048**: Tạo và gán IAM Role cho EC2 để truy cập S3 mà không cần lưu Access Key trên máy chủ.
- [ ] **Lab 000011**: Cài đặt AWS CLI trên máy cục bộ, cấu hình cấu hình profile kết nối với AWS an toàn.
- [ ] **Lab 000057**: Tạo S3 Bucket, cấu hình quyền và bật tính năng Static Website Hosting.
- [ ] **Lab 000008**: Tạo bảng điều khiển giám sát (Dashboard) và thiết lập cảnh báo với Amazon CloudWatch Alarms.

---

## 2. Giai đoạn 2: Công nghệ Serverless & Dữ liệu (Phục vụ Backend)

- [ ] **Lab 000022**: Làm quen với AWS Lambda, kích hoạt hàm xử lý tự động và cấu hình biến môi trường.
- [ ] **Lab 000060**: Tạo bảng Amazon DynamoDB, thiết kế Partition Key / Sort Key, thực hành thêm, sửa, đọc dữ liệu.
- [ ] **Lab 000078**: Xây dựng Backend Serverless (AWS Lambda đọc/ghi dữ liệu DynamoDB và thao tác với file trên S3).
- [ ] **Lab 000079**: Thiết lập Amazon API Gateway kết nối với AWS Lambda, kích hoạt CORS để gọi từ Frontend.
- [ ] **Lab 000081**: Tạo User Pool trên Amazon Cognito và tích hợp xác thực người dùng cho API Gateway.
- [ ] **Lab 000096**: Quản lý thông tin bí mật với AWS Secrets Manager và AWS Systems Manager (SSM) Parameter Store.

---

## 3. Giai đoạn 3: Phân phối & Bảo mật ứng dụng

- [ ] **Lab 000094**: Tạo bản phân phối Amazon CloudFront kết nối với S3 tĩnh để tăng tốc độ tải trang toàn cầu.
- [ ] **Lab 000033**: Quản lý khóa mã hóa dữ liệu với AWS Key Management Service (AWS KMS).
- [ ] **Lab 000026**: Cấu hình tường lửa ứng dụng AWS WAF để bảo vệ API Gateway chống lại tấn công DDoS và quét mã độc.
- [ ] **Lab 000111**: Thiết lập VPC Endpoint dạng Gateway kết nối riêng tư giữa VPC và S3 mà không đi qua Internet công cộng.

---

## 4. Giai đoạn 4: Tự động hóa & DevOps (Tùy chọn nâng cao)

- [ ] **Lab 000015**: Đóng gói ứng dụng thành Docker container trên môi trường cục bộ.
- [ ] **Lab 000016**: Đẩy Docker image lên Amazon ECR và chạy trên cụm Amazon ECS (hoặc ECS Fargate).
- [ ] **Lab 000017**: Thiết lập đường ống tự động tích hợp và triển khai (CI/CD) với AWS CodePipeline.
- [ ] **Lab 000037**: Viết tập lệnh AWS CloudFormation để tự động khởi tạo hạ tầng VPC và EC2.

---

## 5. Giai đoạn 5: Triển khai Dự án Capstone (Agentic RAG on AWS)

- [ ] Chuẩn bị tập tài liệu văn bản mẫu (PDF, Markdown) và tải lên S3 Bucket `knowledge-base-data`.
- [ ] Cấu hình API Key (Google Gemini / OpenAI / Groq) trong AWS Systems Manager Parameter Store.
- [ ] Viết hàm trích xuất văn bản, chunking và embedding tạo kho vector tri thức.
- [ ] Xây dựng Engine Agent điều phối (ReAct loop, phân loại câu hỏi, chọn tool).
- [ ] Viết các Tool Lambda (Tool tra cứu tri thức S3, Tool tra cứu dữ liệu đơn hàng/người dùng trong DynamoDB).
- [ ] Thiết lập bảng DynamoDB `chat-history` với khóa `session_id` và cơ chế xóa tự động TTL.
- [ ] Kết nối API Gateway dạng Streaming hoặc REST để giao tiếp với Frontend.
- [ ] Kiểm thử toàn diện các kịch bản: câu hỏi ngoài luồng, câu hỏi cần tra cứu tài liệu, câu hỏi cần kích hoạt tool hành động.
- [ ] Viết tài liệu hướng dẫn và vẽ sơ đồ kiến trúc hoàn chỉnh cho báo cáo thực tập.
