# Ket Qua Thuc Hanh: Lab 000057 - Luu Tru Website Tinh Tren Amazon S3

- Nguoi thuc hien: Lam Quang Huy
- Ngay hoan thanh: 2026-09-20
- AWS Account ID: 677994024390
- AWS Account Name: huylam
- Default Region: ap-southeast-1 (Singapore)

---

## 1. Muc tieu
- Khoi tao Amazon S3 Bucket voi ten mien toan cau hop le: `huylam-static-web-677994024390`.
- Thiet lap cau hinh Block Public Access co kiem soat phuc vu luu tru website tinh.
- Kich hoat tinh nang Static Website Hosting tren S3 voi tep chi muc mac dinh `index.html`.
- Soan thao va ap dung chinh sach S3 Bucket Policy (JSON) cap quyen doc cong khai `s3:GetObject` theo chuan Least Privilege.
- Xac thuc hoat dong toan trinh qua giao thuc HTTP va dong lenh AWS CLI.

## 2. Thong so he thong da xac thuc qua AWS CLI
- Bucket Name: `huylam-static-web-677994024390`
- Bucket ARN: `arn:aws:s3:::huylam-static-web-677994024390`
- Bucket Website Endpoint: `http://huylam-static-web-677994024390.s3-website-ap-southeast-1.amazonaws.com`
- HTTP Status Code: `200 OK`
- S3 Bucket Policy:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::huylam-static-web-677994024390/*"
        }
    ]
}
```

## 3. Hinh anh minh chung thuc te
- `../images/week2/01-create-bucket-config.png`
- `../images/week2/02-block-public-access-settings.png`
- `../images/week2/03-default-encryption-sse-s3.png`
- `../images/week2/04-bucket-created-success.png`
- `../images/week2/05-upload-index-html.png`
- `../images/week2/06-enable-static-hosting.png`
- `../images/week2/07-static-hosting-endpoint.png`
- `../images/week2/08-bucket-policy-json.png`
- `../images/week2/09-website-live-verification.png`

## 4. Danh gia kien truc & Bao mat
- Tuan thu nguyen tac bao mat thiet yeu: Khong cap quyen `PutObject`, `DeleteObject` hay `PutBucketPolicy` ra ngoai Internet.
- Luu tru khong may chu (Serverless Static Hosting): Tiet kiem chi phi toi da do khong duy tri may ao EC2 24/7, nam trong han muc 5GB Free Tier cua Amazon S3.
