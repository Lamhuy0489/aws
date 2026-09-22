# Bai Tong Hop: Trang Thai Du An & Lo Trinh Hoan Thien (Serverless Hybrid OCR & Translation)

- Nguoi tong hop: Knowledge Base Agent
- Ngay tong hop: 2026-09-22
- Chu de: Tong hop tien do thuc te, kien truc mo rong AWS Native va checklist hanh dong 12 tuan

---

## 1. Tong quan du an chinh thuc

- **Ten de tai**: **Serverless Hybrid Document OCR, Parsing & Technical Translation Platform on AWS**
- **Chu so huu**: Lam Quang Huy (MSSV: 0212267, Lop: 67CS, Dai hoc Xay dung Ha Noi HUCE)
- **AWS Account**: 677994024390 | **User**: dev_admin | **Region**: ap-southeast-1 (Singapore)
- **Pham vi cot loi**:
  1. Boc tach tai lieu so sieu toc Tang 1 (Fast-Path PyMuPDF 0.1s - 0.3s/trang, 0 VND).
  2. Nhan dien thi giac Tang 2 (Selective Vision OCR) cho trang scan qua Kaggle GPU/TPU (Qwen2.5-VL) kem Failover tu dong sang Google Gemini 3.6 Flash.
  3. Dong co Dich thuat Ky thuat da ngon ngu bao toan 100% cau truc Markdown va bang bieu.
  4. Bo xuat ban da dinh dang: Markdown (.md), Microsoft Word (.docx), PDF chuan in an A4 (.pdf).
  5. Giao dien Web Studio SPA muot ma, khong nhap nhay, quan tri xoay tour API Key.
  6. **Tuy chon mo rong AWS Native AI khep kin**: Ho tro Amazon Bedrock (Nova / Claude 3.5 Haiku) hoac Amazon Textract / Amazon Translate. Che do nay la tuy chon phu, mac dinh tat de bao toan FinOps 0 USD.
  - **Luu y quan trong**: Du an khong bao gom Chatbot hay RAG ngoai le.

---

## 2. Checklist tien do thuc te

### Tuan 1 - Tuan 8: Nen tang Ha tang & Container (Hoan thanh 100%)
- [x] Tuan 1: AWS IAM & CloudWatch Metrics
- [x] Tuan 2: Amazon VPC, Subnets, Route Tables, Internet Gateway, NAT Gateway
- [x] Tuan 3: Amazon EC2 Linux/Windows, Amazon EBS Volumes
- [x] Tuan 4: Amazon S3 (Hosting, Lifecycle, Replication), Systems Manager
- [x] Tuan 5: Amazon CloudWatch Alarms & SNS Notifications
- [x] Tuan 6: Application Load Balancer & Auto Scaling Groups
- [x] Tuan 7: AWS CloudFormation (IaC) Stack & Drift Detection
- [x] Tuan 8: Docker, Amazon ECR (huylam-web-app), Amazon ECS Fargate (huylam-ecs-cluster), FinOps Teardown 0 USD

### Ứng dung Local Web Studio (Hoan thanh 100%)
- [x] FastNativeParser (PyMuPDF)
- [x] OCRDispatcher (Kaggle + Gemini Failover)
- [x] DocumentTranslator (Gemini Flash Technical Translation)
- [x] Exporters (.md, .docx, .pdf)
- [x] Web Studio SPA (spa_router.js, studio.js, admin.js, settings.js)
- [x] Kiem thu tu dong: 27/27 pytest passing 100%

### Tuan 9: Thiet ke Kien truc Serverless (Hoan thanh 100%)
- [x] Sơ do kien truc Serverless Microservices 5 tang
- [x] Thiet ke luoc do NoSQL Amazon DynamoDB (document_processing_jobs)
- [x] Co che S3 Presigned URL giai quyet gioi han 10MB cua API Gateway
- [x] Bien soan Worklog Tuan 9 song ngu tren Hugo website va day len GitHub

### Tuan 10: Trien khai Ha tang Dam may AWS (HOAN THANH 100%)
- [x] Soan thao huong dan thiet lap bang tay tung buoc tren AWS Console
- [x] Cap nhat Proposal va Worklog Tuan 10 tren Hugo website va day len GitHub
- [x] Tao Amazon S3 Bucket: huylam-ocr-documents-ap-southeast-1 (uploads/, outputs/, CORS)
- [x] Tao Amazon DynamoDB Table: document_processing_jobs (PK: job_id, SK: created_at, On-Demand)
- [x] Tao AWS Systems Manager Parameter: /huylam-ocr/config (SecureString KMS)
- [x] (Tuy chon) Do kiem co che Amazon Bedrock Model Access & Chinh sach tai khoan
- [x] Ket noi code Python Boto3 voi S3, DynamoDB, SSM (Da do kiem thanh cong 100%)
- [x] Thu thap 9 anh minh chung AWS Console co vien do dinh danh huylam (677994024390)

### Tuan 11: Tich hop Dam may & Do kiem Hieu nang (Du kien)
- [ ] Tich hop tu dong hoa luong xu ly qua S3 Event Notification hoac ECS Fargate
- [ ] Trien khai giao dien len S3 Static Web Hosting + CloudFront CDN
- [ ] Do kiem Benchmark toc do boc tach, dich thuat va xuat file
- [ ] Bien soan Worklog Tuan 11 song ngu va cap nhat anh minh chung

### Tuan 12: Nghiem thu, Kiem toan FinOps & Bao ve Tot nghiep (Du kien)
- [ ] Kiem toan chi phi FinOps 0.00 USD tren AWS Budgets / Cost Explorer
- [ ] Chuan hoa toan bo noi dung workshop/content/5-Workshop/
- [ ] Quay video clip demo san pham hoan chinh
- [ ] Hoan thien Bao cao Tot nghiep va Slide thuyet trinh bao ve

---

## 3. Lien ket tai lieu lien quan
- [[fcj-2026-roadmap]]: Lo trinh 12 tuan tong the.
- [[fcj-2026-checklist]]: Danh muc bai lab FCJ.
- [[fcaj-internship-submission-guide]]: Huong dan xay dung website Hugo.
- Tai lieu goc: [ROADMAP.md](file:///Users/huylam/Downloads/aws/ROADMAP.md) va [AGENT.md](file:///Users/huylam/Downloads/aws/AGENT.md).
