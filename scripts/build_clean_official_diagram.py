#!/usr/bin/env python3
"""
build_clean_official_diagram.py
Generates an authentic, official AWS Reference Architecture diagram matching
AWS Well-Architected Framework and Reference Architecture Standards:
- Standard Multi-AZ Network Topology:
  * Ingress Edge:
    - Internet Gateway (huylam-igw) attached to Amazon VPC edge
  * Availability Zone 1: ap-southeast-1a (Active Primary AZ)
    - Public Subnet 1 (10.0.0.0/20) [Green Lock, Route: 0.0.0.0/0 -> IGW]
      Contains ALB Node 1a (huylam-ocr-alb ENI 1a, Port 80 HTTP Listener)
    - Target Group Layer (huylam-ocr-tg, Port 5000 HTTP, 1/1 Healthy Target)
    - Private Subnet 1 (10.0.128.0/20) [Blue Lock, Route: 10.0.0.0/16 -> local, Isolated]
      Contains Amazon EC2 Web Server (huylam-ocr-web-server, 10.0.8.15:5000, t3.micro)
      and Document Parsing Pipeline (PyMuPDF -> Vision OCR -> Markdown Exporter)
  * Availability Zone 2: ap-southeast-1b (Secondary Standby AZ)
    - Public Subnet 2 (10.0.16.0/20) [Green Lock, Route: 0.0.0.0/0 -> IGW]
      Contains ALB Node 1b (huylam-ocr-alb ENI 1b, Standby Ingress)
    - Private Subnet 2 (10.0.144.0/20) [Blue Lock, Route: 10.0.0.0/16 -> local, Isolated]
      Contains Multi-AZ Standby Target (Auto-Scaling Ready, $0.00 FinOps Scale-to-Zero)
- Perfectly symmetric Subnet alignment:
  * Public Subnets: x=265 to 425 (AZ 1a & AZ 1b)
  * Target Group / Failover Corridor: x=425 to 580
  * Private Subnets: x=580 to 980 (AZ 1a & AZ 1b)
- Hybrid Multimodal AI Tier (Bedrock, Kaggle GPU, Gemini API)
- Serverless Processing & Storage Tier (S3 -> Lambda -> DynamoDB)
- Management, Security & Observability Tier (Cognito, SSM, CloudWatch, IAM)
- 100% collision-free orthogonal arrows, pure white background (#FFFFFF), minimal text, official icons.
"""

import os
import subprocess
import base64
import shutil

def get_base64_image(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        data = f.read()
    ext = os.path.splitext(path)[1].lower().replace(".", "")
    if ext == "svg":
        mime = "image/svg+xml"
    elif ext in ("jpg", "jpeg"):
        mime = "image/jpeg"
    else:
        mime = "image/png"
    return f"data:{mime};base64,{base64.b64encode(data).decode('utf-8')}"

def load_all_icons():
    icons_dir = "/Users/huylam/Downloads/aws/workshop/static/images/aws_icons"
    return {
        'ec2': get_base64_image(f"{icons_dir}/Arch_Amazon-EC2_64.svg"),
        'lambda': get_base64_image(f"{icons_dir}/Arch_AWS-Lambda_64.svg"),
        's3': get_base64_image(f"{icons_dir}/Arch_Amazon-Simple-Storage-Service_64.svg"),
        'ddb': get_base64_image(f"{icons_dir}/Arch_Amazon-DynamoDB_64.svg"),
        'alb': get_base64_image(f"{icons_dir}/Res_Elastic-Load-Balancing_Application-Load-Balancer_48_Light.svg"),
        'igw': get_base64_image(f"{icons_dir}/Res_Amazon-VPC_Internet-Gateway_48_Light.svg"),
        'vpc': get_base64_image(f"{icons_dir}/Arch_Amazon-Virtual-Private-Cloud_64.svg"),
        'cognito': get_base64_image(f"{icons_dir}/Arch_Amazon-Cognito_64.svg"),
        'ssm': get_base64_image(f"{icons_dir}/Arch_AWS-Systems-Manager_64.svg"),
        'cw': get_base64_image(f"{icons_dir}/Arch_Amazon-CloudWatch_64.svg"),
        'iam': get_base64_image(f"{icons_dir}/Arch_AWS-Identity-and-Access-Management_64.svg"),
        'bedrock': get_base64_image(f"{icons_dir}/Arch_Amazon-SageMaker_64.svg"),
        'rtb': get_base64_image(f"{icons_dir}/Res_Amazon-Route-53_Route-Table_48_Light.svg")
    }

def generate_svg(icons):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1780 1020" width="1780" height="1020" style="background:#FFFFFF; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
  <defs>
    <!-- Arrow Markers -->
    <marker id="arr-dark" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#232F3E"/>
    </marker>
    <marker id="arr-purple" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#8C4FFF"/>
    </marker>
    <marker id="arr-green" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#16A34A"/>
    </marker>
    <marker id="arr-orange" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#EA580C"/>
    </marker>
    <marker id="arr-blue" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#0284C7"/>
    </marker>
    <marker id="arr-teal" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#0D9488"/>
    </marker>
  </defs>

  <!-- ==================== HEADER ==================== -->
  <text x="30" y="38" fill="#0F172A" font-size="18" font-weight="800" letter-spacing="-0.5">SERVERLESS HYBRID DOCUMENT OCR, PARSING &amp; TRANSLATION PLATFORM</text>
  <text x="1750" y="38" fill="#64748B" font-size="10.5" font-weight="600" text-anchor="end">AWS Reference Architecture | Multi-AZ High-Availability VPC | Region: ap-southeast-1 (Singapore) | Account: 677994024390</text>
  <line x1="30" y1="50" x2="1750" y2="50" stroke="#CBD5E1" stroke-width="1.2"/>

  <!-- ==================== LEFT COLUMN: CLIENTS & USERS ==================== -->
  <rect x="25" y="70" width="125" height="650" rx="4" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="87.5" y="92" fill="#334155" font-size="10.5" font-weight="700" text-anchor="middle">Clients &amp; Users</text>

  <!-- End Users Node -->
  <g transform="translate(87.5, 125)">
    <circle cx="0" cy="14" r="12" fill="#0F172A"/>
    <path d="M -18 42 C -18 30 -9 26 0 26 C 9 26 18 30 18 42 Z" fill="#0F172A"/>
    <text x="0" y="58" fill="#0F172A" font-size="10" font-weight="700" text-anchor="middle">End Users</text>
    <text x="0" y="70" fill="#64748B" font-size="8" text-anchor="middle">Web Browser / SPA</text>
  </g>

  <!-- Flow 1: Users to Internet -->
  <line x1="87.5" y1="205" x2="87.5" y2="252" stroke="#232F3E" stroke-width="1.8" marker-end="url(#arr-dark)"/>
  <rect x="52" y="220" width="71" height="15" rx="2" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>
  <text x="87.5" y="231" fill="#0F172A" font-size="7" font-weight="700" text-anchor="middle">HTTPS / TLS</text>

  <!-- Internet Node -->
  <g transform="translate(87.5, 260)">
    <circle cx="0" cy="20" r="18" fill="#FFFFFF" stroke="#64748B" stroke-width="1.2"/>
    <ellipse cx="0" cy="20" rx="10" ry="18" fill="none" stroke="#64748B" stroke-width="0.9"/>
    <line x1="-18" y1="20" x2="18" y2="20" stroke="#64748B" stroke-width="0.9"/>
    <line x1="-14" y1="12" x2="14" y2="12" stroke="#64748B" stroke-width="0.7"/>
    <line x1="-14" y1="28" x2="14" y2="28" stroke="#64748B" stroke-width="0.7"/>
    <text x="0" y="49" fill="#0F172A" font-size="10" font-weight="700" text-anchor="middle">Internet</text>
    <text x="0" y="60" fill="#64748B" font-size="7.5" text-anchor="middle">Public Traffic</text>
  </g>

  <!-- ==================== MIDDLE: AWS CLOUD CONTAINER ==================== -->
  <rect x="175" y="70" width="835" height="650" rx="6" fill="#FFFFFF" stroke="#232F3E" stroke-width="1.5"/>

  <!-- AWS Cloud Badge -->
  <g transform="translate(190, 80)">
    <rect x="0" y="0" width="115" height="24" rx="3" fill="#232F3E"/>
    <image href="{icons['vpc']}" x="5" y="3" width="18" height="18"/>
    <text x="28" y="16.5" fill="#FF9900" font-size="10.5" font-weight="700">AWS Cloud</text>
  </g>
  <text x="315" y="96" fill="#64748B" font-size="9.5" font-weight="600">Region: ap-southeast-1 (Singapore)  |  Account ID: 677994024390</text>

  <!-- ==================== AMAZON VPC: huylam-vpc ==================== -->
  <rect x="185" y="112" width="815" height="598" rx="5" fill="#FFFFFF" stroke="#8C4FFF" stroke-width="1.3"/>

  <!-- VPC Header Badge -->
  <g transform="translate(198, 120)">
    <image href="{icons['vpc']}" x="0" y="0" width="18" height="18"/>
    <text x="24" y="13.5" fill="#8C4FFF" font-size="10.5" font-weight="700">Amazon VPC: huylam-vpc</text>
    <text x="180" y="13.5" fill="#475569" font-size="10" font-weight="600">CIDR: 10.0.0.0/16</text>
    <text x="300" y="13.5" fill="#64748B" font-size="8.5">(vpc-0125f4d6db3fbffa6)</text>
  </g>

  <!-- VPC ROUTE TABLES BAR (y=140 to 184) -->
  <!-- Public Route Table -->
  <g transform="translate(198, 140)">
    <rect x="0" y="0" width="375" height="42" rx="3" fill="#FFFFFF" stroke="#16A34A" stroke-width="0.8"/>
    <image href="{icons['rtb']}" x="6" y="4" width="18" height="18"/>
    <text x="28" y="14" fill="#15803D" font-size="8.2" font-weight="700">Public Route Table: huylam-rtb-public</text>
    <text x="28" y="25" fill="#334155" font-size="7" font-weight="600">rtb-012d99ed0350e956f | Assoc: public1 (1a), public2 (1b)</text>
    <text x="28" y="36" fill="#16A34A" font-size="7.2" font-weight="700">0.0.0.0/0 -&gt; igw-0b9db3a6eac29ede9</text>
  </g>

  <!-- Private Route Table -->
  <g transform="translate(585, 140)">
    <rect x="0" y="0" width="405" height="42" rx="3" fill="#FFFFFF" stroke="#0284C7" stroke-width="0.8"/>
    <image href="{icons['rtb']}" x="6" y="4" width="18" height="18"/>
    <text x="28" y="14" fill="#0369A1" font-size="8.2" font-weight="700">Private Route Table: huylam-rtb-private1 &amp; 2</text>
    <text x="28" y="25" fill="#334155" font-size="7" font-weight="600">rtb-0d49944883c933d2a &amp; rtb-00f6e53a047aafc1f | Assoc: private1 &amp; 2</text>
    <text x="28" y="36" fill="#DC2626" font-size="7.2" font-weight="700">10.0.0.0/16 -&gt; local (Isolated / Zero IGW Route)</text>
  </g>

  <!-- ==================== INGRESS EDGE: INTERNET GATEWAY ==================== -->
  <g transform="translate(225, 280)">
    <rect x="-24" y="-35" width="48" height="70" rx="3" fill="#FFFFFF" stroke="#8C4FFF" stroke-width="1"/>
    <image href="{icons['igw']}" x="-16" y="-30" width="32" height="32"/>
    <text x="0" y="14" fill="#0F172A" font-size="7" font-weight="700" text-anchor="middle">Internet</text>
    <text x="0" y="23" fill="#0F172A" font-size="7" font-weight="700" text-anchor="middle">Gateway</text>
    <text x="0" y="32" fill="#8C4FFF" font-size="6.2" font-weight="600" text-anchor="middle">huylam-igw</text>
  </g>

  <!-- ========================================================================= -->
  <!-- ZONE 1: AVAILABILITY ZONE: ap-southeast-1a (ACTIVE PRIMARY AZ)            -->
  <!-- ========================================================================= -->
  <rect x="255" y="192" width="735" height="248" rx="4" fill="#FFFFFF" stroke="#64748B" stroke-width="1.2" stroke-dasharray="5,4"/>

  <!-- AZ 1a Title Badge -->
  <g transform="translate(265, 199)">
    <circle cx="6" cy="6" r="3.5" fill="#16A34A"/>
    <text x="14" y="9.5" fill="#0F172A" font-size="8.5" font-weight="700">Availability Zone: ap-southeast-1a (Active Primary AZ)</text>
  </g>

  <!-- 1A-1. PUBLIC SUBNET 1 (AZ 1a) -->
  <rect x="265" y="217" width="160" height="213" rx="4" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.1"/>
  <!-- Public Subnet 1 Header -->
  <g transform="translate(272, 224)">
    <rect x="0" y="0" width="13" height="13" rx="2" fill="#16A34A"/>
    <path d="M 3.5 5.5 L 3.5 3.5 C 3.5 2 4.5 1.2 6.5 1.2 C 8.5 1.2 9.5 2 9.5 3.5 L 9.5 5.5 Z" fill="none" stroke="#FFFFFF" stroke-width="1"/>
    <rect x="3" y="5" width="7" height="6" rx="1" fill="#FFFFFF"/>
    <circle cx="6.5" cy="7.5" r="0.7" fill="#16A34A"/>
    <text x="17" y="7" fill="#15803D" font-size="7.5" font-weight="700">PUBLIC SUBNET 1</text>
    <text x="17" y="16" fill="#64748B" font-size="6.5">10.0.0.0/20 (4,091 IPs)</text>
  </g>

  <!-- ALB Node 1a inside Public Subnet 1 -->
  <g transform="translate(345, 275)">
    <image href="{icons['alb']}" x="-20" y="-20" width="40" height="40"/>
    <text x="0" y="27" fill="#0F172A" font-size="8" font-weight="700" text-anchor="middle">ALB Node 1a</text>
    <text x="0" y="38" fill="#0284C7" font-size="7.2" font-weight="600" text-anchor="middle">huylam-ocr-alb</text>
  </g>

  <!-- Subnet 1 Specs Footer -->
  <g transform="translate(272, 330)">
    <rect x="0" y="0" width="146" height="90" rx="2" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="0.6"/>
    <text x="8" y="14" fill="#0F172A" font-size="6.8" font-weight="700">SG: huylam-alb-sg</text>
    <text x="8" y="26" fill="#15803D" font-size="6.5" font-weight="600">Port 80 Ingress (0.0.0.0/0)</text>
    <text x="8" y="38" fill="#0284C7" font-size="6.5" font-weight="600">Listener: Port 80 (HTTP)</text>
    <text x="8" y="50" fill="#334155" font-size="6.5">Active Primary ENI</text>
    <text x="8" y="62" fill="#15803D" font-size="6.5" font-weight="600">Handles 100% Live Traffic</text>
    <text x="8" y="74" fill="#64748B" font-size="6.2">Route: 0.0.0.0/0 -&gt; igw</text>
    <text x="8" y="85" fill="#15803D" font-size="6.2">Cross-Zone Balancing: On</text>
  </g>

  <!-- 1A-2. TARGET GROUP CARD (Corridor between Public & Private) -->
  <g transform="translate(440, 230)">
    <rect x="0" y="0" width="125" height="190" rx="3" fill="#FFFFFF" stroke="#8C4FFF" stroke-width="1.2"/>
    <!-- Authentic AWS Bullseye Target Group Icon -->
    <g transform="translate(62.5, 36)">
      <circle cx="0" cy="0" r="18" fill="#FFFFFF" stroke="#8C4FFF" stroke-width="1.8"/>
      <circle cx="0" cy="0" r="11" fill="none" stroke="#8C4FFF" stroke-width="1.2" stroke-dasharray="3,2"/>
      <circle cx="0" cy="0" r="4.5" fill="#8C4FFF"/>
      <line x1="0" y1="-18" x2="0" y2="-12" stroke="#8C4FFF" stroke-width="1.5" stroke-linecap="round"/>
      <line x1="0" y1="12" x2="0" y2="18" stroke="#8C4FFF" stroke-width="1.5" stroke-linecap="round"/>
      <line x1="-18" y1="0" x2="-12" y2="0" stroke="#8C4FFF" stroke-width="1.5" stroke-linecap="round"/>
      <line x1="12" y1="0" x2="18" y2="0" stroke="#8C4FFF" stroke-width="1.5" stroke-linecap="round"/>
    </g>
    <text x="62.5" y="68" fill="#0F172A" font-size="8.5" font-weight="700" text-anchor="middle">Target Group</text>
    <text x="62.5" y="80" fill="#8C4FFF" font-size="7.8" font-weight="700" text-anchor="middle">huylam-ocr-tg</text>
    
    <rect x="8" y="90" width="109" height="48" rx="2" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="0.6"/>
    <text x="62.5" y="103" fill="#334155" font-size="7" font-weight="600" text-anchor="middle">Protocol: HTTP: 5000</text>
    <text x="62.5" y="115" fill="#64748B" font-size="6.8" text-anchor="middle">Target Type: instance</text>
    <text x="62.5" y="127" fill="#15803D" font-size="6.8" font-weight="600" text-anchor="middle">HealthCheck: /health</text>

    <!-- Health Badge -->
    <rect x="10" y="146" width="105" height="24" rx="2" fill="#FFFFFF" stroke="#16A34A" stroke-width="1"/>
    <circle cx="20" cy="158" r="3.5" fill="#16A34A"/>
    <text x="62" y="161" fill="#15803D" font-size="7.2" font-weight="700" text-anchor="middle">Healthy 1/1 Target</text>
  </g>

  <!-- 1A-3. PRIVATE SUBNET 1 (AZ 1a) -->
  <rect x="580" y="217" width="400" height="213" rx="4" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.1"/>
  <!-- Private Subnet 1 Header -->
  <g transform="translate(588, 224)">
    <rect x="0" y="0" width="13" height="13" rx="2" fill="#0284C7"/>
    <path d="M 3.5 5.5 L 3.5 3.5 C 3.5 2 4.5 1.2 6.5 1.2 C 8.5 1.2 9.5 2 9.5 3.5 L 9.5 5.5 Z" fill="none" stroke="#FFFFFF" stroke-width="1"/>
    <rect x="3" y="5" width="7" height="6" rx="1" fill="#FFFFFF"/>
    <circle cx="6.5" cy="7.5" r="0.7" fill="#0284C7"/>
    <text x="17" y="7" fill="#0369A1" font-size="7.8" font-weight="700">PRIVATE SUBNET 1: ap-southeast-1a (Isolated)</text>
    <text x="17" y="16" fill="#64748B" font-size="6.8" font-weight="600">CIDR: 10.0.128.0/20 | subnet-08563e499271091ab | Route: 10.0.0.0/16 -&gt; local</text>
  </g>

  <!-- EC2 Instance Card inside Private Subnet 1 -->
  <g transform="translate(590, 248)">
    <rect x="0" y="0" width="150" height="172" rx="3" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>
    <g transform="translate(75, 32)">
      <image href="{icons['ec2']}" x="-20" y="-20" width="40" height="40"/>
      <text x="0" y="27" fill="#0F172A" font-size="8" font-weight="700" text-anchor="middle">EC2 Web Server</text>
      <text x="0" y="38" fill="#D97706" font-size="7.2" font-weight="700" text-anchor="middle">huylam-ocr-web-server</text>
    </g>

    <rect x="6" y="78" width="138" height="84" rx="2" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="0.6"/>
    <text x="10" y="91" fill="#0F172A" font-size="7" font-weight="700">Instance: t3.micro</text>
    <text x="10" y="103" fill="#0284C7" font-size="7" font-weight="600">IP: 10.0.8.15:5000</text>
    <text x="10" y="115" fill="#334155" font-size="6.8">Amazon Linux 2023</text>
    <text x="10" y="127" fill="#15803D" font-size="6.8" font-weight="600">SG: huylam-web-sg</text>
    <text x="10" y="139" fill="#64748B" font-size="6.5">Gunicorn + Uvicorn Workers</text>
    <text x="10" y="151" fill="#059669" font-size="6.5" font-weight="600">SSM Core (Zero SSH Inbound)</text>
  </g>

  <!-- Document Parsing Pipeline Container -->
  <g transform="translate(755, 248)">
    <rect x="0" y="0" width="215" height="172" rx="3" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>
    <text x="107.5" y="15" fill="#334155" font-size="8" font-weight="700" text-anchor="middle">Document Parsing Pipeline</text>

    <!-- Sub-node 1: PyMuPDF Fast Parser -->
    <g transform="translate(10, 24)">
      <rect x="0" y="0" width="195" height="36" rx="2" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.7"/>
      <rect x="6" y="6" width="20" height="24" rx="2" fill="#FFFFFF" stroke="#16A34A" stroke-width="1"/>
      <path d="M 6 12 L 18 12 M 6 17 L 16 17 M 6 22 L 22 22" stroke="#16A34A" stroke-width="0.8"/>
      <text x="32" y="16" fill="#0F172A" font-size="7.5" font-weight="700">PyMuPDF Fast Parser</text>
      <text x="32" y="27" fill="#15803D" font-size="6.8" font-weight="600">Vector PDF Extraction (0.1s/p)</text>
    </g>

    <!-- Pipeline Step Arrow 1 -->
    <line x1="107.5" y1="61" x2="107.5" y2="70" stroke="#0284C7" stroke-width="1.2" marker-end="url(#arr-blue)"/>
    <text x="138" y="68" fill="#0284C7" font-size="6.2" font-weight="700">Scanned</text>

    <!-- Sub-node 2: Vision OCR Dispatcher -->
    <g transform="translate(10, 72)">
      <rect x="0" y="0" width="195" height="36" rx="2" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.7"/>
      <rect x="6" y="6" width="20" height="24" rx="2" fill="#FFFFFF" stroke="#0284C7" stroke-width="1"/>
      <circle cx="16" cy="18" r="5" fill="none" stroke="#0284C7" stroke-width="1"/>
      <line x1="8" y1="18" x2="24" y2="18" stroke="#0284C7" stroke-width="0.8"/>
      <text x="32" y="16" fill="#0F172A" font-size="7.5" font-weight="700">Vision OCR Dispatcher</text>
      <text x="32" y="27" fill="#0284C7" font-size="6.8" font-weight="600">Routes Complex Pages to AI</text>
    </g>

    <!-- Pipeline Step Arrow 2 -->
    <line x1="107.5" y1="109" x2="107.5" y2="118" stroke="#64748B" stroke-width="1.2" marker-end="url(#arr-dark)"/>
    <text x="138" y="116" fill="#64748B" font-size="6.2" font-weight="700">OCR Text</text>

    <!-- Sub-node 3: Markdown Exporter -->
    <g transform="translate(10, 120)">
      <rect x="0" y="0" width="195" height="36" rx="2" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.7"/>
      <rect x="6" y="6" width="20" height="24" rx="2" fill="#FFFFFF" stroke="#D97706" stroke-width="1"/>
      <text x="16" y="22" fill="#D97706" font-size="8" font-weight="bold" text-anchor="middle">M↓</text>
      <text x="32" y="16" fill="#0F172A" font-size="7.5" font-weight="700">Markdown Exporter</text>
      <text x="32" y="27" fill="#D97706" font-size="6.8" font-weight="600">Preserves Tables &amp; Formulas</text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- ZONE 2: AVAILABILITY ZONE: ap-southeast-1b (SECONDARY STANDBY AZ)         -->
  <!-- ========================================================================= -->
  <rect x="255" y="450" width="735" height="248" rx="4" fill="#FFFFFF" stroke="#64748B" stroke-width="1.2" stroke-dasharray="5,4"/>

  <!-- AZ 1b Title Badge -->
  <g transform="translate(265, 457)">
    <circle cx="6" cy="6" r="3.5" fill="#0284C7"/>
    <text x="14" y="9.5" fill="#0F172A" font-size="8.5" font-weight="700">Availability Zone: ap-southeast-1b (Secondary Multi-AZ Standby)</text>
  </g>

  <!-- 2B-1. PUBLIC SUBNET 2 (AZ 1b) -->
  <rect x="265" y="475" width="160" height="213" rx="4" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.1"/>
  <!-- Public Subnet 2 Header -->
  <g transform="translate(272, 482)">
    <rect x="0" y="0" width="13" height="13" rx="2" fill="#16A34A"/>
    <path d="M 3.5 5.5 L 3.5 3.5 C 3.5 2 4.5 1.2 6.5 1.2 C 8.5 1.2 9.5 2 9.5 3.5 L 9.5 5.5 Z" fill="none" stroke="#FFFFFF" stroke-width="1"/>
    <rect x="3" y="5" width="7" height="6" rx="1" fill="#FFFFFF"/>
    <circle cx="6.5" cy="7.5" r="0.7" fill="#16A34A"/>
    <text x="17" y="7" fill="#15803D" font-size="7.5" font-weight="700">PUBLIC SUBNET 2</text>
    <text x="17" y="16" fill="#64748B" font-size="6.5">10.0.16.0/20 (4,091 IPs)</text>
  </g>

  <!-- ALB Node B inside Public Subnet 2 -->
  <g transform="translate(345, 535)">
    <image href="{icons['alb']}" x="-20" y="-20" width="40" height="40"/>
    <text x="0" y="27" fill="#0F172A" font-size="8" font-weight="700" text-anchor="middle">ALB Node 1b</text>
    <text x="0" y="38" fill="#0284C7" font-size="7.2" font-weight="600" text-anchor="middle">huylam-ocr-alb (Standby)</text>
  </g>

  <g transform="translate(272, 595)">
    <rect x="0" y="0" width="146" height="85" rx="2" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="0.6"/>
    <text x="8" y="14" fill="#0F172A" font-size="6.8" font-weight="700">Multi-AZ HA Ingress</text>
    <text x="8" y="26" fill="#0284C7" font-size="6.5" font-weight="600">Dual-AZ Elastic Network (ENI)</text>
    <text x="8" y="38" fill="#15803D" font-size="6.5">Cross-Zone Failover Ready</text>
    <text x="8" y="50" fill="#64748B" font-size="6.2">Route: 0.0.0.0/0 -&gt; igw</text>
    <text x="8" y="62" fill="#334155" font-size="6.2">Security Group: huylam-alb-sg</text>
    <text x="8" y="74" fill="#059669" font-size="6.2" font-weight="600">Health Check Monitoring</text>
  </g>

  <!-- 2B-2. PRIVATE SUBNET 2 (AZ 1b - Perfectly Symmetrical at x=580 to 980) -->
  <rect x="580" y="475" width="400" height="213" rx="4" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.1"/>
  <!-- Private Subnet 2 Header -->
  <g transform="translate(588, 482)">
    <rect x="0" y="0" width="13" height="13" rx="2" fill="#0284C7"/>
    <path d="M 3.5 5.5 L 3.5 3.5 C 3.5 2 4.5 1.2 6.5 1.2 C 8.5 1.2 9.5 2 9.5 3.5 L 9.5 5.5 Z" fill="none" stroke="#FFFFFF" stroke-width="1"/>
    <rect x="3" y="5" width="7" height="6" rx="1" fill="#FFFFFF"/>
    <circle cx="6.5" cy="7.5" r="0.7" fill="#0284C7"/>
    <text x="17" y="7" fill="#0369A1" font-size="7.8" font-weight="700">PRIVATE SUBNET 2: ap-southeast-1b (Isolated Standby)</text>
    <text x="17" y="16" fill="#64748B" font-size="6.8" font-weight="600">CIDR: 10.0.144.0/20 | subnet-07e20dc44c40fac46 | Route: 10.0.0.0/16 -&gt; local</text>
  </g>

  <!-- Standby Target Card inside Private Subnet 2 -->
  <g transform="translate(590, 508)">
    <rect x="0" y="0" width="380" height="170" rx="3" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8" stroke-dasharray="4,3"/>
    
    <!-- Ghosted Standby EC2 Icon -->
    <g transform="translate(55, 38)">
      <image href="{icons['ec2']}" x="-20" y="-20" width="40" height="40" opacity="0.45"/>
      <text x="0" y="27" fill="#64748B" font-size="8" font-weight="700" text-anchor="middle">Standby Target</text>
      <text x="0" y="38" fill="#8C4FFF" font-size="7.2" font-weight="600" text-anchor="middle">huylam-ocr-tg (Standby)</text>
    </g>

    <!-- Standby Info Description -->
    <rect x="115" y="14" width="255" height="142" rx="2" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="0.6"/>
    <text x="125" y="30" fill="#0F172A" font-size="7.8" font-weight="700">Multi-AZ Disaster Recovery Target</text>
    <text x="125" y="44" fill="#0284C7" font-size="7" font-weight="600">Subnet: huylam-subnet-private2 (10.0.144.0/20)</text>
    <text x="125" y="58" fill="#15803D" font-size="7.2" font-weight="700">FinOps Spend: $0.00 | Scale-to-Zero</text>
    <text x="125" y="72" fill="#334155" font-size="6.8">Target Group Ready: auto registers on scale-out</text>
    <text x="125" y="86" fill="#059669" font-size="6.8" font-weight="600">Security Group: huylam-web-sg (Port 5000)</text>
    <text x="125" y="100" fill="#64748B" font-size="6.5">Route Table: rtb-00f6e53a047aafc1f (Isolated)</text>
    <rect x="125" y="110" width="235" height="36" rx="2" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.6"/>
    <text x="133" y="124" fill="#0F172A" font-size="6.8" font-weight="600">High Availability SLA: 99.99%</text>
    <text x="133" y="136" fill="#15803D" font-size="6.5" font-weight="600">Multi-AZ automatic failover ready</text>
  </g>

  <!-- ==================== THIRD COLUMN: HYBRID MULTIMODAL AI TIER ==================== -->
  <rect x="1030" y="70" width="285" height="650" rx="4" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="1172.5" y="92" fill="#334155" font-size="10.5" font-weight="700" text-anchor="middle">Hybrid Multimodal AI Tier</text>
  <text x="1172.5" y="105" fill="#64748B" font-size="7.5" text-anchor="middle">Vision OCR &amp; Multimodal Reasoning</text>

  <!-- Node 1: Amazon Bedrock -->
  <g transform="translate(1045, 140)">
    <rect x="0" y="0" width="255" height="135" rx="3" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.9"/>
    <g transform="translate(127.5, 34)">
      <image href="{icons['bedrock']}" x="-20" y="-20" width="40" height="40"/>
      <text x="0" y="27" fill="#0F172A" font-size="8.5" font-weight="700" text-anchor="middle">Amazon Bedrock</text>
      <text x="0" y="38" fill="#0D9488" font-size="7.5" font-weight="600" text-anchor="middle">Claude 3.5 Sonnet &amp; Nova Micro</text>
    </g>
    <rect x="10" y="80" width="235" height="45" rx="2" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="0.6"/>
    <text x="20" y="95" fill="#0F172A" font-size="7" font-weight="700">Native AWS Serverless GenAI</text>
    <text x="20" y="107" fill="#0D9488" font-size="6.8" font-weight="600">Bedrock Converse API Stream</text>
    <text x="20" y="118" fill="#64748B" font-size="6.5">Enterprise Document Fallback</text>
  </g>

  <!-- Node 2: Kaggle GPU Cluster -->
  <g transform="translate(1045, 320)">
    <rect x="0" y="0" width="255" height="135" rx="3" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.9"/>
    <g transform="translate(127.5, 34)">
      <rect x="-18" y="-18" width="36" height="36" rx="3" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.2"/>
      <rect x="-10" y="-10" width="20" height="20" rx="1" fill="#0284C7"/>
      <text x="0" y="4" fill="#FFFFFF" font-size="8" font-weight="bold" text-anchor="middle">GPU</text>
      <text x="0" y="27" fill="#0F172A" font-size="8.5" font-weight="700" text-anchor="middle">Kaggle GPU Cluster</text>
      <text x="0" y="38" fill="#0284C7" font-size="7.5" font-weight="600" text-anchor="middle">Qwen-2.5-VL 7B (2x T4 GPU)</text>
    </g>
    <rect x="10" y="80" width="235" height="45" rx="2" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="0.6"/>
    <text x="20" y="95" fill="#0F172A" font-size="7" font-weight="700">High-Throughput Vision OCR</text>
    <text x="20" y="107" fill="#0284C7" font-size="6.8" font-weight="600">Cloudflare Tunnel (Zero-Trust)</text>
    <text x="20" y="118" fill="#15803D" font-size="6.5" font-weight="600">Cost: $0.00 Free Tier Pipeline</text>
  </g>

  <!-- Node 3: Google Gemini API -->
  <g transform="translate(1045, 500)">
    <rect x="0" y="0" width="255" height="135" rx="3" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.9"/>
    <g transform="translate(127.5, 34)">
      <path d="M 0 -16 Q 0 0 16 0 Q 0 0 0 16 Q 0 0 -16 0 Q 0 0 0 -16 Z" fill="#2563EB"/>
      <circle cx="0" cy="0" r="3" fill="#FFFFFF"/>
      <text x="0" y="27" fill="#0F172A" font-size="8.5" font-weight="700" text-anchor="middle">Google Gemini API</text>
      <text x="0" y="38" fill="#2563EB" font-size="7.5" font-weight="600" text-anchor="middle">Gemini 2.5 Flash</text>
    </g>
    <rect x="10" y="80" width="235" height="45" rx="2" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="0.6"/>
    <text x="20" y="95" fill="#0F172A" font-size="7" font-weight="700">Multimodal OCR &amp; Translation</text>
    <text x="20" y="107" fill="#2563EB" font-size="6.8" font-weight="600">Multi-Key Automatic Failover</text>
    <text x="20" y="118" fill="#15803D" font-size="6.5" font-weight="600">Sub-second Latency Response</text>
  </g>

  <!-- ==================== FOURTH COLUMN: SERVERLESS & STORAGE TIER ==================== -->
  <rect x="1335" y="70" width="415" height="650" rx="4" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="1542.5" y="92" fill="#334155" font-size="10.5" font-weight="700" text-anchor="middle">Serverless Processing &amp; Storage Tier</text>

  <!-- Node 1: Amazon S3 -->
  <g transform="translate(1355, 140)">
    <rect x="0" y="0" width="375" height="135" rx="3" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.9"/>
    <g transform="translate(187.5, 34)">
      <image href="{icons['s3']}" x="-22" y="-22" width="44" height="44"/>
      <text x="0" y="28" fill="#0F172A" font-size="9" font-weight="700" text-anchor="middle">Amazon Simple Storage Service (S3)</text>
      <text x="0" y="39" fill="#15803D" font-size="7.8" font-weight="600" text-anchor="middle">huylam-ocr-documents-ap-southeast-1</text>
    </g>
    <rect x="12" y="82" width="351" height="43" rx="2" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="0.6"/>
    <text x="22" y="96" fill="#0F172A" font-size="7" font-weight="700">uploads/ (Raw PDFs)  |  outputs/ (Markdown &amp; JSON)</text>
    <text x="22" y="108" fill="#15803D" font-size="6.8" font-weight="600">Event Trigger: s3:ObjectCreated:* on uploads/</text>
    <text x="22" y="119" fill="#64748B" font-size="6.5">SSE-S3 AES-256 Encryption  |  TLS 1.3 In-Transit</text>
  </g>

  <!-- Flow S3 -> Lambda -->
  <line x1="1542.5" y1="275" x2="1542.5" y2="335" stroke="#EA580C" stroke-width="1.8" marker-end="url(#arr-orange)"/>
  <rect x="1475" y="297" width="135" height="16" rx="2" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>
  <text x="1542.5" y="308.5" fill="#EA580C" font-size="7.2" font-weight="700" text-anchor="middle">s3:ObjectCreated:*</text>

  <!-- Node 2: AWS Lambda -->
  <g transform="translate(1355, 335)">
    <rect x="0" y="0" width="375" height="135" rx="3" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.9"/>
    <g transform="translate(187.5, 34)">
      <image href="{icons['lambda']}" x="-22" y="-22" width="44" height="44"/>
      <text x="0" y="28" fill="#0F172A" font-size="9" font-weight="700" text-anchor="middle">AWS Lambda (Event Processor)</text>
      <text x="0" y="39" fill="#EA580C" font-size="7.8" font-weight="600" text-anchor="middle">huylam-ocr-processor (Python 3.11)</text>
    </g>
    <rect x="12" y="82" width="351" height="43" rx="2" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="0.6"/>
    <text x="22" y="96" fill="#0F172A" font-size="7" font-weight="700">Async Event Processor | Scale-to-Zero Architecture</text>
    <text x="22" y="108" fill="#EA580C" font-size="6.8" font-weight="600">Execution Memory: 128MB  |  Timeout: 300s</text>
    <text x="22" y="119" fill="#64748B" font-size="6.5">Parses S3 Metadata &amp; Updates DynamoDB Job State</text>
  </g>

  <!-- Flow Lambda -> DynamoDB -->
  <line x1="1542.5" y1="470" x2="1542.5" y2="530" stroke="#0284C7" stroke-width="1.8" marker-end="url(#arr-blue)"/>
  <rect x="1465" y="492" width="155" height="16" rx="2" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>
  <text x="1542.5" y="503.5" fill="#0284C7" font-size="7.2" font-weight="700" text-anchor="middle">PutItem (job_id, status)</text>

  <!-- Node 3: Amazon DynamoDB -->
  <g transform="translate(1355, 530)">
    <rect x="0" y="0" width="375" height="135" rx="3" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.9"/>
    <g transform="translate(187.5, 34)">
      <image href="{icons['ddb']}" x="-22" y="-22" width="44" height="44"/>
      <text x="0" y="28" fill="#0F172A" font-size="9" font-weight="700" text-anchor="middle">Amazon DynamoDB (NoSQL Database)</text>
      <text x="0" y="39" fill="#1D4ED8" font-size="7.8" font-weight="600" text-anchor="middle">document_processing_jobs</text>
    </g>
    <rect x="12" y="82" width="351" height="43" rx="2" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="0.6"/>
    <text x="22" y="96" fill="#0F172A" font-size="7" font-weight="700">PK: job_id (String)  |  SK: created_at (ISO 8601)</text>
    <text x="22" y="108" fill="#1D4ED8" font-size="6.8" font-weight="600">Billing Mode: PAY_PER_REQUEST (On-Demand Scale-to-Zero)</text>
    <text x="22" y="119" fill="#64748B" font-size="6.5">Serverless Tracking of Document Conversion Pipeline</text>
  </g>

  <!-- ==================== BOTTOM: MANAGEMENT, SECURITY & OBSERVABILITY ==================== -->
  <rect x="25" y="740" width="1725" height="230" rx="4" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1"/>
  <text x="887.5" y="760" fill="#334155" font-size="11" font-weight="700" text-anchor="middle">Management, Security &amp; Observability Tier (AWS Well-Architected Framework)</text>

  <!-- Cognito Node -->
  <g transform="translate(235, 780)">
    <rect x="-180" y="0" width="360" height="175" rx="3" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>
    <image href="{icons['cognito']}" x="-22" y="15" width="44" height="44"/>
    <text x="0" y="75" fill="#0F172A" font-size="9.5" font-weight="700" text-anchor="middle">Amazon Cognito</text>
    <text x="0" y="88" fill="#E11D48" font-size="8" font-weight="600" text-anchor="middle">User Pool: huylam-auth</text>
    <rect x="-165" y="100" width="330" height="62" rx="2" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="0.6"/>
    <text x="-155" y="115" fill="#0F172A" font-size="7" font-weight="700">Google OAuth 2.0 &amp; Hosted UI Federation</text>
    <text x="-155" y="128" fill="#E11D48" font-size="6.8" font-weight="600">JWT Token Verification on API Endpoints</text>
    <text x="-155" y="141" fill="#64748B" font-size="6.5">Role-Based Access Control (RBAC)</text>
    <text x="-155" y="153" fill="#15803D" font-size="6.5" font-weight="600">Security Group: Strict Zero-Trust Client Token</text>
  </g>

  <!-- SSM Node -->
  <g transform="translate(660, 780)">
    <rect x="-180" y="0" width="360" height="175" rx="3" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>
    <image href="{icons['ssm']}" x="-22" y="15" width="44" height="44"/>
    <text x="0" y="75" fill="#0F172A" font-size="9.5" font-weight="700" text-anchor="middle">AWS Systems Manager</text>
    <text x="0" y="88" fill="#059669" font-size="8" font-weight="600" text-anchor="middle">Session Manager &amp; Parameter Store</text>
    <rect x="-165" y="100" width="330" height="62" rx="2" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="0.6"/>
    <text x="-155" y="115" fill="#0F172A" font-size="7" font-weight="700">Port-Free Shell Access (Zero SSH Ingress)</text>
    <text x="-155" y="128" fill="#059669" font-size="6.8" font-weight="600">SSM Agent Running on EC2 Web Server</text>
    <text x="-155" y="141" fill="#334155" font-size="6.8">Parameter: /huylam-ocr/config encrypted via KMS</text>
    <text x="-155" y="153" fill="#15803D" font-size="6.5" font-weight="600">Zero Open Port 22 in Inbound Security Groups</text>
  </g>

  <!-- CloudWatch Node -->
  <g transform="translate(1085, 780)">
    <rect x="-180" y="0" width="360" height="175" rx="3" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>
    <image href="{icons['cw']}" x="-22" y="15" width="44" height="44"/>
    <text x="0" y="75" fill="#0F172A" font-size="9.5" font-weight="700" text-anchor="middle">Amazon CloudWatch</text>
    <text x="0" y="88" fill="#EA580C" font-size="8" font-weight="600" text-anchor="middle">Unified Logs &amp; Metric Alarms</text>
    <rect x="-165" y="100" width="330" height="62" rx="2" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="0.6"/>
    <text x="-155" y="115" fill="#0F172A" font-size="7" font-weight="700">Log Group: /aws/lambda/huylam-ocr-processor</text>
    <text x="-155" y="128" fill="#EA580C" font-size="6.8" font-weight="600">EC2 Metrics: CPUUtilization, MemoryUtilization</text>
    <text x="-155" y="141" fill="#DC2626" font-size="6.8" font-weight="700">Alarms: CPU &gt; 70% | Lambda Errors &gt; 0</text>
    <text x="-155" y="153" fill="#64748B" font-size="6.5">Dashboard: huylam-ocr-monitoring</text>
  </g>

  <!-- IAM Node -->
  <g transform="translate(1510, 780)">
    <rect x="-180" y="0" width="360" height="175" rx="3" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>
    <image href="{icons['iam']}" x="-22" y="15" width="44" height="44"/>
    <text x="0" y="75" fill="#0F172A" font-size="9.5" font-weight="700" text-anchor="middle">AWS IAM</text>
    <text x="0" y="88" fill="#D97706" font-size="8" font-weight="600" text-anchor="middle">Roles &amp; Least Privilege Policies</text>
    <rect x="-165" y="100" width="330" height="62" rx="2" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="0.6"/>
    <text x="-155" y="115" fill="#0F172A" font-size="7" font-weight="700">Role: huylam-ocr-lambda-role (S3/DDB ReadWrite)</text>
    <text x="-155" y="128" fill="#D97706" font-size="6.8" font-weight="600">Instance Profile: huylam-ssm-role (SSM Core)</text>
    <text x="-155" y="141" fill="#15803D" font-size="6.8">Principle of Least Privilege Strictly Enforced</text>
    <text x="-155" y="153" fill="#64748B" font-size="6.5">Zero Hardcoded Access Keys in Source Code</text>
  </g>

  <!-- ========================================================================= -->
  <!-- 100% COLLISION-FREE ORTHOGONAL CONNECTING ARROWS                          -->
  <!-- ========================================================================= -->

  <!-- Flow 2: Internet -> Internet Gateway (Straight horizontal at y=280) -->
  <line x1="106" y1="280" x2="200" y2="280" stroke="#232F3E" stroke-width="1.8" marker-end="url(#arr-dark)"/>
  <rect x="125" y="272" width="60" height="16" rx="2" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>
  <text x="155" y="283.5" fill="#0F172A" font-size="7.2" font-weight="700" text-anchor="middle">HTTP: 80</text>

  <!-- Flow 3a: Internet Gateway -> ALB Node 1a (Straight horizontal at y=275) -->
  <line x1="250" y1="275" x2="323" y2="275" stroke="#16A34A" stroke-width="1.8" marker-end="url(#arr-green)"/>
  <rect x="265" y="267" width="44" height="16" rx="2" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>
  <text x="287" y="278.5" fill="#15803D" font-size="7" font-weight="700" text-anchor="middle">Port 80</text>

  <!-- Flow 3b: Branch from IGW down to Public Subnet 2 ALB Node B (Standby AZ 1b) -->
  <!-- Leaves IGW bottom at (225, 316) -> down along open margin at x=225 to y=535 -> right into ALB Node 1b at x=323 -->
  <path d="M 225 316 L 225 535 L 323 535" fill="none" stroke="#16A34A" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arr-green)"/>
  <rect x="187" y="475" width="76" height="16" rx="2" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>
  <text x="225" y="486.5" fill="#15803D" font-size="6.8" font-weight="700" text-anchor="middle">Dual-AZ Ingress</text>

  <!-- Flow 4: ALB Node 1a -> Target Group (Straight horizontal at y=275) -->
  <line x1="367" y1="275" x2="438" y2="275" stroke="#16A34A" stroke-width="1.8" marker-end="url(#arr-green)"/>
  <rect x="380" y="267" width="45" height="16" rx="2" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>
  <text x="402.5" y="278.5" fill="#15803D" font-size="7" font-weight="700" text-anchor="middle">Forward</text>

  <!-- Flow 5a: Target Group -> Amazon EC2 Web Server (Straight horizontal at y=275) -->
  <line x1="565" y1="275" x2="588" y2="275" stroke="#16A34A" stroke-width="1.8" marker-end="url(#arr-green)"/>
  <rect x="560" y="258" width="56" height="15" rx="2" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>
  <text x="588" y="269" fill="#15803D" font-size="6.8" font-weight="700" text-anchor="middle">TCP: 5000</text>

  <!-- Flow 5b: Target Group -> Multi-AZ Standby Target in AZ 1b -->
  <!-- Exits Target Group bottom (x=502.5, y=420) -> down open corridor at x=502.5 to y=550 -> right into Standby Target at x=588 -->
  <path d="M 502.5 420 L 502.5 550 L 588 550" fill="none" stroke="#8C4FFF" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#arr-purple)"/>
  <rect x="442" y="475" width="122" height="16" rx="2" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>
  <text x="503" y="486.5" fill="#8C4FFF" font-size="7" font-weight="700" text-anchor="middle">Multi-AZ Standby Route</text>

  <!-- Flow 6: EC2 -> PyMuPDF Fast Parser (Document Parsing Pipeline) -->
  <line x1="740" y1="290" x2="763" y2="290" stroke="#16A34A" stroke-width="1.8" marker-end="url(#arr-green)"/>
  <rect x="732" y="272" width="52" height="15" rx="2" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>
  <text x="758" y="283" fill="#15803D" font-size="6.8" font-weight="700" text-anchor="middle">PDF Ingest</text>

  <!-- Flow 8: Vision OCR Dispatcher to Multimodal AI Tier -->
  <!-- Exits OCR Dispatcher (x=970, y=338), enters AI tier corridor at x=1008 -->
  <path d="M 970 338 L 1008 338" fill="none" stroke="#0284C7" stroke-width="1.6" stroke-dasharray="4,3"/>
  <rect x="968" y="328" width="42" height="15" rx="2" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>
  <text x="989" y="339" fill="#0284C7" font-size="7" font-weight="700" text-anchor="middle">Vision AI</text>

  <!-- Vertical AI Bus at x=1010 inside AI Tier corridor -->
  <line x1="1010" y1="207" x2="1010" y2="567" stroke="#0284C7" stroke-width="1.6" stroke-dasharray="4,3"/>

  <!-- Branch 8a: To Amazon Bedrock (y=207) -->
  <path d="M 1010 207 L 1043 207" fill="none" stroke="#0D9488" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#arr-teal)"/>

  <!-- Branch 8b: To Kaggle GPU Cluster (y=387) -->
  <path d="M 1010 387 L 1043 387" fill="none" stroke="#0284C7" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#arr-blue)"/>

  <!-- Branch 8c: To Google Gemini API (y=567) -->
  <path d="M 1010 567 L 1043 567" fill="none" stroke="#2563EB" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#arr-blue)"/>

  <!-- Flow 9: Markdown Exporter to Amazon S3 -->
  <!-- Exits Exporter (x=970, y=386), turns down at x=995, passes open horizontal corridor at y=675, wraps up into S3 at x=1325 -->
  <path d="M 970 386 L 995 386 L 995 675 L 1325 675 L 1325 207 L 1353 207" fill="none" stroke="#16A34A" stroke-width="1.8" marker-end="url(#arr-green)"/>
  <rect x="1060" y="666" width="200" height="18" rx="2" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>
  <text x="1160" y="678.5" fill="#15803D" font-size="7.5" font-weight="700" text-anchor="middle">Boto3 Uploads (Raw &amp; Markdown to S3)</text>

  <!-- ==================== FOOTER ==================== -->
  <line x1="30" y1="990" x2="1750" y2="990" stroke="#CBD5E1" stroke-width="1.2"/>
  <text x="30" y="1006" fill="#64748B" font-size="8.5">FinOps Spend: $0.00 (AWS Free Tier Always Free + Scale-to-Zero Serverless) | HUCE Internship Report 2026 | Lam Quang Huy</text>
  <text x="1750" y="1006" fill="#64748B" font-size="8.5" text-anchor="end">Production Multi-AZ Architecture: ap-southeast-1a (Active Primary) + ap-southeast-1b (Secondary Standby)</text>
</svg>"""
    return svg

def main():
    icons = load_all_icons()
    svg_content = generate_svg(icons)
    
    out_dir = "/Users/huylam/Downloads/aws/workshop/static/images/architecture"
    os.makedirs(out_dir, exist_ok=True)
    
    svg_path = os.path.join(out_dir, "aws-system-architecture.svg")
    png_path = os.path.join(out_dir, "aws-system-architecture.png")
    drawio_path = os.path.join(out_dir, "aws-system-architecture.drawio")
    brain_path = "/Users/huylam/.gemini/antigravity/brain/d050bbbe-67da-478c-870d-e04cb556c656/aws-system-architecture.png"
    
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated: {svg_path}")
    
    # Save as drawio xml wrapper
    drawio_content = f"""<mxfile host="app.diagrams.net" modified="2026-10-04T15:40:00.000Z" agent="Antigravity" version="21.0.0">
  <diagram id="aws-architecture" name="AWS Reference Architecture">
    <mxGraphModel dx="1780" dy="1020" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1780" pageHeight="1020">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="svg_embed" value="" style="shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image={svg_path};" vertex="1" parent="1">
          <mxGeometry x="0" y="0" width="1780" height="1020" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    with open(drawio_path, "w", encoding="utf-8") as f:
        f.write(drawio_content)
    print(f"Generated: {drawio_path}")
    
    # Render PNG using headless Chrome
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if os.path.exists(chrome_path):
        cmd = [
            chrome_path,
            "--headless=new",
            "--disable-gpu",
            "--force-device-scale-factor=2",
            f"--window-size=1780,1020",
            f"--screenshot={png_path}",
            svg_path
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and os.path.exists(png_path):
            print(f"Rendered: {png_path}")
            shutil.copy2(png_path, brain_path)
            print(f"Copied to brain: {brain_path}")
        else:
            print(f"Error rendering PNG: {res.stderr}")
    else:
        print("Chrome not found for rendering.")

if __name__ == "__main__":
    main()
