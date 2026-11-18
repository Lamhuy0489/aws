# Nhat Ky Van Hanh Bo Nao Tri Thuc (Knowledge Base Log)

## [2026-09-18]
- Khoi tao cau truc bo nao ngoai vi 3 lop (raw/, wiki/, templates/).
- Thiet lap tep quy tac AGENT.md va lien ket bieu tuong CLAUDE.md.
- Khoi tao ban do tri thuc wiki/index.md va cac tep bieu mau templates.
- Chay chu ky Ingest dot 1:
  - Dua 4 tai lieu goc vao raw/labs/ va raw/papers/.
  - Sinh 4 ban tom tat nguon tai wiki/sources/ (fcj-2026-curriculum, fcj-2026-roadmap, fcj-2026-checklist, rag-2026-spec).
  - Trich xuat 4 trang khai niem cot loi tai wiki/concepts/ (agentic-rag, aws-lambda-controller, aws-bedrock-and-llm, fcj-training-framework).
  - Cap nhat toan bo lien ket hai chieu vao wiki/index.md.
- Chay chu ky Ingest va Compile dot 2:
  - Tiep nhan noi quy thuc tap hn-rules.awsfcaj.com vao raw/rules/fcaj-internship-rules-2026.md.
  - Tiep nhan huong dan Workshop Template vao raw/templates/fcaj-workshop-template-guide.md.
  - Tiep nhan phan tich bai nop mau cua hoc vien vao raw/reports/sample-student-workshop-proposal.md.
  - Tao 2 nguon moi trong wiki/sources/ (fcj-2026-internship-rules, fcj-2026-workshop-template).
  - Trich xuat 2 khai niem moi trong wiki/concepts/ (fcj-internship-evaluation, fcj-workshop-structure).
  - Xay dung bai tong hop chuyen sau wiki/syntheses/fcaj-internship-submission-guide.md.
  - Cap nhat dong bo toan bo lien ket vao wiki/index.md.
- Chay chu ky Ingest dot 3:
  - Xac minh ket noi AWS CLI v2 thanh cong voi IAM User dev_admin (Account ID: 677994024390).
  - Ghi nhan ket qua thuc hanh Lab 000001 & 000002 (MFA, IAM User/Group) vao raw/labs/lab-000001-setup-account-and-mfa.md.
  - Ghi nhan ket qua thuc hanh Lab 000007 (AWS Budgets 100$ & 200$) vao raw/labs/lab-000007-aws-budgets.md.
  - Ghi nhan ket qua thuc hanh Lab 000011 (AWS CLI) vao raw/labs/lab-000011-aws-cli.md.
  - Cap nhat Worklog tuan 1 tren website Hugo GitHub Pages tai lamhuy0489.github.io/workshop.

## [2026-09-22]
- Thiet lap nguon su that duy nhat ROADMAP.md tai goc kho luu tru voi day du checklist tien do 12 tuan danh dau [x] va [ ].
- Cap nhat AGENT.md va CLAUDE.md dinh hinh vai tro duy nhat: Serverless Hybrid Document OCR, Parsing & Technical Translation Platform on AWS.
- Xoa bo cac thu muc va logic ngoai le (rag, agents), xac thuc 27/27 test tu dong passing 100%.
- Cap nhat de xuat Proposal va Worklog Tuan 10 song ngu tren website Hugo workshop, bien dich thanh cong 215 trang va day len GitHub.
- Tao bai tong hop chuyen sau wiki/syntheses/project-status-and-roadmap.md va cap nhat wiki/index.md.
- Soan thao huong dan chi tiet thiet lap tung buoc tren AWS Management Console (S3, DynamoDB, SSM Parameter Store).

## [2026-11-18]
- Chay chu ky Compile va Output dot 4:
  - Hoan tat bao ve de tai tot nghiep va danh gia thuc tap TTTN-08b (CLO1 - CLO7, HPself = 9.38/10).
  - Thuc hien chu trinh FinOps Teardown: Kiem toan chi phi AWS Credit (tieu thu 85.48 USD luy ke, bao toan 100% so du con lai).
  - Sao luu toan bo 91 tep du lieu tu S3 ve data/s3_backup/.
  - Giai phong hoan toan cac tai nguyen dam may tinh phi: ALB, Target Group, EC2, EBS, Elastic IPs, S3 buckets, DynamoDB, Lambda, API Gateway, Cognito User Pool, SSM Parameter Store.
  - Bien soan bai tong hop wiki/syntheses/internship-completion-and-resource-teardown.md.
  - Bien soan nhat ky kiem toan chi tiet wiki/outputs/2026-11-18-aws-resource-teardown-and-finops-audit.md.
  - Cap nhat ban do tri thuc wiki/index.md va dong bo toan bo tri thuc len Git.
