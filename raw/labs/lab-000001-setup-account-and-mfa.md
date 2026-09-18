# Ket Qua Thuc Hanh: Lab 000001 & Lab 000002 - Khoi Tao Tai Khoan AWS va Bao Mat IAM

- Nguoi thuc hien: Lam Huy
- Ngay hoan thanh: 2026-09-18
- AWS Account ID: 677994024390
- Default Region: ap-southeast-1 (Singapore)

---

## 1. Muc tieu
- Dang ky tai khoan AWS moi voi goi Free Tier 12 thang.
- Thiet lap xac thuc 2 lop (MFA) cho tai khoan goc (Root Account) de phong chong truy cap trai phep.
- Khoi tao IAM User va IAM Group danh rieng cho lap trinh va quan tri hang ngay, tuan thu nguyen tac khong su dung tai khoan Root cho cac tac vu phat trien.

## 2. Thong so he thong da xac thuc qua AWS CLI
- IAM User: `dev_admin`
- User ARN: `arn:aws:iam::677994024390:user/dev_admin`
- User ID: `AIDAZ3W4XZXDELB4KHD3N`
- Root Account MFA Status: `Enabled (MFA: 1)`
- Number of IAM Groups: `1`
- Number of IAM Roles: `7`

## 3. Cac buoc da thuc hien tren AWS Console
1. Dang ky tai khoan AWS tai aws.amazon.com, hoan tat xac minh thanh toan the quoc te.
2. Dang nhap tai khoan Root, truy cap IAM Console -> Security credentials -> Kich hoat Virtual MFA Device qua ung dung xac thuc tren dien thoai.
3. Vao muc IAM -> User Groups: Tao nhom quan tri.
4. Vao muc IAM -> Users: Tao user `dev_admin`, gan quyen quan tri `AdministratorAccess`.
5. Tao Access Key ID va Secret Access Key cho `dev_admin` phuc vu giao tiep CLI.

## 4. Ket luan & Danh gia an toan
Tai khoan da dap ung day du tieu chuan an toan co ban theo CIS AWS Foundations Benchmark (Root account co MFA, cong viec hang ngay thuc hien qua IAM User).
