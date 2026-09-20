# Báo Cáo Thực Hành: Lab 000037 - Infrastructure as Code (IaC) Với AWS CloudFormation

- Người thực hiện: Lâm Quang Huy
- MSSV: 0212267 - Lớp: 67CS, HUCE
- Ngày hoàn thành: 2026-09-21
- AWS Account ID: 677994024390
- AWS Account Name: huylam
- Default Region: ap-southeast-1 (Singapore)
- Stack Name: huylam-cfn-stack
- Stack ID: arn:aws:cloudformation:ap-southeast-1:677994024390:stack/huylam-cfn-stack/54395360-b520-11f1-90f4-0a4ed60f7479

---

## 1. Mục tiêu thực hành

- Nghiên cứu và áp dụng mô hình Hạ tầng dưới dạng mã nguồn (Infrastructure as Code - IaC) trên môi trường AWS bằng dịch vụ AWS CloudFormation.
- Xây dựng bản mẫu khai báo hạ tầng (CloudFormation Template) chuẩn hóa bằng định dạng YAML, chia tách rõ ràng các khối `AWSTemplateFormatVersion`, `Description`, `Parameters`, `Resources` và `Outputs`.
- Tự động hóa phân giải hình ảnh máy ảo AMI Amazon Linux 2023 mới nhất theo thời gian thực thông qua cơ chế tích hợp kiểu tham số chuyên dụng `AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>` trỏ đến đường dẫn `/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-6.1-x86_64`.
- Tự động hóa quá trình cài đặt phần mềm máy chủ web Apache (`httpd`) bằng kịch bản `UserData` mã hóa Base64, kết xuất động trang giao diện định danh học viên Lâm Quang Huy (MSSV: `0212267`), lớp 67CS, Trường ĐH Xây dựng Hà Nội (HUCE).
- Khởi tạo ngăn xếp tài nguyên (CloudFormation Stack) `huylam-cfn-stack`, theo dõi luồng sự kiện (Stack Events) cho đến khi đạt trạng thái hoàn tất thành công `CREATE_COMPLETE`.
- Kiểm tra các giá trị đầu ra (Stack Outputs) bao gồm Public IPv4 `47.129.129.6`, Security Group ID `sg-059146261d1b7c5eb`, tên Stack và đường dẫn truy cập website trực tiếp.
- Xác thực trực tiếp trên trình duyệt web, đảm bảo máy chủ phản hồi mã trạng thái HTTP 200 OK và hiển thị chuẩn xác thông tin học viên.
- Thực hiện kiểm tra phát hiện trôi dạt cấu hình (CloudFormation Drift Detection) nhằm kiểm soát tính toàn vẹn giữa hạ tầng thực tế và bản thiết kế trong template.
- Áp dụng quy trình FinOps Teardown: Thu hồi và dọn dẹp toàn bộ tài nguyên ngăn xếp để bảo toàn ngân sách AWS Free Tier (0 USD).

---

## 2. Thông số kỹ thuật xác thực trên AWS

### 2.1. Định danh & Môi trường thực thi
- **AWS Account ID**: `677994024390`
- **Tên tài khoản (Account Name)**: `huylam`
- **IAM Principal**: `dev_admin` (`arn:aws:iam::677994024390:user/dev_admin`)
- **AWS Region**: `ap-southeast-1` (Asia Pacific - Singapore)
- **Availability Zone**: `ap-southeast-1c`
- **VPC trực thuộc**: Default VPC (`vpc-0c84feaf395ece4dd`)
- **Subnet ID**: `subnet-0bba3228d80514181` (Public Subnet)

### 2.2. Chi tiết ngăn xếp CloudFormation
- **Stack Name**: `huylam-cfn-stack`
- **Stack ID**: `arn:aws:cloudformation:ap-southeast-1:677994024390:stack/huylam-cfn-stack/54395360-b520-11f1-90f4-0a4ed60f7479`
- **Thời gian khởi tạo**: `2026-09-20 18:23:08 UTC`
- **Trạng thái ngăn xếp (Stack Status)**: `CREATE_COMPLETE`
- **Thời gian triển khai**: 25 giây
- **Chính sách khôi phục (Rollback Configuration)**: Rollback on failure (mặc định)

### 2.3. Tham số đầu vào (Stack Parameters)
- **EnvironmentName**: `FCJ-Bootcamp-2026`
- **InstanceType**: `t3.micro`
- **LatestAmiId**: `/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-6.1-x86_64`
  - Resolved Dynamic AMI: `ami-085b17e53d4c8f0cb`
- **StudentID**: `0212267`
- **StudentName**: `Lam Quang Huy`

### 2.4. Máy chủ ảo được tạo bởi IaC (EC2 Instance)
- **Logical Resource ID**: `WebServerInstance`
- **Physical Resource ID**: `i-0b328b3c9bf942cd7`
- **Resource Type**: `AWS::EC2::Instance`
- **Instance State**: `running`
- **Public IPv4 Address**: `47.129.129.6`
- **Private IPv4 Address**: `172.31.15.0`
- **Public DNS**: `ec2-47-129-129-6.ap-southeast-1.compute.amazonaws.com`
- **Instance Type**: `t3.micro` (1 vCPU, 2 GiB RAM burstable)
- **AMI ID**: `ami-085b17e53d4c8f0cb` (Amazon Linux 2023)
- **Tags**:
  - `Name`: `huylam-cfn-webserver`
  - `Project`: `FCJ-Bootcamp-2026`
  - `StudentID`: `0212267`
  - `aws:cloudformation:stack-name`: `huylam-cfn-stack`
  - `aws:cloudformation:logical-id`: `WebServerInstance`

### 2.5. Nhóm bảo mật được tạo bởi IaC (Security Group)
- **Logical Resource ID**: `WebServerSecurityGroup`
- **Physical Resource ID**: `huylam-cfn-stack-WebServerSecurityGroup-oatvCIRD2205`
- **Security Group ID**: `sg-059146261d1b7c5eb`
- **Resource Type**: `AWS::EC2::SecurityGroup`
- **Inbound Rules**: Cổng 80 (HTTP) từ `0.0.0.0/0`
- **Outbound Rules**: All traffic (`0.0.0.0/0`)

### 2.6. Giá trị đầu ra của ngăn xếp (Stack Outputs)
- **WebServerPublicIp**: `47.129.129.6`
- **WebServerUrl**: `http://47.129.129.6`
- **SecurityGroupId**: `huylam-cfn-stack-WebServerSecurityGroup-oatvCIRD2205`
- **StackName**: `huylam-cfn-stack`

### 2.7. Đo kiểm trôi dạt cấu hình (Drift Detection)
- **Drift Detection ID**: `8240c5e0-b520-11f1-854d-0205312630e5`
- **Timestamp**: `2026-09-20 18:29:44 UTC`
- **Security Group Status**: `IN_SYNC`
- **EC2 Instance Status**: `MODIFIED` (do địa chỉ IP động và ENI runtime được gắn thêm)

---

## 3. Mã nguồn tệp mẫu CloudFormation (huylam-cfn-week7.yaml)

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: >
  AWS CloudFormation Lab 000037 - Infrastructure as Code (IaC)
  Student: Lam Quang Huy | Student ID: 0212267 | Class: 67CS - HUCE
  FCJ Cloud Journey Bootcamp 2026

Parameters:
  EnvironmentName:
    Type: String
    Default: FCJ-Bootcamp-2026
    Description: Deployment environment tag name

  StudentName:
    Type: String
    Default: Lam Quang Huy
    Description: Student full name

  StudentID:
    Type: String
    Default: "0212267"
    Description: Student ID number

  InstanceType:
    Type: String
    Default: t3.micro
    AllowedValues:
      - t2.micro
      - t3.micro
    Description: Amazon EC2 instance type (Free Tier eligible)

  LatestAmiId:
    Type: 'AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>'
    Default: '/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-6.1-x86_64'
    Description: Automatically resolve the latest Amazon Linux 2023 AMI via AWS Systems Manager Parameter Store

Resources:
  WebServerSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Enable HTTP access from anywhere for HuyLam Web Server
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
      Tags:
        - Key: Name
          Value: !Sub '${AWS::StackName}-web-sg'
        - Key: Project
          Value: !Ref EnvironmentName
        - Key: StudentID
          Value: !Ref StudentID

  WebServerInstance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: !Ref InstanceType
      ImageId: !Ref LatestAmiId
      SecurityGroupIds:
        - !Ref WebServerSecurityGroup
      UserData:
        Fn::Base64: !Sub |
          #!/bin/bash
          dnf update -y
          dnf install -y httpd
          systemctl start httpd
          systemctl enable httpd
          cat <<EOF > /var/www/html/index.html
          <!DOCTYPE html>
          <html lang="vi">
          <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AWS CloudFormation Lab 000037 - ${StudentName}</title>
            <style>
              body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 40px 20px; display: flex; justify-content: center; align-items: center; min-height: 80vh; }
              .card { background: #1e293b; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); padding: 36px; max-width: 650px; width: 100%; border: 1px solid #334155; }
              h1 { color: #38bdf8; font-size: 24px; margin-top: 0; border-bottom: 2px solid #334155; padding-bottom: 12px; }
              .badge { display: inline-block; background-color: #0284c7; color: white; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 13px; margin-bottom: 16px; }
              .info-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #334155; }
              .label { color: #94a3b8; font-weight: 500; }
              .value { font-weight: 600; color: #f1f5f9; }
              .success { color: #4ade80; font-weight: bold; }
              .footer { margin-top: 24px; text-align: center; color: #64748b; font-size: 13px; }
            </style>
          </head>
          <body>
            <div class="card">
              <span class="badge">AWS CloudFormation IaC</span>
              <h1>Web Server Deployed via CloudFormation</h1>
              <div class="info-row"><span class="label">Hoc vien:</span><span class="value">${StudentName}</span></div>
              <div class="info-row"><span class="label">MSSV:</span><span class="value">${StudentID}</span></div>
              <div class="info-row"><span class="label">Lop:</span><span class="value">67CS - Truong DH Xay dung Ha Noi (HUCE)</span></div>
              <div class="info-row"><span class="label">Stack Name:</span><span class="value">${AWS::StackName}</span></div>
              <div class="info-row"><span class="label">Region:</span><span class="value">${AWS::Region}</span></div>
              <div class="info-row"><span class="label">Du an:</span><span class="value">${EnvironmentName}</span></div>
              <div class="info-row"><span class="label">Trang thai:</span><span class="value success">SUCCESSFULLY PROVISIONED</span></div>
              <div class="footer">FCJ Cloud Journey Bootcamp 2026 - Infrastructure as Code Module</div>
            </div>
          </body>
          </html>
          EOF
      Tags:
        - Key: Name
          Value: huylam-cfn-webserver
        - Key: Project
          Value: !Ref EnvironmentName
        - Key: StudentID
          Value: !Ref StudentID

Outputs:
  WebServerPublicIp:
    Description: Public IPv4 address of the web server
    Value: !GetAtt WebServerInstance.PublicIp

  WebServerUrl:
    Description: HTTP URL to access the deployed website
    Value: !Sub 'http://${WebServerInstance.PublicIp}'

  SecurityGroupId:
    Description: ID of the Security Group created
    Value: !Ref WebServerSecurityGroup

  StackName:
    Description: Name of the deployed CloudFormation Stack
    Value: !Ref 'AWS::StackName'
```

---

## 4. Danh mục 12 hình ảnh minh chứng thực tế trên AWS

Tất cả các hình ảnh minh chứng đều được trích xuất từ bảng điều khiển AWS Console và trình duyệt thực tế của sinh viên Lâm Quang Huy (MSSV: 0212267). Các vùng trọng yếu gồm Account Badge `huylam (677994024390)`, khu vực Singapore `ap-southeast-1` và các thông số kỹ thuật cốt lõi đều được đóng khung viền đỏ chuẩn xác:

1. **01-cfn-stacks-list-initial.png**: Danh sách Stacks ban đầu (`Stacks (0)`, `No stacks to display`) với nút `Create stack`.
2. **02-cfn-create-stack-upload-template.png**: Tải lên thành công tệp mẫu `huylam-cfn-week7.yaml`.
3. **03-cfn-specify-stack-details.png**: Cấu hình Stack name `huylam-cfn-stack` và 5 tham số đầu vào.
4. **04-cfn-stack-create-in-progress.png**: Trạng thái ngăn xếp đang tạo `CREATE_IN_PROGRESS`.
5. **05-cfn-webserver-browser-verification.png**: Trình duyệt truy cập `http://47.129.129.6` hiển thị thông tin học viên Lâm Quang Huy.
6. **06-cfn-stack-info-create-complete.png**: Thẻ Stack info xác nhận trạng thái hoàn thành `CREATE_COMPLETE`.
7. **07-cfn-stack-events-all-complete.png**: Thẻ Stack events ghi nhận đầy đủ chuỗi sự kiện tạo tài nguyên thành công.
8. **08-cfn-stack-resources-list.png**: Thẻ Resources xác nhận 2 tài nguyên `WebServerInstance` và `WebServerSecurityGroup`.
9. **09-cfn-stack-outputs-values.png**: Thẻ Outputs hiển thị 4 giá trị đầu ra gồm Public IP, URL, Security Group ID, Stack Name.
10. **10-cfn-stack-template-yaml.png**: Thẻ Template hiển thị mã nguồn YAML của ngăn xếp.
11. **11-cfn-stacks-list-actions-menu.png**: Menu Stack actions chọn tùy chọn phát hiện trôi dạt cấu hình `Detect drift`.
12. **12-cfn-stack-drift-detection.png**: Thông báo kiểm tra Drift detection thành công kèm ID và trạng thái hoàn tất.

---

## 5. Quy trình FinOps Teardown & Dọn dẹp

Để đưa chi phí về 0 USD và bảo toàn tài nguyên AWS Free Tier:

```bash
# 1. Xóa toàn bộ CloudFormation Stack (tự động xóa EC2 và Security Group)
aws cloudformation delete-stack --stack-name huylam-cfn-stack

# 2. Chờ cho đến khi ngăn xếp được xóa hoàn toàn
aws cloudformation wait stack-delete-complete --stack-name huylam-cfn-stack

# 3. Xác thực không còn tài nguyên tồn đọng
aws cloudformation describe-stacks --stack-name huylam-cfn-stack 2>&1 | grep "does not exist"
aws ec2 describe-instances --filters "Name=tag:aws:cloudformation:stack-name,Values=huylam-cfn-stack" \
  --query "Reservations[*].Instances[*].[InstanceId,State.Name]" --output table
aws ec2 describe-security-groups --filters "Name=group-name,Values=*huylam-cfn-stack*" \
  --query "SecurityGroups[*].[GroupId,GroupName]" --output table
```
