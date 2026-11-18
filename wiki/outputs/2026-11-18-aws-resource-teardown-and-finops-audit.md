# Nhat Ky Kiem Toan FinOps Va Lenh Teardown Giai Phong Tai Nguyen (2026-11-18)

Nhat ky chi tiet qua trinh ra soat chi phi AWS Credit, kiem tra cac tai nguyen hoat dong va cac lenh CLI thuc thi giai phong ha tang dam may.

---

## 1. So lieu kiem toan chi phi truoc khi huy tai nguyen

* **Tai khoan thuc thi**: `677994024390` (IAM User: `dev_admin`, Region: `ap-southeast-1`).
* **Chi phi thang 11/2026 (01/11 - 18/11)**:
  * Tong chi phi su dung (Usage): 22.10 USD.
  * Elastic Load Balancing: 10.24 USD.
  * Amazon VPC (Public IPv4): 6.09 USD.
  * Amazon EC2 Compute: 5.34 USD.
  * Amazon EBS: 0.43 USD.
  * Ghi nhan khau tru Credit: -22.10 USD (Tien phai tra: 0.00 USD).
* **Luy ke Credit da su dung toan bo thoi gian**:
  * 2026-07: 11.79 USD
  * 2026-08: 0.00 USD
  * 2026-09: 11.09 USD
  * 2026-10: 40.50 USD
  * 2026-11 (den 18/11): 22.10 USD
  * **Tong da dung**: 85.48 USD.
  * **Uoc tinh Credit con lai**: ~14.52 USD (neu goi 100 USD) hoac ~114.52 USD (neu goi 200 USD).

---

## 2. Nhat ky cac lenh thuc thi giai phong (Teardown Execution)

1. **Sao luu toan bo du lieu S3 ve may cuc bo**:
   ```bash
   aws s3 sync s3://huylam-ocr-documents-ap-southeast-1 /Users/huylam/Downloads/aws/data/s3_backup
   # Ket qua: Dong bo thanh cong 91 tep (29.3 MiB) ve thu muc data/s3_backup/
   ```

2. **Xoa Application Load Balancer va Target Group**:
   ```bash
   aws elbv2 delete-load-balancer --region ap-southeast-1 --load-balancer-arn "arn:aws:elasticloadbalancing:ap-southeast-1:677994024390:loadbalancer/app/huylam-ocr-alb/68ac5f1a04e35614"
   aws elbv2 delete-target-group --region ap-southeast-1 --target-group-arn "arn:aws:elasticloadbalancing:ap-southeast-1:677994024390:targetgroup/huylam-ocr-tg/9840edd6b7d65bf3"
   ```

3. **Terminate may chu EC2**:
   ```bash
   aws ec2 terminate-instances --region ap-southeast-1 --instance-ids "i-0566e1eedaacea52d"
   # Ket qua: Instance chuyen tu running -> shutting-down -> terminated.
   # O dia EBS 8GB gp3 tu dong duoc giai phong.
   ```

4. **Kiem tra va giai phong Elastic IPs**:
   ```bash
   aws ec2 describe-addresses --region ap-southeast-1
   # Ket qua: Khong con bat ky Elastic IP nao ton tai tren he thong.
   ```

5. **Xoa toan bo S3 buckets cua du an**:
   ```bash
   aws s3 rb s3://huylam-ocr-documents-ap-southeast-1 --force
   aws s3 rb s3://huylam-static-web-677994024390 --force
   ```

6. **Xoa cac tai nguyen Serverless**:
   ```bash
   aws dynamodb delete-table --region ap-southeast-1 --table-name "document_processing_jobs"
   aws lambda delete-function --region ap-southeast-1 --function-name "huylam-ocr-processor"
   aws apigatewayv2 delete-api --region ap-southeast-1 --api-id "hpyewvtaya"
   aws ssm delete-parameter --region ap-southeast-1 --name "/huylam-ocr/config"
   ```

7. **Xoa Cognito User Pool va Domain**:
   ```bash
   aws cognito-idp delete-user-pool-domain --region ap-southeast-1 --user-pool-id "ap-southeast-1_dNJkc4IWG" --domain "ap-southeast-1dnjkc4iwg"
   aws cognito-idp update-user-pool --region ap-southeast-1 --user-pool-id "ap-southeast-1_dNJkc4IWG" --deletion-protection "INACTIVE"
   aws cognito-idp delete-user-pool --region ap-southeast-1 --user-pool-id "ap-southeast-1_dNJkc4IWG"
   ```

8. **Don dep CloudWatch Log Groups**:
   ```bash
   aws logs delete-log-group --region ap-southeast-1 --log-group-name "/aws/lambda/huylam-ocr-processor"
   aws logs delete-log-group --region ap-southeast-1 --log-group-name "/ecs/huylam-web-task"
   aws logs delete-log-group --region ap-southeast-1 --log-group-name "/aws/vpc/flowlogs"
   ```

---

## 3. Bien ban nghiem thu trang thai tai nguyen

Toan bo truy van kiem tra tai Region `ap-southeast-1` deu tra ve danh sach rong:
- EC2 Instances: 0 instance active.
- Elastic Load Balancers: 0 ALB.
- Target Groups: 0 Target Group.
- EBS Volumes: 0 volume.
- Elastic IPs: 0 IP.
- Lambda Functions: 0 function.
- DynamoDB Tables: 0 table.
- API Gateways: 0 API.
- Cognito User Pools: 0 pool.
- S3 Project Buckets: 0 bucket.

Chi phi van hanh moi gio tren tai khoan da dua ve **0.00 USD**, dam bao tuyet doi khong phat sinh phi ngoai y muon.
