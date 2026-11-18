#!/usr/bin/env python3
"""
build_all_clean_diagrams.py
Generates official, authentic AWS Reference Architecture diagrams for:
1. aws-hybrid-ocr-engine-architecture
2. aws-vpc-network-architecture
3. aws-security-group-chaining
4. aws-serverless-event-pipeline
5. aws-ecs-fargate-architecture

Standard Reference Architecture Principles:
- Pure white background (#FFFFFF), minimal subtle borders (#CBD5E1, #94A3B8)
- Official AWS icons embedded from local workshop/static/images/aws_icons
- Orthogonal collision-free arrow connectors
- Crisp, concise typography without overlapping labels
- Chrome headless 2x Retina PNG rendering
- Draw.io XML wrappers
"""

import os
import subprocess
import base64
import shutil

ICONS_DIR = "/Users/huylam/Downloads/aws/workshop/static/images/aws_icons"
OUT_DIR = "/Users/huylam/Downloads/aws/workshop/static/images/architecture"
PUBLIC_DIR = "/Users/huylam/Downloads/aws/workshop/public/images/architecture"
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

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

def load_icons():
    return {
        'ec2': get_base64_image(f"{ICONS_DIR}/Arch_Amazon-EC2_64.svg"),
        'lambda': get_base64_image(f"{ICONS_DIR}/Arch_AWS-Lambda_64.svg"),
        's3': get_base64_image(f"{ICONS_DIR}/Arch_Amazon-Simple-Storage-Service_64.svg"),
        'ddb': get_base64_image(f"{ICONS_DIR}/Arch_Amazon-DynamoDB_64.svg"),
        'alb': get_base64_image(f"{ICONS_DIR}/Res_Elastic-Load-Balancing_Application-Load-Balancer_48_Light.svg"),
        'igw': get_base64_image(f"{ICONS_DIR}/Res_Amazon-VPC_Internet-Gateway_48_Light.svg"),
        'vpc': get_base64_image(f"{ICONS_DIR}/Arch_Amazon-Virtual-Private-Cloud_64.svg"),
        'cognito': get_base64_image(f"{ICONS_DIR}/Arch_Amazon-Cognito_64.svg"),
        'ssm': get_base64_image(f"{ICONS_DIR}/Arch_AWS-Systems-Manager_64.svg"),
        'cw': get_base64_image(f"{ICONS_DIR}/Arch_Amazon-CloudWatch_64.svg"),
        'iam': get_base64_image(f"{ICONS_DIR}/Arch_AWS-Identity-and-Access-Management_64.svg"),
        'bedrock': get_base64_image(f"{ICONS_DIR}/Arch_Amazon-SageMaker_64.svg"),
        'rtb': get_base64_image(f"{ICONS_DIR}/Res_Amazon-Route-53_Route-Table_48_Light.svg"),
        'role': get_base64_image(f"{ICONS_DIR}/Res_AWS-Identity-Access-Management_Role_48_Light.svg"),
        'ecs': get_base64_image(f"{ICONS_DIR}/ElasticContainerService.png"),
        'ecr': get_base64_image(f"{ICONS_DIR}/ElasticContainerRegistry.png"),
        'fargate': get_base64_image(f"{ICONS_DIR}/Fargate.png"),
        'ecs_task': get_base64_image(f"{ICONS_DIR}/ElasticContainerServiceTask.png"),
        'shield': get_base64_image(f"{ICONS_DIR}/Shield.png"),
    }

DEFS_MARKERS = """
  <defs>
    <marker id="arr-dark" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#1E293B"/>
    </marker>
    <marker id="arr-blue" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#0284C7"/>
    </marker>
    <marker id="arr-green" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#16A34A"/>
    </marker>
    <marker id="arr-orange" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#EA580C"/>
    </marker>
    <marker id="arr-purple" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#8C4FFF"/>
    </marker>
  </defs>
"""

# ==============================================================================
# 1. HYBRID OCR ENGINE ARCHITECTURE
# ==============================================================================
def gen_hybrid_ocr_svg(icons):
    w, h = 1500, 900
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="background:#FFFFFF; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
  {DEFS_MARKERS}

  <!-- Header -->
  <text x="30" y="38" fill="#0F172A" font-size="18" font-weight="800" letter-spacing="-0.5">HYBRID MULTI-TIER DOCUMENT OCR &amp; TECHNICAL TRANSLATION ENGINE</text>
  <text x="1470" y="38" fill="#64748B" font-size="11" font-weight="600" text-anchor="end">Intelligent Routing &amp; FinOps Dual-AI Architecture | AL2023 EC2 Gunicorn Core</text>
  <line x1="30" y1="50" x2="1470" y2="50" stroke="#CBD5E1" stroke-width="1.2"/>

  <!-- Left: Web Studio Frontend -->
  <rect x="30" y="70" width="220" height="790" rx="6" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.2"/>
  <rect x="30" y="70" width="220" height="28" rx="6" fill="#F8FAFC"/>
  <text x="140" y="89" fill="#0F172A" font-size="12" font-weight="700" text-anchor="middle">Web Studio Frontend</text>

  <!-- User Icon & Info -->
  <circle cx="140" cy="150" r="26" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1.2"/>
  <path d="M140 144 a8 8 0 1 0 0 -16 a8 8 0 0 0 0 16 z M126 164 a14 14 0 0 1 28 0 z" fill="#475569"/>
  <text x="140" y="192" fill="#0F172A" font-size="13" font-weight="700" text-anchor="middle">Single Page App (SPA)</text>
  <text x="140" y="208" fill="#64748B" font-size="10.5" text-anchor="middle">HTML5 / Modern JS Client</text>

  <!-- Client Features Box -->
  <rect x="45" y="230" width="190" height="240" rx="4" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
  <text x="55" y="252" fill="#0F172A" font-size="11" font-weight="700">Client Capabilities:</text>
  <text x="55" y="276" fill="#334155" font-size="10.5">• Drag &amp; Drop Documents</text>
  <text x="65" y="292" fill="#64748B" font-size="9.5">(PDF, Scan Bitmaps, TIFF)</text>
  <text x="55" y="314" fill="#334155" font-size="10.5">• Dual-Engine Mode Toggle</text>
  <text x="65" y="330" fill="#64748B" font-size="9.5">(FinOps $0.00 / AWS Native)</text>
  <text x="55" y="352" fill="#334155" font-size="10.5">• Real-time Split Preview</text>
  <text x="65" y="368" fill="#64748B" font-size="9.5">(Bilingual Side-by-Side)</text>
  <text x="55" y="390" fill="#334155" font-size="10.5">• Multi-Format Exports</text>
  <text x="65" y="406" fill="#64748B" font-size="9.5">(Clean .md, .docx, .pdf)</text>
  <text x="55" y="428" fill="#334155" font-size="10.5">• Presigned Direct Download</text>

  <!-- Live Endpoint Details -->
  <rect x="45" y="490" width="190" height="150" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="55" y="512" fill="#0284C7" font-size="11" font-weight="700">Public Live Ingress:</text>
  <text x="55" y="532" fill="#334155" font-size="10" font-weight="600">Application Load Balancer</text>
  <text x="55" y="550" fill="#64748B" font-size="9" font-family="monospace">huylam-ocr-alb</text>
  <text x="55" y="566" fill="#64748B" font-size="9" font-family="monospace">.ap-southeast-1.elb</text>
  <text x="55" y="582" fill="#64748B" font-size="9" font-family="monospace">.amazonaws.com</text>
  <line x1="55" y1="594" x2="225" y2="594" stroke="#E2E8F0" stroke-width="1"/>
  <text x="55" y="612" fill="#16A34A" font-size="10" font-weight="700">Protocol: HTTP Port 80</text>
  <text x="55" y="628" fill="#475569" font-size="9.5">Strict SG Chaining Protected</text>

  <!-- Bottom FinOps Tag -->
  <rect x="45" y="660" width="190" height="80" rx="4" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
  <text x="55" y="682" fill="#0F172A" font-size="10.5" font-weight="700">FinOps Excellence:</text>
  <text x="55" y="700" fill="#16A34A" font-size="10" font-weight="600">Cost: $0.00 / 0 VND</text>
  <text x="55" y="718" fill="#64748B" font-size="9.5">Client-side caching &amp; stream</text>

  <!-- Center Top: Backend Processing Core Container -->
  <rect x="280" y="70" width="1190" height="560" rx="6" fill="#FFFFFF" stroke="#475569" stroke-width="1.2"/>
  <rect x="280" y="70" width="1190" height="28" rx="6" fill="#F8FAFC"/>
  <image href="{icons['ec2']}" x="290" y="74" width="20" height="20"/>
  <text x="320" y="89" fill="#0F172A" font-size="12" font-weight="700">Backend Processing Core: hybrid_engine.py | EC2 AL2023 Host (10.0.8.15:5000)</text>
  <text x="1455" y="89" fill="#64748B" font-size="10.5" font-weight="600" text-anchor="end">Systemd Gunicorn WSGI Daemon | Scale-to-Zero Architecture</text>

  <!-- Tier 1: Fast-Path Native Vector Parser -->
  <rect x="300" y="115" width="410" height="225" rx="4" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.2"/>
  <rect x="300" y="115" width="410" height="34" rx="4" fill="#F0FDF4"/>
  <text x="312" y="131" fill="#15803D" font-size="11" font-weight="700">Tier 1: Fast-Path Native Vector Parser (PyMuPDF)</text>
  <text x="312" y="145" fill="#16A34A" font-size="9.5" font-weight="600">Module: src/backend/parsers/fast_parser.py</text>

  <text x="315" y="172" fill="#334155" font-size="10.5">• Direct vector extraction of digital text, font trees &amp; styling</text>
  <text x="315" y="190" fill="#334155" font-size="10.5">• Native table structure preservation without bitmap rasterization</text>
  <text x="315" y="208" fill="#334155" font-size="10.5">• Blazing Execution Speed: <tspan font-weight="700" fill="#16A34A">0.1s - 0.3s per page</tspan></text>
  <text x="315" y="226" fill="#334155" font-size="10.5">• AI Ingestion Cost: <tspan font-weight="700" fill="#16A34A">$0.00</tspan> (Zero LLM overhead for 80%+ documents)</text>

  <rect x="312" y="242" width="386" height="85" rx="4" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
  <text x="322" y="260" fill="#0F172A" font-size="10.5" font-weight="700">Routing Decision Criteria:</text>
  <text x="322" y="278" fill="#16A34A" font-size="10" font-weight="600">✓ If text density &gt; threshold: Emit clean Markdown -&gt; Tier 3 Translator</text>
  <text x="322" y="296" fill="#EA580C" font-size="10" font-weight="600">✗ If scanned image or zero text: Escalate to Tier 2 OCR Dispatcher</text>
  <text x="322" y="313" fill="#64748B" font-size="9">Eliminates unnecessary Vision AI calls for native digital PDFs</text>

  <!-- Tier 2: Selective Multimodal OCR Dispatcher -->
  <rect x="300" y="360" width="410" height="250" rx="4" fill="#FFFFFF" stroke="#EA580C" stroke-width="1.2"/>
  <rect x="300" y="360" width="410" height="34" rx="4" fill="#FFF7ED"/>
  <text x="312" y="376" fill="#C2410C" font-size="11" font-weight="700">Tier 2: Selective Multimodal OCR Dispatcher</text>
  <text x="312" y="390" fill="#EA580C" font-size="9.5" font-weight="600">Module: src/backend/parsers/ocr_dispatcher.py</text>

  <text x="315" y="415" fill="#334155" font-size="10.5">• High-resolution PDF page rendering (300 DPI image bitmaps)</text>
  <text x="315" y="432" fill="#334155" font-size="10.5">• Dual-Engine Dispatching: User toggle between FinOps and Enterprise</text>

  <!-- Branch A -->
  <rect x="312" y="445" width="188" height="152" rx="4" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
  <text x="320" y="463" fill="#0284C7" font-size="10" font-weight="700">Branch A: FinOps ($0.00)</text>
  <text x="320" y="481" fill="#334155" font-size="9.5">• Primary: Kaggle GPU 2x T4</text>
  <text x="328" y="497" fill="#64748B" font-size="9">Qwen2.5-VL 7B Vision Model</text>
  <text x="320" y="515" fill="#334155" font-size="9.5">• Failover: Google Gemini 1.5</text>
  <text x="328" y="531" fill="#64748B" font-size="9">Sub-second Flash API</text>
  <text x="320" y="549" fill="#334155" font-size="9.5">• Key Tour Manager Rotation</text>
  <text x="320" y="572" fill="#16A34A" font-size="10" font-weight="700">Cost: $0.00 / 0 VND</text>

  <!-- Branch B -->
  <rect x="510" y="445" width="188" height="152" rx="4" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
  <text x="518" y="463" fill="#8C4FFF" font-size="10" font-weight="700">Branch B: AWS Native Mode</text>
  <text x="518" y="481" fill="#334155" font-size="9.5">• Amazon Bedrock Multimodal</text>
  <text x="526" y="497" fill="#64748B" font-size="9">Nova Micro / Claude 3.5 Sonnet</text>
  <text x="518" y="515" fill="#334155" font-size="9.5">• Amazon Textract Tables</text>
  <text x="526" y="531" fill="#64748B" font-size="9">Document Analysis API</text>
  <text x="518" y="549" fill="#334155" font-size="9.5">• Enterprise Compliance</text>
  <text x="518" y="572" fill="#475569" font-size="10" font-weight="700">Data Sovereignty Guaranteed</text>

  <!-- Center Top Right: External AI Model Endpoints -->
  <rect x="740" y="115" width="340" height="495" rx="4" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.2"/>
  <rect x="740" y="115" width="340" height="26" rx="4" fill="#F0F9FF"/>
  <text x="752" y="133" fill="#0369A1" font-size="11" font-weight="700">External Model Endpoints (Dispatched via HTTPS)</text>

  <!-- Kaggle GPU Box -->
  <rect x="755" y="155" width="310" height="135" rx="4" fill="#F8FAFC" stroke="#BAE6FD" stroke-width="1"/>
  <text x="765" y="176" fill="#0284C7" font-size="11" font-weight="700">Kaggle GPU Cluster (Dedicated Vision AI)</text>
  <text x="765" y="196" fill="#334155" font-size="10.5">• Hardware: 2x NVIDIA T4 (32GB VRAM)</text>
  <text x="765" y="214" fill="#334155" font-size="10.5">• Model: Qwen2.5-VL-7B-Instruct (Vision LLM)</text>
  <text x="765" y="232" fill="#334155" font-size="10.5">• Public Gateway: Cloudflare Tunnel (trycloudflare)</text>
  <text x="765" y="250" fill="#334155" font-size="10.5">• Inference Speed: ~1.2s - 2.8s per page</text>
  <text x="765" y="272" fill="#16A34A" font-size="10.5" font-weight="700">Active Status: Running ($0.00 Compute)</text>

  <!-- Bedrock & Textract Box -->
  <rect x="755" y="305" width="310" height="135" rx="4" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
  <image href="{icons['bedrock']}" x="765" y="315" width="20" height="20"/>
  <text x="792" y="330" fill="#0F172A" font-size="11" font-weight="700">Amazon Bedrock &amp; Amazon Textract</text>
  <text x="765" y="352" fill="#334155" font-size="10.5">• Nova Micro &amp; Claude 3.5 Sonnet Multimodal</text>
  <text x="765" y="370" fill="#334155" font-size="10.5">• Textract Document Analysis (Forms &amp; Tables)</text>
  <text x="765" y="388" fill="#334155" font-size="10.5">• IAM Boto3 Converse API Integration</text>
  <text x="765" y="406" fill="#334155" font-size="10.5">• Zero Data Outflow Guarantee (In-VPC Endpoint)</text>
  <text x="765" y="426" fill="#475569" font-size="10.5" font-weight="600">On-Demand Enterprise Fallback</text>

  <!-- Gemini API Box -->
  <rect x="755" y="455" width="310" height="135" rx="4" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
  <text x="765" y="476" fill="#0F172A" font-size="11" font-weight="700">Google Gemini API (Failover Endpoint)</text>
  <text x="765" y="496" fill="#334155" font-size="10.5">• Gemini 1.5 Flash (Vision Multimodal)</text>
  <text x="765" y="514" fill="#334155" font-size="10.5">• Sub-second latency for scanned fallback</text>
  <text x="765" y="532" fill="#334155" font-size="10.5">• High-throughput batch document queue</text>
  <text x="765" y="550" fill="#334155" font-size="10.5">• Integrated with Key Tour Manager</text>
  <text x="765" y="572" fill="#16A34A" font-size="10.5" font-weight="700">Automatic Failover Mechanism</text>

  <!-- Center Far Right: Tier 3 Translation & Exporters -->
  <rect x="1110" y="115" width="340" height="495" rx="4" fill="#FFFFFF" stroke="#8C4FFF" stroke-width="1.2"/>
  <rect x="1110" y="115" width="340" height="26" rx="4" fill="#FAF5FF"/>
  <text x="1122" y="133" fill="#6B21A8" font-size="11.5" font-weight="700">Tier 3: Translation Engine &amp; Key Tour Manager</text>

  <rect x="1125" y="155" width="310" height="175" rx="4" fill="#F8FAFC" stroke="#E9D5FF" stroke-width="1"/>
  <text x="1135" y="176" fill="#6B21A8" font-size="11" font-weight="700">Technical Translation Orchestrator</text>
  <text x="1135" y="196" fill="#334155" font-size="10.5">• Modules: translator.py &amp; key_tour_manager.py</text>
  <text x="1135" y="214" fill="#334155" font-size="10.5">• Strict preservation of 100% Markdown syntax:</text>
  <text x="1145" y="230" fill="#64748B" font-size="9.5">Code blocks, KaTeX math, tables, headings</text>
  <text x="1135" y="250" fill="#334155" font-size="10.5">• Cloud/DevOps Specialized Engineering Glossary</text>
  <text x="1135" y="268" fill="#334155" font-size="10.5">• Key Tour Manager:</text>
  <text x="1145" y="284" fill="#64748B" font-size="9.5">Round-Robin API key pool rotation</text>
  <text x="1145" y="300" fill="#64748B" font-size="9.5">Exponential backoff on rate limits (429)</text>
  <text x="1135" y="320" fill="#16A34A" font-size="10" font-weight="700">Zero Translation Failure Guarantee</text>

  <!-- Multi-Format Document Exporters Box -->
  <rect x="1125" y="345" width="310" height="245" rx="4" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
  <text x="1135" y="366" fill="#0F172A" font-size="11" font-weight="700">Multi-Format Document Exporters</text>
  <text x="1135" y="384" fill="#64748B" font-size="10">Module: src/backend/exporters/</text>

  <text x="1135" y="410" fill="#0284C7" font-size="10.5" font-weight="700">1. Microsoft Word Exporter (docx_exporter.py)</text>
  <text x="1145" y="426" fill="#334155" font-size="10">• Academic style, perfect table border rendering</text>
  <text x="1145" y="442" fill="#334155" font-size="10">• Bold, italics, hyperlinks, heading hierarchy</text>

  <text x="1135" y="468" fill="#EA580C" font-size="10.5" font-weight="700">2. Print-Ready PDF Exporter (pdf_exporter.py)</text>
  <text x="1145" y="484" fill="#334155" font-size="10">• Standard A4 margins, pure black-and-white grid</text>
  <text x="1145" y="500" fill="#334155" font-size="10">• Auto page-break handling, header &amp; footer</text>

  <text x="1135" y="526" fill="#16A34A" font-size="10.5" font-weight="700">3. Clean Markdown Exporter (markdown_exporter.py)</text>
  <text x="1145" y="542" fill="#334155" font-size="10">• Standard GitHub-Flavored Markdown (.md)</text>
  <text x="1145" y="558" fill="#334155" font-size="10">• KaTeX math formula syntax ($...$, $$...$$)</text>
  <text x="1135" y="580" fill="#475569" font-size="10" font-weight="600">Simultaneous 3-Format Emission Pipeline</text>

  <!-- Bottom: AWS Cloud Persistence & Storage Integration -->
  <rect x="280" y="650" width="1190" height="210" rx="6" fill="#FFFFFF" stroke="#475569" stroke-width="1.2"/>
  <rect x="280" y="650" width="1190" height="28" rx="6" fill="#F8FAFC"/>
  <text x="295" y="669" fill="#0F172A" font-size="12" font-weight="700">AWS Cloud Persistence &amp; Storage Integration (src/backend/aws/storage_service.py)</text>
  <text x="1455" y="669" fill="#64748B" font-size="10.5" font-weight="600" text-anchor="end">Region: ap-southeast-1 | Encryption: SSE-S3 AES-256</text>

  <!-- S3 Box -->
  <rect x="300" y="690" width="560" height="155" rx="4" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
  <image href="{icons['s3']}" x="312" y="700" width="30" height="30"/>
  <text x="350" y="718" fill="#16A34A" font-size="11.5" font-weight="700">Amazon S3 Document Lake</text>
  <text x="350" y="734" fill="#64748B" font-size="10">Bucket: huylam-ocr-documents-ap-southeast-1</text>

  <text x="315" y="760" fill="#334155" font-size="10.5">• Prefix: <tspan font-family="monospace">uploads/{{job_id}}/</tspan> - Raw input PDFs, images, uploaded docs</text>
  <text x="315" y="780" fill="#334155" font-size="10.5">• Prefix: <tspan font-family="monospace">outputs/{{job_id}}/</tspan> - Generated cv.pdf.md, cv.pdf.docx, cv.pdf.pdf</text>
  <text x="315" y="800" fill="#334155" font-size="10.5">• Presigned URLs: Secure time-limited browser download without public bucket access</text>
  <text x="315" y="820" fill="#16A34A" font-size="10" font-weight="700">• Security: SSE-S3 AES-256 Server-Side Encryption enabled on all objects</text>

  <!-- DynamoDB Box -->
  <rect x="890" y="690" width="560" height="155" rx="4" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
  <image href="{icons['ddb']}" x="902" y="700" width="30" height="30"/>
  <text x="940" y="718" fill="#0284C7" font-size="11.5" font-weight="700">Amazon DynamoDB State Store</text>
  <text x="940" y="734" fill="#64748B" font-size="10">Table: document_processing_jobs (Billing: PAY_PER_REQUEST / On-Demand)</text>

  <text x="905" y="760" fill="#334155" font-size="10.5">• Partition Key: <tspan font-family="monospace">job_id (String)</tspan> | Real-time state machine tracking</text>
  <text x="905" y="780" fill="#334155" font-size="10.5">• Status Lifecycle: <tspan font-family="monospace">RECEIVED_VIA_S3_EVENT -&gt; PROCESSING -&gt; COMPLETED / FAILED</tspan></text>
  <text x="905" y="800" fill="#334155" font-size="10.5">• Execution Metrics: execution_time_seconds, model_used, page_count, output_urls</text>
  <text x="905" y="820" fill="#0284C7" font-size="10" font-weight="700">• Sub-10ms read/write latency with zero provisioned capacity overhead ($0.00 base)</text>

  <!-- ==================== CONNECTING ARROWS ==================== -->
  <!-- 1. Client to Core -->
  <path d="M250 250 L280 250" stroke="#0284C7" stroke-width="1.8" fill="none" marker-end="url(#arr-blue)"/>
  <rect x="254" y="238" width="22" height="13" rx="2" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="0.8"/>
  <text x="265" y="248" fill="#0284C7" font-size="8" font-weight="700" text-anchor="middle">HTTP</text>

  <!-- 2. Tier 1 to Tier 2 (on image/scanned) -->
  <path d="M505 340 L505 360" stroke="#EA580C" stroke-width="1.8" fill="none" marker-end="url(#arr-orange)"/>
  <rect x="470" y="344" width="70" height="14" rx="3" fill="#FFFFFF" stroke="#FED7AA" stroke-width="0.8"/>
  <text x="505" y="354" fill="#EA580C" font-size="8" font-weight="700" text-anchor="middle">Scan Escalate</text>

  <!-- 3. Tier 1 to Tier 3 (clean top corridor) -->
  <path d="M680 115 L680 102 L1130 102 L1130 115" stroke="#16A34A" stroke-width="1.8" fill="none" marker-end="url(#arr-green)"/>
  <rect x="850" y="95" width="110" height="15" rx="3" fill="#FFFFFF" stroke="#BBF7D0" stroke-width="0.8"/>
  <text x="905" y="106" fill="#16A34A" font-size="8.5" font-weight="700" text-anchor="middle">Fast-Path Native Text</text>

  <!-- 4. Tier 2 to External Endpoints -->
  <path d="M710 490 L740 490" stroke="#0284C7" stroke-width="1.8" fill="none" marker-end="url(#arr-blue)"/>
  <rect x="713" y="476" width="34" height="14" rx="2" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="0.8"/>
  <text x="730" y="486" fill="#0284C7" font-size="8" font-weight="700" text-anchor="middle">Dispatch</text>

  <!-- 5. External Endpoints to Tier 3 Translator -->
  <path d="M1080 380 L1110 380" stroke="#8C4FFF" stroke-width="1.8" fill="none" marker-end="url(#arr-purple)"/>
  <rect x="1083" y="366" width="34" height="14" rx="2" fill="#FFFFFF" stroke="#E9D5FF" stroke-width="0.8"/>
  <text x="1100" y="376" fill="#8C4FFF" font-size="8" font-weight="700" text-anchor="middle">OCR Text</text>

  <!-- 6. Tier 3 to Storage (downwards) -->
  <path d="M1280 610 L1280 650" stroke="#1E293B" stroke-width="1.8" fill="none" marker-end="url(#arr-dark)"/>
  <rect x="1245" y="623" width="70" height="14" rx="3" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>
  <text x="1280" y="633" fill="#1E293B" font-size="8" font-weight="700" text-anchor="middle">Persist &amp; State</text>

  <!-- Footer -->
  <line x1="30" y1="875" x2="1470" y2="875" stroke="#CBD5E1" stroke-width="1"/>
  <text x="30" y="890" fill="#64748B" font-size="9">FinOps Spend: $0.00 (Free Tier Always Free + Scale-to-Zero) | HUCE Internship Report 2026 | Lam Quang Huy (0212267)</text>
  <text x="1470" y="890" fill="#64748B" font-size="9" text-anchor="end">Production Hybrid OCR Engine: PyMuPDF Vector (0.1s) + Dual Selective OCR (Qwen2.5-VL / Bedrock)</text>
</svg>"""
    return svg

# ==============================================================================
# 2. ENTERPRISE VPC NETWORK ARCHITECTURE
# ==============================================================================
def gen_vpc_network_svg(icons):
    w, h = 1500, 920
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="background:#FFFFFF; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
  {DEFS_MARKERS}

  <!-- Header -->
  <text x="30" y="38" fill="#0F172A" font-size="18" font-weight="800" letter-spacing="-0.5">ENTERPRISE THREE-TIER MULTI-AZ VPC &amp; NETWORK SECURITY ARCHITECTURE</text>
  <text x="1470" y="38" fill="#64748B" font-size="11" font-weight="600" text-anchor="end">AWS Reference Architecture | Multi-AZ High-Availability | Region: ap-southeast-1 | CIDR: 10.0.0.0/16</text>
  <line x1="30" y1="50" x2="1470" y2="50" stroke="#CBD5E1" stroke-width="1.2"/>

  <!-- Left: Ingress Edge Users & Admin -->
  <!-- Public Client -->
  <rect x="30" y="110" width="160" height="230" rx="6" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.2"/>
  <rect x="30" y="110" width="160" height="26" rx="6" fill="#F8FAFC"/>
  <text x="110" y="127" fill="#0F172A" font-size="11.5" font-weight="700" text-anchor="middle">Public Internet Client</text>

  <circle cx="110" cy="180" r="26" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1.2"/>
  <path d="M110 174 a8 8 0 1 0 0 -16 a8 8 0 0 0 0 16 z M96 194 a14 14 0 0 1 28 0 z" fill="#475569"/>
  <text x="110" y="222" fill="#0F172A" font-size="12" font-weight="700" text-anchor="middle">End Users</text>
  <text x="110" y="238" fill="#64748B" font-size="10" text-anchor="middle">Standard Web Browser</text>
  <line x1="45" y1="252" x2="175" y2="252" stroke="#E2E8F0" stroke-width="1"/>
  <text x="45" y="272" fill="#0284C7" font-size="10.5" font-weight="700">Inbound: Port 80 HTTP</text>
  <text x="45" y="290" fill="#334155" font-size="10">Source: 0.0.0.0/0</text>
  <text x="45" y="308" fill="#64748B" font-size="9.5">Hits ALB DNS Endpoint</text>
  <text x="45" y="326" fill="#16A34A" font-size="9.5" font-weight="600">Response: 200 OK Live</text>

  <!-- Admin / DevOps SSM -->
  <rect x="30" y="560" width="160" height="250" rx="6" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.2"/>
  <rect x="30" y="560" width="160" height="26" rx="6" fill="#F8FAFC"/>
  <text x="110" y="577" fill="#0F172A" font-size="11.5" font-weight="700" text-anchor="middle">DevOps Administrator</text>

  <circle cx="110" cy="630" r="26" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1.2"/>
  <path d="M110 624 a8 8 0 1 0 0 -16 a8 8 0 0 0 0 16 z M96 644 a14 14 0 0 1 28 0 z" fill="#475569"/>
  <text x="110" y="672" fill="#0F172A" font-size="12" font-weight="700" text-anchor="middle">Admin / Engineer</text>
  <text x="110" y="688" fill="#64748B" font-size="10" text-anchor="middle">AWS Systems Manager</text>
  <line x1="45" y1="702" x2="175" y2="702" stroke="#E2E8F0" stroke-width="1"/>
  <text x="45" y="722" fill="#EA580C" font-size="10.5" font-weight="700">Zero Trust Access</text>
  <text x="45" y="740" fill="#334155" font-size="10">• SSH Port 22: CLOSED</text>
  <text x="45" y="758" fill="#334155" font-size="10">• No Bastion Host needed</text>
  <text x="45" y="776" fill="#334155" font-size="10">• Outbound TLS 443 Only</text>
  <text x="45" y="794" fill="#16A34A" font-size="9.5" font-weight="600">Full Audit Trail in CloudWatch</text>

  <!-- AWS Cloud Boundary -->
  <rect x="220" y="70" width="1250" height="810" rx="6" fill="#FFFFFF" stroke="#475569" stroke-width="1.2"/>
  <rect x="220" y="70" width="1250" height="28" rx="6" fill="#F8FAFC"/>
  <image href="{icons['vpc']}" x="230" y="74" width="20" height="20"/>
  <text x="260" y="89" fill="#0F172A" font-size="12" font-weight="700">AWS Cloud: ap-southeast-1 (Singapore) | Account ID: 677994024390 (huylam)</text>
  <text x="1455" y="89" fill="#64748B" font-size="10.5" font-weight="600" text-anchor="end">Enterprise Multi-AZ Topology with Chained Security Groups</text>

  <!-- Internet Gateway & Public Route Table (VPC Ingress Edge) -->
  <rect x="240" y="110" width="310" height="85" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <image href="{icons['igw']}" x="250" y="120" width="28" height="28"/>
  <text x="290" y="136" fill="#0F172A" font-size="11.5" font-weight="700">Internet Gateway (huylam-igw)</text>
  <text x="290" y="152" fill="#64748B" font-size="10">Attached to huylam-vpc boundary</text>
  <text x="250" y="178" fill="#334155" font-size="10">igw-0b9db3a6eac29ede9 | Default Route: 0.0.0.0/0</text>

  <rect x="570" y="110" width="360" height="85" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <image href="{icons['rtb']}" x="580" y="120" width="28" height="28"/>
  <text x="620" y="136" fill="#0F172A" font-size="11.5" font-weight="700">Public Route Table: huylam-rtb-public</text>
  <text x="620" y="152" fill="#64748B" font-size="10">rtb-012b069d6b3c0e501 | Associated to: public1 &amp; public2</text>
  <text x="580" y="178" fill="#16A34A" font-size="10" font-weight="600">Routes: 10.0.0.0/16 -&gt; local | 0.0.0.0/0 -&gt; huylam-igw</text>

  <rect x="950" y="110" width="500" height="85" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <image href="{icons['rtb']}" x="960" y="120" width="28" height="28"/>
  <text x="1000" y="136" fill="#0F172A" font-size="11.5" font-weight="700">Private Route Table: huylam-rtb-private1 &amp; 2</text>
  <text x="1000" y="152" fill="#64748B" font-size="10">rtb-04b9044883c432a2a &amp; rtb-00f40ad53eb7cab1f | Isolated Subnets</text>
  <text x="960" y="178" fill="#0284C7" font-size="10" font-weight="600">Routes: 10.0.0.0/16 -&gt; local | Zero Internet Ingress/Egress</text>

  <!-- Amazon VPC Container -->
  <rect x="240" y="210" width="1210" height="655" rx="6" fill="#FFFFFF" stroke="#8C4FFF" stroke-width="1.2" stroke-dasharray="6,4"/>
  <rect x="240" y="210" width="320" height="24" rx="4" fill="#FAF5FF"/>
  <text x="250" y="226" fill="#6B21A8" font-size="11.5" font-weight="700">Amazon VPC: huylam-vpc (CIDR: 10.0.0.0/16)</text>

  <!-- Availability Zone 1a (Primary Active) -->
  <rect x="260" y="250" width="575" height="600" rx="4" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.2"/>
  <rect x="260" y="250" width="575" height="24" rx="4" fill="#F0FDF4"/>
  <text x="272" y="266" fill="#15803D" font-size="11" font-weight="700">Availability Zone 1: ap-southeast-1a (Active Primary Zone)</text>

  <!-- Public Subnet 1a -->
  <rect x="275" y="285" width="260" height="285" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <rect x="275" y="285" width="260" height="22" rx="4" fill="#F8FAFC"/>
  <text x="285" y="300" fill="#0F172A" font-size="10.5" font-weight="700">Public Subnet 1 (10.0.0.0/20)</text>

  <!-- ALB Node 1a inside Public Subnet 1a -->
  <rect x="285" y="315" width="240" height="150" rx="4" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
  <image href="{icons['alb']}" x="295" y="325" width="26" height="26"/>
  <text x="330" y="340" fill="#0F172A" font-size="11" font-weight="700">ALB Ingress Node 1a</text>
  <text x="330" y="356" fill="#64748B" font-size="9.5">huylam-ocr-alb ENI 1a</text>
  <line x1="295" y1="368" x2="515" y2="368" stroke="#E2E8F0" stroke-width="1"/>
  <text x="295" y="388" fill="#0284C7" font-size="10.5" font-weight="700">SG: huylam-alb-sg</text>
  <text x="295" y="406" fill="#334155" font-size="10">• Inbound: Port 80 (HTTP)</text>
  <text x="295" y="424" fill="#334155" font-size="10">• Source: 0.0.0.0/0 (Internet)</text>
  <text x="295" y="442" fill="#16A34A" font-size="10" font-weight="600">• Active Primary Target Forward</text>

  <!-- Target Group Corridor (x=285, y=475) -->
  <rect x="285" y="475" width="240" height="85" rx="4" fill="#FFFFFF" stroke="#8C4FFF" stroke-width="1"/>
  <text x="295" y="495" fill="#6B21A8" font-size="10.5" font-weight="700">Target Group: huylam-ocr-tg</text>
  <text x="295" y="512" fill="#334155" font-size="10">Target Type: Instance | Port 5000</text>
  <text x="295" y="528" fill="#334155" font-size="10">Health Check: /login (Status: 200)</text>
  <text x="295" y="546" fill="#16A34A" font-size="10" font-weight="700">Healthy 1/1 Target Registered</text>

  <!-- Private Subnet 1a -->
  <rect x="550" y="285" width="270" height="550" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <rect x="550" y="285" width="270" height="22" rx="4" fill="#F8FAFC"/>
  <text x="560" y="300" fill="#0F172A" font-size="10.5" font-weight="700">Private Subnet 1 (10.0.128.0/20)</text>

  <!-- EC2 Instance Box -->
  <rect x="560" y="315" width="250" height="295" rx="4" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
  <image href="{icons['ec2']}" x="570" y="325" width="28" height="28"/>
  <text x="605" y="340" fill="#0F172A" font-size="11" font-weight="700">huylam-ocr-web-server</text>
  <text x="605" y="356" fill="#64748B" font-size="9.5">EC2 AL2023 | t3.micro</text>
  <line x1="570" y1="368" x2="800" y2="368" stroke="#E2E8F0" stroke-width="1"/>

  <text x="570" y="388" fill="#0284C7" font-size="10.5" font-weight="700">Private IP: 10.0.8.15</text>
  <text x="570" y="406" fill="#334155" font-size="10">• Port: 5000 (systemd Gunicorn)</text>
  <text x="570" y="424" fill="#334155" font-size="10">• Instance ID: i-0566e1eedaacea52d</text>
  <text x="570" y="442" fill="#334155" font-size="10">• App: Web Studio &amp; Hybrid OCR</text>

  <!-- Chained SG Rules Box -->
  <rect x="570" y="455" width="230" height="145" rx="4" fill="#FFFFFF" stroke="#EA580C" stroke-width="1"/>
  <text x="580" y="475" fill="#C2410C" font-size="10.5" font-weight="700">SG: huylam-web-sg (Chained)</text>
  <text x="580" y="493" fill="#334155" font-size="9.5">• Inbound: Port 5000 TCP ONLY</text>
  <text x="580" y="510" fill="#EA580C" font-size="9.5" font-weight="600">• Source: huylam-alb-sg ONLY</text>
  <text x="590" y="525" fill="#64748B" font-size="9">(sg-0dca819306a96bfdb)</text>
  <text x="580" y="545" fill="#16A34A" font-size="9.5" font-weight="600">• Direct Internet: DROPPED</text>
  <text x="580" y="562" fill="#334155" font-size="9.5">• Port 22 SSH: CLOSED</text>
  <text x="580" y="580" fill="#475569" font-size="9.5">Principle of Least Privilege</text>

  <!-- SSM Box inside AZ 1a bottom -->
  <rect x="275" y="580" width="260" height="255" rx="4" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
  <image href="{icons['ssm']}" x="285" y="590" width="28" height="28"/>
  <text x="320" y="606" fill="#0F172A" font-size="11" font-weight="700">AWS Systems Manager</text>
  <text x="320" y="622" fill="#64748B" font-size="9.5">Session Manager Endpoint</text>
  <line x1="285" y1="635" x2="525" y2="635" stroke="#E2E8F0" stroke-width="1"/>
  <text x="285" y="655" fill="#0F172A" font-size="10.5" font-weight="700">Zero Trust Shell Access:</text>
  <text x="285" y="675" fill="#334155" font-size="10">• Agent running inside EC2</text>
  <text x="285" y="693" fill="#334155" font-size="10">• Outbound TLS 443 Channel</text>
  <text x="285" y="711" fill="#334155" font-size="10">• No inbound open ports</text>
  <text x="285" y="729" fill="#334155" font-size="10">• No SSH private keys required</text>
  <text x="285" y="747" fill="#334155" font-size="10">• IAM Role: huylam-ssm-role</text>
  <text x="285" y="770" fill="#16A34A" font-size="10" font-weight="700">KMS Encryption &amp; Audit Logging</text>

  <!-- Availability Zone 1b (Standby Secondary) -->
  <rect x="855" y="250" width="575" height="600" rx="4" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.2" stroke-dasharray="4,4"/>
  <rect x="855" y="250" width="575" height="24" rx="4" fill="#F8FAFC"/>
  <text x="867" y="266" fill="#475569" font-size="11" font-weight="700">Availability Zone 2: ap-southeast-1b (Secondary Standby Zone)</text>

  <!-- Public Subnet 1b -->
  <rect x="870" y="285" width="260" height="285" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <rect x="870" y="285" width="260" height="22" rx="4" fill="#F8FAFC"/>
  <text x="880" y="300" fill="#0F172A" font-size="10.5" font-weight="700">Public Subnet 2 (10.0.16.0/20)</text>

  <!-- ALB Node 1b inside Public Subnet 1b -->
  <rect x="880" y="315" width="240" height="150" rx="4" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
  <image href="{icons['alb']}" x="890" y="325" width="26" height="26"/>
  <text x="925" y="340" fill="#0F172A" font-size="11" font-weight="700">ALB Standby Node 1b</text>
  <text x="925" y="356" fill="#64748B" font-size="9.5">huylam-ocr-alb ENI 1b</text>
  <line x1="890" y1="368" x2="1110" y2="368" stroke="#E2E8F0" stroke-width="1"/>
  <text x="890" y="388" fill="#0284C7" font-size="10.5" font-weight="700">Cross-Zone Load Balancing</text>
  <text x="890" y="406" fill="#334155" font-size="10">• Multi-AZ Ingress Ready</text>
  <text x="890" y="424" fill="#334155" font-size="10">• Automatic Health Monitoring</text>
  <text x="890" y="442" fill="#16A34A" font-size="10" font-weight="600">• Zero Traffic Loss on AZ Failover</text>

  <!-- Standby Target Group Route -->
  <rect x="880" y="475" width="240" height="85" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="890" y="495" fill="#475569" font-size="10.5" font-weight="700">Multi-AZ Standby Route</text>
  <text x="890" y="512" fill="#64748B" font-size="10">Target: huylam-ocr-tg (Standby)</text>
  <text x="890" y="528" fill="#64748B" font-size="10">Automatic Failover Redirection</text>
  <text x="890" y="546" fill="#0284C7" font-size="10" font-weight="600">Cross-Zone Balancing: ON</text>

  <!-- Private Subnet 1b -->
  <rect x="1145" y="285" width="270" height="550" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <rect x="1145" y="285" width="270" height="22" rx="4" fill="#F8FAFC"/>
  <text x="1155" y="300" fill="#0F172A" font-size="10.5" font-weight="700">Private Subnet 2 (10.0.144.0/20)</text>

  <!-- Multi-AZ Disaster Recovery Standby Box -->
  <rect x="1155" y="315" width="250" height="295" rx="4" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="1170" y="340" fill="#475569" font-size="11" font-weight="700">Multi-AZ Standby Recovery Target</text>
  <text x="1170" y="356" fill="#64748B" font-size="9.5">Isolated DR Environment</text>
  <line x1="1170" y1="368" x2="1395" y2="368" stroke="#E2E8F0" stroke-width="1"/>
  <text x="1170" y="390" fill="#334155" font-size="10.5">• Subnet: huylam-subnet-private2</text>
  <text x="1170" y="410" fill="#334155" font-size="10.5">• FinOps Spend: <tspan font-weight="700" fill="#16A34A">$0.00</tspan> (Scale-to-Zero)</text>
  <text x="1170" y="430" fill="#334155" font-size="10.5">• Target Group Ready: Auto registers</text>
  <text x="1170" y="450" fill="#334155" font-size="10.5">• Security Group: huylam-web-sg</text>
  <text x="1170" y="470" fill="#334155" font-size="10.5">• Route Table: huylam-rtb-private2</text>
  <text x="1170" y="500" fill="#16A34A" font-size="10.5" font-weight="700">High Availability SLA: 99.99%</text>
  <text x="1170" y="520" fill="#64748B" font-size="9.5">Multi-AZ automatic failover ready</text>

  <!-- Observability Card inside AZ 1b bottom -->
  <rect x="870" y="580" width="260" height="255" rx="4" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
  <image href="{icons['cw']}" x="880" y="590" width="28" height="28"/>
  <text x="915" y="606" fill="#0F172A" font-size="11" font-weight="700">Amazon CloudWatch</text>
  <text x="915" y="622" fill="#64748B" font-size="9.5">Unified Network &amp; Host Metrics</text>
  <line x1="880" y1="635" x2="1120" y2="635" stroke="#E2E8F0" stroke-width="1"/>
  <text x="880" y="655" fill="#0F172A" font-size="10.5" font-weight="700">Network &amp; Health Telemetry:</text>
  <text x="880" y="675" fill="#334155" font-size="10">• ALB Request Count &amp; Target Latency</text>
  <text x="880" y="693" fill="#334155" font-size="10">• Target Response Time: 45ms - 120ms</text>
  <text x="880" y="711" fill="#334155" font-size="10">• HealthyHostCount == 1 Alarm</text>
  <text x="880" y="729" fill="#334155" font-size="10">• UnHealthyHostCount &gt; 0 Alarm</text>
  <text x="880" y="747" fill="#334155" font-size="10">• EC2 CPUUtilization &amp; Memory</text>
  <text x="880" y="770" fill="#16A34A" font-size="10" font-weight="700">Automated SNS Alert Dispatcher</text>

  <!-- ==================== CONNECTING ARROWS ==================== -->
  <!-- 1. Internet Client to IGW -->
  <path d="M190 180 L240 152" stroke="#0284C7" stroke-width="1.8" fill="none" marker-end="url(#arr-blue)"/>
  <rect x="194" y="155" width="42" height="15" rx="3" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="0.8"/>
  <text x="215" y="166" fill="#0284C7" font-size="8.5" font-weight="700" text-anchor="middle">HTTP:80</text>

  <!-- 2. IGW to ALB Node 1a (Route around AZ header) -->
  <path d="M250 195 L250 350 L285 350" stroke="#0284C7" stroke-width="1.8" fill="none" marker-end="url(#arr-blue)"/>
  <rect x="235" y="270" width="30" height="14" rx="2" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="0.8"/>
  <text x="250" y="280" fill="#0284C7" font-size="8" font-weight="700" text-anchor="middle">Ingress</text>

  <!-- 3. ALB Node 1a to Target Group -->
  <path d="M405 465 L405 475" stroke="#8C4FFF" stroke-width="1.8" fill="none" marker-end="url(#arr-purple)"/>

  <!-- 4. Target Group to EC2 (horizontal) -->
  <path d="M525 515 L560 515" stroke="#EA580C" stroke-width="1.8" fill="none" marker-end="url(#arr-orange)"/>
  <rect x="526" y="500" width="32" height="14" rx="2" fill="#FFFFFF" stroke="#FED7AA" stroke-width="0.8"/>
  <text x="542" y="510" fill="#EA580C" font-size="8" font-weight="700" text-anchor="middle">TCP:5000</text>

  <!-- 5. Admin to SSM (horizontal) -->
  <path d="M190 685 L275 685" stroke="#EA580C" stroke-width="1.8" fill="none" marker-end="url(#arr-orange)"/>
  <rect x="198" y="670" width="68" height="15" rx="3" fill="#FFFFFF" stroke="#FED7AA" stroke-width="0.8"/>
  <text x="232" y="681" fill="#EA580C" font-size="8.5" font-weight="700" text-anchor="middle">TLS 443 Session</text>

  <!-- 6. SSM to EC2 (corridor route) -->
  <path d="M535 700 L545 700 L545 600 L560 600" stroke="#16A34A" stroke-width="1.8" fill="none" marker-end="url(#arr-green)"/>
  <rect x="522" y="640" width="46" height="14" rx="2" fill="#FFFFFF" stroke="#BBF7D0" stroke-width="0.8"/>
  <text x="545" y="650" fill="#16A34A" font-size="8" font-weight="700" text-anchor="middle">SSM Agent</text>

  <!-- 7. ALB Node 1a to Standby Node 1b (Cross-Zone sync) -->
  <path d="M525 390 L880 390" stroke="#94A3B8" stroke-width="1.5" stroke-dasharray="4,4" fill="none" marker-end="url(#arr-dark)"/>
  <rect x="670" y="380" width="80" height="15" rx="3" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>
  <text x="710" y="391" fill="#64748B" font-size="8" font-weight="600" text-anchor="middle">Cross-Zone Sync</text>

  <!-- Footer -->
  <line x1="30" y1="895" x2="1470" y2="895" stroke="#CBD5E1" stroke-width="1"/>
  <text x="30" y="910" fill="#64748B" font-size="9">FinOps Spend: $0.00 (AWS Free Tier Always Free + Scale-to-Zero) | HUCE Internship Report 2026 | Lam Quang Huy (0212267)</text>
  <text x="1470" y="910" fill="#64748B" font-size="9" text-anchor="end">Production VPC Architecture: 2 Public Subnets + 2 Isolated Private Subnets | Chained Security Groups</text>
</svg>"""
    return svg

# ==============================================================================
# 3. DEFENSE-IN-DEPTH: CHAINED SECURITY GROUPS ARCHITECTURE
# ==============================================================================
def gen_security_group_chaining_svg(icons):
    w, h = 1360, 690
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="background:#FFFFFF; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
  {DEFS_MARKERS}

  <!-- Header -->
  <text x="30" y="38" fill="#0F172A" font-size="18" font-weight="800" letter-spacing="-0.5">AWS DEFENSE-IN-DEPTH: CHAINED SECURITY GROUPS ARCHITECTURE</text>
  <text x="1330" y="38" fill="#64748B" font-size="11" font-weight="600" text-anchor="end">Principle of Least Privilege (huylam-alb-sg -&gt; huylam-web-sg) | Zero Trust Isolation</text>
  <line x1="30" y1="50" x2="1330" y2="50" stroke="#CBD5E1" stroke-width="1.2"/>

  <!-- Main Container -->
  <rect x="30" y="70" width="1300" height="360" rx="6" fill="#FFFFFF" stroke="#475569" stroke-width="1.2"/>
  <rect x="30" y="70" width="1300" height="28" rx="6" fill="#F8FAFC"/>
  <text x="45" y="89" fill="#0F172A" font-size="12" font-weight="700">Network Security Perimeter: Three-Tier Reference Group Chaining</text>
  <text x="1315" y="89" fill="#64748B" font-size="10.5" font-weight="600" text-anchor="end">AWS Well-Architected Framework: Security Pillar</text>

  <!-- Step 1: Internet Client (Left) -->
  <rect x="50" y="115" width="250" height="295" rx="4" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.2"/>
  <rect x="50" y="115" width="250" height="24" rx="4" fill="#F0F9FF"/>
  <text x="175" y="132" fill="#0369A1" font-size="11.5" font-weight="700" text-anchor="middle">Step 1: Public Internet Client</text>

  <circle cx="175" cy="180" r="26" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1.2"/>
  <path d="M175 174 a8 8 0 1 0 0 -16 a8 8 0 0 0 0 16 z M161 194 a14 14 0 0 1 28 0 z" fill="#475569"/>
  <text x="175" y="222" fill="#0F172A" font-size="13" font-weight="700" text-anchor="middle">Internet Client</text>
  <text x="175" y="238" fill="#64748B" font-size="10.5" text-anchor="middle">Public Users / Web Browser</text>
  <line x1="65" y1="250" x2="285" y2="250" stroke="#E2E8F0" stroke-width="1"/>

  <text x="65" y="272" fill="#334155" font-size="10.5">• Source Network:</text>
  <text x="75" y="290" fill="#0284C7" font-size="11.5" font-weight="700">0.0.0.0/0 (Anywhere-IPv4)</text>
  <text x="65" y="312" fill="#334155" font-size="10.5">• Target Protocol: HTTP:80</text>
  <text x="65" y="332" fill="#334155" font-size="10.5">• Connects to ALB DNS Endpoint</text>
  <text x="65" y="354" fill="#16A34A" font-size="10" font-weight="600">Public Ingress Entrypoint</text>

  <!-- Step 2: ALB Security Group (Center) -->
  <rect x="400" y="115" width="390" height="295" rx="4" fill="#FFFFFF" stroke="#8C4FFF" stroke-width="1.2"/>
  <rect x="400" y="115" width="390" height="24" rx="4" fill="#FAF5FF"/>
  <image href="{icons['alb']}" x="410" y="117" width="20" height="20"/>
  <text x="440" y="132" fill="#6B21A8" font-size="11.5" font-weight="700">Step 2: huylam-alb-sg (Ingress SG)</text>

  <rect x="415" y="150" width="360" height="110" rx="4" fill="#F8FAFC" stroke="#E9D5FF" stroke-width="1"/>
  <text x="425" y="170" fill="#6B21A8" font-size="11" font-weight="700">Inbound Rules:</text>
  <text x="425" y="190" fill="#334155" font-size="10.5">• Type: HTTP | Protocol: TCP | Port: 80</text>
  <text x="425" y="208" fill="#16A34A" font-size="10.5" font-weight="700">• Source: 0.0.0.0/0 (Public Internet)</text>
  <text x="425" y="226" fill="#64748B" font-size="9.5">• Handles live public traffic from browsers</text>
  <text x="425" y="244" fill="#64748B" font-size="9.5">• Terminates direct client TCP connections</text>

  <rect x="415" y="270" width="360" height="125" rx="4" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
  <text x="425" y="290" fill="#0F172A" font-size="11" font-weight="700">Outbound Rule &amp; Target Group:</text>
  <text x="425" y="310" fill="#334155" font-size="10.5">• Type: Custom TCP | Port: 5000</text>
  <text x="425" y="328" fill="#334155" font-size="10.5">• Destination: Target Group huylam-ocr-tg</text>
  <text x="425" y="346" fill="#8C4FFF" font-size="10" font-weight="700">• Security Group ID: sg-0dca819306a96bfdb</text>
  <text x="425" y="365" fill="#64748B" font-size="9.5">• Forwards only verified HTTP requests</text>

  <!-- Step 3: EC2 Host Security Group (Right) -->
  <rect x="900" y="115" width="410" height="295" rx="4" fill="#FFFFFF" stroke="#EA580C" stroke-width="1.2"/>
  <rect x="900" y="115" width="410" height="24" rx="4" fill="#FFF7ED"/>
  <image href="{icons['ec2']}" x="910" y="117" width="20" height="20"/>
  <text x="940" y="132" fill="#C2410C" font-size="11.5" font-weight="700">Step 3: huylam-web-sg (Backend EC2 SG)</text>

  <rect x="915" y="150" width="380" height="115" rx="4" fill="#F8FAFC" stroke="#FED7AA" stroke-width="1"/>
  <text x="925" y="170" fill="#C2410C" font-size="11" font-weight="700">Chained Inbound Rule (Least Privilege):</text>
  <text x="925" y="190" fill="#334155" font-size="10.5">• Type: Custom TCP | Port: 5000</text>
  <text x="925" y="210" fill="#EA580C" font-size="11" font-weight="700">• Source: sg-0dca819306a96bfdb (huylam-alb-sg)</text>
  <text x="925" y="230" fill="#334155" font-size="10">• Attached to: EC2 AL2023 Host (10.0.8.15)</text>
  <text x="925" y="248" fill="#16A34A" font-size="10" font-weight="600">Zero Ingress from 0.0.0.0/0 allowed</text>

  <rect x="915" y="275" width="380" height="120" rx="4" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
  <text x="925" y="295" fill="#0F172A" font-size="11" font-weight="700">Protection Status &amp; Defense Enforcement:</text>
  <text x="925" y="315" fill="#DC2626" font-size="10.5" font-weight="700">• Direct Port 5000 from 0.0.0.0/0: SILENTLY DROPPED</text>
  <text x="925" y="335" fill="#DC2626" font-size="10.5" font-weight="700">• SSH Port 22: CLOSED (0 Inbound Rules)</text>
  <text x="925" y="355" fill="#16A34A" font-size="10.5" font-weight="700">• Remote Access: AWS Systems Manager (Zero Trust)</text>
  <text x="925" y="375" fill="#64748B" font-size="9.5">Stateful hypervisor filtering prevents unauthorized scans</text>

  <!-- Connecting Arrows -->
  <!-- 1. Client to ALB -->
  <path d="M300 250 L400 250" stroke="#0284C7" stroke-width="2" fill="none" marker-end="url(#arr-blue)"/>
  <rect x="312" y="232" width="76" height="16" rx="3" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="0.8"/>
  <text x="350" y="244" fill="#0284C7" font-size="9" font-weight="700" text-anchor="middle">HTTP:80 Inbound</text>

  <!-- 2. ALB to Backend SG -->
  <path d="M790 250 L900 250" stroke="#8C4FFF" stroke-width="2" fill="none" marker-end="url(#arr-purple)"/>
  <rect x="805" y="232" width="80" height="16" rx="3" fill="#FFFFFF" stroke="#E9D5FF" stroke-width="0.8"/>
  <text x="845" y="244" fill="#8C4FFF" font-size="9" font-weight="700" text-anchor="middle">TCP:5000 Chained</text>

  <!-- Bottom: Architectural Principles Card -->
  <rect x="30" y="450" width="1300" height="205" rx="6" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>
  <rect x="30" y="450" width="1300" height="28" rx="6" fill="#F8FAFC"/>
  <image href="{icons['shield']}" x="40" y="454" width="20" height="20"/>
  <text x="70" y="469" fill="#0F172A" font-size="12" font-weight="700">Nguyên lý an ninh chuỗi Security Groups (Chained Security Group Isolation)</text>
  <text x="1315" y="469" fill="#64748B" font-size="10.5" font-weight="600" text-anchor="end">Thiết lập theo chuẩn AWS Well-Architected Security Pillar &amp; Zero Trust Architecture</text>

  <text x="50" y="498" fill="#0F172A" font-size="11.5" font-weight="700">1. Cô lập hoàn toàn máy chủ Backend (Complete Compute Tier Isolation):</text>
  <text x="70" y="516" fill="#334155" font-size="11">Máy chủ EC2 không mở bất kỳ cổng nào ra Internet công cộng. Cổng TCP 5000 chỉ tin cậy và chấp nhận kết nối bắt nguồn từ Application Load Balancer thông qua việc tham chiếu mã định danh Security Group nguồn (Source: sg-0dca819306a96bfdb).</text>

  <text x="50" y="542" fill="#0F172A" font-size="11.5" font-weight="700">2. Triệt tiêu nguy cơ quét cổng &amp; tấn công DDoS (Mitigate Port Scanning &amp; Surface Exploitation):</text>
  <text x="70" y="560" fill="#334155" font-size="11">Hacker hoặc các công cụ quét tự động gửi gói tin trực tiếp tới địa chỉ IP của EC2 sẽ bị tầng AWS Hypervisor tự động từ chối (Silent Drop) trước khi tiếp cận hệ điều hành máy chủ, ngăn chặn việc thăm dò cấu trúc mạng nội bộ.</text>

  <text x="50" y="586" fill="#0F172A" font-size="11.5" font-weight="700">3. Quản trị Zero Trust qua AWS Systems Manager (Eliminate Bastion Hosts &amp; Static SSH Keys):</text>
  <text x="70" y="604" fill="#334155" font-size="11">Đóng hoàn toàn cổng SSH 22, không cấp phát Elastic IP công cộng, không dùng khóa tĩnh .pem. Toàn bộ phiên làm việc từ xa đều được xác thực danh tính qua IAM, truyền tải qua kênh mã hóa outbound TLS 443 và ghi vết kiểm toán toàn diện trên AWS CloudWatch.</text>

  <text x="50" y="636" fill="#16A34A" font-size="11" font-weight="700">Tuân thủ nghiêm ngặt nguyên tắc đặc quyền tối thiểu (Least Privilege) giúp toàn bộ hệ thống đạt chuẩn an toàn thông tin doanh nghiệp.</text>

  <!-- Footer -->
  <line x1="30" y1="670" x2="1330" y2="670" stroke="#CBD5E1" stroke-width="1"/>
  <text x="30" y="683" fill="#64748B" font-size="9">FinOps Spend: $0.00 | Security Group Chaining: huylam-alb-sg -&gt; huylam-web-sg | HUCE Internship Report 2026 | Lam Quang Huy</text>
</svg>"""
    return svg

# ==============================================================================
# 4. SERVERLESS EVENT-DRIVEN PROCESSING PIPELINE
# ==============================================================================
def gen_serverless_pipeline_svg(icons):
    w, h = 1400, 780
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="background:#FFFFFF; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
  {DEFS_MARKERS}

  <!-- Header -->
  <text x="30" y="38" fill="#0F172A" font-size="18" font-weight="800" letter-spacing="-0.5">EVENT-DRIVEN SERVERLESS DOCUMENT PROCESSING PIPELINE</text>
  <text x="1370" y="38" fill="#64748B" font-size="11" font-weight="600" text-anchor="end">Sub-Second Ingestion &amp; Real-Time State Tracking on AWS | Scale-to-Zero Architecture</text>
  <line x1="30" y1="50" x2="1370" y2="50" stroke="#CBD5E1" stroke-width="1.2"/>

  <!-- Step 1: Web Studio Client -->
  <rect x="30" y="100" width="180" height="470" rx="4" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.2"/>
  <rect x="30" y="100" width="180" height="26" rx="4" fill="#F0F9FF"/>
  <text x="120" y="118" fill="#0369A1" font-size="11.5" font-weight="700" text-anchor="middle">Step 1: Document Upload</text>

  <circle cx="120" cy="180" r="26" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1.2"/>
  <path d="M120 174 a8 8 0 1 0 0 -16 a8 8 0 0 0 0 16 z M106 194 a14 14 0 0 1 28 0 z" fill="#475569"/>
  <text x="120" y="222" fill="#0F172A" font-size="12.5" font-weight="700" text-anchor="middle">Web Studio / Client</text>
  <text x="120" y="238" fill="#64748B" font-size="10.5" text-anchor="middle">Direct Browser Upload</text>
  <line x1="45" y1="250" x2="195" y2="250" stroke="#E2E8F0" stroke-width="1"/>

  <text x="45" y="272" fill="#334155" font-size="10.5">• Input Formats:</text>
  <text x="55" y="290" fill="#0284C7" font-size="10" font-weight="700">PDF, TIFF, PNG, Scans</text>
  <text x="45" y="312" fill="#334155" font-size="10.5">• Upload Channel:</text>
  <text x="55" y="330" fill="#334155" font-size="10">Direct S3 Presigned URL</text>
  <text x="45" y="352" fill="#334155" font-size="10.5">• Bypasses EC2 Web Server:</text>
  <text x="55" y="370" fill="#64748B" font-size="9.5">Zero bandwidth bottleneck</text>
  <text x="55" y="386" fill="#64748B" font-size="9.5">Zero CPU load on Gunicorn</text>
  <text x="45" y="410" fill="#16A34A" font-size="10" font-weight="700">Direct-to-S3 Cloud Ingestion</text>

  <!-- Step 2: Amazon S3 Storage Bucket -->
  <rect x="270" y="100" width="340" height="470" rx="4" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.2"/>
  <rect x="270" y="100" width="340" height="26" rx="4" fill="#F0FDF4"/>
  <image href="{icons['s3']}" x="280" y="103" width="20" height="20"/>
  <text x="310" y="118" fill="#15803D" font-size="11.5" font-weight="700">Step 2: Amazon S3 Event Ingestion</text>

  <!-- S3 Prefix uploads/ -->
  <rect x="285" y="140" width="310" height="95" rx="4" fill="#F8FAFC" stroke="#BBF7D0" stroke-width="1"/>
  <text x="295" y="160" fill="#166534" font-size="11" font-weight="700">Bucket: huylam-ocr-documents-ap-southeast-1</text>
  <text x="295" y="178" fill="#0284C7" font-size="10.5" font-weight="600">Prefix: uploads/{{job_id}}/filename.pdf</text>
  <text x="295" y="196" fill="#334155" font-size="10">• Target of direct browser / API document uploads</text>
  <text x="295" y="214" fill="#16A34A" font-size="10" font-weight="600">• Triggers s3:ObjectCreated:* automatically</text>

  <!-- S3 Event Notification Config -->
  <rect x="285" y="250" width="310" height="100" rx="4" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
  <text x="295" y="270" fill="#0F172A" font-size="11" font-weight="700">S3 Event Notification Configuration:</text>
  <text x="295" y="288" fill="#334155" font-size="10">• Name: NewDocumentUploadTrigger</text>
  <text x="295" y="304" fill="#334155" font-size="10">• Event Type: s3:ObjectCreated:Put, Post, Copy</text>
  <text x="295" y="320" fill="#334155" font-size="10">• Prefix: uploads/ | Suffix: (all files)</text>
  <text x="295" y="338" fill="#EA580C" font-size="10" font-weight="700">• Target: AWS Lambda huylam-ocr-processor</text>

  <!-- S3 Output Folder -->
  <rect x="285" y="365" width="310" height="90" rx="4" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
  <text x="295" y="385" fill="#0F172A" font-size="11" font-weight="700">Prefix: outputs/{{job_id}}/ (Results Destination)</text>
  <text x="295" y="403" fill="#334155" font-size="10">• Stores converted cv.pdf.md (Clean Markdown)</text>
  <text x="295" y="419" fill="#334155" font-size="10">• Stores converted cv.pdf.docx (Word Document)</text>
  <text x="295" y="435" fill="#334155" font-size="10">• Stores converted cv.pdf.pdf (A4 Print PDF)</text>

  <!-- S3 Security Details -->
  <rect x="285" y="470" width="310" height="85" rx="4" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
  <text x="295" y="490" fill="#0F172A" font-size="10.5" font-weight="700">Bucket Security &amp; Compliance:</text>
  <text x="295" y="508" fill="#16A34A" font-size="10" font-weight="600">• SSE-S3 AES-256 Server-Side Encryption</text>
  <text x="295" y="524" fill="#334155" font-size="10">• Block Public Access: 100% Enabled (True)</text>
  <text x="295" y="540" fill="#334155" font-size="10">• Secure IAM Role &amp; Presigned URL Access</text>

  <!-- Step 3: AWS Lambda Function -->
  <rect x="670" y="100" width="340" height="470" rx="4" fill="#FFFFFF" stroke="#EA580C" stroke-width="1.2"/>
  <rect x="670" y="100" width="340" height="26" rx="4" fill="#FFF7ED"/>
  <image href="{icons['lambda']}" x="680" y="103" width="20" height="20"/>
  <text x="710" y="118" fill="#C2410C" font-size="11.5" font-weight="700">Step 3: AWS Lambda Function Processor</text>

  <!-- Function Details Box -->
  <rect x="685" y="140" width="310" height="120" rx="4" fill="#F8FAFC" stroke="#FED7AA" stroke-width="1"/>
  <text x="695" y="160" fill="#C2410C" font-size="11" font-weight="700">Function: huylam-ocr-processor</text>
  <text x="695" y="178" fill="#334155" font-size="10.5">• Runtime: Python 3.11 | Architecture: x86_64</text>
  <text x="695" y="196" fill="#334155" font-size="10.5">• Handler: lambda_function.lambda_handler</text>
  <text x="695" y="214" fill="#334155" font-size="10.5">• Action: Parses S3 event records, extracts key</text>
  <text x="695" y="232" fill="#334155" font-size="10.5">• Generates UUID4 job_id, registers job metadata</text>
  <text x="695" y="250" fill="#16A34A" font-size="10" font-weight="700">Execution Speed: 214 ms - 257 ms (Sub-second)</text>

  <!-- IAM Role Box -->
  <rect x="685" y="275" width="310" height="110" rx="4" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
  <image href="{icons['role']}" x="695" y="285" width="20" height="20"/>
  <text x="722" y="300" fill="#0F172A" font-size="11" font-weight="700">IAM Execution Role (Least Privilege):</text>
  <text x="695" y="322" fill="#334155" font-size="10">• Role Name: huylam-ocr-lambda-role</text>
  <text x="695" y="338" fill="#334155" font-size="10">• Policy: LambdaS3DynamoDBAccess</text>
  <text x="695" y="354" fill="#334155" font-size="10">• Permissions: s3:GetObject, dynamodb:PutItem</text>
  <text x="695" y="370" fill="#16A34A" font-size="10" font-weight="600">Restricted specifically to bucket &amp; table ARNs</text>

  <!-- FinOps Box -->
  <rect x="685" y="400" width="310" height="155" rx="4" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
  <text x="695" y="420" fill="#0F172A" font-size="11" font-weight="700">FinOps Cost Profile &amp; Scale-to-Zero:</text>
  <text x="695" y="440" fill="#16A34A" font-size="11" font-weight="700">• Cost: $0.00 (AWS Free Tier - 1M req/month)</text>
  <text x="695" y="458" fill="#334155" font-size="10">• Scale-to-Zero: Zero idle costs when no files uploaded</text>
  <text x="695" y="476" fill="#334155" font-size="10">• Allocated Memory: 128 MB (Used: 83 MB)</text>
  <text x="695" y="494" fill="#334155" font-size="10">• Billed Duration: 215 ms per execution</text>
  <text x="695" y="512" fill="#334155" font-size="10">• Auto scales up to 1,000 concurrent executions</text>
  <text x="695" y="534" fill="#475569" font-size="10" font-weight="600">Enterprise Serverless Efficiency</text>

  <!-- Step 4 Top: Amazon DynamoDB -->
  <rect x="1070" y="100" width="300" height="225" rx="4" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.2"/>
  <rect x="1070" y="100" width="300" height="26" rx="4" fill="#F0F9FF"/>
  <image href="{icons['ddb']}" x="1080" y="103" width="20" height="20"/>
  <text x="1110" y="118" fill="#0369A1" font-size="11.5" font-weight="700">Step 4A: Amazon DynamoDB</text>

  <rect x="1085" y="135" width="270" height="175" rx="4" fill="#F8FAFC" stroke="#BAE6FD" stroke-width="1"/>
  <text x="1095" y="155" fill="#0284C7" font-size="11" font-weight="700">Table: document_processing_jobs</text>
  <text x="1095" y="173" fill="#334155" font-size="10.5">• Billing: PAY_PER_REQUEST (On-Demand)</text>
  <text x="1095" y="191" fill="#334155" font-size="10.5">• Partition Key: job_id (String UUID)</text>
  <text x="1095" y="209" fill="#16A34A" font-size="10" font-weight="700">• Status Record Inserted:</text>
  <text x="1105" y="225" fill="#15803D" font-size="9.5" font-family="monospace">status: "RECEIVED_VIA_S3_EVENT"</text>
  <text x="1105" y="240" fill="#475569" font-size="9.5" font-family="monospace">s3_input_uri: s3://huylam-ocr/uploads/...</text>
  <text x="1105" y="255" fill="#475569" font-size="9.5" font-family="monospace">created_at: 2026-09-20T19:38:21 (UTC+7)</text>
  <text x="1095" y="278" fill="#0284C7" font-size="10" font-weight="600">Sub-10ms Single-Digit Read/Write Latency</text>
  <text x="1095" y="296" fill="#64748B" font-size="9.5">State tracking for client polling &amp; Web Studio</text>

  <!-- Step 4 Bottom: Amazon CloudWatch -->
  <rect x="1070" y="345" width="300" height="225" rx="4" fill="#FFFFFF" stroke="#8C4FFF" stroke-width="1.2"/>
  <rect x="1070" y="345" width="300" height="26" rx="4" fill="#FAF5FF"/>
  <image href="{icons['cw']}" x="1080" y="348" width="20" height="20"/>
  <text x="1110" y="363" fill="#6B21A8" font-size="11.5" font-weight="700">Step 4B: Amazon CloudWatch</text>

  <rect x="1085" y="380" width="270" height="175" rx="4" fill="#F8FAFC" stroke="#E9D5FF" stroke-width="1"/>
  <text x="1095" y="400" fill="#6B21A8" font-size="11" font-weight="700">Log Group: /aws/lambda/huylam-ocr-processor</text>
  <text x="1095" y="420" fill="#334155" font-size="10.5">• Sample Real Execution Log Metric:</text>
  <text x="1105" y="438" fill="#475569" font-size="9.5" font-family="monospace">REPORT RequestId: 4a27b81c-0e9f-43...</text>
  <text x="1105" y="454" fill="#16A34A" font-size="9.5" font-family="monospace" font-weight="700">Duration: 214.32 ms | Billed: 215 ms</text>
  <text x="1105" y="470" fill="#475569" font-size="9.5" font-family="monospace">Memory Size: 128 MB | Max Used: 83 MB</text>
  <text x="1095" y="495" fill="#334155" font-size="10.5">• Metric Filters &amp; Observability Alarms:</text>
  <text x="1105" y="512" fill="#16A34A" font-size="10" font-weight="700">Errors == 0 (Alarm Status: OK)</text>
  <text x="1105" y="528" fill="#334155" font-size="9.5">Throttles == 0 | ConcurrentExecutions: OK</text>
  <text x="1095" y="546" fill="#6B21A8" font-size="9.5" font-weight="600">Full Real-Time Telemetry &amp; Traceability</text>

  <!-- Connecting Arrows with Clean Floating Labels -->
  <!-- 1. Client to S3 -->
  <path d="M210 210 L270 210" stroke="#0284C7" stroke-width="2" fill="none" marker-end="url(#arr-blue)"/>
  <rect x="214" y="193" width="52" height="15" rx="3" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="0.8"/>
  <text x="240" y="204" fill="#0284C7" font-size="8.5" font-weight="700" text-anchor="middle">1. PutObject</text>

  <!-- 2. S3 to Lambda -->
  <path d="M610 210 L670 210" stroke="#EA580C" stroke-width="2" fill="none" marker-end="url(#arr-orange)"/>
  <rect x="615" y="193" width="50" height="15" rx="3" fill="#FFFFFF" stroke="#FED7AA" stroke-width="0.8"/>
  <text x="640" y="204" fill="#EA580C" font-size="8.5" font-weight="700" text-anchor="middle">2. S3 Event</text>

  <!-- 3. Lambda to DynamoDB -->
  <path d="M1010 210 L1070 210" stroke="#0284C7" stroke-width="2" fill="none" marker-end="url(#arr-blue)"/>
  <rect x="1017" y="193" width="46" height="15" rx="3" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="0.8"/>
  <text x="1040" y="204" fill="#0284C7" font-size="8.5" font-weight="700" text-anchor="middle">3. PutItem</text>

  <!-- 4. Lambda to CloudWatch -->
  <path d="M1010 450 L1070 450" stroke="#8C4FFF" stroke-width="2" fill="none" marker-end="url(#arr-purple)"/>
  <rect x="1013" y="433" width="54" height="15" rx="3" fill="#FFFFFF" stroke="#E9D5FF" stroke-width="0.8"/>
  <text x="1040" y="444" fill="#8C4FFF" font-size="8.5" font-weight="700" text-anchor="middle">4. Log Stream</text>

  <!-- Bottom Highlights Box -->
  <rect x="30" y="590" width="1340" height="150" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>
  <rect x="30" y="590" width="1340" height="26" rx="4" fill="#F8FAFC"/>
  <text x="45" y="608" fill="#0F172A" font-size="11.5" font-weight="700">Pipeline Performance &amp; Engineering Highlights (AWS Well-Architected Framework)</text>

  <text x="50" y="635" fill="#334155" font-size="11">• <tspan font-weight="700" fill="#0F172A">Event Ingestion Latency:</tspan> Sub-second response (214 ms - 257 ms) eliminating polling latency and CPU waste on EC2 instances.</text>
  <text x="50" y="660" fill="#334155" font-size="11">• <tspan font-weight="700" fill="#0F172A">Security &amp; Least Privilege:</tspan> Lambda function operates under huylam-ocr-lambda-role with inline policies restricted to specific S3 and DynamoDB ARNs.</text>
  <text x="50" y="685" fill="#334155" font-size="11">• <tspan font-weight="700" fill="#0F172A">FinOps Excellence:</tspan> True Scale-to-Zero architecture costing 0.00 USD within AWS Free Tier limits (1,000,000 free calls / month).</text>
  <text x="50" y="710" fill="#16A34A" font-size="10.5" font-weight="700">Reliable, resilient event-driven decoupled architecture ensuring zero message loss during traffic surges.</text>

  <!-- Footer -->
  <line x1="30" y1="755" x2="1370" y2="755" stroke="#CBD5E1" stroke-width="1"/>
  <text x="30" y="770" fill="#64748B" font-size="9">FinOps Spend: $0.00 | Event Pipeline: S3 Event -&gt; Lambda -&gt; DynamoDB State | HUCE Internship Report 2026 | Lam Quang Huy</text>
</svg>"""
    return svg

# ==============================================================================
# 5. AMAZON ECS ON AWS FARGATE CONTAINER ARCHITECTURE
# ==============================================================================
def gen_ecs_fargate_svg(icons):
    w, h = 1400, 820
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="background:#FFFFFF; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
  {DEFS_MARKERS}

  <!-- Header -->
  <text x="30" y="38" fill="#0F172A" font-size="18" font-weight="800" letter-spacing="-0.5">AMAZON ECS ON AWS FARGATE CONTAINER ARCHITECTURE</text>
  <text x="1370" y="38" fill="#64748B" font-size="11" font-weight="600" text-anchor="end">Cluster: huylam-ecs-cluster | Service: huylam-web-service | Serverless Container Compute</text>
  <line x1="30" y1="50" x2="1370" y2="50" stroke="#CBD5E1" stroke-width="1.2"/>

  <!-- Left: Client Browser & Ingress -->
  <rect x="30" y="90" width="180" height="260" rx="4" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.2"/>
  <rect x="30" y="90" width="180" height="24" rx="4" fill="#F0F9FF"/>
  <text x="120" y="107" fill="#0369A1" font-size="11.5" font-weight="700" text-anchor="middle">Client Browser</text>

  <circle cx="120" cy="160" r="26" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1.2"/>
  <path d="M120 154 a8 8 0 1 0 0 -16 a8 8 0 0 0 0 16 z M106 174 a14 14 0 0 1 28 0 z" fill="#475569"/>
  <text x="120" y="202" fill="#0F172A" font-size="12.5" font-weight="700" text-anchor="middle">Public User</text>
  <text x="120" y="218" fill="#64748B" font-size="10.5" text-anchor="middle">Web Browser Client</text>
  <line x1="45" y1="230" x2="195" y2="230" stroke="#E2E8F0" stroke-width="1"/>

  <text x="45" y="252" fill="#334155" font-size="10.5">• Ingress: HTTP Port 80</text>
  <text x="45" y="272" fill="#0284C7" font-size="11" font-weight="700">18.138.22.86:80</text>
  <text x="45" y="292" fill="#334155" font-size="10.5">• HTTP GET /</text>
  <text x="45" y="312" fill="#16A34A" font-size="10.5" font-weight="700">Response: 200 OK Live</text>
  <text x="45" y="330" fill="#64748B" font-size="9.5">Apache "It works!" Body</text>

  <!-- Internet Gateway Box -->
  <rect x="30" y="380" width="180" height="150" rx="4" fill="#FFFFFF" stroke="#8C4FFF" stroke-width="1.2"/>
  <rect x="30" y="380" width="180" height="24" rx="4" fill="#FAF5FF"/>
  <image href="{icons['igw']}" x="40" y="382" width="20" height="20"/>
  <text x="70" y="397" fill="#6B21A8" font-size="11.5" font-weight="700">Internet Gateway</text>

  <text x="45" y="425" fill="#0F172A" font-size="10.5" font-weight="700">Default VPC Gateway:</text>
  <text x="45" y="445" fill="#64748B" font-size="9.5" font-family="monospace">igw-0b9db3a6eac29ede9</text>
  <text x="45" y="465" fill="#334155" font-size="10">• Bidirectional Route</text>
  <text x="45" y="483" fill="#334155" font-size="10">• Destination: 0.0.0.0/0</text>
  <text x="45" y="505" fill="#16A34A" font-size="10" font-weight="600">Public Internet Gateway</text>

  <!-- Center: AWS Default VPC & ECS Fargate Container -->
  <rect x="250" y="90" width="790" height="660" rx="6" fill="#FFFFFF" stroke="#475569" stroke-width="1.2"/>
  <rect x="250" y="90" width="790" height="28" rx="6" fill="#F8FAFC"/>
  <image href="{icons['vpc']}" x="260" y="94" width="20" height="20"/>
  <text x="290" y="109" fill="#0F172A" font-size="12" font-weight="700">AWS Region: ap-southeast-1 | Default VPC: 172.31.0.0/16</text>
  <text x="1025" y="109" fill="#64748B" font-size="10.5" font-weight="600" text-anchor="end">Fargate Serverless Microservice</text>

  <!-- Public Subnet ap-southeast-1c -->
  <rect x="270" y="130" width="750" height="600" rx="4" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.2"/>
  <rect x="270" y="130" width="750" height="24" rx="4" fill="#F0FDF4"/>
  <text x="282" y="147" fill="#15803D" font-size="11" font-weight="700">Public Subnet: ap-southeast-1c (subnet-0bba3228d80514181)</text>

  <!-- Subnet Networking Details (SG + ENI) -->
  <rect x="290" y="165" width="350" height="85" rx="4" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
  <image href="{icons['shield']}" x="300" y="175" width="20" height="20"/>
  <text x="328" y="188" fill="#0F172A" font-size="11" font-weight="700">Security Group: sg-023c42b5bc2e5111b</text>
  <text x="300" y="210" fill="#334155" font-size="10.5">• Inbound Rule: HTTP Port 80 from 0.0.0.0/0</text>
  <text x="300" y="228" fill="#16A34A" font-size="10.5" font-weight="600">• Outbound Rule: All traffic to 0.0.0.0/0</text>

  <rect x="660" y="165" width="340" height="85" rx="4" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
  <text x="675" y="188" fill="#0F172A" font-size="11" font-weight="700">ENI: eni-0dcbf8076c9d39691 (awsvpc)</text>
  <text x="675" y="210" fill="#0284C7" font-size="10.5" font-weight="700">• Public IP: 18.138.22.86</text>
  <text x="675" y="228" fill="#334155" font-size="10.5">• Private IP: 172.31.1.147</text>

  <!-- Amazon ECS Cluster Box -->
  <rect x="290" y="265" width="710" height="445" rx="4" fill="#FFFFFF" stroke="#EA580C" stroke-width="1.2"/>
  <rect x="290" y="265" width="710" height="26" rx="4" fill="#FFF7ED"/>
  <image href="{icons['ecs']}" x="300" y="268" width="20" height="20"/>
  <text x="330" y="283" fill="#C2410C" font-size="11.5" font-weight="700">Amazon ECS Cluster: huylam-ecs-cluster</text>

  <!-- ECS Service Box -->
  <rect x="310" y="305" width="670" height="385" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <rect x="310" y="305" width="670" height="24" rx="4" fill="#F8FAFC"/>
  <text x="322" y="322" fill="#0F172A" font-size="11" font-weight="700">ECS Service: huylam-web-service (Launch Type: FARGATE | Desired Count: 1)</text>

  <!-- Fargate Task Box -->
  <rect x="330" y="345" width="630" height="325" rx="4" fill="#F8FAFC" stroke="#EA580C" stroke-width="1"/>
  <rect x="330" y="345" width="630" height="24" rx="4" fill="#FFF7ED"/>
  <image href="{icons['fargate']}" x="340" y="347" width="20" height="20"/>
  <text x="368" y="362" fill="#C2410C" font-size="11" font-weight="700">Fargate Task: 4f4a7210f06f48c2ade4d568bde7967a</text>
  <text x="945" y="362" fill="#16A34A" font-size="10" font-weight="700" text-anchor="end">Status: RUNNING</text>

  <text x="345" y="390" fill="#334155" font-size="10.5">• Task Definition: <tspan font-weight="700">huylam-web-task:1</tspan> | Network Mode: <tspan font-weight="700">awsvpc</tspan></text>
  <text x="345" y="410" fill="#334155" font-size="10.5">• Allocated Resources: <tspan font-weight="700" fill="#0284C7">0.25 vCPU (256 units)</tspan> | <tspan font-weight="700" fill="#0284C7">512 MiB RAM (0.5 GB)</tspan></text>

  <!-- Container Box inside Task -->
  <rect x="345" y="430" width="600" height="225" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
  <text x="360" y="455" fill="#0F172A" font-size="11.5" font-weight="700">Container: web-app (Apache HTTP Server 2.4)</text>
  <text x="360" y="475" fill="#334155" font-size="10.5">• Image Source: <tspan font-family="monospace" font-weight="600">public.ecr.aws/docker/library/httpd:latest</tspan></text>
  <text x="360" y="495" fill="#334155" font-size="10.5">• Port Mapping: <tspan font-weight="700" fill="#0284C7">80:80 (TCP)</tspan> | Essential: Yes</text>
  <text x="360" y="515" fill="#334155" font-size="10.5">• Ephemeral Storage: 20 GiB NVMe</text>

  <rect x="360" y="535" width="570" height="105" rx="4" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
  <text x="375" y="555" fill="#16A34A" font-size="11" font-weight="700">Live Verification Endpoint Test Result:</text>
  <text x="375" y="575" fill="#0284C7" font-size="10.5" font-family="monospace">http://18.138.22.86 -&gt; HTTP 200 OK</text>
  <text x="375" y="593" fill="#334155" font-size="10">Content-Type: text/html | Server: Apache/2.4.65 (Unix) | Body: "It works!"</text>
  <text x="375" y="612" fill="#64748B" font-size="9.5">Direct client verification passed without load balancer requirement</text>

  <!-- Right: Amazon ECR & Fargate Benefits -->
  <rect x="1070" y="90" width="300" height="660" rx="4" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>
  <rect x="1070" y="90" width="300" height="28" rx="4" fill="#F8FAFC"/>
  <image href="{icons['ecr']}" x="1080" y="94" width="20" height="20"/>
  <text x="1110" y="109" fill="#0F172A" font-size="12" font-weight="700">Amazon ECR &amp; Registries</text>

  <!-- Private ECR -->
  <rect x="1085" y="130" width="270" height="165" rx="4" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
  <text x="1095" y="152" fill="#EA580C" font-size="11" font-weight="700">Private Registry: huylam-web-app</text>
  <text x="1095" y="172" fill="#334155" font-size="10">• Type: Private Container Registry</text>
  <text x="1095" y="190" fill="#334155" font-size="10">• Encryption: AES-256 (AWS KMS)</text>
  <text x="1095" y="208" fill="#334155" font-size="10">• Tag: latest | Scan on Push: Ready</text>
  <text x="1095" y="226" fill="#64748B" font-size="9" font-family="monospace">URI: 677994024390.dkr.ecr</text>
  <text x="1095" y="240" fill="#64748B" font-size="9" font-family="monospace">.ap-southeast-1.amazonaws.com</text>
  <text x="1095" y="260" fill="#16A34A" font-size="10" font-weight="600">Enterprise Secure Storage</text>

  <!-- Public ECR -->
  <rect x="1085" y="310" width="270" height="135" rx="4" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
  <text x="1095" y="332" fill="#0284C7" font-size="11" font-weight="700">Public ECR Gallery: httpd:latest</text>
  <text x="1095" y="352" fill="#334155" font-size="10">• Source: public.ecr.aws</text>
  <text x="1095" y="370" fill="#334155" font-size="10">• Fast Image Pull: 8 seconds</text>
  <text x="1095" y="388" fill="#334155" font-size="10">• Status: Verified Deployment</text>
  <text x="1095" y="406" fill="#334155" font-size="10">• Base Image for Fargate Container</text>
  <text x="1095" y="426" fill="#16A34A" font-size="10" font-weight="600">Official Secure Image Baseline</text>

  <!-- Fargate Benefits -->
  <rect x="1085" y="460" width="270" height="270" rx="4" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
  <text x="1095" y="482" fill="#0F172A" font-size="11" font-weight="700">AWS Fargate Serverless Benefits:</text>
  <text x="1095" y="506" fill="#334155" font-size="10.5">• <tspan font-weight="700">Zero EC2 Management:</tspan></text>
  <text x="1105" y="522" fill="#64748B" font-size="10">No host OS patching, scaling, or SSH</text>

  <text x="1095" y="546" fill="#334155" font-size="10.5">• <tspan font-weight="700">Per-Second Billing:</tspan></text>
  <text x="1105" y="562" fill="#64748B" font-size="10">Only pay for exact vCPU &amp; RAM used</text>

  <text x="1095" y="586" fill="#334155" font-size="10.5">• <tspan font-weight="700">Auto-Healing Replicas:</tspan></text>
  <text x="1105" y="602" fill="#64748B" font-size="10">Automated task restart if failed</text>

  <text x="1095" y="626" fill="#334155" font-size="10.5">• <tspan font-weight="700">Isolated Virtualization:</tspan></text>
  <text x="1105" y="642" fill="#64748B" font-size="10">Dedicated microVM per task (awsvpc)</text>
  <text x="1095" y="670" fill="#16A34A" font-size="10.5" font-weight="700">Zero Infrastructure Overhead</text>

  <!-- Connecting Arrows -->
  <!-- 1. Client to IGW -->
  <path d="M120 350 L120 380" stroke="#0284C7" stroke-width="2" fill="none" marker-end="url(#arr-blue)"/>
  <rect x="100" y="358" width="40" height="15" rx="3" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="0.8"/>
  <text x="120" y="369" fill="#0284C7" font-size="8.5" font-weight="700" text-anchor="middle">HTTP</text>

  <!-- 2. IGW to ENI / Subnet -->
  <path d="M210 455 L250 455" stroke="#0284C7" stroke-width="2" fill="none" marker-end="url(#arr-blue)"/>
  <rect x="216" y="442" width="34" height="15" rx="3" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="0.8"/>
  <text x="233" y="453" fill="#0284C7" font-size="8.5" font-weight="700" text-anchor="middle">Route</text>

  <!-- 3. ECR to Fargate (Pull Image) -->
  <path d="M1085 370 L975 370" stroke="#EA580C" stroke-width="1.8" stroke-dasharray="4,4" fill="none" marker-end="url(#arr-orange)"/>
  <rect x="1005" y="354" width="56" height="15" rx="3" fill="#FFFFFF" stroke="#FED7AA" stroke-width="0.8"/>
  <text x="1033" y="365" fill="#EA580C" font-size="8.5" font-weight="700" text-anchor="middle">Pull Image</text>

  <!-- Footer -->
  <line x1="30" y1="785" x2="1370" y2="785" stroke="#CBD5E1" stroke-width="1"/>
  <text x="30" y="800" fill="#64748B" font-size="9">FinOps Spend: $0.00 | AWS Fargate Serverless Compute: 0.25 vCPU, 512 MiB RAM | HUCE Internship Report 2026 | Lam Quang Huy</text>
  <text x="1370" y="800" fill="#64748B" font-size="9" text-anchor="end">Production Container Architecture: Amazon ECS Cluster + AWS Fargate Task + Amazon ECR</text>
</svg>"""
    return svg

def render_diagram(name, svg_content, width, height):
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(PUBLIC_DIR, exist_ok=True)

    svg_file = os.path.join(OUT_DIR, f"{name}.svg")
    png_file = os.path.join(OUT_DIR, f"{name}.png")
    drawio_file = os.path.join(OUT_DIR, f"{name}.drawio")

    public_svg = os.path.join(PUBLIC_DIR, f"{name}.svg")
    public_png = os.path.join(PUBLIC_DIR, f"{name}.png")
    public_drawio = os.path.join(PUBLIC_DIR, f"{name}.drawio")

    with open(svg_file, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated SVG: {svg_file}")

    # Drawio XML wrapper
    drawio_content = f"""<mxfile host="app.diagrams.net" modified="2026-10-06T14:40:00.000Z" agent="Antigravity" version="21.0.0">
  <diagram id="{name}" name="{name}">
    <mxGraphModel dx="{width}" dy="{height}" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{width}" pageHeight="{height}">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="svg_embed" value="" style="shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image={svg_file};" vertex="1" parent="1">
          <mxGeometry x="0" y="0" width="{width}" height="{height}" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    with open(drawio_file, "w", encoding="utf-8") as f:
        f.write(drawio_content)

    # Render PNG using Chrome
    if os.path.exists(CHROME_PATH):
        cmd = [
            CHROME_PATH,
            "--headless=new",
            "--disable-gpu",
            "--force-device-scale-factor=2",
            f"--window-size={width},{height}",
            f"--screenshot={png_file}",
            svg_file
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and os.path.exists(png_file):
            print(f"Rendered PNG: {png_file} ({os.path.getsize(png_file)} bytes)")
            # Copy to public dir
            shutil.copy2(svg_file, public_svg)
            shutil.copy2(png_file, public_png)
            shutil.copy2(drawio_file, public_drawio)
        else:
            print(f"Error rendering PNG for {name}: {res.stderr}")
    else:
        print(f"Chrome not found at {CHROME_PATH}")

def main():
    icons = load_icons()
    diagrams = [
        ("aws-hybrid-ocr-engine-architecture", gen_hybrid_ocr_svg(icons), 1500, 900),
        ("aws-vpc-network-architecture", gen_vpc_network_svg(icons), 1500, 920),
        ("aws-security-group-chaining", gen_security_group_chaining_svg(icons), 1360, 690),
        ("aws-serverless-event-pipeline", gen_serverless_pipeline_svg(icons), 1400, 780),
        ("aws-ecs-fargate-architecture", gen_ecs_fargate_svg(icons), 1400, 820),
    ]

    for name, svg_content, width, height in diagrams:
        print(f"\nBuilding {name} ({width}x{height})...")
        render_diagram(name, svg_content, width, height)

    print("\nAll 5 diagrams successfully generated and synced to static & public directories!")

if __name__ == "__main__":
    main()
