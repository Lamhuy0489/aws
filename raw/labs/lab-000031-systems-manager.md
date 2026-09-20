# Báo Cáo Thực Hành: Lab 000031 - Quản Trị Hệ Thống Với AWS Systems Manager & Resource Governance

- Người thực hiện: Lâm Quang Huy
- MSSV: 0212267 - Lớp: 67CS, HUCE
- Ngày hoàn thành: 2026-09-21
- AWS Account ID: 677994024390
- AWS Account Name: huylam
- Default Region: ap-southeast-1 (Singapore)
- Custom VPC: huylam-vpc (vpc-0125f4d6db3fbffa6)

---

## 1. Mục tiêu thực hành

- Nắm vững giải pháp quản trị máy chủ từ xa AWS Systems Manager (SSM) bao gồm Fleet Manager, Session Manager, Parameter Store và Run Command theo chuẩn kiến trúc Zero Trust.
- Triển khai kiến trúc bảo mật máy chủ ảo Zero Inbound Ports: Cấu hình Security Group `huylam-ssm-sg` hoàn toàn không mở cổng Inbound (0 Inbound Rules, không mở cổng SSH 22 truyền thống), triệt tiêu hoàn toàn bề mặt tấn công từ Internet.
- Thiết lập phân quyền IAM Role chuyên dụng `huylam-ssm-role`: Gắn chính sách `AmazonSSMManagedInstanceCore` và `AmazonSSMReadOnlyAccess` cho phép máy chủ EC2 tự động đăng ký và liên lạc hai chiều an toàn với Systems Manager Control Plane qua SSM Agent.
- Kiểm nghiệm kết nối từ xa không cần SSH Key thông qua AWS Systems Manager Session Manager: Truy cập shell Linux tương tác trực tiếp trên trình duyệt web, xác thực phiên làm việc dưới quyền người dùng an toàn `ssm-user`.
- Quản trị tập trung tham số và bí mật ứng dụng với AWS Systems Manager Parameter Store: Khởi tạo tham số chuỗi thông thường (String) và tham số mã hóa bảo mật cao (SecureString) tích hợp khóa mã hóa AWS Key Management Service (AWS KMS `alias/aws/ssm`).
- Kiểm chứng giải mã tham số bảo mật động ngay trong phiên Session Manager: Sử dụng AWS CLI thực thi lệnh `aws ssm get-parameter --with-decryption` trích xuất thông tin định danh sinh viên Lâm Quang Huy (MSSV: `0212267`) và mật khẩu cơ sở dữ liệu đã giải mã.
- Tự động hóa tác vụ quản trị hàng loạt bằng AWS Systems Manager Run Command: Thực thi tài liệu lệnh `AWS-RunShellScript` trên máy chủ từ xa mà không cần đăng nhập trực tiếp, thu thập kết quả thực thi đạt trạng thái `Success` và kiểm tra nhật ký chi tiết (Standard Output).
- Thiết lập cơ chế quản trị tài nguyên tập trung với AWS Resource Groups & Tagging: Xây dựng Resource Group `huylam-fcj-resources` gom cụm tự động 6 tài nguyên dựa trên thẻ phân loại chuẩn hóa `Project = FCJ-Bootcamp-2026`.
- Duy trì kỷ luật tài chính đám mây FinOps: Đo kiểm định kỳ trang tổng quan AWS Billing and Cost Management, ghi nhận chi phí lũy kế Month-to-date (0.10 USD), kiểm soát 2 chỉ tiêu ngân sách AWS Budgets đạt trạng thái `Healthy` và giải phóng tài nguyên sau thực nghiệm.

---

## 2. Thông số kỹ thuật xác thực trên AWS

### 2.1. Phân quyền IAM Role (IAM Role & Policies)
- **IAM Role Name**: `huylam-ssm-role`
- **Role ARN**: `arn:aws:iam::677994024390:role/huylam-ssm-role`
- **Trust Entity**: `ec2.amazonaws.com`
- **Chính sách gắn kèm (Attached Policies)**:
  - `AmazonSSMManagedInstanceCore`
  - `AmazonSSMReadOnlyAccess`

### 2.2. Nhóm bảo mật tối ưu hóa Zero Trust (Security Group)
- **Security Group Name**: `huylam-ssm-sg`
- **Security Group ID**: `sg-08a93d881545a9cf8`
- **VPC ID**: `vpc-0125f4d6db3fbffa6` (`huylam-vpc`)
- **Inbound Rules**: 0 rules (No inbound rules). Không mở cổng SSH 22, HTTP 80, hay HTTPS 443 từ bên ngoài.
- **Outbound Rules**: All traffic (`0.0.0.0/0`) cho phép SSM Agent thiết lập kết nối chiều ra (Outbound TLS HTTPS 443) tới Systems Manager Service Endpoints.

### 2.3. Máy chủ EC2 được quản lý (Managed EC2 Instance)
- **Instance Name Tag**: `huylam-ssm-instance`
- **Instance ID**: `i-07c150e87aa231c61`
- **Subnet ID**: `subnet-0efa7c3a5818035dc` (Public Subnet)
- **Instance Type**: `t3.micro` (2 vCPUs, 1 GiB RAM)
- **Private IPv4**: `10.0.1.240`
- **Public IPv4**: `13.212.80.147`
- **Hệ điều hành**: Amazon Linux 2023 (Kernel 6.18.48-109.150.amzn2023.x86_64)
- **Trạng thái SSM Agent (Ping Status)**: `Online`
- **Phiên bản SSM Agent**: `3.3.4624.0`
- **Trạng thái kết nối Session Manager**: `Connected`

### 2.4. Quản trị cấu hình và bí mật (SSM Parameter Store)
- **Tham số môi trường ứng dụng**:
  - Name: `/huylam/app/environment`
  - Type: `String`
  - Value: `Production-Bootcamp`
- **Tham số định danh sinh viên**:
  - Name: `/huylam/app/student_name`
  - Type: `String`
  - Value: `Lam Quang Huy - MSSV: 0212267 - Class: 67CS`
- **Tham số mật khẩu cơ sở dữ liệu (SecureString)**:
  - Name: `/huylam/app/db_password`
  - Type: `SecureString`
  - KMS Key ID: `alias/aws/ssm`
  - Plaintext Value: `HuyLam2026!SecureDBPassword`
  - Tags: `Project = FCJ-Bootcamp-2026`, `StudentID = 0212267`

### 2.5. Tự động hóa tác vụ từ xa (SSM Run Command)
- **Command ID**: `ab82dba7-47c6-4727-9a72-ffe6d89b1598`
- **Command Document**: `AWS-RunShellScript`
- **Target Instance**: `i-07c150e87aa231c61`
- **Trạng thái thực thi**: `Success` (Response code: 0)
- **Standard Output**:
  ```text
  === AWS SYSTEMS MANAGER RUN COMMAND LAB ===
  Student Name: Lam Quang Huy
  Student ID: 0212267
  Class: 67CS - HUCE
  Host: ip-10-0-1-240.ap-southeast-1.compute.internal
  Current User: ssm-user
  Kernel: 6.18.48-109.150.amzn2023.x86_64
  SSM Agent Status: Active (running)
  Uptime: up 18 minutes
  ```

### 2.6. Nhóm tài nguyên AWS Resource Groups
- **Tên Resource Group**: `huylam-fcj-resources`
- **Resource Group ARN**: `arn:aws:resource-groups:ap-southeast-1:677994024390:group/huylam-fcj-resources`
- **Tiêu chí gom nhóm**: `Project = FCJ-Bootcamp-2026`
- **Danh sách 6 tài nguyên thành viên**:
  1. Parameter: `/huylam/app/student_name`
  2. Parameter: `/huylam/app/db_password`
  3. Security Group: `huylam-ssm-sg` (`sg-08a93d881545a9cf8`)
  4. EC2 Instance: `huylam-ssm-instance` (`i-07c150e87aa231c61`)
  5. EC2 Instance: `huylam-ssm-instance` (`i-0a5174023e7d2f6dc`)
  6. Resource Group: `huylam-fcj-resources`

### 2.7. Quản trị chi phí FinOps
- **Month-to-date Cost**: `0.10 USD`
- **Forecasted Cost**: `0.26 USD`
- **AWS Budgets**: 2 ngân sách cảnh báo trạng thái `OK / Healthy`.
- **Đánh giá FinOps**: Toàn bộ tài nguyên được triển khai trong phạm vi gói AWS Free Tier.

---

## 3. Danh mục hình ảnh minh chứng

| STT | Tên tệp ảnh | Nội dung minh chứng | Vị trí khoanh đỏ |
| :--- | :--- | :--- | :--- |
| 1 | `01-ssm-fleet-manager-managed-node.png` | Fleet Manager Managed Nodes | Account Badge, Instance row `i-07c150e87aa231c61` Online |
| 2 | `02-ec2-security-group-no-inbound.png` | Security Group `huylam-ssm-sg` | Account Badge, Details card, Bảng Inbound rules 0 |
| 3 | `03-ssm-session-manager-connect.png` | EC2 Connect qua Session Manager | Account Badge, Tab SSM Session Manager, Card agent info Online |
| 4 | `04-ssm-session-manager-commands.png` | Terminal Session Manager | Instance ID thanh header, Khối lệnh định danh sinh viên |
| 5 | `05-ssm-parameter-store-create-string.png` | Tạo Parameter `/huylam/app/student_name` | Account Badge, Trường Name, Trường Value sinh viên |
| 6 | `06-ssm-parameter-store-details.png` | Tạo SecureString `/huylam/app/db_password` | Account Badge, Cấu hình KMS `alias/aws/ssm`, Bảng Tags |
| 7 | `07-ssm-parameter-decryption-test.png` | Giải mã tham số bằng AWS CLI | Instance ID thanh header, Lệnh CLI và mật khẩu giải mã |
| 8 | `08-ssm-run-command-submit.png` | Soạn thảo Run Command `AWS-RunShellScript` | Account Badge, Tài liệu chọn, Khung soạn thảo script |
| 9 | `09-ssm-run-command-output-success.png` | Kết quả Run Command Success | Account Badge, Trạng thái Success, Output terminal |
| 10 | `10-resource-groups-details.png` | Tạo Resource Group `huylam-fcj-resources` | Account Badge, Thẻ cấu hình tên và tag tiêu chí |
| 11 | `11-resource-groups-members.png` | 6 tài nguyên thành viên Resource Group | Account Badge, ARN nhóm, Bảng 6 tài nguyên |
| 12 | `12-aws-billing-cost-finops.png` | Bảng điều khiển Billing & Budgets FinOps | Account Badge, Thẻ Cost summary MTD, Thẻ Cost monitor |

---

## 4. Tổng kết và Đánh giá

Bài thực hành chứng minh tính ưu việt của mô hình quản trị hạ tầng điện toán đám mây hiện đại:
- Triệt tiêu hoàn toàn nhu cầu mở cổng mạng quản trị (SSH port 22) ra Internet.
- Kiểm soát truy cập tập trung thông qua AWS IAM và ghi vết đầy đủ hoạt động qua AWS CloudTrail.
- Quản lý tập trung cấu hình và bí mật ứng dụng với cơ chế mã hóa tiêu chuẩn từ AWS KMS.
- Vận hành và giám sát hàng loạt máy chủ bằng Run Command nhanh chóng, an toàn và có thể lập trình tự động.

---

## 5. Quy trình dọn dẹp tài nguyên (FinOps Teardown)

Để duy trì chi phí ở mức 0 USD và bảo toàn toàn vẹn định mức miễn phí của gói AWS Free Tier, toàn bộ các tài nguyên sau bài kiểm nghiệm được giải phóng theo đúng trình tự kỹ thuật:

```bash
# 1. Chấm dứt máy chủ ảo EC2 (Terminate Instance)
aws ec2 terminate-instances --instance-ids i-07c150e87aa231c61

# Chờ máy chủ chuyển đổi trạng thái sang terminated hoàn tất
aws ec2 wait instance-terminated --instance-ids i-07c150e87aa231c61

# 2. Xóa các tham số trong Parameter Store
aws ssm delete-parameters --names \
  "/huylam/app/db_password" \
  "/huylam/app/environment" \
  "/huylam/app/student_name"

# 3. Xóa nhóm tài nguyên Resource Groups
aws resource-groups delete-group --group-name huylam-fcj-resources

# 4. Xóa nhóm bảo mật Security Group (khi instance đã terminated)
aws ec2 delete-security-group --group-id sg-08a93d881545a9cf8

# 5. Kiểm tra xác nhận không còn tài nguyên hoạt động
aws ec2 describe-instances --filters "Name=instance-state-name,Values=running,pending" \
  --query "Reservations[*].Instances[*].[InstanceId,State.Name]" --output table
aws ssm describe-parameters --query "Parameters[*].[Name]" --output table
aws resource-groups list-groups --query "GroupIdentifiers[*].[GroupName]" --output table
```
*Trạng thái sau dọn dẹp: 100% tài nguyên đã được thu hồi, chi phí phát sinh duy trì ở mức 0 USD.*
