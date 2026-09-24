#!/bin/bash
# ==============================================================================
# Script tu dong dong bo ma nguon va cap nhat may chu EC2 (One-Click Deploy)
# Huylam OCR Platform - Account ID: 677994024390 - Region: ap-southeast-1
# ==============================================================================
set -e

INSTANCE_ID="i-0566e1eedaacea52d"
REGION="ap-southeast-1"
ALB_URL="http://huylam-ocr-alb-1284818160.ap-southeast-1.elb.amazonaws.com/login"

echo "[1/3] Dang day ma nguon cuc bo len GitHub (origin main)..."
git push origin main || true

echo "[2/3] Gui lenh cap nhat toi may chu EC2 qua AWS Systems Manager (SSM)..."
COMMAND_ID=$(aws ssm send-command \
  --region "$REGION" \
  --instance-ids "$INSTANCE_ID" \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=["cd /opt/huylam-ocr && git pull origin main && systemctl restart huylam-ocr.service && systemctl status huylam-ocr.service --no-pager"]' \
  --query "Command.CommandId" \
  --output text)

echo "Lenh da duoc gui thanh cong (Command ID: $COMMAND_ID)."
echo "Dang cho may chu EC2 keo code va khoi dong lai Gunicorn..."
sleep 5

aws ssm get-command-invocation \
  --region "$REGION" \
  --command-id "$COMMAND_ID" \
  --instance-id "$INSTANCE_ID" \
  --query "StandardOutputContent" \
  --output text

HTTPS_URL="https://hpyewvtaya.execute-api.ap-southeast-1.amazonaws.com/login"
ALB_URL="http://huylam-ocr-alb-1284818160.ap-southeast-1.elb.amazonaws.com/login"

echo "[3/3] Kiem tra phan hoi thuc te tu HTTPS API Gateway & ALB..."
HTTP_STATUS=$(curl -s -L -o /dev/null -w "%{http_code}" "$HTTPS_URL")

if [ "$HTTP_STATUS" = "200" ]; then
  echo "CAP NHAT THANH CONG! May chu phan hoi HTTP $HTTP_STATUS OK qua HTTPS."
  echo "URL Live HTTPS (Khuyen nghi): $HTTPS_URL"
  echo "URL ALB: $ALB_URL"
else
  echo "Canh bao: May chu tra ve ma HTTP $HTTP_STATUS. Vui long kiem tra log."
fi
