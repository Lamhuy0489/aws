# Ket Qua Thuc Hanh: Lab 000006 - Tu Dong Co Gian He Thong Voi EC2 Auto Scaling & Application Load Balancer

- Nguoi thuc hien: Lam Quang Huy
- MSSV: 0212267 - Lop: 67CS, HUCE
- Ngay hoan thanh: 2026-09-20
- AWS Account ID: 677994024390
- AWS Account Name: huylam
- Default Region: ap-southeast-1 (Singapore)
- Custom VPC: huylam-vpc (vpc-0125f4d6db3fbffa6)
- ALB DNS Name: huylam-alb-1974057692.ap-southeast-1.elb.amazonaws.com

---

## 1. Muc tieu thuc hanh
- Thiet ke va trien khai kien truc tinh toan do san sang cao (High Availability) va kha nang mo rong tu dong (Auto Scaling) tren ha tang Custom VPC Multi-AZ.
- Xay dung 2 lop tuong lua ao Security Group:
  - Security Group cho Application Load Balancer (`huylam-alb-sg`): Tiep nhan luu luong HTTP (cong 80) tu toan bo Internet (`0.0.0.0/0`).
  - Security Group cho may chu web backend (`huylam-asg-web-sg`): Chi cho phep tiep nhan luu luong HTTP tu `huylam-alb-sg` va SSH tu xa, ngan chan truy cap truc tiep vao backend instances tu ben ngoai.
- Khoi tao Launch Template (`huylam-launch-template`) voi Amazon Linux 2023 AMI, phien ban phan cung `t3.micro`, tich hop tap lenh User Data su dung IMDSv2 token de tu dong cai dat Apache Web Server va khoi tao giao dien the thong tin sinh vien phan anh dong Instance ID va Availability Zone.
- Tao Target Group (`huylam-alb-tg`) loai Target Instance voi giao thuc HTTP port 80 va duong dan Health Check `/`.
- Khoi tao Application Load Balancer (`huylam-alb`) Internet-facing, dinh tuyen qua 2 Public Subnets tren 2 Availability Zones (`ap-southeast-1a` va `ap-southeast-1b`), thiet lap Listener HTTP:80 forward toi `huylam-alb-tg`.
- Khoi tao Auto Scaling Group (`huylam-asg`) voi dung luong Desired: 2, Min: 1, Max: 4, gan voi Launch Template va Target Group da tao, phan bo tren 2 Availability Zones.
- Kiem nghiem trang thai Healthy cua cac target (2/2 targets dat trang thai Healthy).
- Kiem tra co che can bang tai vong tron (Round-Robin) thong qua DNS cua ALB tren trinh duyet web, xac thuc luu luong duoc phan phoi luan phien giua 2 Instance ID thuoc 2 Availability Zones khac nhau.
- Thuc hien quy trinh FinOps: Giai phong toan bo tai nguyen tinh toan (ASG, EC2 instances, ALB, Target Group, Launch Template, Security Groups) de bao toan han muc AWS Free Tier.

---

## 2. Thong so ky thuat xac thuc tren AWS

### 2.1. Mang ao & Nhom bao mat (VPC & Security Groups)
- **VPC ID**: `vpc-0125f4d6db3fbffa6` (`huylam-vpc`, CIDR `10.0.0.0/16`)
- **ALB Security Group**:
  - SG ID: `sg-066b3dc2f4c6b4c86`
  - Name: `huylam-alb-sg`
  - Inbound Rule: HTTP (TCP 80), Source `0.0.0.0/0`
  - Outbound Rule: All traffic, Destination `0.0.0.0/0`
- **ASG Web Security Group**:
  - SG ID: `sg-0a9dede4860cae619`
  - Name: `huylam-asg-web-sg`
  - Inbound Rule 1: HTTP (TCP 80), Source `sg-066b3dc2f4c6b4c86` (`huylam-alb-sg`)
  - Inbound Rule 2: SSH (TCP 22), Source `0.0.0.0/0`
  - Outbound Rule: All traffic, Destination `0.0.0.0/0`

### 2.2. Launch Template
- **Launch Template ID**: `lt-064a116476cc47e0a`
- **Launch Template Name**: `huylam-launch-template`
- **Default Version**: `1`
- **AMI ID**: `ami-095f155a67469a548` (Amazon Linux 2023 Kernel 6.1 x86_64)
- **Instance Type**: `t3.micro`
- **Security Groups**: `sg-0a9dede4860cae619` (`huylam-asg-web-sg`)
- **User Data Script**:
  - Lay IMDSv2 Token (thoi han 21600 giay).
  - Truy van metadata: `instance-id`, `local-ipv4`, `placement/availability-zone`.
  - Cai dat va khoi chay Apache httpd.
  - Render trang HTML the thong tin sinh vien Lam Quang Huy (MSSV: 0212267) tich hop tham so may chu.

### 2.3. Target Group
- **Target Group ARN**: `arn:aws:elasticloadbalancing:ap-southeast-1:677994024390:targetgroup/huylam-alb-tg/01224986629b1f06`
- **Target Group Name**: `huylam-alb-tg`
- **Target Type**: `instance`
- **Protocol**: `HTTP`
- **Port**: `80`
- **VPC**: `vpc-0125f4d6db3fbffa6`
- **Health Check Path**: `/`
- **Health Check Protocol**: `HTTP`
- **Trang thai Targets**: 2/2 targets Healthy

### 2.4. Application Load Balancer
- **ALB ARN**: `arn:aws:elasticloadbalancing:ap-southeast-1:677994024390:loadbalancer/app/huylam-alb/1d3845375aef8945`
- **ALB Name**: `huylam-alb`
- **Scheme**: `internet-facing`
- **IP Address Type**: `ipv4`
- **VPC**: `vpc-0125f4d6db3fbffa6`
- **Subnets Mapping**:
  - `subnet-0efa7c3a5818035dc` (`ap-southeast-1a`)
  - `subnet-0e07eb2fd44d1ac91` (`ap-southeast-1b`)
- **Security Group**: `sg-066b3dc2f4c6b4c86` (`huylam-alb-sg`)
- **DNS Name**: `huylam-alb-1974057692.ap-southeast-1.elb.amazonaws.com`
- **Listener**: HTTP:80 forwarding toi `huylam-alb-tg`
- **State**: `active`

### 2.5. Auto Scaling Group
- **ASG Name**: `huylam-asg`
- **Launch Template**: `huylam-launch-template` (Version 1)
- **Subnets**: `subnet-0efa7c3a5818035dc`, `subnet-0e07eb2fd44d1ac91`
- **Target Groups**: `huylam-alb-tg`
- **Health Check Type**: `ELB`
- **Health Check Grace Period**: `300` seconds
- **Desired Capacity**: `2`
- **Minimum Capacity**: `1`
- **Maximum Capacity**: `4`
- **Danh sach Instances khoi tao**:
  - Instance 1: `i-01abe8b9b987aad60` | Zone: `ap-southeast-1a` | Private IP: `10.0.9.229` | Public IP: `47.129.221.209`
  - Instance 2: `i-0e633e2910dd9ea8f` | Zone: `ap-southeast-1b` | Private IP: `10.0.25.48` | Public IP: `54.255.196.87`

---

## 3. Ket qua kiem nghiem phan phoi tai Round-Robin

### 3.1. Kiem tra Target Health Check qua AWS CLI
```bash
aws elbv2 describe-target-health \
  --target-group-arn arn:aws:elasticloadbalancing:ap-southeast-1:677994024390:targetgroup/huylam-alb-tg/01224986629b1f06 \
  --query "TargetHealthDescriptions[*].[Target.Id,Target.Port,TargetHealth.State]" \
  --output table
```
Ket qua:
```text
---------------------------------------------
|            DescribeTargetHealth           |
+----------------------+-----+--------------+
|  i-01abe8b9b987aad60 |  80 |  healthy     |
|  i-0e633e2910dd9ea8f |  80 |  healthy     |
+----------------------+-----+--------------+
```

### 3.2. Kiem tra phan phoi tai qua trinh duyet web
- Truy cap 1: Trinh duyet gui request toi `http://huylam-alb-1974057692.ap-southeast-1.elb.amazonaws.com/`. ALB phan phoi toi may chu backend tai Availability Zone `ap-southeast-1b`:
  - Instance ID: `i-0e633e2910dd9ea8f`
  - Private IP: `10.0.25.48`
  - Availability Zone: `ap-southeast-1b`
  - Trang thai: `Active / Healthy`
- Truy cap 2 (Reload trang): Trinh duyet gui request tiep theo toi ALB DNS. ALB ap dung thuat toan Round-Robin chuyen huong request toi may chu backend tai Availability Zone `ap-southeast-1a`:
  - Instance ID: `i-01abe8b9b987aad60`
  - Private IP: `10.0.9.229`
  - Availability Zone: `ap-southeast-1a`
  - Trang thai: `Active / Healthy`

Ket qua xac thuc: He thong can bang tai hoat dong hoan hao giua 2 mien kha dung doc lap, dam bao tinh chiu loi (Fault Tolerance) va san sang cao (High Availability).

---

## 4. Thuc hanh FinOps - Giai phong tai nguyen
Do Application Load Balancer co muc phi co dinh duy tri khoang 0.0225 USD/gio (~16.2 USD/thang) va 2 instance EC2 backend dang hoat dong, toan bo cac buoc don dep da duoc thuc hien ngay sau khi kiem nghiem thanh cong:
1. Xoa Auto Scaling Group `huylam-asg` qua lenh `--force-delete`: Tu dong giai phong va terminate ca 2 instance EC2 backend.
2. Xoa Application Load Balancer `huylam-alb`.
3. Xoa Target Group `huylam-alb-tg`.
4. Xoa Launch Template `huylam-launch-template`.
5. Xoa Security Groups `huylam-asg-web-sg` va `huylam-alb-sg`.
6. Xac nhan trang thai cac instance da chuyen sang `terminated`, dua chi phi van hanh ve muc 0 USD.
