# Ket Qua Thuc Hanh: Lab 000008 - Giam Sat He Thong Voi Amazon CloudWatch Alarms & Quan Tri Chi Phi FinOps

- Nguoi thuc hien: Lam Quang Huy
- MSSV: 0212267 - Lop: 67CS, HUCE
- Ngay hoan thanh: 2026-09-20
- AWS Account ID: 677994024390
- AWS Account Name: huylam
- Default Region: ap-southeast-1 (Singapore)
- Custom VPC: huylam-vpc (vpc-0125f4d6db3fbffa6)

---

## 1. Muc tieu thuc hanh

- Nam vung ba tru cot quan sat (Observability) tren nen tang dien toan dam may AWS: Metrics (Chi so dinh luong), Logs (Nhat ky su kien), va Alarms / Traces (Canh bao va truy vet).
- Khai thac Amazon CloudWatch Metrics: Theo doi cac chi so CPUUtilization, NetworkIn, NetworkOut cua may chu ao Amazon EC2; ap dung bieu thuc toan hoc Metric Math de tong hop luu luong mang theo thoi gian thuc.
- Quan ly tap trung CloudWatch Logs: Khoi tao Log Groups, Log Streams, day nhat ky su kien he thong tu EC2 ve CloudWatch va su dung ngon ngu truy van CloudWatch Logs Insights de trich xuat ban ghi co cau truc.
- Thiet lap co che canh bao chu dong CloudWatch Alarms: Tao canh bao qua tai vi xu ly voi nguong tinh (Static Threshold >= 70%), tich hop kenh thong bao Amazon SNS (Simple Notification Service) toi hop thu dien tu ca nhan.
- Thuc hien kiem nghiem tai cao (Stress Test): Kich hoat tai CPU 100% tren may chu EC2 de xac thuc qua trinh chuyen doi trang thai tu OK sang ALARM, tiep nhan email thong bao va tu dong phuc hoi ve OK khi ket thuc stress test.
- Xay dung bang dieu khien truc quan CloudWatch Dashboard: Tong hop cac widget theo doi trang thai canh bao, gia tri chi so don le, bieu do duong bien dong CPU kem nguong canh bao va bieu do Metric Math.
- Quan tri chi phi va thuc hanh FinOps: Kiem tra AWS Billing and Cost Management, danh gia chi phi luy ke Month-to-date (MTD), xac thuc trang thai van hanh cua 2 AWS Budgets va tien hanh giai phong toan bo tai nguyen tinh toan sau thuc hanh.

---

## 2. Thong so ky thuat xac thuc tren AWS

### 2.1. Ha tang tinh toan va mang (Compute & Networking)
- **VPC ID**: `vpc-0125f4d6db3fbffa6` (`huylam-vpc`)
- **Danh sach EC2 Instances thu nghiem**:
  - Instance 1: `i-010014c0c84c08ef6` (Amazon Linux 2023, t3.micro)
  - Instance 2: `i-048fa1b4099b74bb7` (Amazon Linux 2023, t3.micro, phuc vu stress test)

### 2.2. Dich vu thong bao Amazon SNS (Simple Notification Service)
- **SNS Topic Name**: `huylam-cw-alarms`
- **SNS Topic ARN**: `arn:aws:sns:ap-southeast-1:677994024390:huylam-cw-alarms`
- **Giao thuc Subscription**: Email
- **Email nhan thong bao**: `huyngu127@gmail.com`
- **Trang thai xac thuc**: `Confirmed`

### 2.3. Chi so va Bieu thuc toan hoc (CloudWatch Metrics & Metric Math)
- **Namespace**: `AWS/EC2`
- **Cac chi so giam sat**:
  - `m1`: `CPUUtilization` (InstanceId: `i-048fa1b4099b74bb7`, Unit: Percent, Period: 60s)
  - `m2`: `NetworkIn` (InstanceId: `i-048fa1b4099b74bb7`, Unit: Bytes, Period: 60s)
  - `m3`: `NetworkOut` (InstanceId: `i-048fa1b4099b74bb7`, Unit: Bytes, Period: 60s)
- **Bieu thuc Metric Math**:
  - **Id**: `e1`
  - **Expression**: `(m2 + m3) / 1024`
  - **Label**: `Total Network KB`
  - **Muc dich**: Chuyen doi tong luu luong mang vao va ra tu don vi Bytes sang Kilobytes (KB) de truc quan hoa de dang tren do thi.

### 2.4. Nhat ky CloudWatch Logs va Truy van Logs Insights
- **Log Groups da tao**:
  - `/huylam/cloudwatch/system-logs`: Luu tru nhat ky van hanh he thong.
  - `/huylam/cloudwatch/httpd-access`: Luu tru nhat ky truy cap web server.
- **Log Stream**: `ec2-system-stream`
- **Cau lenh truy van Logs Insights**:
  ```sql
  fields @timestamp, @message
  | sort @timestamp desc
  | limit 20
  ```
- **Ket qua truy van**: Tra ve 8 ban ghi he thong ghi nhan thong tin sinh vien Lam Quang Huy (MSSV: 0212267).

### 2.5. Canh bao CloudWatch Alarm
- **Alarm Name**: `huylam-ec2-high-cpu-alarm`
- **Alarm ARN**: `arn:aws:cloudwatch:ap-southeast-1:677994024390:alarm:huylam-ec2-high-cpu-alarm`
- **Mo ta**: `CloudWatch Alarm for student Lam Quang Huy (MSSV: 0212267) - High CPU Utilization on i-048fa1b4099b74bb7`
- **Chi so giam sat**: `AWS/EC2` -> `CPUUtilization`
- **Dieu kien kich hoat (Threshold Conditions)**:
  - Loai nguong: Static Threshold
  - Phep so sanh: Greater than or equal to (`>=`)
  - Gia tri nguong: `70%`
  - Chu ky danh gia: 1 chu ky danh gia 60 giay (1 out of 1 datapoints)
  - Xu ly du lieu thieu (Missing data treatment): Treat missing data as missing
- **Hanh dong khi canh bao (Alarm Action)**:
  - Khi chuyen trang thai sang `In ALARM`: Gui thong bao toi SNS Topic `huylam-cw-alarms` (`arn:aws:sns:ap-southeast-1:677994024390:huylam-cw-alarms`)

### 2.6. Bang dieu khien CloudWatch Dashboard
- **Dashboard Name**: `huylam-monitoring-dashboard`
- **Cau truc 4 Widgets**:
  1. Widget 1: Alarm status widget - Hien thi trang thai canh bao cua `huylam-ec2-high-cpu-alarm`.
  2. Widget 2: Single value widget - Do luong CPU Utilization tuc thoi.
  3. Widget 3: Line graph widget - Bieu do duong the hien CPU Utilization theo thoi gian kem duong nguong do tinh (70%) va dinh tai stress test.
  4. Widget 4: Line graph widget - Bieu do Metric Math hien thi tong luu luong mang Network In + Out tinh theo Kilobytes.

### 2.7. Quan tri chi phi AWS Billing, Cost Explorer & Budgets
- **Month-to-date (MTD) actual spend**: 0.10 USD
- **Forecasted spend**: 0.14 USD
- **Trang thai AWS Budgets**: 2 budgets hoat dong o trang thai `HEALTHY` (nguong canh bao 5 USD va 10 USD).
- **Ty trong chi phi**: Virtual Private Cloud chiem 0.10 USD (trong han muc an toan Free Tier).

---

## 3. Quy trinh kiem nghiem va ket qua do dac

### 3.1. Kich hoat Stress Test tren EC2 Instance
- Thuc hien sinh tai CPU 100% tren instance `i-048fa1b4099b74bb7` thong qua cong cu stress:
  ```bash
  stress-ng --cpu 2 --timeout 300s --metrics-brief
  ```
- **Ket qua quan sat**:
  - Muc do su dung CPU tang dot bien tu muc nghi (<5%) len `93.858%` (`93.86%`).
  - Sau 60 giay danh gia, CloudWatch Alarm phat hien vi pham nguong 70% va chuyen trang thai tu `OK` sang `ALARM`.

### 3.2. Tiep nhan thong bao canh bao qua Email
- Hop thu `huyngu127@gmail.com` tiep nhan email tu `AWS Notifications <no-reply@sns.amazonaws.com>` voi cac thong so:
  - Tieu de: `ALARM: "huylam-ec2-high-cpu-alarm" in Asia Pacific (Singapore)`
  - Datapoint ghi nhan: `93.85833333333333 (20/09/26 16:14:00)` vuot nguong `70.0%`.
  - Mo ta dinh danh: `CloudWatch Alarm for student Lam Quang Huy (MSSV: 0212267) - High CPU Utilization on i-048fa1b4099b74bb7`.
  - AWS Account: `677994024390`.

### 3.3. Tu dong phuc hoi ve trang thai OK
- Sau khi tien trinh stress-ng ket thuc, CPU ha xuong muc `6.46%`.
- Tai chu ky danh gia tiep theo, CloudWatch Alarm xac nhan gia tri thap hon nguong 70% va tu dong chuyen trang thai tu `ALARM` ve `OK`.

---

## 4. Quy trinh don dep tai nguyen FinOps (Resource Cleanup)

De dam bao khong phat sinh chi phi duy tri va bao toan han muc AWS Free Tier, toan bo tai nguyen thuc hanh da duoc xoa bo theo thu tu logic sau:
1. Xoa bo Alarm: `aws cloudwatch delete-alarms --alarm-names huylam-ec2-high-cpu-alarm`
2. Xoa bo Dashboard: `aws cloudwatch delete-dashboards --dashboard-names huylam-monitoring-dashboard`
3. Xoa bo Log Groups:
   - `aws logs delete-log-group --log-group-name /huylam/cloudwatch/system-logs`
   - `aws logs delete-log-group --log-group-name /huylam/cloudwatch/httpd-access`
4. Xoa bo SNS Topic: `aws sns delete-topic --topic-arn arn:aws:sns:ap-southeast-1:677994024390:huylam-cw-alarms`
5. Terminate cac EC2 Instances: `aws ec2 terminate-instances --instance-ids i-010014c0c84c08ef6 i-048fa1b4099b74bb7`

Ket qua kiem tra sau don dep: So luong tai nguyen tinh toan va giam sat hoat dong tro ve 0, chi phi duy tri he thong dat 0 USD.
