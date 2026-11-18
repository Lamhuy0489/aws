# -*- coding: utf-8 -*-
"""
Generate standard, authentic AWS Reference Architecture Diagram
matching official draw.io mxgraph.aws4 stencils and AWS Reference Architecture standards.
Reflecting live infrastructure from AWS Account 677994024390 (ap-southeast-1).
"""
import os
import re
import base64
import subprocess

def extract_base64_icons():
    with open("workshop/static/images/architecture/aws-system-architecture.svg") as f:
        orig = f.read()

    imgs = re.findall(r"<image[^>]+href=\"(data:image/[^;]+;base64,[^\"]+)\"[^>]*>", orig)
    
    icons = {
        "aws_badge": imgs[0],
        "vpc": imgs[1],
        "igw": imgs[2],
        "alb": imgs[3],
        "ec2": imgs[4],
        "s3": imgs[5],
        "lambda": imgs[6],
        "ddb": imgs[7],
        "ssm": imgs[8],
        "cw": imgs[9],
        "bedrock": imgs[10],
        "users": imgs[11],
        "dev": imgs[12],
        "github": imgs[13],
        "kaggle": imgs[14],
    }

    # Add cropped SNS, Cognito, IAM
    for name in ["sns_clean", "cognito_clean", "iam_clean"]:
        path = f"/tmp/{name}.png"
        if os.path.exists(path):
            with open(path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
                key = name.replace("_clean", "")
                icons[key] = f"data:image/png;base64,{b64}"
    
    return icons

def generate_svg(icons):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1060" width="1600" height="1060" style="background:#FFFFFF; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  <defs>
    <!-- Standard Marker Arrows -->
    <marker id="arr-black" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#232F3E" />
    </marker>
    <marker id="arr-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#0284C7" />
    </marker>
    <marker id="arr-purple" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#8C4FFF" />
    </marker>
    <marker id="arr-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#16A34A" />
    </marker>
    <marker id="arr-orange" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#EA580C" />
    </marker>
    <marker id="arr-magenta" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#E11D48" />
    </marker>
    <!-- Drop Shadow for subtle depth -->
    <filter id="box-shadow" x="-2%" y="-2%" width="104%" height="104%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="1" stdDeviation="2" flood-opacity="0.05"/>
    </filter>
  </defs>

  <!-- ==================== TOP TITLE / HEADER ==================== -->
  <g transform="translate(40, 25)">
    <text x="0" y="16" fill="#0F172A" font-size="16" font-weight="700" letter-spacing="0.2">SERVERLESS HYBRID DOCUMENT OCR, PARSING &amp; TECHNICAL TRANSLATION PLATFORM</text>
    <text x="960" y="16" fill="#475569" font-size="12" font-weight="500">AWS Reference Architecture  |  Region: ap-southeast-1 (Singapore)  |  Account: 677994024390</text>
    <line x1="0" y1="26" x2="1520" y2="26" stroke="#CBD5E1" stroke-width="1"/>
  </g>

  <!-- ==================== CLIENTS / WORKSTATIONS LAYER (LEFT) ==================== -->
  <rect x="35" y="65" width="175" height="405" rx="6" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.5" stroke-dasharray="4,4"/>
  <text x="48" y="87" fill="#334155" font-size="12" font-weight="700">Clients &amp; Workstations</text>

  <!-- End Users Icon + Label -->
  <g transform="translate(92, 105)">
    <image href="{icons['users']}" x="0" y="0" width="56" height="56"/>
    <text x="28" y="70" fill="#0F172A" font-size="12" font-weight="700" text-anchor="middle">End Users</text>
    <text x="28" y="84" fill="#475569" font-size="10" text-anchor="middle">Web Browser / SPA</text>
    <text x="28" y="97" fill="#64748B" font-size="9" text-anchor="middle">PDF &amp; Scan Uploads</text>
  </g>

  <!-- Internet Cloud Indicator -->
  <g transform="translate(68, 220)">
    <rect x="0" y="0" width="110" height="40" rx="20" fill="#F1F5F9" stroke="#94A3B8" stroke-width="1.2"/>
    <text x="55" y="24" fill="#334155" font-size="11" font-weight="600" text-anchor="middle">Internet</text>
  </g>

  <!-- DevOps / Admin Icon + Label -->
  <g transform="translate(92, 280)">
    <image href="{icons['dev']}" x="0" y="0" width="56" height="56"/>
    <text x="28" y="70" fill="#0F172A" font-size="12" font-weight="700" text-anchor="middle">DevOps / Admin</text>
    <text x="28" y="84" fill="#475569" font-size="10" text-anchor="middle">Lâm Quang Huy (67CS)</text>
    <text x="28" y="97" fill="#64748B" font-size="9" text-anchor="middle">MSSV: 0212267</text>
  </g>

  <!-- GitHub Repo Icon + Box -->
  <g transform="translate(50, 395)">
    <rect x="0" y="0" width="145" height="60" rx="6" fill="#FFFFFF" stroke="#334155" stroke-width="1.2"/>
    <image href="{icons['github']}" x="8" y="10" width="38" height="38"/>
    <text x="52" y="26" fill="#0F172A" font-size="11" font-weight="700">GitHub Repo</text>
    <text x="52" y="39" fill="#2563EB" font-size="9.5" font-weight="600">Lamhuy0489/aws</text>
    <text x="52" y="51" fill="#64748B" font-size="8.5">CI/CD: deploy.sh</text>
  </g>

  <!-- ==================== EXTERNAL HYBRID AI ACCELERATOR (BOTTOM-LEFT) ==================== -->
  <rect x="35" y="490" width="175" height="270" rx="6" fill="#F0F9FF" stroke="#0284C7" stroke-width="1.5"/>
  <text x="48" y="512" fill="#075985" font-size="11.5" font-weight="700">External AI Cluster</text>
  <text x="48" y="525" fill="#0369A1" font-size="9">(Hybrid Acceleration)</text>

  <!-- Kaggle GPU Icon + Box -->
  <g transform="translate(48, 538)">
    <rect x="0" y="0" width="150" height="105" rx="5" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.2" filter="url(#box-shadow)"/>
    <image href="{icons['kaggle']}" x="10" y="10" width="36" height="36"/>
    <text x="52" y="25" fill="#0F172A" font-size="11" font-weight="700">Kaggle GPU</text>
    <text x="52" y="38" fill="#0284C7" font-size="9" font-weight="600">Qwen-2.5-VL 7B</text>
    <line x1="10" y1="50" x2="140" y2="50" stroke="#E2E8F0" stroke-width="1"/>
    <text x="10" y="65" fill="#475569" font-size="8.5">Hardware: 2x NVIDIA T4</text>
    <text x="10" y="78" fill="#475569" font-size="8.5">32GB VRAM  |  FastAPI</text>
    <text x="10" y="94" fill="#0284C7" font-size="8.5" font-weight="600">Cloudflare HTTPS Tunnel</text>
  </g>

  <!-- Google Gemini Flash API Box -->
  <g transform="translate(48, 655)">
    <rect x="0" y="0" width="150" height="85" rx="5" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.2" filter="url(#box-shadow)"/>
    <rect x="10" y="10" width="30" height="30" rx="4" fill="#0284C7"/>
    <text x="16" y="30" fill="#FFFFFF" font-size="11" font-weight="bold">AI</text>
    <text x="48" y="24" fill="#0F172A" font-size="10.5" font-weight="700">Google Gemini</text>
    <text x="48" y="37" fill="#0369A1" font-size="9">Gemini 2.5 Flash</text>
    <line x1="10" y1="48" x2="140" y2="48" stroke="#E2E8F0" stroke-width="1"/>
    <text x="10" y="63" fill="#475569" font-size="8.5">Vision OCR &amp; Translation</text>
    <text x="10" y="77" fill="#64748B" font-size="8">High-concurrency API fallback</text>
  </g>

  <!-- ==================== AWS CLOUD CONTAINER (MAIN) ==================== -->
  <rect x="230" y="65" width="1335" height="960" rx="8" fill="#FFFFFF" stroke="#232F3E" stroke-width="1.8"/>

  <!-- AWS Cloud Badge (Official Top-Left) -->
  <g transform="translate(245, 75)">
    <rect x="0" y="0" width="130" height="28" rx="4" fill="#232F3E"/>
    <image href="{icons['aws_badge']}" x="6" y="3" width="22" height="22"/>
    <text x="34" y="19" fill="#FF9900" font-size="12" font-weight="700">AWS Cloud</text>
  </g>
  <text x="390" y="94" fill="#475569" font-size="11" font-weight="600">Region: ap-southeast-1 (Singapore)  |  Default VPC CIDR: 10.0.0.0/16  |  Account ID: 677994024390</text>

  <!-- ==================== AMAZON VPC CONTAINER ==================== -->
  <rect x="250" y="115" width="750" height="645" rx="6" fill="#FAF5FF" stroke="#8C4FFF" stroke-width="1.5"/>
  
  <!-- VPC Header Badge -->
  <g transform="translate(265, 126)">
    <image href="{icons['vpc']}" x="0" y="0" width="20" height="20"/>
    <text x="26" y="15" fill="#6B21A8" font-size="12" font-weight="700">Amazon VPC: huylam-vpc</text>
    <text x="215" y="15" fill="#8C4FFF" font-size="11" font-weight="600">(10.0.0.0/16  |  vpc-0125f4d6db3fbffa6)</text>
  </g>

  <!-- ==================== PUBLIC SUBNET (MULTI-AZ) ==================== -->
  <rect x="265" y="155" width="300" height="585" rx="6" fill="#F7FBF0" stroke="#7AA116" stroke-width="1.5"/>
  <g transform="translate(280, 168)">
    <rect x="0" y="0" width="16" height="16" rx="2" fill="#7AA116"/>
    <path d="M 4 8 L 4 5 A 4 4 0 0 1 12 5 L 12 8" fill="none" stroke="#FFFFFF" stroke-width="1.5"/>
    <text x="22" y="13" fill="#365314" font-size="11" font-weight="700">Public Subnet (Multi-AZ)</text>
    <text x="0" y="28" fill="#4D7C0F" font-size="9">ap-southeast-1a (10.0.0.0/20) &amp; 1b (10.0.16.0/20)</text>
    <text x="0" y="40" fill="#64748B" font-size="8">subnet-0efa7c3a5818035dc &amp; subnet-0e07eb2fd44d1ac91</text>
  </g>

  <!-- Internet Gateway (IGW) Icon + Label -->
  <g transform="translate(390, 215)">
    <image href="{icons['igw']}" x="0" y="0" width="52" height="52"/>
    <text x="26" y="66" fill="#0F172A" font-size="11" font-weight="700" text-anchor="middle">Internet Gateway</text>
    <text x="26" y="79" fill="#475569" font-size="9.5" text-anchor="middle">huylam-igw</text>
    <text x="26" y="91" fill="#64748B" font-size="8.5" text-anchor="middle">igw-0b9db3a6eac29ede9</text>
  </g>

  <!-- Application Load Balancer (ALB) Icon + Label -->
  <g transform="translate(390, 345)">
    <image href="{icons['alb']}" x="0" y="0" width="52" height="52"/>
    <text x="26" y="66" fill="#0F172A" font-size="11.5" font-weight="700" text-anchor="middle">Application Load Balancer</text>
    <text x="26" y="80" fill="#2563EB" font-size="10" font-weight="600" text-anchor="middle">huylam-ocr-alb</text>
    <text x="26" y="93" fill="#475569" font-size="9" text-anchor="middle">Listener: HTTP / Port 80</text>
    <text x="26" y="105" fill="#64748B" font-size="8.5" text-anchor="middle">SG: huylam-alb-sg</text>
  </g>

  <!-- Target Group Box -->
  <g transform="translate(285, 515)">
    <rect x="0" y="0" width="260" height="85" rx="6" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.2" filter="url(#box-shadow)"/>
    <rect x="10" y="10" width="24" height="24" rx="3" fill="#16A34A"/>
    <text x="14" y="26" fill="#FFFFFF" font-size="10" font-weight="700">TG</text>
    <text x="42" y="22" fill="#14532D" font-size="11" font-weight="700">Target Group: huylam-ocr-tg</text>
    <text x="42" y="36" fill="#475569" font-size="9.5">Protocol: HTTP  |  Target Port: 5000</text>
    <text x="10" y="55" fill="#475569" font-size="9">Health Check: /login (HTTP 200 OK)</text>
    <rect x="10" y="63" width="95" height="16" rx="3" fill="#ECFDF5"/>
    <text x="57" y="75" fill="#059669" font-size="9" font-weight="700" text-anchor="middle">Healthy 1/1 (Active)</text>
  </g>

  <!-- ==================== PRIVATE SUBNET (APPLICATION TIER) ==================== -->
  <rect x="585" y="155" width="400" height="585" rx="6" fill="#F0F9FF" stroke="#0284C7" stroke-width="1.5"/>
  <g transform="translate(600, 168)">
    <rect x="0" y="0" width="16" height="16" rx="2" fill="#0284C7"/>
    <path d="M 4 8 L 4 5 A 4 4 0 0 1 12 5 L 12 8" fill="none" stroke="#FFFFFF" stroke-width="1.5"/>
    <text x="22" y="13" fill="#075985" font-size="11" font-weight="700">Private Subnet (Application Tier)</text>
    <text x="0" y="28" fill="#0369A1" font-size="9">ap-southeast-1a (10.0.128.0/20) &amp; 1b (10.0.144.0/20)</text>
    <text x="0" y="40" fill="#64748B" font-size="8">subnet-08563e499271091ab &amp; subnet-07e20dc44c40fac46</text>
  </g>

  <!-- Amazon EC2 Instance Container -->
  <g transform="translate(605, 205)">
    <rect x="0" y="0" width="360" height="515" rx="6" fill="#FFFFFF" stroke="#EA580C" stroke-width="1.5" filter="url(#box-shadow)"/>
    
    <!-- EC2 Icon + Label Header -->
    <image href="{icons['ec2']}" x="15" y="12" width="50" height="50"/>
    <text x="75" y="32" fill="#0F172A" font-size="12" font-weight="700">Amazon EC2 (Web Studio Host)</text>
    <text x="75" y="46" fill="#C2410C" font-size="10.5" font-weight="600">huylam-ocr-web-server (10.0.8.15)</text>
    <text x="75" y="59" fill="#475569" font-size="9.5">i-0566e1eedaacea52d  |  t3.micro  |  Amazon Linux 2023</text>
    <line x1="12" y1="72" x2="348" y2="72" stroke="#FED7AA" stroke-width="1"/>

    <!-- Security Group Tag -->
    <rect x="15" y="80" width="330" height="24" rx="4" fill="#FEF3C7" stroke="#FDE68A"/>
    <text x="25" y="96" fill="#92400E" font-size="9" font-weight="600">Chained SG: huylam-web-sg (Inbound TCP 5000 from ALB-SG ONLY)</text>

    <!-- Sub-Component 1: Gunicorn WSGI + FastAPI -->
    <g transform="translate(15, 115)">
      <rect x="0" y="0" width="330" height="65" rx="4" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="12" y="20" fill="#0F172A" font-size="10.5" font-weight="700">Web Studio Frontend &amp; API Service</text>
      <text x="12" y="35" fill="#475569" font-size="9.5">Gunicorn WSGI + FastAPI daemon (Port 5000)</text>
      <text x="12" y="49" fill="#64748B" font-size="9">Systemd service: huylam-ocr.service (Active running)</text>
      <text x="12" y="60" fill="#15803D" font-size="8.5" font-weight="600">Zero-Crash Process Supervision</text>
    </g>

    <!-- Sub-Component 2: Tier 1 Fast-Path Native Parser -->
    <g transform="translate(15, 190)">
      <rect x="0" y="0" width="330" height="85" rx="4" fill="#F0FDF4" stroke="#BBF7D0"/>
      <text x="12" y="19" fill="#166534" font-size="10.5" font-weight="700">Tier 1: Fast-Path Native Parser (PyMuPDF)</text>
      <text x="12" y="34" fill="#15803D" font-size="9.5">Direct vector &amp; text extraction (0.1s - 0.3s/page)</text>
      <text x="12" y="48" fill="#15803D" font-size="9.5">Cost: $0.00  |  Handles 80%+ digital PDF documents</text>
      <text x="12" y="63" fill="#166534" font-size="9">100% table layout and heading hierarchy preservation</text>
      <text x="12" y="76" fill="#475569" font-size="8.5">Zero GPU / CPU overhead on local EC2 t3.micro</text>
    </g>

    <!-- Sub-Component 3: Tier 2 Selective OCR & Translation Dispatcher -->
    <g transform="translate(15, 285)">
      <rect x="0" y="0" width="330" height="85" rx="4" fill="#FFF7ED" stroke="#FED7AA"/>
      <text x="12" y="19" fill="#9A3412" font-size="10.5" font-weight="700">Tier 2: Selective Vision OCR Dispatcher</text>
      <text x="12" y="34" fill="#C2410C" font-size="9.5">Triggered selectively for scanned pages &amp; forms</text>
      <text x="12" y="48" fill="#C2410C" font-size="9.5">LLM Document Translator (Technical EN -&gt; VI)</text>
      <text x="12" y="63" fill="#9A3412" font-size="9">Context-aware terminology translation engine</text>
      <text x="12" y="76" fill="#475569" font-size="8.5">Dispatches heavy compute to external Kaggle GPU cluster</text>
    </g>

    <!-- Sub-Component 4: Multi-Format Exporters -->
    <g transform="translate(15, 380)">
      <rect x="0" y="0" width="330" height="75" rx="4" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="12" y="20" fill="#0F172A" font-size="10.5" font-weight="700">Multi-Format Document Exporters</text>
      <text x="12" y="36" fill="#475569" font-size="9.5">DocxExporter: Native Word (.docx) with tables</text>
      <text x="12" y="50" fill="#64748B" font-size="9">Outputs: Markdown (.md), Microsoft Word, PDF</text>
      <text x="12" y="64" fill="#15803D" font-size="8.5" font-weight="600">Preserves document formatting &amp; formulas</text>
    </g>

    <!-- Sub-Component 5: CloudWatch & SSM Agents -->
    <g transform="translate(15, 465)">
      <rect x="0" y="0" width="330" height="40" rx="4" fill="#F1F5F9" stroke="#CBD5E1"/>
      <text x="12" y="18" fill="#334155" font-size="9.5" font-weight="600">System Daemons: amazon-ssm-agent &amp; amazon-cloudwatch-agent</text>
      <text x="12" y="32" fill="#64748B" font-size="8.5">Port-free remote administration &amp; automated log forwarding</text>
    </g>
  </g>

  <!-- ==================== SERVERLESS & STORAGE TIER (RIGHT) ==================== -->
  <rect x="1025" y="115" width="515" height="645" rx="6" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.5" stroke-dasharray="4,4"/>
  <text x="1040" y="138" fill="#334155" font-size="12" font-weight="700">Serverless Processing &amp; Managed Storage Tier</text>

  <!-- Amazon S3 Container -->
  <g transform="translate(1045, 155)">
    <rect x="0" y="0" width="475" height="135" rx="6" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.5" filter="url(#box-shadow)"/>
    <image href="{icons['s3']}" x="15" y="15" width="52" height="52"/>
    <text x="78" y="32" fill="#0F172A" font-size="12" font-weight="700">Amazon Simple Storage Service (S3)</text>
    <text x="78" y="47" fill="#15803D" font-size="10.5" font-weight="600">huylam-ocr-documents-ap-southeast-1</text>
    <line x1="78" y1="56" x2="460" y2="56" stroke="#BBF7D0" stroke-width="1"/>
    
    <text x="78" y="73" fill="#166534" font-size="10" font-weight="600">uploads/ :</text>
    <text x="135" y="73" fill="#475569" font-size="9.5">Raw user documents &amp; scan files (CORS direct upload)</text>
    
    <text x="78" y="92" fill="#166534" font-size="10" font-weight="600">outputs/ :</text>
    <text x="135" y="92" fill="#475569" font-size="9.5">Processed Markdown, translated Word (.docx), PDF</text>
    
    <text x="78" y="110" fill="#64748B" font-size="9">Security: SSE-S3 AES-256 Server-Side Encryption  |  TLS 1.3 In-Transit</text>
    <text x="78" y="124" fill="#64748B" font-size="8.5">Lifecycle: S3 Standard with automated cleanup rules</text>
  </g>

  <!-- AWS Lambda Container -->
  <g transform="translate(1045, 310)">
    <rect x="0" y="0" width="475" height="130" rx="6" fill="#FFFFFF" stroke="#EA580C" stroke-width="1.5" filter="url(#box-shadow)"/>
    <image href="{icons['lambda']}" x="15" y="15" width="52" height="52"/>
    <text x="78" y="32" fill="#0F172A" font-size="12" font-weight="700">AWS Lambda (Serverless Event Processor)</text>
    <text x="78" y="47" fill="#C2410C" font-size="10.5" font-weight="600">huylam-ocr-processor (Python 3.11)</text>
    <line x1="78" y1="56" x2="460" y2="56" stroke="#FED7AA" stroke-width="1"/>
    
    <text x="78" y="73" fill="#9A3412" font-size="10" font-weight="600">Event Trigger:</text>
    <text x="155" y="73" fill="#475569" font-size="9.5">s3:ObjectCreated:* on uploads/ prefix</text>
    
    <text x="78" y="92" fill="#9A3412" font-size="10" font-weight="600">Execution:</text>
    <text x="155" y="92" fill="#475569" font-size="9.5">Latency: ~214ms  |  Memory: 88MB  |  FinOps: $0.00</text>
    
    <text x="78" y="108" fill="#475569" font-size="9">Role: huylam-ocr-lambda-role (S3 ReadWrite + DynamoDB PutItem)</text>
    <text x="78" y="122" fill="#64748B" font-size="8.5">Event-driven compute: zero idle cost, scales to zero automatically</text>
  </g>

  <!-- Amazon DynamoDB Container -->
  <g transform="translate(1045, 460)">
    <rect x="0" y="0" width="475" height="130" rx="6" fill="#FFFFFF" stroke="#2563EB" stroke-width="1.5" filter="url(#box-shadow)"/>
    <image href="{icons['ddb']}" x="15" y="15" width="52" height="52"/>
    <text x="78" y="32" fill="#0F172A" font-size="12" font-weight="700">Amazon DynamoDB (NoSQL Database)</text>
    <text x="78" y="47" fill="#1D4ED8" font-size="10.5" font-weight="600">document_processing_jobs</text>
    <line x1="78" y1="56" x2="460" y2="56" stroke="#BFDBFE" stroke-width="1"/>
    
    <text x="78" y="73" fill="#1E40AF" font-size="10" font-weight="600">Schema:</text>
    <text x="135" y="73" fill="#475569" font-size="9.5">PK: job_id (String)  |  SK: created_at (ISO 8601)</text>
    
    <text x="78" y="92" fill="#1E40AF" font-size="10" font-weight="600">Billing Mode:</text>
    <text x="155" y="92" fill="#475569" font-size="9.5">PAY_PER_REQUEST (On-Demand Mode, Scale-to-Zero)</text>
    
    <text x="78" y="108" fill="#475569" font-size="9">Stores: Job metadata, processing stages, latency records, download URLs</text>
    <text x="78" y="122" fill="#64748B" font-size="8.5">Single-digit millisecond latency access from EC2 and Lambda</text>
  </g>

  <!-- Amazon Bedrock Container (Optional / Native Multimodal) -->
  <g transform="translate(1045, 610)">
    <rect x="0" y="0" width="475" height="120" rx="6" fill="#FFFFFF" stroke="#0D9488" stroke-width="1.2" filter="url(#box-shadow)"/>
    <image href="{icons['bedrock']}" x="15" y="15" width="48" height="48"/>
    <text x="78" y="30" fill="#0F172A" font-size="11.5" font-weight="700">Amazon Bedrock (Native Cloud Multimodal AI)</text>
    <text x="78" y="45" fill="#0F766E" font-size="10" font-weight="600">Bedrock Converse API  |  Claude 3.5 Sonnet &amp; Nova Micro</text>
    <line x1="78" y1="54" x2="460" y2="54" stroke="#99F6E4" stroke-width="1"/>
    <text x="78" y="72" fill="#475569" font-size="9">Zero Data Retention  |  Enterprise HIPAA-Ready &amp; Compliance-Grade</text>
    <text x="78" y="88" fill="#64748B" font-size="8.5">Secondary high-security native cloud fallback engine for document understanding</text>
    <text x="78" y="104" fill="#0F766E" font-size="8.5" font-weight="600">FinOps Mode: Secondary Optional (Zero baseline cost when inactive)</text>
  </g>

  <!-- ==================== MANAGEMENT, SECURITY & OBSERVABILITY TIER (BOTTOM) ==================== -->
  <rect x="250" y="780" width="1290" height="225" rx="6" fill="#F8FAFC" stroke="#475569" stroke-width="1.5"/>
  <text x="270" y="802" fill="#1E293B" font-size="12" font-weight="700">Management, Security &amp; Observability Tier (AWS Well-Architected Operational Excellence)</text>

  <!-- Service 1: Amazon Cognito -->
  <g transform="translate(270, 815)">
    <rect x="0" y="0" width="235" height="175" rx="6" fill="#FFFFFF" stroke="#C026D3" stroke-width="1.2" filter="url(#box-shadow)"/>
    <image href="{icons.get('cognito', icons['ssm'])}" x="15" y="12" width="44" height="44"/>
    <text x="68" y="30" fill="#0F172A" font-size="11.5" font-weight="700">Amazon Cognito</text>
    <text x="68" y="44" fill="#9333EA" font-size="9.5" font-weight="600">User Identity &amp; Auth</text>
    <line x1="12" y1="62" x2="223" y2="62" stroke="#F3E8FF" stroke-width="1"/>
    <text x="12" y="80" fill="#334155" font-size="9" font-weight="600">User Pool: User pool - qp0rmn</text>
    <text x="12" y="95" fill="#475569" font-size="8.5">ID: ap-southeast-1_dNJkc4IWG</text>
    <text x="12" y="112" fill="#334155" font-size="9" font-weight="600">Federated Identity:</text>
    <text x="12" y="127" fill="#475569" font-size="8.5">Google Console OAuth 2.0 Client</text>
    <text x="12" y="145" fill="#15803D" font-size="8.5" font-weight="600">Live Login Screen Integration</text>
    <text x="12" y="160" fill="#64748B" font-size="8">Managed hosted UI &amp; JWT Tokens</text>
  </g>

  <!-- Service 2: AWS Systems Manager -->
  <g transform="translate(525, 815)">
    <rect x="0" y="0" width="235" height="175" rx="6" fill="#FFFFFF" stroke="#9333EA" stroke-width="1.2" filter="url(#box-shadow)"/>
    <image href="{icons['ssm']}" x="15" y="12" width="44" height="44"/>
    <text x="68" y="30" fill="#0F172A" font-size="11.5" font-weight="700">AWS Systems Manager</text>
    <text x="68" y="44" fill="#7E22CE" font-size="9.5" font-weight="600">Operational Management</text>
    <line x1="12" y1="62" x2="223" y2="62" stroke="#F3E8FF" stroke-width="1"/>
    <text x="12" y="80" fill="#334155" font-size="9" font-weight="600">SSM Parameter Store:</text>
    <text x="12" y="95" fill="#475569" font-size="8.5">/huylam-ocr/config (SecureString)</text>
    <text x="12" y="112" fill="#334155" font-size="9" font-weight="600">Session Manager:</text>
    <text x="12" y="127" fill="#475569" font-size="8.5">Port-Free Zero-SSH EC2 Access</text>
    <text x="12" y="145" fill="#15803D" font-size="8.5" font-weight="600">100% Zero Hardcoded Keys</text>
    <text x="12" y="160" fill="#64748B" font-size="8">KMS-encrypted parameters storage</text>
  </g>

  <!-- Service 3: Amazon CloudWatch -->
  <g transform="translate(780, 815)">
    <rect x="0" y="0" width="245" height="175" rx="6" fill="#FFFFFF" stroke="#E11D48" stroke-width="1.2" filter="url(#box-shadow)"/>
    <image href="{icons['cw']}" x="15" y="12" width="44" height="44"/>
    <text x="68" y="30" fill="#0F172A" font-size="11.5" font-weight="700">Amazon CloudWatch</text>
    <text x="68" y="44" fill="#BE123C" font-size="9.5" font-weight="600">Observability &amp; Metrics</text>
    <line x1="12" y1="62" x2="233" y2="62" stroke="#FFE4E6" stroke-width="1"/>
    <text x="12" y="80" fill="#334155" font-size="9" font-weight="600">Log Groups:</text>
    <text x="12" y="95" fill="#475569" font-size="8.5">/aws/lambda/huylam-ocr-processor</text>
    <text x="12" y="108" fill="#475569" font-size="8.5">/aws/vpc/flowlogs  |  syslog</text>
    <text x="12" y="126" fill="#334155" font-size="9" font-weight="600">Metrics &amp; Static Alarms:</text>
    <text x="12" y="141" fill="#475569" font-size="8.5">CPUUtilization > 70% (1 min)</text>
    <text x="12" y="158" fill="#E11D48" font-size="8.5" font-weight="600">Auto-triggers SNS Alerting</text>
  </g>

  <!-- Service 4: Amazon SNS -->
  <g transform="translate(1045, 815)">
    <rect x="0" y="0" width="235" height="175" rx="6" fill="#FFFFFF" stroke="#E11D48" stroke-width="1.2" filter="url(#box-shadow)"/>
    <image href="{icons.get('sns', icons['cw'])}" x="15" y="12" width="44" height="44"/>
    <text x="68" y="30" fill="#0F172A" font-size="11.5" font-weight="700">Amazon SNS</text>
    <text x="68" y="44" fill="#BE123C" font-size="9.5" font-weight="600">Notification Service</text>
    <line x1="12" y1="62" x2="223" y2="62" stroke="#FFE4E6" stroke-width="1"/>
    <text x="12" y="80" fill="#334155" font-size="9" font-weight="600">Topic: huylam-ocr-alerts</text>
    <text x="12" y="98" fill="#334155" font-size="9" font-weight="600">Subscription Protocol:</text>
    <text x="12" y="113" fill="#475569" font-size="8.5">Email Notifications</text>
    <text x="12" y="132" fill="#334155" font-size="9" font-weight="600">Action Target:</text>
    <text x="12" y="147" fill="#475569" font-size="8.5">Real-time administrator email alert</text>
    <text x="12" y="160" fill="#64748B" font-size="8">Triggered on fatal errors &amp; spikes</text>
  </g>

  <!-- Service 5: AWS IAM Roles -->
  <g transform="translate(1300, 815)">
    <rect x="0" y="0" width="225" height="175" rx="6" fill="#FFFFFF" stroke="#D97706" stroke-width="1.2" filter="url(#box-shadow)"/>
    <image href="{icons.get('iam', icons['ec2'])}" x="15" y="12" width="44" height="44"/>
    <text x="68" y="30" fill="#0F172A" font-size="11.5" font-weight="700">AWS IAM</text>
    <text x="68" y="44" fill="#B45309" font-size="9.5" font-weight="600">Security &amp; Roles</text>
    <line x1="12" y1="62" x2="213" y2="62" stroke="#FEF3C7" stroke-width="1"/>
    <text x="12" y="80" fill="#334155" font-size="9" font-weight="600">huylam-ssm-role (EC2):</text>
    <text x="12" y="95" fill="#475569" font-size="8.5">SSMManagedInstanceCore</text>
    <text x="12" y="108" fill="#475569" font-size="8.5">+ Inline S3/DynamoDB/SSM</text>
    <text x="12" y="128" fill="#334155" font-size="9" font-weight="600">huylam-ocr-lambda-role:</text>
    <text x="12" y="143" fill="#475569" font-size="8.5">AWSLambdaBasicExecution</text>
    <text x="12" y="158" fill="#15803D" font-size="8.5" font-weight="600">Principle of Least Privilege</text>
  </g>

  <!-- FinOps Summary Banner (Bottom of AWS Cloud) -->
  <g transform="translate(250, 1010)">
    <rect x="0" y="0" width="1290" height="28" rx="4" fill="#F0FDF4" stroke="#BBF7D0"/>
    <text x="645" y="19" fill="#166534" font-size="10.5" font-weight="700" text-anchor="middle">FinOps Cloud Financial Discipline (Zero-Breach): Cumulative Production Spend = $0.00 USD  |  AWS Free Tier + External Kaggle GPU Cluster</text>
  </g>

  <!-- ==================== CLEAN ORTHOGONAL CONNECTOR ARROWS ==================== -->

  <!-- C1: End Users -> Internet (Straight Down) -->
  <path d="M 120 160 L 120 220" fill="none" stroke="#2563EB" stroke-width="2" marker-end="url(#arr-blue)"/>
  <text x="126" y="190" fill="#1D4ED8" font-size="9" font-weight="600">HTTPS</text>

  <!-- C2: Internet -> Internet Gateway (Clean Horizontal Entry) -->
  <path d="M 178 240 L 390 240" fill="none" stroke="#232F3E" stroke-width="2" marker-end="url(#arr-black)"/>
  <text x="235" y="232" fill="#0F172A" font-size="9.5" font-weight="700">HTTP : 80 / Public Traffic</text>

  <!-- C3: Internet Gateway -> ALB (Straight Down) -->
  <path d="M 416 267 L 416 345" fill="none" stroke="#8C4FFF" stroke-width="2" marker-end="url(#arr-purple)"/>
  <text x="424" y="305" fill="#6B21A8" font-size="9.5" font-weight="600">Route: 0.0.0.0/0</text>

  <!-- C4: ALB -> Target Group (Straight Down) -->
  <path d="M 416 445 L 416 515" fill="none" stroke="#16A34A" stroke-width="1.8" stroke-dasharray="3,3" marker-end="url(#arr-green)"/>
  <text x="424" y="480" fill="#15803D" font-size="9" font-weight="600">HTTP / Port 5000</text>

  <!-- C5: Target Group -> EC2 Instance (Horizontal Forwarding) -->
  <path d="M 545 555 L 605 555" fill="none" stroke="#16A34A" stroke-width="2.2" marker-end="url(#arr-green)"/>
  <text x="550" y="547" fill="#15803D" font-size="9.5" font-weight="700">Forward TCP 5000</text>

  <!-- C6: EC2 -> S3 (Uploads raw documents) -->
  <path d="M 965 230 L 1045 230" fill="none" stroke="#16A34A" stroke-width="2" marker-end="url(#arr-green)"/>
  <text x="972" y="222" fill="#15803D" font-size="9.5" font-weight="700">Boto3: uploads/</text>

  <!-- C7: S3 -> Lambda (ObjectCreated Trigger) -->
  <path d="M 1282 290 L 1282 310" fill="none" stroke="#EA580C" stroke-width="2.5" marker-end="url(#arr-orange)"/>
  <text x="1290" y="303" fill="#C2410C" font-size="9.5" font-weight="700">s3:ObjectCreated:*</text>

  <!-- C8: Lambda <-> DynamoDB (Job State & Metadata) -->
  <path d="M 1282 440 L 1282 460" fill="none" stroke="#2563EB" stroke-width="2.2" marker-end="url(#arr-blue)"/>
  <text x="1290" y="453" fill="#1D4ED8" font-size="9.5" font-weight="700">PutItem / State</text>

  <!-- C9: EC2 <-> DynamoDB (Sync Job Status) -->
  <path d="M 965 525 L 1045 525" fill="none" stroke="#2563EB" stroke-width="1.8" stroke-dasharray="4,4" marker-end="url(#arr-blue)"/>
  <text x="972" y="517" fill="#1D4ED8" font-size="9.5" font-weight="700">Job Sync / Poll</text>

  <!-- C10: EC2 -> S3 (Save Exported Outputs) -->
  <path d="M 965 255 L 1045 255" fill="none" stroke="#16A34A" stroke-width="1.5" stroke-dasharray="3,3" marker-end="url(#arr-green)"/>
  <text x="972" y="270" fill="#15803D" font-size="8.5">outputs/ (.md, .docx, .pdf)</text>

  <!-- C11: EC2 <-> Kaggle GPU (Cloudflare Tunnel: Scanned Page Fallback) -->
  <path d="M 605 450 L 210 450 L 210 590 L 198 590" fill="none" stroke="#0284C7" stroke-width="1.8" stroke-dasharray="4,4" marker-end="url(#arr-blue)"/>
  <text x="215" y="468" fill="#0369A1" font-size="9" font-weight="600">Cloudflare Tunnel (Qwen-2.5-VL OCR)</text>

  <!-- C12: DevOps -> GitHub -->
  <path d="M 120 336 L 120 395" fill="none" stroke="#334155" stroke-width="1.5" marker-end="url(#arr-black)"/>
  <text x="126" y="365" fill="#334155" font-size="9">git push</text>

  <!-- C13: GitHub -> SSM Run / deploy.sh -->
  <path d="M 122 455 L 122 475 L 642 475 L 642 815" fill="none" stroke="#7E22CE" stroke-width="1.5" stroke-dasharray="4,4" marker-end="url(#arr-purple)"/>
  <text x="220" y="470" fill="#7E22CE" font-size="9" font-weight="600">CI/CD deploy.sh via SSM RunCommand</text>

  <!-- C14: CloudWatch -> SNS Notification -->
  <path d="M 1025 900 L 1045 900" fill="none" stroke="#E11D48" stroke-width="2" marker-end="url(#arr-magenta)"/>
  <text x="1027" y="893" fill="#BE123C" font-size="8.5" font-weight="600">Alarm</text>

  <!-- C15: Cognito -> ALB / SPA Authentication -->
  <path d="M 387 815 L 387 680 L 330 680 L 330 600" fill="none" stroke="#C026D3" stroke-width="1.5" stroke-dasharray="4,4" marker-end="url(#arr-purple)"/>
  <text x="338" y="674" fill="#9333EA" font-size="8.5" font-weight="600">Google OAuth 2.0 Auth</text>
</svg>"""
    return svg

def generate_drawio():
    xml = """<mxfile host="app.diagrams.net" modified="2026-10-04T07:15:00.000Z" agent="Antigravity" version="24.0.0" type="device">
  <diagram id="aws-official-reference-architecture" name="AWS Reference Architecture Official">
    <mxGraphModel dx="1600" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1654" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- Title -->
        <mxCell id="title" value="&lt;b style=&quot;font-size: 16px;&quot;&gt;SERVERLESS HYBRID DOCUMENT OCR, PARSING &amp;amp; TECHNICAL TRANSLATION PLATFORM&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#475569&quot; style=&quot;font-size: 12px;&quot;&gt;AWS Reference Architecture | Region: ap-southeast-1 (Singapore) | Account ID: 677994024390&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="40" y="20" width="1400" height="40" as="geometry" />
        </mxCell>

        <!-- AWS Cloud Group -->
        <mxCell id="aws_cloud" value="AWS Cloud (Region: ap-southeast-1 | Account: 677994024390)" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=1;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.groupCenter;grIcon=mxgraph.aws4.group_aws_cloud;strokeColor=#232F3E;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#232F3E;" vertex="1" parent="1">
          <mxGeometry x="230" y="70" width="1335" height="960" as="geometry" />
        </mxCell>

        <!-- VPC Container -->
        <mxCell id="vpc" value="Amazon VPC: huylam-vpc (10.0.0.0/16 | vpc-0125f4d6db3fbffa6)" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=1;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.groupCenter;grIcon=mxgraph.aws4.group_vpc;strokeColor=#8C4FFF;strokeWidth=2;fillColor=#FAF5FF;verticalAlign=top;align=left;spacingLeft=30;fontColor=#8C4FFF;" vertex="1" parent="aws_cloud">
          <mxGeometry x="20" y="45" width="750" height="645" as="geometry" />
        </mxCell>

        <!-- Public Subnet -->
        <mxCell id="sub_pub" value="Public Subnet (Multi-AZ: 10.0.0.0/20 &amp;amp; 10.0.16.0/20)" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=11;fontStyle=1;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.groupCenter;grIcon=mxgraph.aws4.group_public_subnet;strokeColor=#7AA116;strokeWidth=1.5;fillColor=#F7FBF0;verticalAlign=top;align=left;spacingLeft=30;fontColor=#7AA116;" vertex="1" parent="vpc">
          <mxGeometry x="15" y="40" width="300" height="585" as="geometry" />
        </mxCell>

        <!-- Internet Gateway Icon -->
        <mxCell id="igw" value="" style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws4.internet_gateway;fillColor=#8C4FFF;gradientColor=none;" vertex="1" parent="sub_pub">
          <mxGeometry x="124" y="60" width="52" height="52" as="geometry" />
        </mxCell>
        <mxCell id="igw_lbl" value="&lt;b&gt;Internet Gateway&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#475569&quot; style=&quot;font-size: 10px;&quot;&gt;huylam-igw (igw-0b9db3a6eac29ede9)&lt;br&gt;Route: 0.0.0.0/0 -&amp;gt; igw&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=top;whiteSpace=wrap;rounded=0;" vertex="1" parent="sub_pub">
          <mxGeometry x="40" y="115" width="220" height="40" as="geometry" />
        </mxCell>

        <!-- Application Load Balancer Icon -->
        <mxCell id="alb" value="" style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws4.application_load_balancer;fillColor=#8C4FFF;gradientColor=none;" vertex="1" parent="sub_pub">
          <mxGeometry x="124" y="190" width="52" height="52" as="geometry" />
        </mxCell>
        <mxCell id="alb_lbl" value="&lt;b&gt;Application Load Balancer&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#2563eb&quot; style=&quot;font-size: 10px;&quot;&gt;&lt;b&gt;huylam-ocr-alb&lt;/b&gt;&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#475569&quot; style=&quot;font-size: 9.5px;&quot;&gt;Listener: HTTP:80 | SG: huylam-alb-sg&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=top;whiteSpace=wrap;rounded=0;" vertex="1" parent="sub_pub">
          <mxGeometry x="30" y="245" width="240" height="45" as="geometry" />
        </mxCell>

        <!-- Target Group -->
        <mxCell id="tg" value="&lt;b&gt;Target Group: huylam-ocr-tg&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#475569&quot; style=&quot;font-size: 9.5px;&quot;&gt;Port: 5000 | Health: /login (200 OK)&lt;br&gt;&lt;font color=&quot;#059669&quot;&gt;&lt;b&gt;Healthy 1/1 (Active Live)&lt;/b&gt;&lt;/font&gt;&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;strokeColor=#16a34a;strokeWidth=1.5;fillColor=#ffffff;fontColor=#166534;fontSize=10;" vertex="1" parent="sub_pub">
          <mxGeometry x="20" y="360" width="260" height="85" as="geometry" />
        </mxCell>

        <!-- Private Subnet -->
        <mxCell id="sub_priv" value="Private Subnet (Application Tier: 10.0.128.0/20 &amp;amp; 10.0.144.0/20)" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=11;fontStyle=1;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.groupCenter;grIcon=mxgraph.aws4.group_private_subnet;strokeColor=#0284C7;strokeWidth=1.5;fillColor=#F0F9FF;verticalAlign=top;align=left;spacingLeft=30;fontColor=#0284C7;" vertex="1" parent="vpc">
          <mxGeometry x="335" y="40" width="400" height="585" as="geometry" />
        </mxCell>

        <!-- EC2 Container -->
        <mxCell id="ec2_box" value="" style="rounded=1;whiteSpace=wrap;html=1;strokeColor=#EA580C;strokeWidth=1.5;fillColor=#ffffff;" vertex="1" parent="sub_priv">
          <mxGeometry x="20" y="50" width="360" height="515" as="geometry" />
        </mxCell>

        <!-- EC2 Icon -->
        <mxCell id="ec2" value="" style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws4.ec2;fillColor=#ED7100;gradientColor=none;" vertex="1" parent="ec2_box">
          <mxGeometry x="15" y="12" width="50" height="50" as="geometry" />
        </mxCell>
        <mxCell id="ec2_lbl" value="&lt;b&gt;Amazon EC2 (Web Studio Host)&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#c2410c&quot; style=&quot;font-size: 10px;&quot;&gt;&lt;b&gt;huylam-ocr-web-server (10.0.8.15)&lt;/b&gt;&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#475569&quot; style=&quot;font-size: 9px;&quot;&gt;t3.micro | i-0566e1eedaacea52d | AL2023&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=top;whiteSpace=wrap;rounded=0;" vertex="1" parent="ec2_box">
          <mxGeometry x="75" y="12" width="270" height="50" as="geometry" />
        </mxCell>

        <!-- Chained SG Tag -->
        <mxCell id="sg_tag" value="&lt;b&gt;Chained SG: huylam-web-sg&lt;/b&gt; (Inbound TCP 5000 from ALB-SG ONLY)" style="rounded=1;whiteSpace=wrap;html=1;strokeColor=#FDE68A;fillColor=#FEF3C7;fontColor=#92400E;fontSize=9.5;" vertex="1" parent="ec2_box">
          <mxGeometry x="15" y="80" width="330" height="24" as="geometry" />
        </mxCell>

        <!-- Sub components inside EC2 -->
        <mxCell id="ec2_c1" value="&lt;b&gt;Web Studio Frontend &amp;amp; API Service&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#475569&quot; style=&quot;font-size: 9px;&quot;&gt;Gunicorn WSGI + FastAPI daemon (Port 5000)&lt;br&gt;Systemd: huylam-ocr.service (Auto-restart)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;strokeColor=#E2E8F0;fillColor=#F8FAFC;fontSize=10;align=left;spacingLeft=10;" vertex="1" parent="ec2_box">
          <mxGeometry x="15" y="115" width="330" height="65" as="geometry" />
        </mxCell>

        <mxCell id="ec2_c2" value="&lt;b&gt;Tier 1: Fast-Path Native Parser (PyMuPDF)&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#15803D&quot; style=&quot;font-size: 9px;&quot;&gt;Direct text extraction (0.1s - 0.3s/page) | Cost: $0.00&lt;br&gt;100% table layout and heading hierarchy preservation&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;strokeColor=#BBF7D0;fillColor=#F0FDF4;fontSize=10;align=left;spacingLeft=10;" vertex="1" parent="ec2_box">
          <mxGeometry x="15" y="190" width="330" height="85" as="geometry" />
        </mxCell>

        <mxCell id="ec2_c3" value="&lt;b&gt;Tier 2: Selective Vision OCR Dispatcher&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#C2410C&quot; style=&quot;font-size: 9px;&quot;&gt;Dispatches scanned pages to Kaggle GPU (Qwen-2.5-VL)&lt;br&gt;LLM Document Translator (Technical EN -&gt; VI)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;strokeColor=#FED7AA;fillColor=#FFF7ED;fontSize=10;align=left;spacingLeft=10;" vertex="1" parent="ec2_box">
          <mxGeometry x="15" y="285" width="330" height="85" as="geometry" />
        </mxCell>

        <mxCell id="ec2_c4" value="&lt;b&gt;Multi-Format Document Exporters&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#475569&quot; style=&quot;font-size: 9px;&quot;&gt;DocxExporter: Native Word (.docx) with tables&lt;br&gt;Outputs: Markdown (.md), Microsoft Word, PDF&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;strokeColor=#E2E8F0;fillColor=#F8FAFC;fontSize=10;align=left;spacingLeft=10;" vertex="1" parent="ec2_box">
          <mxGeometry x="15" y="380" width="330" height="75" as="geometry" />
        </mxCell>

        <!-- Right Side: Serverless & Managed Storage Tier -->
        <mxCell id="serverless_group" value="Serverless Processing &amp;amp; Managed Storage Tier" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=1;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;strokeColor=#94A3B8;strokeWidth=1.5;dashed=1;dashPattern=4 4;fillColor=none;verticalAlign=top;align=left;spacingLeft=15;fontColor=#334155;" vertex="1" parent="aws_cloud">
          <mxGeometry x="795" y="45" width="515" height="645" as="geometry" />
        </mxCell>

        <!-- S3 Container -->
        <mxCell id="s3_box" value="&lt;b&gt;Amazon Simple Storage Service (S3)&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#15803d&quot; style=&quot;font-size: 10px;&quot;&gt;&lt;b&gt;huylam-ocr-documents-ap-southeast-1&lt;/b&gt;&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#475569&quot; style=&quot;font-size: 9px;&quot;&gt;&amp;bull; &lt;b&gt;uploads/&lt;/b&gt;: Raw user documents &amp;amp; scan files (CORS direct)&lt;br&gt;&amp;bull; &lt;b&gt;outputs/&lt;/b&gt;: Processed Markdown, translated Word, PDF&lt;br&gt;Security: SSE-S3 AES-256 Server-Side Encryption | TLS 1.3&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;strokeColor=#16A34A;strokeWidth=1.5;fillColor=#ffffff;align=left;spacingLeft=70;verticalAlign=middle;" vertex="1" parent="serverless_group">
          <mxGeometry x="20" y="40" width="475" height="135" as="geometry" />
        </mxCell>
        <mxCell id="s3_icon" value="" style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws4.s3;fillColor=#7AA116;gradientColor=none;" vertex="1" parent="s3_box">
          <mxGeometry x="15" y="20" width="48" height="48" as="geometry" />
        </mxCell>

        <!-- Lambda Container -->
        <mxCell id="lambda_box" value="&lt;b&gt;AWS Lambda (Serverless Event Processor)&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#c2410c&quot; style=&quot;font-size: 10px;&quot;&gt;&lt;b&gt;huylam-ocr-processor (Python 3.11)&lt;/b&gt;&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#475569&quot; style=&quot;font-size: 9px;&quot;&gt;&amp;bull; &lt;b&gt;Event Trigger&lt;/b&gt;: s3:ObjectCreated:* on uploads/ prefix&lt;br&gt;&amp;bull; &lt;b&gt;Execution&lt;/b&gt;: Latency: ~214ms | Memory: 88MB | FinOps: $0.00&lt;br&gt;&amp;bull; &lt;b&gt;Role&lt;/b&gt;: huylam-ocr-lambda-role (S3 ReadWrite + DynamoDB)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;strokeColor=#EA580C;strokeWidth=1.5;fillColor=#ffffff;align=left;spacingLeft=70;verticalAlign=middle;" vertex="1" parent="serverless_group">
          <mxGeometry x="20" y="195" width="475" height="130" as="geometry" />
        </mxCell>
        <mxCell id="lambda_icon" value="" style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws4.lambda;fillColor=#ED7100;gradientColor=none;" vertex="1" parent="lambda_box">
          <mxGeometry x="15" y="20" width="48" height="48" as="geometry" />
        </mxCell>

        <!-- DynamoDB Container -->
        <mxCell id="ddb_box" value="&lt;b&gt;Amazon DynamoDB (NoSQL Database)&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#1d4ed8&quot; style=&quot;font-size: 10px;&quot;&gt;&lt;b&gt;document_processing_jobs&lt;/b&gt;&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#475569&quot; style=&quot;font-size: 9px;&quot;&gt;&amp;bull; &lt;b&gt;Schema&lt;/b&gt;: PK: job_id (String) | SK: created_at (ISO 8601)&lt;br&gt;&amp;bull; &lt;b&gt;Billing&lt;/b&gt;: PAY_PER_REQUEST (On-Demand Mode, Scale-to-Zero)&lt;br&gt;&amp;bull; &lt;b&gt;Stores&lt;/b&gt;: Job metadata, processing stages, latency, download URLs&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;strokeColor=#2563EB;strokeWidth=1.5;fillColor=#ffffff;align=left;spacingLeft=70;verticalAlign=middle;" vertex="1" parent="serverless_group">
          <mxGeometry x="20" y="345" width="475" height="130" as="geometry" />
        </mxCell>
        <mxCell id="ddb_icon" value="" style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws4.dynamodb;fillColor=#2E27AD;gradientColor=none;" vertex="1" parent="ddb_box">
          <mxGeometry x="15" y="20" width="48" height="48" as="geometry" />
        </mxCell>

        <!-- Bedrock Container -->
        <mxCell id="bedrock_box" value="&lt;b&gt;Amazon Bedrock (Native Cloud Multimodal AI)&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#0f766e&quot; style=&quot;font-size: 10px;&quot;&gt;&lt;b&gt;Bedrock Converse API | Claude 3.5 Sonnet &amp;amp; Nova Micro&lt;/b&gt;&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#475569&quot; style=&quot;font-size: 9px;&quot;&gt;Zero Data Retention | Enterprise HIPAA-Ready &amp;amp; Compliance-Grade&lt;br&gt;Secondary high-security native cloud fallback engine&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;strokeColor=#0D9488;strokeWidth=1.2;fillColor=#ffffff;align=left;spacingLeft=70;verticalAlign=middle;" vertex="1" parent="serverless_group">
          <mxGeometry x="20" y="495" width="475" height="120" as="geometry" />
        </mxCell>
        <mxCell id="bedrock_icon" value="" style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws4.bedrock;fillColor=#01A88D;gradientColor=none;" vertex="1" parent="bedrock_box">
          <mxGeometry x="15" y="20" width="48" height="48" as="geometry" />
        </mxCell>

        <!-- Bottom: Management, Security & Observability Tier -->
        <mxCell id="sec_group" value="Management, Security &amp;amp; Observability Tier (AWS Well-Architected Operational Excellence)" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=1;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;strokeColor=#475569;strokeWidth=1.5;fillColor=#F8FAFC;verticalAlign=top;align=left;spacingLeft=20;fontColor=#1E293B;" vertex="1" parent="aws_cloud">
          <mxGeometry x="20" y="710" width="1290" height="225" as="geometry" />
        </mxCell>

        <!-- Cognito -->
        <mxCell id="cog_box" value="&lt;b&gt;Amazon Cognito&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#9333ea&quot; style=&quot;font-size: 9.5px;&quot;&gt;User Identity &amp;amp; Auth&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#475569&quot; style=&quot;font-size: 8.5px;&quot;&gt;User Pool: qp0rmn&lt;br&gt;Google OAuth 2.0 Auth&lt;br&gt;Live Login Screen Integration&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;strokeColor=#C026D3;strokeWidth=1.2;fillColor=#ffffff;align=center;verticalAlign=bottom;spacingBottom=10;" vertex="1" parent="sec_group">
          <mxGeometry x="20" y="35" width="235" height="175" as="geometry" />
        </mxCell>
        <mxCell id="cog_icon" value="" style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws4.cognito;fillColor=#C925D1;gradientColor=none;" vertex="1" parent="cog_box">
          <mxGeometry x="95" y="15" width="44" height="44" as="geometry" />
        </mxCell>

        <!-- SSM -->
        <mxCell id="ssm_box" value="&lt;b&gt;AWS Systems Manager&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#7e22ce&quot; style=&quot;font-size: 9.5px;&quot;&gt;Operational Management&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#475569&quot; style=&quot;font-size: 8.5px;&quot;&gt;Parameter Store: /huylam-ocr/config&lt;br&gt;Session Manager: Zero-Port SSH&lt;br&gt;100% Zero Hardcoded Secrets&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;strokeColor=#9333EA;strokeWidth=1.2;fillColor=#ffffff;align=center;verticalAlign=bottom;spacingBottom=10;" vertex="1" parent="sec_group">
          <mxGeometry x="275" y="35" width="235" height="175" as="geometry" />
        </mxCell>
        <mxCell id="ssm_icon" value="" style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws4.systems_manager;fillColor=#C925D1;gradientColor=none;" vertex="1" parent="ssm_box">
          <mxGeometry x="95" y="15" width="44" height="44" as="geometry" />
        </mxCell>

        <!-- CloudWatch -->
        <mxCell id="cw_box" value="&lt;b&gt;Amazon CloudWatch&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#be123c&quot; style=&quot;font-size: 9.5px;&quot;&gt;Observability &amp;amp; Metrics&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#475569&quot; style=&quot;font-size: 8.5px;&quot;&gt;Logs: /aws/lambda/huylam-ocr-processor&lt;br&gt;Metrics: CPUUtilization, NetworkIn/Out&lt;br&gt;Alarms: CPU &gt; 70% (Auto SNS alert)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;strokeColor=#E11D48;strokeWidth=1.2;fillColor=#ffffff;align=center;verticalAlign=bottom;spacingBottom=10;" vertex="1" parent="sec_group">
          <mxGeometry x="530" y="35" width="245" height="175" as="geometry" />
        </mxCell>
        <mxCell id="cw_icon" value="" style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws4.cloudwatch;fillColor=#E7157B;gradientColor=none;" vertex="1" parent="cw_box">
          <mxGeometry x="100" y="15" width="44" height="44" as="geometry" />
        </mxCell>

        <!-- SNS -->
        <mxCell id="sns_box" value="&lt;b&gt;Amazon SNS&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#be123c&quot; style=&quot;font-size: 9.5px;&quot;&gt;Notification Service&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#475569&quot; style=&quot;font-size: 8.5px;&quot;&gt;Topic: huylam-ocr-alerts&lt;br&gt;Protocol: Email Subscriptions&lt;br&gt;Real-time alert on fatal spikes&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;strokeColor=#E11D48;strokeWidth=1.2;fillColor=#ffffff;align=center;verticalAlign=bottom;spacingBottom=10;" vertex="1" parent="sec_group">
          <mxGeometry x="795" y="35" width="235" height="175" as="geometry" />
        </mxCell>
        <mxCell id="sns_icon" value="" style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws4.sns;fillColor=#E7157B;gradientColor=none;" vertex="1" parent="sns_box">
          <mxGeometry x="95" y="15" width="44" height="44" as="geometry" />
        </mxCell>

        <!-- IAM -->
        <mxCell id="iam_box" value="&lt;b&gt;AWS IAM&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#b45309&quot; style=&quot;font-size: 9.5px;&quot;&gt;Security &amp;amp; Roles&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#475569&quot; style=&quot;font-size: 8.5px;&quot;&gt;huylam-ssm-role (EC2)&lt;br&gt;huylam-ocr-lambda-role&lt;br&gt;Principle of Least Privilege&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;strokeColor=#D97706;strokeWidth=1.2;fillColor=#ffffff;align=center;verticalAlign=bottom;spacingBottom=10;" vertex="1" parent="sec_group">
          <mxGeometry x="1050" y="35" width="220" height="175" as="geometry" />
        </mxCell>
        <mxCell id="iam_icon" value="" style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws4.iam;fillColor=#C925D1;gradientColor=none;" vertex="1" parent="iam_box">
          <mxGeometry x="88" y="15" width="44" height="44" as="geometry" />
        </mxCell>

        <!-- External Workstations -->
        <mxCell id="usr_icon" value="" style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws4.users;fillColor=#0284c7;gradientColor=none;" vertex="1" parent="1">
          <mxGeometry x="90" y="105" width="56" height="56" as="geometry" />
        </mxCell>
        <mxCell id="usr_lbl" value="&lt;b&gt;End Users&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#475569&quot; style=&quot;font-size: 10px;&quot;&gt;Web Browser / SPA&lt;br&gt;PDF &amp;amp; Scan Uploads&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=top;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="40" y="165" width="160" height="40" as="geometry" />
        </mxCell>

        <mxCell id="internet" value="&lt;b&gt;Internet&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F1F5F9;strokeColor=#94A3B8;arcSize=50;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="68" y="220" width="110" height="40" as="geometry" />
        </mxCell>

        <!-- Orthogonal Edges -->
        <mxCell id="e1" value="HTTPS" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#2563EB;strokeWidth=2;fontColor=#1D4ED8;fontSize=9.5;" edge="1" parent="1" source="usr_icon" target="internet">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <mxCell id="e2" value="HTTP : 80 / Public Traffic" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#232F3E;strokeWidth=2;fontColor=#0F172A;fontSize=9.5;fontStyle=1;" edge="1" parent="1" source="internet" target="igw">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <mxCell id="e3" value="Route: 0.0.0.0/0" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#8C4FFF;strokeWidth=2;fontColor=#6B21A8;fontSize=9.5;" edge="1" parent="1" source="igw" target="alb">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <mxCell id="e4" value="Port 5000" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#16A34A;strokeWidth=1.8;dashed=1;fontColor=#15803D;fontSize=9;" edge="1" parent="1" source="alb" target="tg">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <mxCell id="e5" value="Forward TCP 5000" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#16A34A;strokeWidth=2.2;fontColor=#15803D;fontSize=9.5;fontStyle=1;" edge="1" parent="1" source="tg" target="ec2_box">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <mxCell id="e6" value="Boto3: uploads/" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#16A34A;strokeWidth=2;fontColor=#15803D;fontSize=9.5;fontStyle=1;" edge="1" parent="1" source="ec2_box" target="s3_box">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1000" y="320" />
              <mxPoint x="1000" y="180" />
            </Array>
          </mxGeometry>
        </mxCell>

        <mxCell id="e7" value="s3:ObjectCreated:*" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#EA580C;strokeWidth=2.5;fontColor=#C2410C;fontSize=9.5;fontStyle=1;" edge="1" parent="1" source="s3_box" target="lambda_box">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <mxCell id="e8" value="PutItem / State" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#2563EB;strokeWidth=2.2;fontColor=#1D4ED8;fontSize=9.5;fontStyle=1;" edge="1" parent="1" source="lambda_box" target="ddb_box">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <mxCell id="e9" value="Job Sync / Poll" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#2563EB;strokeWidth=1.8;dashed=1;fontColor=#1D4ED8;fontSize=9.5;fontStyle=1;" edge="1" parent="1" source="ec2_box" target="ddb_box">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    return xml

def render_png(svg_path, png_path):
    cmd = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless",
        "--disable-gpu",
        "--force-device-scale-factor=2",
        "--window-size=1600,1060",
        f"--screenshot={png_path}",
        f"file://{os.path.abspath(svg_path)}"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"Rendered Retina PNG successfully: {png_path}")
    else:
        print(f"Error rendering PNG: {res.stderr}")

if __name__ == "__main__":
    icons = extract_base64_icons()
    
    # 1. Generate SVG
    svg_content = generate_svg(icons)
    svg_dest = "workshop/static/images/architecture/aws-system-architecture.svg"
    with open(svg_dest, "w") as f:
        f.write(svg_content)
    print(f"Generated SVG: {svg_dest}")

    # 2. Render Retina PNG
    png_dest = "workshop/static/images/architecture/aws-system-architecture.png"
    render_png(svg_dest, png_dest)

    # 3. Generate Draw.io
    drawio_content = generate_drawio()
    drawio_dest = "workshop/static/images/architecture/aws-system-architecture.drawio"
    with open(drawio_dest, "w") as f:
        f.write(drawio_content)
    print(f"Generated Draw.io: {drawio_dest}")
