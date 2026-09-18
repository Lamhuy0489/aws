# Phan Tich Bai Nop Mau Cua Hoc Vien (Second-Hand Marketplace)

Nguon: https://chien13092004-ship-it.github.io/Workshop/2-proposal/
Tac gia tham khao: chien13092004

---

## 1. Tong quan de tai mau
- De tai: "Second-Hand Marketplace - A Cloud-Native Second-Hand Marketplace on AWS".
- Loai ung dung: San thuong mai dien tu do cu, phan tich cac bai toan CRUD, upload anh, authentication va hosting tren AWS.

## 2. Kien truc ky thuat cua bai mau
- Ngon ngu & Framework: Node.js, Express.js, EJS, MongoDB Atlas.
- Containerization: Dong goi Docker, day image vao Amazon ECR.
- Tinh toan (Compute): Chay tren Amazon ECS Fargate, nam sau Application Load Balancer (ALB).
- Luu tru: Amazon S3 chua anh san pham.
- Tu dong hoa CI/CD: AWS CodeBuild tu dong build Docker image va deploy vao ECS Fargate khi co commit tren GitHub.
- Mang & Bao mat: Amazon VPC (Public/Private subnets), Security Group, AWS Secrets Manager (luu connection string MongoDB), Route 53 va AWS Certificate Manager (ACM) cap SSL/HTTPS.
- Giam sat: Amazon CloudWatch.

## 3. Cau truc 7 phan cua website bao cao thuc tap
Nguoi hoc da to chuc website Hugo day du cac muc theo dung yeu cau cua FCAJ:
1. `1-worklog/`: Ghi chep tu Week 1 den Week 12 (1.1 Week 1 Worklog ... 1.12 Week 12 Worklog).
2. `2-proposal/`: Ban de xuat chi tiet:
   - 1. Executive Summary (Tom tat du an).
   - 2. Problem Statement (Boi canh, thach thuc va giai phap).
   - 3. Architecture Diagram (So do kien truc tong the).
   - 4. Technology Stack (Cac cong nghe su dung).
   - 5. High-Level Flow (Luong hoat dong cua he thong).
   - 6. Prerequisites (Dieu kien tien quyet).
   - 7. Implementation Roadmap & Timeline (Lich trinh trien khai).
   - 8. Expected Outcomes (Ket qua dau ra mong doi).
3. `3-blogsposted/`: 3 bai blog chia se chuyen mon (3.1 Blog 1, 3.2 Blog 2, 3.3 Blog 3).
4. `4-eventparticipated/`: 3 su kien cong dong da tham gia (4.1 Community Day, 4.2 Technical Sharing Meeting, 4.3 Community Day).
5. `5-workshop/`: Huong dan thuc hanh chi tiet chia thanh 12 buoc:
   - 5.1 Workshop Overview
   - 5.2 Prerequisite
   - 5.3 Prepare Project
   - 5.4 Networking (VPC, Subnets)
   - 5.5 Application Services (MongoDB Atlas, S3, Secrets Manager)
   - 5.6 Containerization (Build Docker, Push ECR)
   - 5.7 Deploy Application (Configure ALB, Deploy ECS Fargate)
   - 5.8 Domain and HTTPS (Route 53, ACM)
   - 5.9 CI/CD (AWS CodeBuild, CodePipeline)
   - 5.10 Monitoring (Amazon CloudWatch)
   - 5.11 Testing (Gui request, kiem tra log)
   - 5.12 Cleanup Resources (Xoa sach tai nguyen)
6. `6-self-evaluation/`: Tu danh gia 8 tieu chi nang luc.
7. `7-feedback/`: Phan hoi va danh gia ve chuong trinh dao tao.

## 4. Bai hoc ap dung cho du an Agentic RAG cua ban
Chung ta hoan toan co the ap dung chinh xac cau truc 7 phan nay cho de tai **Agentic RAG on AWS**:
- Thay vi deploy ung dung web Node.js tren ECS, chung ta se huong dan deploy:
  - Frontend tren S3 + CloudFront (hoac Streamlit/Next.js).
  - Backend Agent tren AWS Lambda + API Gateway.
  - Luu tru tri thuc S3 + DynamoDB Memory + SSM Parameter Store quan ly External API Key.
  - Cung day du cac buoc tu Preparation, VPC, Compute, Security, Testing den Clean-up.
