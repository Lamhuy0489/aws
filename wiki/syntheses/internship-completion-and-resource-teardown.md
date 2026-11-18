# Tong Ket Hoan Tat Thuc Tap Va Giai Phong Ha Tang AWS (Internship Completion & Resource Teardown)

Tai lieu tong hop toan dien ket qua nghiem thu de tai "Serverless Hybrid Document OCR, Parsing & Technical Translation Platform", hoan tat 12 tuan thuc tap dam may FCJ 2026, va quy trinh giai phong ha tang dam may nham bao toan han muc AWS Credit theo nguyen tac FinOps.

---

## 1. Tong quan ket qua 12 tuan thuc tap

De tai duoc thiet ke va van hanh dua tren cac tieu chuan cua [[aws-well-architected]] ket hop voi mo hinh dien toan lai Hybrid Cloud va phuong phap quan ly tri thuc bo nao ngoai vi:

1. **Giai doan 1 (Tuan 1 - 4): Xay dung nen tang ha tang va an ninh**
   - Khoi tao tai khoan AWS, thiet lap xac thuc da yeu to MFA, phan quyen quan tri qua IAM User `dev_admin`.
   - Thiet lap ngan sach kiem soat chi phi AWS Budgets voi hai nguong canh bao 100 USD va 200 USD.
   - Trien khai mang rieng ao Amazon VPC tuy bien voi kien truc Multi-AZ, Application Load Balancer va Auto Scaling Group (ASG).
2. **Giai doan 2 (Tuan 5 - 8): Phat trien bo may xu ly lai (Hybrid OCR Engine)**
   - Xay dung Tang 1 (Fast-Path): Boc tach luong van ban so qua PyMuPDF voi toc do 0.1s - 0.3s/trang va chi phi 0 USD.
   - Xay dung Tang 2 (Selective OCR): Dieu phoi tai tinh toan nang sang cum GPU ngoai vi tren Kaggle (2x NVIDIA T4) chay mo hinh thi giac Qwen2.5-VL qua Cloudflare HTTPS Tunnel.
   - Tich hop cong cu xuat ban da dinh dang (Markdown, Microsoft Word DOCX, PDF in an) bao toan 100% bang bieu va cong thuc.
3. **Giai doan 3 (Tuan 9 - 10): Luu tru dam may va quan tri cau hinh**
   - Thiet lap kho luu tru Amazon S3 voi CORS an toan va ma hoa tinh SSE-S3.
   - Khoi tao bang co so du lieu NoSQL Amazon DynamoDB (`document_processing_jobs`) o che do On-Demand (PAY_PER_REQUEST).
   - Ap dung nguyen tac Zero Hardcoded Secrets qua AWS Systems Manager (SSM) Parameter Store (`/huylam-ocr/config`) ma hoa KMS AES-256.
4. **Giai doan 4 (Tuan 11 - 12): Tich hop toan trinh va trien khai Production**
   - Dong goi ung dung Web Studio bang Dockerfile nen Python 3.11-slim.
   - Thiet lap tu dong hoa Serverless qua S3 Event Notification kich hoat AWS Lambda (`huylam-ocr-processor`) voi thoi gian khoi chay 214 ms va 88 MB bo nho.
   - Trien khai ha tang mang 3 tang Enterprise voi chuoi bao mat Security Group Chaining, ALB Multi-AZ va may chu EC2 Gunicorn duoc giam sat bang systemd.
   - Cung cap quy trinh trien khai mot cham tu dong (One-Click Deploy) qua `deploy.sh` su dung AWS Systems Manager Run Command ma khong can mo cong SSH 22.

---

## 2. Ket qua danh gia va ho so tot nghiep

- **Bao cao thuc tap tot nghiep**: Bien soan day du tap bao cao khoa hoc, slide thuyet trinh chuan Retina va bo so do kien truc chuan AWS Reference Architecture.
- **Bieu mau danh gia TTTN-08b**: Tu dong dien diem CLO1 - CLO7 (Muc 4, diem tong ket 9.38 / 10), danh gia 6 tieu chi chuyen mon va hoan tat chu ky sinh vien dung dinh dang Monochrome Academic Style.
- **Hien thi cong khai tren website Hugo**: Xuat ban 215 trang worklog song ngu va toan bo tai lieu tai repository `workshop`.

---

## 3. Quy trinh giai phong ha tang va kiem toan FinOps (Ngay 18/11/2026)

Nham thuc hien triet de nguyen tac ky luat tai chinh dam may (FinOps), sau khi hoan tat bao ve va nghiem thu thuc tap, toan bo tai nguyen tinh phi tren AWS da duoc giai phong hoan toan:

* **Sao luu du lieu dam may**: Dong bo toan bo 91 tep tai lieu va ket qua OCR tu S3 ve thu muc cuc bo `data/s3_backup/`.
* **Tieu huy Application Load Balancer**: Xoa ALB `huylam-ocr-alb` va Target Group `huylam-ocr-tg`, cham dut khoan phi co dinh ~23.40 USD/thang.
* **Giai phong dia chi Public IPv4**: Thu hoi toan bo Elastic IP de tranh phi 0.005 USD/IP/gio.
* **Terminate may chu EC2**: Cham dut may chu `i-0566e1eedaacea52d`, tu dong giai phong o dia EBS gp3 8GB.
* **Doi voi cac dich vu Serverless**: Xoa S3 bucket, DynamoDB table, AWS Lambda, API Gateway, Cognito User Pool va SSM Parameter Store de dua tai khoan ve trang thai sach se 100%.

---

## 4. Ket luan va bao toan ngan sach

Tong luong Credit da su dung luy ke qua cac thang la **85.48 USD**. Toan bo hoa don thuc te ma sinh vien phai tra luon duoc duy tri o muc **0.00 USD**. Toan bo so du Credit con lai (khoang 14.52 USD hoac 114.52 USD tuy goi tai tro ban dau) da duoc bao toan tron ven de phuc vu cho cac du an nghien cuu tiep theo tren AWS.

---

## 5. Cac lien ket lien quan trong Knowledge Brain
- [[project-status-and-roadmap]]: Chi tiet 12 tuan trien khai thuc tap.
- [[fcaj-internship-submission-guide]]: Quy chuan bao cao Hugo GitHub Pages.
- [[2026-11-18-aws-resource-teardown-and-finops-audit]]: Nhat ky kiem toan va ket qua lenh teardown chi tiet.
