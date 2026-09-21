# Báo Cáo Thực Hành: Lab 000016 - Điều Phối Container Với Amazon ECS (AWS Fargate)

- Người thực hiện: Lâm Quang Huy
- MSSV: 0212267 - Lớp: 67CS, HUCE
- Ngày hoàn thành: 2026-09-21
- AWS Account ID: 677994024390
- AWS Account Name: huylam
- Default Region: ap-southeast-1 (Singapore)
- Cluster Name: huylam-ecs-cluster
- Service Name: huylam-web-service
- Task Definition: huylam-web-task:1

---

## 1. Mục tiêu thực hành

- Tìm hiểu và thực hành quy trình đóng gói ứng dụng bằng Docker container và quản lý kho lưu trữ container với Amazon Elastic Container Registry (ECR).
- Làm quen với các thành phần cốt lõi của Amazon Elastic Container Service (ECS): Cluster, Task Definition, Service và Task.
- Lựa chọn mô hình tính toán phi máy chủ (Serverless Compute) **AWS Fargate** nhằm loại bỏ chi phí duy trì và gánh nặng vận hành máy chủ ảo EC2 nền.
- Cấu hình Task Definition với định mức tài nguyên tối thiểu (0.25 vCPU, 0.5 GB RAM) đủ điều kiện AWS Free Tier, chạy container Apache Web Server (`httpd:latest`) mở cổng HTTP 80.
- Khởi tạo ECS Service duy trì liên tục 1 Task hoạt động trên mạng Default VPC, tự động cấp phát Public IPv4.
- Kiểm tra toàn bộ vòng đời tác vụ Fargate từ trạng thái `PROVISIONING` -> `PENDING` -> `RUNNING`.
- Đo kiểm kết nối qua Internet bằng lệnh `curl` và trình duyệt web tại địa chỉ Public IP được cấp phát, ghi nhận phản hồi `HTTP/1.1 200 OK` và trang nội dung `It works!`.
- Áp dụng nguyên tắc FinOps: Thực hiện quy trình Teardown dọn dẹp sạch toàn bộ tài nguyên ECS và ECR sau khi hoàn thành đo kiểm để bảo toàn chi phí 0 USD.

---

## 2. Thông số kỹ thuật xác thực trên AWS

### 2.1. Định danh & Môi trường thực thi
- **AWS Account ID**: `677994024390`
- **Tên tài khoản (Account Name)**: `huylam`
- **IAM Principal**: `dev_admin` (`arn:aws:iam::677994024390:user/dev_admin`)
- **AWS Region**: `ap-southeast-1` (Asia Pacific - Singapore)
- **Availability Zone**: `ap-southeast-1c`
- **VPC trực thuộc**: Default VPC (`vpc-0c84feaf395ece4dd`)
- **Subnet ID**: `subnet-0bba3228d80514181` (Public Subnet)
- **Security Group**: `sg-023c42b5bc2e5111b` (Mở cổng 80 TCP từ `0.0.0.0/0`, Rule ID: `sgr-046178368b83207ba`)
- **IAM Service-Linked Role**: `AWSServiceRoleForECS`

### 2.2. Chi tiết kho lưu trữ Amazon ECR
- **Repository Name**: `huylam-web-app`
- **Repository ARN**: `arn:aws:ecr:ap-southeast-1:677994024390:repository/huylam-web-app`
- **Repository URI**: `677994024390.dkr.ecr.ap-southeast-1.amazonaws.com/huylam-web-app`
- **Visibility**: Private
- **Encryption**: AES-256

### 2.3. Chi tiết cụm Amazon ECS Cluster
- **Cluster Name**: `huylam-ecs-cluster`
- **Cluster ARN**: `arn:aws:ecs:ap-southeast-1:677994024390:cluster/huylam-ecs-cluster`
- **Trạng thái**: `ACTIVE`
- **Capacity Providers**: `FARGATE`, `FARGATE_SPOT`

### 2.4. Bản mô tả tác vụ ECS Task Definition
- **Family**: `huylam-web-task`
- **Revision**: `1`
- **Task Definition ARN**: `arn:aws:ecs:ap-southeast-1:677994024390:task-definition/huylam-web-task:1`
- **Mô hình**: `FARGATE`
- **CPU / Memory**: `256` (0.25 vCPU) / `512` (0.5 GB)
- **Container Name**: `web-app`
- **Container Image**: `public.ecr.aws/docker/library/httpd:latest`
- **Port Mapping**: Port `80` (HTTP)
- **Network Mode**: `awsvpc`

### 2.5. Dịch vụ duy trì Amazon ECS Service
- **Service Name**: `huylam-web-service`
- **Service ARN**: `arn:aws:ecs:ap-southeast-1:677994024390:service/huylam-ecs-cluster/huylam-web-service`
- **Desired Count**: `1`
- **Launch Type**: `FARGATE`
- **Platform Version**: `1.4.0` (LATEST)
- **Scheduling Strategy**: `REPLICA`

### 2.6. Tác vụ thực thi ECS Task Instance
- **Task ID**: `4f4a7210f06f48c2ade4d568bde7967a`
- **Task ARN**: `arn:aws:ecs:ap-southeast-1:677994024390:task/huylam-ecs-cluster/4f4a7210f06f48c2ade4d568bde7967a`
- **Trạng thái**: `RUNNING`
- **Giao diện mạng ENI**: `eni-0dcbf8076c9d39691`
- **Private IP**: `172.31.1.147`
- **Public IP**: `18.138.22.86`
- **Public DNS**: `ec2-18-138-22-86.ap-southeast-1.compute.amazonaws.com`

### 2.7. Kết quả đo kiểm phản hồi Web
- **Địa chỉ truy cập**: `http://18.138.22.86`
- **Mã phản hồi**: `HTTP/1.1 200 OK`
- **Web Server**: `Apache/2.4.68 (Unix)`
- **Nội dung trang**: `It works!`

---

## 3. Danh mục hình ảnh minh chứng thực hành

1. `01-ecr-repositories-list-initial.png`: Bảng điều khiển Amazon ECR ban đầu rỗng.
2. `02-ecr-create-repository.png`: Cấu hình khởi tạo ECR Repository `huylam-web-app`.
3. `03-ecr-repository-details-empty.png`: Chi tiết kho ECR và hướng dẫn bộ lệnh đẩy image.
4. `04-ecs-clusters-list-initial.png`: Danh sách cụm Amazon ECS ban đầu rỗng (0 clusters).
5. `05-ecs-create-cluster-fargate.png`: Cấu hình tạo cụm `huylam-ecs-cluster` với AWS Fargate.
6. `06-ecs-create-task-definition.png`: Cấu hình Task Definition `huylam-web-task` mở cổng 80.
7. `07-ecs-task-definition-created.png`: Đăng ký thành công `huylam-web-task:1` ở trạng thái Active.
8. `08-ecs-create-service-deployment.png`: Cấu hình triển khai Service `huylam-web-service`.
9. `09-ecs-service-running-tasks.png`: Chi tiết tác vụ Fargate hoạt động ở trạng thái RUNNING.
10. `09a-ecs-task-networking-public-ip.png`: Cấu hình mạng chi tiết hiển thị Public IP 18.138.22.86.
11. `10-ecs-webserver-browser-verification.png`: Trình duyệt truy cập thành công hiển thị trang It works!.

---

## 4. Quy trình FinOps Teardown dọn dẹp tài nguyên

Thực hiện giải phóng toàn bộ tài nguyên qua AWS CLI:

```bash
# 1. Cập nhật desired-count = 0
aws ecs update-service --cluster huylam-ecs-cluster --service huylam-web-service --desired-count 0 --region ap-southeast-1

# 2. Xóa ECS Service
aws ecs delete-service --cluster huylam-ecs-cluster --service huylam-web-service --region ap-southeast-1

# 3. Xóa ECS Cluster
aws ecs delete-cluster --cluster huylam-ecs-cluster --region ap-southeast-1

# 4. Hủy Task Definition
aws ecs deregister-task-definition --task-definition huylam-web-task:1 --region ap-southeast-1

# 5. Xóa kho ECR
aws ecr delete-repository --repository-name huylam-web-app --force --region ap-southeast-1

# 6. Thu hồi port 80 trên Security Group
aws ec2 revoke-security-group-ingress --group-id sg-023c42b5bc2e5111b --protocol tcp --port 80 --cidr 0.0.0.0/0 --region ap-southeast-1
```
