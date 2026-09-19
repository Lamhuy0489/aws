# Ket Qua Thuc Hanh: Lab 000048 - Gan Va Kiem Nghiem IAM Role Cho Amazon EC2

- Nguoi thuc hien: Lam Quang Huy
- Ngay hoan thanh: 2026-09-20
- AWS Account ID: 677994024390
- AWS Account Name: huylam
- Default Region: ap-southeast-1 (Singapore)
- IAM Role Name: huylam-ec2-s3-readonly-role
- Gan vao Instance: i-0520ad41a8d6ce258 (huylam-web-server)

---

## 1. Muc tieu
- Thiet ke va khoi tao IAM Role danh rieng cho dich vu Amazon EC2 compute.
- Gan chinh sach AWS Managed Policy `AmazonS3ReadOnlyAccess` theo dung nguyen tac dac quyen toi thieu (Least Privilege).
- Gan IAM Role vao may chu ao EC2 `huylam-web-server` (`i-0520ad41a8d6ce258`).
- Kiem nghiem co che cap quyen tam thoi (temporary security credentials) thong qua EC2 Instance Metadata Service (IMDS) bang cach thuc thi lenh `aws s3 ls` qua EC2 Instance Connect ma khong luu tru Access Key tren may.

## 2. Thong so ky thuat da xac thuc
- Role Name: `huylam-ec2-s3-readonly-role`
- Role ARN: `arn:aws:iam::677994024390:role/huylam-ec2-s3-readonly-role`
- Instance Profile ARN: `arn:aws:iam::677994024390:instance-profile/huylam-ec2-s3-readonly-role`
- Attached Policy: `arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess`
- Trusted Entity: Service `ec2.amazonaws.com`
- Trust Policy (JSON):
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

## 3. Ket qua kiem nghiem qua EC2 Instance Connect
Ket noi an toan vao may chu EC2 qua EC2 Instance Connect va chay lenh kiem tra:
```bash
[ec2-user@ip-172-31-27-251 ~]$ aws s3 ls
2026-09-19 16:59:16 huylam-static-web-677994024390
```
Ket qua tra ve danh sach S3 Bucket xac nhan rang:
1. May chu EC2 da tu dong nhan duoc temporary credentials tu IMDS thong qua IAM Role `huylam-ec2-s3-readonly-role`.
2. Khong he co file cau hinh `~/.aws/credentials` hay bien moi truong `AWS_ACCESS_KEY_ID` nao duoc luu tru tren may ao.
3. Kien truc hoan toan khang duoc rủi ro lo lot thong tin bi mat (credential leak).

## 4. Hinh anh minh chung thuc te
- `../images/week2/10-iam-role-trusted-entity.png`
- `../images/week2/11-iam-role-permissions-s3-readonly.png`
- `../images/week2/12-iam-role-name-review.png`
- `../images/week2/13-iam-role-created-success.png`
- `../images/week2/18-ec2-instance-connect-s3-ls.png`

## 5. Danh gia an toan & Best Practices
- **Trien khai IAM Role thay vi IAM User Access Key**: Tuyet doi khong tao IAM Access Key cho ung dung chay tren EC2. IAM Role tu dong xoay vong khoa bao mat (automatic credential rotation), triet tieu nguy co bi danh cap credentials khi may chu bi tan cong hoac backup bi ro ri.
- **Tuan thu Least Privilege**: Chi gan quyen `AmazonS3ReadOnlyAccess` phuc vu nhu cau doc du lieu, ngan chan hoan toan cac thao tac ghi de, xoa bucket hoac thay doi chinh sach phan quyen.
