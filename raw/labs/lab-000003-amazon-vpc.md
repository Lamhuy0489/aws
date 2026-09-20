# Ket Qua Thuc Hanh: Lab 000003 - Thiet Ke Va Trien Khai Amazon Custom VPC & Networking

- Nguoi thuc hien: Lam Quang Huy
- Ngay hoan thanh: 2026-09-20
- AWS Account ID: 677994024390
- AWS Account Name: huylam
- Default Region: ap-southeast-1 (Singapore)
- Custom VPC Name: huylam-vpc
- Custom VPC ID: vpc-0125f4d6db3fbffa6
- EC2 Test Instance: huylam-vpc-test-server (i-02a465d3907141cfb)

---

## 1. Muc tieu
- Thiet ke va xay dung mang ao tuy bien Amazon VPC voi dai dia chi IPv4 CIDR `10.0.0.0/16`.
- Trien khai kien truc Multi-AZ do san sang cao gom 2 Availability Zones (`ap-southeast-1a` va `ap-southeast-1b`), 2 Public Subnets va 2 Private Subnets.
- Khoi tao Internet Gateway `huylam-igw` va gan ket vao Custom VPC.
- Thiet lap bang dinh tuyen Route Tables phan tach ro rang luu luong Internet va luu luong noi bo.
- Kich hoat tinh nang tu dong cap phat Public IPv4 tren Public Subnet.
- Cau hinh tuong lua ao Security Group mo cong SSH (22), HTTP (80) va ICMP IPv4.
- Kiem tra cau hinh mang con Network ACL (Stateless Firewall).
- Khoi tao may chu ao EC2 kiem nghiem ket noi mang qua Internet Gateway, do do tre ICMP ping va phan giai ten mien DNS qua curl.
- Ap dung nguyen tac FinOps giai phong tai nguyen compute sau khi do kiem.

## 2. Thong so ky thuat da xac thuc tren AWS

### 2.1. Mang ao Custom VPC
- VPC ID: `vpc-0125f4d6db3fbffa6`
- VPC Name: `huylam-vpc`
- IPv4 CIDR: `10.0.0.0/16` (65,536 dia chi IP)
- DNS Resolution: `Enabled`
- DNS Hostnames: `Enabled`
- State: `available`

### 2.2. Internet Gateway
- IGW ID: `igw-0b9db3a6eac29ede9`
- Name: `huylam-igw`
- Attachment: `vpc-0125f4d6db3fbffa6`

### 2.3. Danh sach Subnets
- Public Subnet 1: `subnet-0efa7c3a5818035dc` (`huylam-subnet-public1-ap-southeast-1a`), CIDR `10.0.0.0/20`, AZ `ap-southeast-1a`, Auto-assign Public IP: `Yes`.
- Public Subnet 2: `subnet-0e07eb2fd44d1ac91` (`huylam-subnet-public2-ap-southeast-1b`), CIDR `10.0.16.0/20`, AZ `ap-southeast-1b`, Auto-assign Public IP: `No`.
- Private Subnet 1: `subnet-08563e499271091ab` (`huylam-subnet-private1-ap-southeast-1a`), CIDR `10.0.128.0/20`, AZ `ap-southeast-1a`.
- Private Subnet 2: `subnet-07e20dc44c40fac46` (`huylam-subnet-private2-ap-southeast-1b`), CIDR `10.0.144.0/20`, AZ `ap-southeast-1b`.

### 2.4. Route Tables
- Public RTB: `rtb-012d99ed0350e956f` (`huylam-rtb-public`), Routes: `10.0.0.0/16 local`, `0.0.0.0/0 -> igw-0b9db3a6eac29ede9`.
- Private RTB 1: `rtb-0d49944883c933d2a` (`huylam-rtb-private1-ap-southeast-1a`), Route: `10.0.0.0/16 local`.
- Private RTB 2: `rtb-00f6e53a047aafc1f` (`huylam-rtb-private2-ap-southeast-1b`), Route: `10.0.0.0/16 local`.

### 2.5. Security Group
- SG ID: `sg-0dbd6bbde1b366070` (`huylam-vpc-web-sg`)
- Inbound:
  - TCP 22 (SSH) tu `0.0.0.0/0`
  - TCP 80 (HTTP) tu `0.0.0.0/0`
  - All ICMP - IPv4 tu `0.0.0.0/0`
- Outbound: All traffic toi `0.0.0.0/0`

### 2.6. Network ACL
- NACL ID: `acl-09a50f9e28bc6477d`
- Associated Subnets: 4 Subnets cua `huylam-vpc`
- Inbound: Rule 100 Allow all traffic, Rule * Deny
- Outbound: Rule 100 Allow all traffic, Rule * Deny

### 2.7. EC2 Test Instance
- Instance ID: `i-02a465d3907141cfb` (`huylam-vpc-test-server`)
- Instance Type: `t3.micro`
- Public IP: `54.151.162.47`
- Private IP: `10.0.14.174`
- Status: Da kiem thu thanh cong va thuc hien Terminate de bao toan gio Free Tier.

## 3. Ket qua kiem nghiem ket noi mang

### 3.1. Ping tu moi truong cuc bo toi Public IP EC2
```text
PING 54.151.162.47 (54.151.162.47): 56 data bytes
64 bytes from 54.151.162.47: icmp_seq=0 ttl=114 time=49.123 ms
64 bytes from 54.151.162.47: icmp_seq=1 ttl=114 time=48.910 ms
64 bytes from 54.151.162.47: icmp_seq=2 ttl=114 time=49.450 ms
64 bytes from 54.151.162.47: icmp_seq=3 ttl=114 time=49.020 ms

4 packets transmitted, 4 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 48.910/49.126/49.450/0.201 ms
```

### 3.2. Ping tu EC2 ra DNS Server cong cong (8.8.8.8) qua IGW
```text
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=114 time=1.12 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=114 time=1.11 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=114 time=1.20 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=114 time=1.10 ms

4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/mdev = 1.103/1.133/1.200/0.038 ms
```

### 3.3. Phan giai ten mien DNS va ket noi HTTPS
```text
HTTP/1.1 301 Moved Permanently
Server: Server
Date: Sun, 20 Sep 2026 09:39:26 GMT
Content-Type: text/html
Connection: keep-alive
Location: https://www.amazon.com/
x-amz-rid: 7S4DNVXPQM3D0EMFTPF1
Vary: User-Agent,Accept-Encoding
```

## 4. Danh sach anh minh chung
Tat ca hinh anh da duoc luu tru va khoanh vien do xac thuc tai `workshop/static/images/week3/` va `raw/images/week3/`:
1. `01-vpc-create-settings-preview.png`: Cau hinh tao Custom VPC huylam-vpc va ban do tai nguyen
2. `02-vpc-create-nat-dns-options.png`: Thiet lap NAT Gateway (None) va DNS Options
3. `03-vpc-resource-map.png`: So do tai nguyen Resource Map cua huylam-vpc
4. `04-subnet-enable-auto-assign-public-ip.png`: Kich hoat tinh nang Auto-assign Public IP cho Public Subnet
5. `05-security-group-create-rules.png`: Thiet lap Inbound Rules cho huylam-vpc-web-sg
6. `06-security-group-created-success.png`: Xac nhan tao Security Group thanh cong
7. `07-ec2-launch-custom-vpc-network-settings.png`: Cau hinh mang cho EC2 instance trong Custom VPC
8. `08-ec2-launch-success.png`: Thong bao khoi tao EC2 thanh cong
9. `09-ec2-instance-summary-running.png`: Bang tom tat may chu ao EC2 hoat dong (Running)
10. `10-ec2-instance-connect-terminal-test.png`: Kiem thu ping va curl tren EC2 Instance Connect Terminal
11. `11-vpc-network-acl-inbound-rules.png`: Kiem tra bang Inbound Rules cua Network ACL
