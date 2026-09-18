# Kế Hoạch Và Lộ Trình Thực Tập Cloud / AWS (FCJ Workforce Standard)

Tài liệu này xác định mục tiêu, các giai đoạn thực hiện, tiêu chí đánh giá và các mốc hoàn thành cho kỳ thực tập dựa trên tiêu chuẩn của chương trình **FCJ Workforce Program**.

---

## 1. Mục tiêu kỳ thực tập

- Nắm vững kiến thức nền tảng về hạ tầng đám mây và các dịch vụ cốt lõi của AWS.
- Xây dựng tư duy thiết kế hệ thống theo chuẩn **AWS Well-Architected Framework** (Bảo mật, Độ tin cậy, Hiệu năng, Tối ưu chi phí, Vận hành xuất sắc).
- Hoàn thành bộ hồ sơ năng lực (Portfolio) gồm **5 dự án thực hành chuẩn chỉnh**, trong đó có 1 dự án trọng điểm (Capstone Project) là **Hệ thống Agentic RAG trên AWS**.
- Đạt điều kiện tốt nghiệp FCJ Workforce và tự tin ứng tuyển vị trí Cloud Engineer / DevOps / Backend Engineer tại các đối tác của AWS.

---

## 2. Tiêu chí tốt nghiệp & Đánh giá dự án (FCJ Standards)

Để được đánh giá hoàn thành kỳ thực tập ở mức xuất sắc, bạn cần thỏa mãn các tiêu chí sau:

### a. Bộ 5 Dự Án Thực Tế (Proud Projects)
Mỗi dự án phải là một Case Study hoàn chỉnh đáp ứng đủ 6 thành phần:
1. **Bản vẽ kiến trúc chi tiết (Architecture Diagram)**: Thể hiện rõ các tầng mạng VPC, bảo mật, lưu trữ, tính toán và luồng dữ liệu.
2. **Mã nguồn hoàn chỉnh (Implementation)**: Được đẩy lên GitHub cá nhân, cấu trúc rõ ràng, có quản lý hạ tầng bằng mã (Terraform hoặc AWS CloudFormation/CDK).
3. **Tài liệu hướng dẫn (Documentation / README)**: Hướng dẫn cài đặt, cấu hình biến môi trường và chạy thử nghiệm từng bước.
4. **Video demo ngắn (3 - 5 phút)**: Minh chứng hệ thống hoạt động thực tế trên AWS Console và giao diện client.
5. **Bài viết kỹ thuật (Technical Blog Post)**: Phân tích bài toán, các quyết định thiết kế (design decisions), thách thức gặp phải và bài học kinh nghiệm.
6. **Bản trình bày (Presentation Slide)**: Slide tóm tắt dùng để bảo vệ trước giảng viên / mentor hoặc trình bày tại meetup cộng đồng.

### b. Danh mục 5 dự án đề xuất cho kỳ thực tập
- **Project 1 (Junior - Foundation)**: Xây dựng hệ thống lưu trữ website tĩnh bảo mật cao với Amazon S3, CloudFront, Route 53 và ACM (SSL/TLS).
- **Project 2 (Junior - Backend Serverless)**: Xây dựng RESTful API không máy chủ hoàn chỉnh với API Gateway, AWS Lambda, DynamoDB và xác thực qua Amazon Cognito.
- **Project 3 (Middle - Automation & CI/CD)**: Thiết lập pipeline tự động hóa CI/CD với AWS CodePipeline / GitHub Actions, tự động test và deploy ứng dụng lên AWS Lambda/ECS.
- **Project 4 (Middle - Monitoring & Security)**: Xây dựng giải pháp giám sát tập trung với Amazon CloudWatch Logs/Metrics, cảnh báo tự động qua Slack và bảo vệ API bằng AWS WAF.
- **Project 5 (Capstone - Middle/Senior)**: **Hệ thống Agentic RAG trên AWS** (Điều phối Agent đa công cụ, tích hợp LLM an toàn qua AWS Secrets Manager/SSM, bộ nhớ phiên hội thoại DynamoDB, S3 Document Knowledge Base).

---

## 3. Lộ trình thực tập theo từng giai đoạn (Timeline 12 Tuần)

### Giai đoạn 1: Thiết lập nền tảng & An toàn tài khoản (Tuần 1 - Tuần 2)
- Khởi tạo tài khoản AWS cá nhân.
- Cấu hình bảo mật gốc: Kích hoạt MFA cho tài khoản Root, tạo IAM Admin Group và IAM User riêng để làm việc.
- Cài đặt **AWS Budgets**: Ngưỡng cảnh báo chi phí 5 USD và 10 USD gửi email tự động.
- Cài đặt và cấu hình AWS CLI, VS Code AWS Toolkit trên máy cục bộ.
- Hoàn thành các lab cơ bản: IAM (000002), VPC (000003), EC2 (000004), S3 (000057), RDS (000005).

### Giai đoạn 2: Khám phá Serverless & Dịch vụ dữ liệu (Tuần 3 - Tuần 4)
- Học sâu về AWS Lambda, DynamoDB và API Gateway.
- Hoàn thành chuỗi workshop Serverless Book Store (labs 000078, 000079, 000080).
- Hoàn thành và đóng gói **Project 1 & Project 2**.

### Giai đoạn 3: Nghiên cứu Kiến trúc Agentic RAG & Tích hợp (Tuần 5 - Tuần 7)
- Nghiên cứu cơ chế hoạt động của RAG và Agent (ReAct Framework, Tool Calling, Vector Embeddings).
- Thiết lập lưu trữ tài liệu thô trên Amazon S3.
- Xây dựng kho lưu trữ tri thức vector (Vector Store).
- Cấu hình lưu trữ an toàn API Key (Google Gemini / OpenAI / Groq) trong **AWS Systems Manager Parameter Store**.
- Viết các hàm Lambda đóng vai trò là Tool của Agent (truy vấn DynamoDB, tra cứu thông tin hệ thống).

### Giai đoạn 4: Hoàn thiện ứng dụng Agentic RAG (Tuần 8 - Tuần 9)
- Tích hợp điều phối Agent (LangGraph / Python engine) với backend API Gateway.
- Kết nối quản lý bộ nhớ lịch sử trò chuyện (Conversation Memory) qua DynamoDB.
- Xây dựng giao diện Frontend (Next.js hoặc Streamlit) cho phép người dùng chat, xem tài liệu tham khảo và kích hoạt công cụ.
- Đóng gói toàn bộ hạ tầng bằng Terraform hoặc CloudFormation.
- Hoàn thành **Project 5 (Capstone Project)**.

### Giai đoạn 5: Vận hành, Bảo mật & CI/CD (Tuần 10 - Tuần 11)
- Thiết lập pipeline tự động kiểm thử và triển khai (CI/CD) cho mã nguồn backend.
- Bật CloudWatch Log Insights và theo dõi thời gian thực thi (Latency, Errors, Token usage).
- Kiểm tra lại các quy tắc bảo mật: IAM Least Privilege (nguyên tắc đặc quyền tối thiểu), mã hóa dữ liệu tĩnh và truyền tải.
- Hoàn thành **Project 3 & Project 4**.

### Giai đoạn 6: Viết báo cáo thực tập & Trình bày (Tuần 12)
- Hoàn thiện tài liệu kỹ thuật trên GitHub: Sơ đồ kiến trúc, hướng dẫn triển khai, kết quả đo lường hiệu năng.
- Viết bài blog kỹ thuật chia sẻ về hành trình xây dựng hệ thống Agentic RAG trên AWS.
- Quay video demo sản phẩm và soạn slide báo cáo thực tập.
- Rà soát tài nguyên trên AWS Console, xóa hoặc dừng các dịch vụ không cần thiết để tránh phát sinh chi phí.

---

## 4. Nguyên tắc FinOps & Quản trị chi phí tài khoản

1. **Nguyên tắc "Tắt khi không dùng"**: Với các tài nguyên tính phí theo giờ (như EC2, RDS, NAT Gateway), xóa hoặc tắt ngay sau khi kết thúc buổi thực hành.
2. **Ưu tiên Serverless**: Tận dụng tối đa AWS Lambda, DynamoDB, S3 vì các dịch vụ này chỉ tính phí khi có request thực tế và nằm trong gói Free Tier hào phóng.
3. **Kiểm tra hóa đơn hàng tuần**: Truy cập mục **AWS Cost Explorer** và **Billing and Cost Management** mỗi tuần một lần để nắm rõ từng dòng chi phí phát sinh.
