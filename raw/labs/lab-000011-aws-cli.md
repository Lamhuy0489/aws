# Ket Qua Thuc Hanh: Lab 000011 - Cai Dat Va Cau Hinh AWS CLI

- Nguoi thuc hien: Lam Huy
- Ngay hoan thanh: 2026-09-18
- Duong dan binary: /usr/local/bin/aws

---

## 1. Muc tieu
- Cai dat giao dien dong lenh AWS Command Line Interface (CLI) phien ban v2 tren he dieu hanh macOS.
- Thiet lap thong tin xac thuc profile mac dinh ket noi toi tai khoan AWS bang Access Key ID va Secret Access Key cua IAM User `dev_admin`.

## 2. Thong so moi truong da xac thuc
- Phien ban CLI: `aws-cli/2.36.48`
- Phien ban Python di kem: `Python/3.14.6`
- Kien truc may: `Darwin/21.6.0 exe/x86_64`
- Default Region: `ap-southeast-1`
- Output Format: `json`

## 3. Cac lenh kiem tra thanh cong
```bash
aws sts get-caller-identity
# Ket qua:
# {
#     "UserId": "AIDAZ3W4XZXDELB4KHD3N",
#     "Account": "677994024390",
#     "Arn": "arn:aws:iam::677994024390:user/dev_admin"
# }
```
