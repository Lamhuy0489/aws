# Ket Qua Thuc Hanh: Lab 000004 - Tu Dong Hoa Cai Dat Web Server Voi EC2 User Data

- Nguoi thuc hien: Lam Quang Huy
- Ngay hoan thanh: 2026-09-20
- AWS Account ID: 677994024390
- AWS Account Name: huylam
- Default Region: ap-southeast-1 (Singapore)
- Instance Name: huylam-web-server
- Instance ID: i-0520ad41a8d6ce258
- Public IPv4: 47.129.234.42

---

## 1. Muc tieu
- Khoi tao may chu ao Amazon EC2 tren nen tang he dieu hanh Amazon Linux 2023 thuoc goi Free Tier (t3.micro).
- Thiet lap nhom bao mat mang (Security Group) mo cong 22 (SSH) quan tri va cong 80 (HTTP) tiep nhan luu luong truy cap web.
- Su dung tinh nang EC2 User Data de tu dong hoa quy trinh bootstrap: cap nhat he dieu hanh, cai dat Apache HTTP Server, khoi dong dich vu daemon va sinh giao dien the sinh vien.
- Kiem tra va xac thuc kha nang phan hoi cua web server qua trinh duyet thuc te voi ma trang thai HTTP 200 OK.

## 2. Thong so ky thuat da xac thuc
- Instance ID: `i-0520ad41a8d6ce258`
- Instance Type: `t3.micro`
- Architecture: `x86_64`
- Operating System: `Amazon Linux 2023 AMI`
- VPC ID: `vpc-0c84feaf395ece4dd` (Default VPC)
- Subnet ID: `subnet-0497f256c54a58825` (`ap-southeast-1a`)
- Security Group ID: `sg-0eb53b21a70a15a9c`
- Inbound Rules:
  - TCP 22 (SSH) tu `0.0.0.0/0`
  - TCP 80 (HTTP) tu `0.0.0.0/0`
- Web Server Service: Apache `httpd 2.4.68`
- Endpoint kiem tra: `http://47.129.234.42`
- HTTP Response: `200 OK`

## 3. Ma nguon tap lenh EC2 User Data (Bootstrap Script)
```bash
#!/bin/bash
dnf update -y
dnf install -y httpd
systemctl start httpd
systemctl enable httpd

cat << 'EOF' > /var/www/html/index.html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Amazon EC2 Web Server - Lam Quang Huy</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background: #0f172a; color: #f8fafc; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
        .card { background: #1e293b; border: 1px solid #334155; border-radius: 12px; max-width: 600px; width: 100%; padding: 32px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        .badge { display: inline-block; background: #059669; color: #ffffff; padding: 4px 12px; border-radius: 9999px; font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 16px; }
        h1 { font-size: 24px; font-weight: 700; margin-bottom: 8px; color: #38bdf8; }
        p.subtitle { color: #94a3b8; font-size: 14px; margin-bottom: 24px; }
        .info-grid { display: grid; grid-template-columns: 140px 1fr; gap: 12px; font-size: 14px; border-top: 1px solid #334155; padding-top: 20px; }
        .label { color: #94a3b8; font-weight: 500; }
        .value { color: #f1f5f9; font-weight: 600; font-family: monospace; }
        .footer { margin-top: 24px; padding-top: 16px; border-top: 1px solid #334155; font-size: 12px; color: #64748b; text-align: center; }
    </style>
</head>
<body>
    <div class="card">
        <div class="badge">Web Server Live</div>
        <h1>Amazon EC2 Apache Web Server</h1>
        <p class="subtitle">Thuc Hanh Tuan 2 - First Cloud Journey Workforce 2026</p>
        <div class="info-grid">
            <div class="label">Sinh Vien:</div>
            <div class="value">Lam Quang Huy</div>
            <div class="label">AWS Account ID:</div>
            <div class="value">677994024390</div>
            <div class="label">Account Name:</div>
            <div class="value">huylam</div>
            <div class="label">Region:</div>
            <div class="value">ap-southeast-1 (Singapore)</div>
            <div class="label">Instance ID:</div>
            <div class="value">i-0520ad41a8d6ce258</div>
            <div class="label">Public IPv4:</div>
            <div class="value">47.129.234.42</div>
            <div class="label">De Tai Capstone:</div>
            <div class="value">Enterprise Agentic RAG Platform on AWS</div>
        </div>
        <div class="footer">
            Trien khai tu dong qua EC2 User Data tren nen Amazon Linux 2023
        </div>
    </div>
</body>
</html>
EOF
```

## 4. Hinh anh minh chung thuc te
- `../images/week2/14-ec2-launch-security-group.png`
- `../images/week2/15-ec2-launch-user-data-script.png`
- `../images/week2/16-ec2-launch-success.png`
- `../images/week2/17-ec2-web-server-browser-verification.png`

## 5. Danh gia kien truc & FinOps
- **Tu dong hoa ha tang (Infrastructure as Code / Bootstrap)**: Loai bo hoan toan thao tac thu cong qua SSH sau khi khoi tao may chu, giam thieu sai sot va dam bao tinh nhat quan.
- **Quan ly chi phi (FinOps)**: May chu su dung loai `t3.micro` nam trong han muc 750 gio/thang Free Tier. Sau khi hoan tat buoc kiem tra va chup anh minh chung, instance can duoc stop hoac terminate de bao ve ngan sach tai khoan.
