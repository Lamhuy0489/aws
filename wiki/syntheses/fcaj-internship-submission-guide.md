# Bai Tong Hop: Huong Dan Xay Dung Va Nop Bao Cao Thuc Tap FCAJ Bang Website Hugo

- Nguoi tong hop: Agentic Brain
- Ngay tong hop: 2026-09-18
- Chu de: Quy trinh xay dung website bao cao thuc tap tren GitHub Pages cho du an Agentic RAG

---

## 1. Tong quan quy trinh nop bai thuc tap
Trong chuong trinh FCAJ Workforce Bootcamp, hoc vien khong nop file Word hay PDF roi rac ma nop thong qua mot **Website Bao Cao Thuc Tap (Internship Report)** duoc tao bang Hugo, deploy len GitHub Pages va ho tro song ngu (Tieng Viet va Tieng Anh).

Day la san pham chinh danh gia toan dien ky nang thiet ke kien truc, ky nang lap trinh, ky nang viet tai lieu va tinh ky luat cua hoc vien.

---

## 2. Lo trinh 4 buoc de hoan thanh website bao cao

### Buoc 1: Clone va thiet lap Hugo Website
1. Clone bo template mau tu repo cua cong dong:
   ```bash
   git clone https://github.com/AWS-First-Cloud-Journey/Workshop-template.git workshop-report
   cd workshop-report
   ```
2. Cai dat Hugo (ban extended) va chay thu nghiem:
   ```bash
   brew install hugo
   hugo server -D
   ```
3. Chinh sua file `config.toml`:
   - Dat `baseURL = "https://Lamhuy0489.github.io/aws-workshop-report/"`
   - Chinh sua `title = "Agentic RAG on AWS - Internship Report"`
   - Cau hinh 2 ngon ngu `en` va `vi`.

### Buoc 2: Soan thao noi dung theo 7 muc bat buoc
Dua tren de tai **Agentic RAG on AWS**, ta phan bo noi dung vao thu muc `content/`:

1. `content/1-worklog/`:
   - Ghi chep nhat ky 12 tuan (tuan 1 hoc VPC/IAM, tuan 2 hoc EC2/S3, tuan 3-4 hoc Lambda/DynamoDB, tuan 5-8 code Agentic RAG, tuan 9-10 CI/CD & CloudWatch, tuan 11-12 hoan thien website).
2. `content/2-proposal/`:
   - De xuat de tai "Enterprise Agentic RAG Platform on AWS".
   - So do kien truc tong the (Next.js -> API Gateway -> Lambda Agent -> S3/DynamoDB/External LLM).
   - Ly do lua chon cac dich vu AWS va phan tich chi phi 0 dong (FinOps).
3. `content/3-blogsposted/`:
   - Blog 1: "Toi uu chi phi LLM tren AWS voi SSM Parameter Store va Gemini API".
   - Blog 2: "Kien truc ReAct Agent khong may chu voi AWS Lambda va DynamoDB".
   - Blog 3: "Thuc hanh tot nhat ve bao mat IAM va S3 cho he thong RAG".
4. `content/4-events/`:
   - Ghi nhan 3 buoi tham gia FCAJ Community Day, Technical Sharing Meetup hoac AWS Summit.
5. `content/5-workshop/`:
   - Day la phan quan trong nhat (chiem 6.0 diem):
     - 5.1 Overview & Prerequisites (Tao tai khoan, cai AWS CLI).
     - 5.2 Storage Setup (Tao S3 Bucket luu raw documents).
     - 5.3 Database & State (Tao bang DynamoDB luu chat history voi TTL).
     - 5.4 Secret Management (Luu API Key an toan trong AWS Systems Manager).
     - 5.5 Backend Agent Deployment (Dong goi Lambda Function va lien ket API Gateway).
     - 5.6 Frontend Deployment (Luu web chat tren S3 va phan phoi qua CloudFront).
     - 5.7 Monitoring & Logging (Theo doi latency, token qua CloudWatch).
     - 5.8 Testing (Gui cac mau test query phuc tap, kiem tra ReAct reasoning).
     - 5.9 Clean-up Resources (Huong dan xoa tai nguyen de khong bi tru tien).
6. `content/6-evaluation/`:
   - Tu danh gia 8 tieu chi nang luc.
7. `content/7-feedback/`:
   - Danh gia cam nhan ve khoa hoc va loi cam on gui den cac anh chi mentor.

### Buoc 3: Trien khai len GitHub Pages
1. Tao GitHub repository moi (vi du: `aws-workshop-report`) o che do Public.
2. Thiet lap GitHub Actions (`.github/workflows/hugo.yml`) de moi khi push code len nhanh `main`, he thong tu dong build Hugo va deploy vao nhanh `gh-pages`.
3. Kiem tra website hoat dong tai dia chi: `https://Lamhuy0489.github.io/aws-workshop-report/`.

### Buoc 4: Nop bao cao va Nhan moc thuc tap
- Nop duong link website GitHub Pages cho Mentor.
- Dam bao da co du toi thieu 10 buoi check-in tai van phong Tang 7 Toa Grand Terra Ha Noi va 3 buoi su kien de nhan tron 4.0 diem chuyen can/tac phong/event.
- Diem tong ket se dat tu 8.5 den 9.5 / 10 diem nho de tai Agentic RAG hien dai va trinh bay chuan muc.

---

## 3. Lien ket lien quan
- [[fcaj-2026-internship-rules]]
- [[fcaj-internship-evaluation]]
- [[fcaj-workshop-structure]]
- [[agentic-rag]]
- [[aws-lambda-controller]]
