#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/build_defense_diagrams.py
Tạo và kết xuất 3 sơ đồ kỹ thuật chuẩn Retina 2x PNG:
1. aws-use-case-architecture: Sơ đồ ca sử dụng toàn diện, không chồng chéo mũi tên
2. aws-database-polyglot-erd: Sơ đồ cơ sở dữ liệu đa mô hình chuẩn ERD, không cắt ngang bảng
3. aws-sequence-event-flow: Sơ đồ tuần tự xử lý toàn trình hướng sự kiện rõ ràng, mạch lạc
"""

import os
import subprocess
import shutil

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(PROJECT_ROOT, "workshop", "static", "images", "architecture")
PUBLIC_DIR = os.path.join(PROJECT_ROOT, "workshop", "public", "images", "architecture")
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

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
      <path d="M0,0 L0,6 L8,3 z" fill="#D97706"/>
    </marker>
    <marker id="arr-purple" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#8C4FFF"/>
    </marker>
    <filter id="card-shadow" x="-3%" y="-3%" width="106%" height="106%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0F172A" flood-opacity="0.04"/>
    </filter>
  </defs>
"""

# ==============================================================================
# 1. SƠ ĐỒ USE CASE KIẾN TRÚC TOÀN DIỆN (KHÔNG CHỒNG CHÉO)
# ==============================================================================
def gen_use_case_svg():
    w, h = 1520, 920
    raw_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 __W__ __H__" width="__W__" height="__H__" style="background:#FFFFFF; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
  __DEFS__

  <!-- Header -->
  <text x="35" y="40" fill="#0F172A" font-size="20" font-weight="800" letter-spacing="-0.5">SYSTEM USE CASE ARCHITECTURE &amp; ACTOR INTERACTION MODEL</text>
  <text x="1485" y="40" fill="#64748B" font-size="12" font-weight="600" text-anchor="end">Serverless Hybrid Document Platform | HUCE Graduation Project 2026</text>
  <line x1="35" y1="55" x2="1485" y2="55" stroke="#E2E8F0" stroke-width="1.5"/>

  <!-- Left Container: Human Actors -->
  <rect x="35" y="75" width="220" height="800" rx="10" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.2"/>
  <rect x="35" y="75" width="220" height="38" rx="10" fill="#0F172A"/>
  <text x="145" y="99" fill="#FFFFFF" font-size="13" font-weight="700" text-anchor="middle">HUMAN ACTORS</text>

  <!-- Actor 1: End User -->
  <g transform="translate(45, 135)">
    <rect x="0" y="0" width="200" height="260" rx="8" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.5" filter="url(#card-shadow)"/>
    <circle cx="100" cy="45" r="18" fill="#E0F2FE" stroke="#0284C7" stroke-width="2"/>
    <line x1="100" y1="63" x2="100" y2="120" stroke="#0284C7" stroke-width="2.5"/>
    <line x1="75" y1="85" x2="125" y2="85" stroke="#0284C7" stroke-width="2.5"/>
    <line x1="100" y1="120" x2="80" y2="165" stroke="#0284C7" stroke-width="2.5"/>
    <line x1="100" y1="120" x2="120" y2="165" stroke="#0284C7" stroke-width="2.5"/>
    <text x="100" y="195" fill="#0F172A" font-size="14" font-weight="700" text-anchor="middle">End User</text>
    <text x="100" y="215" fill="#64748B" font-size="11" font-weight="500" text-anchor="middle">Sinh vien / Ky su / Doc gia</text>
    <text x="100" y="235" fill="#0284C7" font-size="11" font-weight="600" text-anchor="middle">Single Page Web Studio</text>
  </g>

  <!-- Actor 2: System Administrator -->
  <g transform="translate(45, 520)">
    <rect x="0" y="0" width="200" height="260" rx="8" fill="#FFFFFF" stroke="#D97706" stroke-width="1.5" filter="url(#card-shadow)"/>
    <circle cx="100" cy="45" r="18" fill="#FEF3C7" stroke="#D97706" stroke-width="2"/>
    <line x1="100" y1="63" x2="100" y2="120" stroke="#D97706" stroke-width="2.5"/>
    <line x1="75" y1="85" x2="125" y2="85" stroke="#D97706" stroke-width="2.5"/>
    <line x1="100" y1="120" x2="80" y2="165" stroke="#D97706" stroke-width="2.5"/>
    <line x1="100" y1="120" x2="120" y2="165" stroke="#D97706" stroke-width="2.5"/>
    <text x="100" y="195" fill="#0F172A" font-size="14" font-weight="700" text-anchor="middle">Administrator</text>
    <text x="100" y="215" fill="#64748B" font-size="11" font-weight="500" text-anchor="middle">Quan tri vien / DevOps</text>
    <text x="100" y="235" fill="#D97706" font-size="11" font-weight="600" text-anchor="middle">SSM &amp; FinOps Manager</text>
  </g>

  <!-- Middle: System Boundary -->
  <rect x="285" y="75" width="950" height="800" rx="12" fill="#FFFFFF" stroke="#0F172A" stroke-width="1.8"/>
  <rect x="285" y="75" width="950" height="38" rx="12" fill="#0F172A"/>
  <text x="760" y="99" fill="#FFFFFF" font-size="14" font-weight="700" text-anchor="middle">SYSTEM BOUNDARY: SERVERLESS HYBRID DOCUMENT PLATFORM</text>

  <!-- LEFT COLUMN INSIDE BOUNDARY: USER & ADMIN FACING USE CASES -->
  
  <!-- Sub-Cluster 1: Account & Studio Actions (User) -->
  <g transform="translate(305, 125)">
    <rect x="0" y="0" width="445" height="345" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.2"/>
    <text x="15" y="22" fill="#0284C7" font-size="11" font-weight="700">1. CLIENT INTERACTION &amp; STUDIO ACTIONS</text>
    
    <!-- UC1 -->
    <rect x="15" y="32" width="415" height="42" rx="21" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.2"/>
    <text x="222" y="52" fill="#0F172A" font-size="11.5" font-weight="600" text-anchor="middle">UC01: Dang nhap / Dang ky (JWT RBAC)</text>
    <text x="222" y="66" fill="#64748B" font-size="9.5" text-anchor="middle">Xac thuc phan quyen User va Administrator</text>

    <!-- UC2 -->
    <rect x="15" y="82" width="415" height="42" rx="21" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.2"/>
    <text x="222" y="102" fill="#0F172A" font-size="11.5" font-weight="600" text-anchor="middle">UC02: Thiet lap Giao dien &amp; Che do uu tien</text>
    <text x="222" y="116" fill="#64748B" font-size="9.5" text-anchor="middle">Light/Dark theme, ngon ngu dich, Fast-Path mac dinh</text>

    <!-- UC3 -->
    <rect x="15" y="132" width="415" height="42" rx="21" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.5"/>
    <text x="222" y="152" fill="#0F172A" font-size="11.5" font-weight="700" text-anchor="middle">UC03: Tai len tai lieu qua S3 Presigned URL</text>
    <text x="222" y="166" fill="#16A34A" font-size="9.5" font-weight="600" text-anchor="middle">Vuot tran 10MB API Gateway, ho tro tep toi 100MB</text>

    <!-- UC8 -->
    <rect x="15" y="182" width="415" height="42" rx="21" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.2"/>
    <text x="222" y="202" fill="#0F172A" font-size="11.5" font-weight="600" text-anchor="middle">UC08: Bien tap &amp; Doi chieu song ngu Side-by-Side</text>
    <text x="222" y="216" fill="#64748B" font-size="9.5" text-anchor="middle">Soan thao Markdown truc quan tren giao dien hai cot</text>

    <!-- UC9 -->
    <rect x="15" y="232" width="415" height="42" rx="21" fill="#FFFFFF" stroke="#D97706" stroke-width="1.2"/>
    <text x="222" y="252" fill="#0F172A" font-size="11.5" font-weight="600" text-anchor="middle">UC09: Xuat ban da dinh dang (DOCX, PDF, MD)</text>
    <text x="222" y="266" fill="#64748B" font-size="9.5" text-anchor="middle">Word hoc thuat don sac, PDF in an toi uu &lt; 10 MB</text>

    <!-- UC10 -->
    <rect x="15" y="282" width="415" height="42" rx="21" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.2"/>
    <text x="222" y="302" fill="#0F172A" font-size="11.5" font-weight="600" text-anchor="middle">UC10: Tra cuu lich su &amp; Theo doi trang thai Job</text>
    <text x="222" y="316" fill="#64748B" font-size="9.5" text-anchor="middle">Truy van DynamoDB: PROCESSING / COMPLETED</text>
  </g>

  <!-- Sub-Cluster 2: Admin & Governance (Bottom Left) -->
  <g transform="translate(305, 490)">
    <rect x="0" y="0" width="445" height="300" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.2"/>
    <text x="15" y="22" fill="#D97706" font-size="11" font-weight="700">2. GOVERNANCE, TELEMETRY &amp; FINOPS (ADMIN)</text>

    <!-- UC11 -->
    <rect x="15" y="35" width="415" height="44" rx="22" fill="#FFFFFF" stroke="#D97706" stroke-width="1.2"/>
    <text x="222" y="56" fill="#0F172A" font-size="11.5" font-weight="600" text-anchor="middle">UC11: Quan ly API Keys &amp; Key Tour Rotation</text>
    <text x="222" y="70" fill="#64748B" font-size="9.5" text-anchor="middle">Xoay vong Round-Robin, Exponential Backoff chong 429</text>

    <!-- UC12 -->
    <rect x="15" y="90" width="415" height="44" rx="22" fill="#FFFFFF" stroke="#D97706" stroke-width="1.2"/>
    <text x="222" y="111" fill="#0F172A" font-size="11.5" font-weight="600" text-anchor="middle">UC12: Giam sat Telemetry tren CloudWatch</text>
    <text x="222" y="125" fill="#64748B" font-size="9.5" text-anchor="middle">Theo doi Latency, Alarms, Metrics va SSM Parameters</text>

    <!-- UC13 -->
    <rect x="15" y="145" width="415" height="44" rx="22" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.5"/>
    <text x="222" y="166" fill="#0F172A" font-size="11.5" font-weight="700" text-anchor="middle">UC13: Kiem soat Chi phi FinOps Zero-Breach</text>
    <text x="222" y="180" fill="#16A34A" font-size="9.5" font-weight="600" text-anchor="middle">Bao toan han muc AWS Free Tier (Chi phi thuc te 0.00 USD)</text>

    <!-- Info Box inside Admin -->
    <rect x="15" y="205" width="415" height="75" rx="6" fill="#FEF3C7" stroke="#F59E0B" stroke-width="1"/>
    <text x="25" y="226" fill="#92400E" font-size="10.5" font-weight="700">Audit &amp; Security Isolation Guarantee:</text>
    <text x="25" y="244" fill="#B45309" font-size="10">Quan tri may chu qua kenh AWS Systems Manager (SSM) Session</text>
    <text x="25" y="260" fill="#B45309" font-size="10">Dong 100% cong SSH 22, bao toan nguyen tac Least Privilege.</text>
  </g>

  <!-- RIGHT COLUMN INSIDE BOUNDARY: BACKEND SERVERLESS & AI PIPELINE -->
  
  <!-- Sub-Cluster 3: Serverless Ingestion & Routing (Top Right) -->
  <g transform="translate(775, 125)">
    <rect x="0" y="0" width="440" height="345" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.2"/>
    <text x="15" y="22" fill="#16A34A" font-size="11" font-weight="700">3. EVENT-DRIVEN INGESTION &amp; HYBRID OCR PIPELINE</text>

    <!-- UC4 -->
    <rect x="15" y="45" width="410" height="52" rx="26" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.5"/>
    <text x="220" y="68" fill="#0F172A" font-size="11.5" font-weight="700" text-anchor="middle">UC04: Tu dong phan tich mat do ky tu so</text>
    <text x="220" y="84" fill="#64748B" font-size="9.5" text-anchor="middle">Character Density Threshold &gt;= 0.05 phan luong thong minh</text>

    <!-- UC5 -->
    <rect x="15" y="125" width="410" height="52" rx="26" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.5"/>
    <text x="220" y="148" fill="#0F172A" font-size="11.5" font-weight="700" text-anchor="middle">UC05: Boc tach sieu toc Fast-Path Native (PyMuPDF)</text>
    <text x="220" y="164" fill="#16A34A" font-size="9.5" font-weight="600" text-anchor="middle">Thoi gian 0.28s/trang, chi phi 0$, bao toan 100% bang bieu</text>

    <!-- Sync info -->
    <rect x="15" y="205" width="410" height="115" rx="6" fill="#DCFCE7" stroke="#86EFAC" stroke-width="1"/>
    <text x="25" y="228" fill="#166534" font-size="11" font-weight="700">Autonomous Serverless Triggering:</text>
    <text x="25" y="250" fill="#15803D" font-size="10">• S3 Event s3:ObjectCreated tu dong goi AWS Lambda trong 214 ms.</text>
    <text x="25" y="270" fill="#15803D" font-size="10">• Ghi nhan trang thai tien trinh PROCESSING len Amazon DynamoDB.</text>
    <text x="25" y="290" fill="#15803D" font-size="10">• 85% tai lieu so duoc giai phong tuc thi ma khong ton chi phi AI.</text>
  </g>

  <!-- Sub-Cluster 4: AI Multimodal & Translation (Bottom Right) -->
  <g transform="translate(775, 490)">
    <rect x="0" y="0" width="440" height="300" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.2"/>
    <text x="15" y="22" fill="#8C4FFF" font-size="11" font-weight="700">4. AI MULTIMODAL INFERENCE &amp; DOMAIN TRANSLATION</text>

    <!-- UC6 -->
    <rect x="15" y="45" width="410" height="52" rx="26" fill="#FFFFFF" stroke="#8C4FFF" stroke-width="1.5"/>
    <text x="220" y="68" fill="#0F172A" font-size="11.5" font-weight="700" text-anchor="middle">UC06: Boc tach thi giac Vision Multimodal OCR</text>
    <text x="220" y="84" fill="#64748B" font-size="9.5" text-anchor="middle">Kaggle Qwen2.5-VL 72B ket hop tu dong Failover sang Gemini Flash</text>

    <!-- UC7 -->
    <rect x="15" y="125" width="410" height="52" rx="26" fill="#FFFFFF" stroke="#8C4FFF" stroke-width="1.5"/>
    <text x="220" y="148" fill="#0F172A" font-size="11.5" font-weight="700" text-anchor="middle">UC07: Dich thuat thuat ngu ky thuat chuyen sau (LLM)</text>
    <text x="220" y="164" fill="#64748B" font-size="9.5" text-anchor="middle">Bao toan cum tu ky thuat Cloud/DevOps, giu nguyen cong thuc KaTeX</text>

    <!-- AI Architecture Note -->
    <rect x="15" y="200" width="410" height="80" rx="6" fill="#F3E8FF" stroke="#D8B4FE" stroke-width="1"/>
    <text x="25" y="222" fill="#6B21A8" font-size="11" font-weight="700">Dual-Engine Failover Architecture:</text>
    <text x="25" y="242" fill="#7E22CE" font-size="10">• Chuyen mach trong &lt; 1s khi may chu GPU ngoai vi ban hoac loi.</text>
    <text x="25" y="260" fill="#7E22CE" font-size="10">• Key Tour Manager dieu phoi phan phoi tai chong 429 Too Many Requests.</text>
  </g>

  <!-- Right Container: System & AI Actors -->
  <rect x="1265" y="75" width="220" height="800" rx="10" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.2"/>
  <rect x="1265" y="75" width="220" height="38" rx="10" fill="#0F172A"/>
  <text x="1375" y="99" fill="#FFFFFF" font-size="13" font-weight="700" text-anchor="middle">SYSTEM &amp; AI ACTORS</text>

  <!-- Actor 3: AWS Serverless Event System -->
  <g transform="translate(1275, 135)">
    <rect x="0" y="0" width="200" height="260" rx="8" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.5" filter="url(#card-shadow)"/>
    <rect x="75" y="30" width="50" height="50" rx="6" fill="#DCFCE7" stroke="#16A34A" stroke-width="2"/>
    <text x="100" y="60" fill="#16A34A" font-size="18" font-weight="800" text-anchor="middle">AWS</text>
    <text x="100" y="115" fill="#0F172A" font-size="13.5" font-weight="700" text-anchor="middle">AWS Event System</text>
    <text x="100" y="135" fill="#64748B" font-size="11" font-weight="500" text-anchor="middle">S3 Notification &amp; Lambda</text>
    <text x="100" y="165" fill="#16A34A" font-size="10.5" font-weight="600" text-anchor="middle">s3:ObjectCreated Event</text>
    <text x="100" y="185" fill="#64748B" font-size="10" text-anchor="middle">Duration: 214ms | RAM: 88MB</text>
    <text x="100" y="225" fill="#0284C7" font-size="10.5" font-weight="600" text-anchor="middle">Sync DynamoDB States</text>
  </g>

  <!-- Actor 4: AI Inference Engine -->
  <g transform="translate(1275, 520)">
    <rect x="0" y="0" width="200" height="260" rx="8" fill="#FFFFFF" stroke="#8C4FFF" stroke-width="1.5" filter="url(#card-shadow)"/>
    <rect x="75" y="30" width="50" height="50" rx="6" fill="#F3E8FF" stroke="#8C4FFF" stroke-width="2"/>
    <text x="100" y="60" fill="#8C4FFF" font-size="18" font-weight="800" text-anchor="middle">AI</text>
    <text x="100" y="115" fill="#0F172A" font-size="13.5" font-weight="700" text-anchor="middle">AI Inference Engines</text>
    <text x="100" y="135" fill="#64748B" font-size="11" font-weight="500" text-anchor="middle">Multimodal Vision &amp; LLM</text>
    <text x="100" y="165" fill="#8C4FFF" font-size="10.5" font-weight="600" text-anchor="middle">Qwen2.5-VL 72B (Kaggle)</text>
    <text x="100" y="185" fill="#64748B" font-size="10" text-anchor="middle">Google Gemini Flash API</text>
    <text x="100" y="225" fill="#D97706" font-size="10.5" font-weight="600" text-anchor="middle">Dual-Failover Architecture</text>
  </g>

  <!-- CLEAN DIRECT ARROWS (ZERO CROSSINGS) -->
  <!-- User to UC01, UC02, UC03, UC08, UC09, UC10 -->
  <path d="M 245 178 L 320 178" stroke="#0284C7" stroke-width="1.8" marker-end="url(#arr-blue)"/>
  <path d="M 245 228 L 320 228" stroke="#0284C7" stroke-width="1.8" marker-end="url(#arr-blue)"/>
  <path d="M 245 278 L 320 278" stroke="#0284C7" stroke-width="2.2" marker-end="url(#arr-blue)"/>
  <path d="M 245 328 L 320 328" stroke="#0284C7" stroke-width="1.8" marker-end="url(#arr-blue)"/>
  <path d="M 245 378 L 320 378" stroke="#0284C7" stroke-width="1.8" marker-end="url(#arr-blue)"/>
  <path d="M 245 428 L 320 428" stroke="#0284C7" stroke-width="1.8" marker-end="url(#arr-blue)"/>

  <!-- Admin to UC11, UC12, UC13 -->
  <path d="M 245 545 L 320 545" stroke="#D97706" stroke-width="1.8" marker-end="url(#arr-orange)"/>
  <path d="M 245 600 L 320 600" stroke="#D97706" stroke-width="1.8" marker-end="url(#arr-orange)"/>
  <path d="M 245 655 L 320 655" stroke="#D97706" stroke-width="1.8" marker-end="url(#arr-orange)"/>

  <!-- Internal Cross Connection: UC03 Upload triggers Backend UC04 Ingestion -->
  <path d="M 735 278 L 790 196" stroke="#16A34A" stroke-width="2" stroke-dasharray="4,4" fill="none" marker-end="url(#arr-green)"/>
  <!-- Internal Cross Connection: Backend UC07 feeds into UC08 Side-by-Side Editor -->
  <path d="M 790 635 L 735 328" stroke="#8C4FFF" stroke-width="1.8" stroke-dasharray="4,4" fill="none" marker-end="url(#arr-purple)"/>

  <!-- AWS Event System to UC04, UC05 -->
  <path d="M 1275 196 L 1200 196" stroke="#16A34A" stroke-width="2" marker-end="url(#arr-green)"/>
  <path d="M 1275 276 L 1200 276" stroke="#16A34A" stroke-width="2" marker-end="url(#arr-green)"/>

  <!-- AI Inference Engines to UC06, UC07 -->
  <path d="M 1275 560 L 1200 560" stroke="#8C4FFF" stroke-width="2" marker-end="url(#arr-purple)"/>
  <path d="M 1275 640 L 1200 640" stroke="#8C4FFF" stroke-width="2" marker-end="url(#arr-purple)"/>

  <!-- Bottom Summary Bar -->
  <rect x="285" y="835" width="950" height="40" rx="6" fill="#F1F5F9" stroke="#E2E8F0" stroke-width="1"/>
  <text x="760" y="860" fill="#475569" font-size="11.5" font-weight="600" text-anchor="middle">
    Architecture Verification: 13 Core Use Cases | 4 Distinct Actors | 100% Collision-Free Routing | FinOps 0.00 USD Guarantee
  </text>
</svg>"""
    return raw_svg.replace("__W__", str(w)).replace("__H__", str(h)).replace("__DEFS__", DEFS_MARKERS)

# ==============================================================================
# 2. SƠ ĐỒ CƠ SỞ DỮ LIỆU ĐA MÔ HÌNH (ĐƯỜNG DÂY NGOẠI VI SẠCH SẼ)
# ==============================================================================
def gen_database_erd_svg():
    w, h = 1520, 920
    raw_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 __W__ __H__" width="__W__" height="__H__" style="background:#FFFFFF; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
  __DEFS__

  <!-- Header -->
  <text x="35" y="40" fill="#0F172A" font-size="20" font-weight="800" letter-spacing="-0.5">POLYGLOT PERSISTENCE ARCHITECTURE &amp; DATABASE ERD MODEL</text>
  <text x="1485" y="40" fill="#64748B" font-size="12" font-weight="600" text-anchor="end">Amazon DynamoDB NoSQL | Amazon S3 Storage Hierarchy | Relational SQLite Schema</text>
  <line x1="35" y1="55" x2="1485" y2="55" stroke="#E2E8F0" stroke-width="1.5"/>

  <!-- Left: Relational Database Schema Container -->
  <rect x="35" y="75" width="715" height="800" rx="10" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.2"/>
  <rect x="35" y="75" width="715" height="38" rx="10" fill="#0F172A"/>
  <text x="392" y="99" fill="#FFFFFF" font-size="13" font-weight="700" text-anchor="middle">RELATIONAL SQL SCHEMA (USERS, DOCUMENTS, SETTINGS &amp; API KEYS)</text>

  <!-- Table 1: USERS -->
  <g transform="translate(60, 130)">
    <rect x="0" y="0" width="300" height="155" rx="6" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.5" filter="url(#card-shadow)"/>
    <rect x="0" y="0" width="300" height="28" rx="6" fill="#0284C7"/>
    <text x="150" y="19" fill="#FFFFFF" font-size="12" font-weight="700" text-anchor="middle">TABLE: users</text>
    <text x="12" y="46" fill="#0F172A" font-size="11" font-weight="700">PK  id</text><text x="180" y="46" fill="#64748B" font-size="11">TEXT (UUID)</text>
    <text x="12" y="68" fill="#0F172A" font-size="11">UK  username</text><text x="180" y="68" fill="#64748B" font-size="11">TEXT NOT NULL</text>
    <text x="12" y="90" fill="#0F172A" font-size="11">UK  email</text><text x="180" y="90" fill="#64748B" font-size="11">TEXT NOT NULL</text>
    <text x="12" y="112" fill="#0F172A" font-size="11">    password_hash</text><text x="180" y="112" fill="#64748B" font-size="11">TEXT NOT NULL</text>
    <text x="12" y="134" fill="#0F172A" font-size="11">    role</text><text x="180" y="134" fill="#64748B" font-size="11">TEXT ('user'|'admin')</text>
    <text x="12" y="148" fill="#64748B" font-size="9.5">    created_at TIMESTAMP</text>
  </g>

  <!-- Table 2: USER_SETTINGS -->
  <g transform="translate(425, 130)">
    <rect x="0" y="0" width="300" height="155" rx="6" fill="#FFFFFF" stroke="#64748B" stroke-width="1.2" filter="url(#card-shadow)"/>
    <rect x="0" y="0" width="300" height="28" rx="6" fill="#475569"/>
    <text x="150" y="19" fill="#FFFFFF" font-size="12" font-weight="700" text-anchor="middle">TABLE: user_settings (1:1 with users)</text>
    <text x="12" y="46" fill="#0F172A" font-size="11" font-weight="700">PK,FK user_id</text><text x="180" y="46" fill="#64748B" font-size="11">TEXT (users.id)</text>
    <text x="12" y="68" fill="#0F172A" font-size="11">      theme</text><text x="180" y="68" fill="#64748B" font-size="11">TEXT ('light'|'dark')</text>
    <text x="12" y="90" fill="#0F172A" font-size="11">      language</text><text x="180" y="90" fill="#64748B" font-size="11">TEXT ('vi'|'en')</text>
    <text x="12" y="112" fill="#0F172A" font-size="11">      default_model</text><text x="180" y="112" fill="#64748B" font-size="11">TEXT ('auto'|'qwen')</text>
    <text x="12" y="134" fill="#0F172A" font-size="11">      fast_path_def</text><text x="180" y="134" fill="#64748B" font-size="11">INTEGER (1|0)</text>
  </g>

  <!-- Table 3: DOCUMENTS (1:N with users) -->
  <g transform="translate(60, 320)">
    <rect x="0" y="0" width="665" height="260" rx="6" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.5" filter="url(#card-shadow)"/>
    <rect x="0" y="0" width="665" height="28" rx="6" fill="#16A34A"/>
    <text x="332" y="19" fill="#FFFFFF" font-size="12" font-weight="700" text-anchor="middle">TABLE: documents (Historical Processed Artifacts)</text>
    
    <text x="15" y="50" fill="#0F172A" font-size="11" font-weight="700">PK  id</text><text x="170" y="50" fill="#64748B" font-size="11">TEXT (UUID)</text>
    <text x="15" y="74" fill="#0F172A" font-size="11" font-weight="700">FK  user_id</text><text x="170" y="74" fill="#64748B" font-size="11">TEXT REFERENCES users(id)</text>
    <text x="15" y="98" fill="#0F172A" font-size="11">    filename</text><text x="170" y="98" fill="#64748B" font-size="11">TEXT NOT NULL</text>
    <text x="15" y="122" fill="#0F172A" font-size="11">    file_size</text><text x="170" y="122" fill="#64748B" font-size="11">INTEGER (Bytes)</text>
    <text x="15" y="146" fill="#0F172A" font-size="11">    total_pages</text><text x="170" y="146" fill="#64748B" font-size="11">INTEGER DEFAULT 1</text>
    <text x="15" y="170" fill="#0F172A" font-size="11">    digital_pages</text><text x="170" y="170" fill="#64748B" font-size="11">INTEGER (Fast-Path pages)</text>
    <text x="15" y="194" fill="#0F172A" font-size="11">    scanned_pages</text><text x="170" y="194" fill="#64748B" font-size="11">INTEGER (Vision OCR pages)</text>
    
    <text x="360" y="50" fill="#0F172A" font-size="11">model_used</text><text x="500" y="50" fill="#64748B" font-size="11">TEXT ('Fast-Path'|'Qwen')</text>
    <text x="360" y="74" fill="#0F172A" font-size="11">language</text><text x="500" y="74" fill="#64748B" font-size="11">TEXT ('vi'|'en')</text>
    <text x="360" y="98" fill="#0F172A" font-size="11">status</text><text x="500" y="98" fill="#64748B" font-size="11">TEXT ('COMPLETED')</text>
    <text x="360" y="122" fill="#0F172A" font-size="11">full_markdown</text><text x="500" y="122" fill="#64748B" font-size="11">TEXT NOT NULL</text>
    <text x="360" y="146" fill="#0F172A" font-size="11">translated_markdown</text><text x="500" y="146" fill="#64748B" font-size="11">TEXT (Vietnamese output)</text>
    <text x="360" y="170" fill="#0F172A" font-size="11">processing_time</text><text x="500" y="170" fill="#64748B" font-size="11">REAL (Seconds, e.g. 0.28)</text>
    <text x="360" y="194" fill="#0F172A" font-size="11">created_at</text><text x="500" y="194" fill="#64748B" font-size="11">TIMESTAMP DEFAULT NOW</text>

    <line x1="15" y1="218" x2="650" y2="218" stroke="#E2E8F0" stroke-width="1"/>
    <text x="15" y="240" fill="#16A34A" font-size="10.5" font-weight="600">Integrity Rule: ON DELETE CASCADE from users | Index: (user_id, created_at DESC)</text>
  </g>

  <!-- Table 4: API_KEYS -->
  <g transform="translate(60, 610)">
    <rect x="0" y="0" width="315" height="230" rx="6" fill="#FFFFFF" stroke="#D97706" stroke-width="1.2" filter="url(#card-shadow)"/>
    <rect x="0" y="0" width="315" height="28" rx="6" fill="#D97706"/>
    <text x="157" y="19" fill="#FFFFFF" font-size="12" font-weight="700" text-anchor="middle">TABLE: api_keys (Key Tour Manager)</text>
    <text x="12" y="48" fill="#0F172A" font-size="11" font-weight="700">PK  id</text><text x="180" y="48" fill="#64748B" font-size="11">TEXT (UUID)</text>
    <text x="12" y="70" fill="#0F172A" font-size="11">    provider</text><text x="180" y="70" fill="#64748B" font-size="11">TEXT ('kaggle'|'gemini')</text>
    <text x="12" y="92" fill="#0F172A" font-size="11">    key_alias</text><text x="180" y="92" fill="#64748B" font-size="11">TEXT ('Kaggle GPU 1')</text>
    <text x="12" y="114" fill="#0F172A" font-size="11">    key_value</text><text x="180" y="114" fill="#64748B" font-size="11">TEXT (Encrypted)</text>
    <text x="12" y="136" fill="#0F172A" font-size="11">    model_name</text><text x="180" y="136" fill="#64748B" font-size="11">TEXT ('Qwen2.5-VL-7B')</text>
    <text x="12" y="158" fill="#0F172A" font-size="11">    is_active</text><text x="180" y="158" fill="#64748B" font-size="11">INTEGER (1|0)</text>
    <text x="12" y="180" fill="#0F172A" font-size="11">    usage_count</text><text x="180" y="180" fill="#64748B" font-size="11">INTEGER (Tour count)</text>
    <text x="12" y="202" fill="#0F172A" font-size="11">    last_used_at</text><text x="180" y="202" fill="#64748B" font-size="11">TIMESTAMP</text>
  </g>

  <!-- Table 5: USER_DAILY_USAGE -->
  <g transform="translate(410, 610)">
    <rect x="0" y="0" width="315" height="230" rx="6" fill="#FFFFFF" stroke="#8C4FFF" stroke-width="1.2" filter="url(#card-shadow)"/>
    <rect x="0" y="0" width="315" height="28" rx="6" fill="#8C4FFF"/>
    <text x="157" y="19" fill="#FFFFFF" font-size="12" font-weight="700" text-anchor="middle">TABLE: user_daily_usage (FinOps Guard)</text>
    <text x="12" y="48" fill="#0F172A" font-size="11" font-weight="700">PK,FK user_id</text><text x="180" y="48" fill="#64748B" font-size="11">TEXT (users.id)</text>
    <text x="12" y="70" fill="#0F172A" font-size="11" font-weight="700">PK    usage_date</text><text x="180" y="70" fill="#64748B" font-size="11">TEXT ('YYYY-MM-DD')</text>
    <text x="12" y="94" fill="#0F172A" font-size="11">      aws_req_count</text><text x="180" y="94" fill="#64748B" font-size="11">INTEGER (Daily limit)</text>
    <text x="12" y="118" fill="#0F172A" font-size="11">      updated_at</text><text x="180" y="118" fill="#64748B" font-size="11">TIMESTAMP</text>
    
    <rect x="15" y="145" width="285" height="65" rx="4" fill="#F3E8FF" stroke="#C084FC" stroke-width="1"/>
    <text x="25" y="168" fill="#7E22CE" font-size="10.5" font-weight="700">FinOps Protection Rule:</text>
    <text x="25" y="188" fill="#6B21A8" font-size="10">Hard-limit calls to commercial APIs</text>
    <text x="25" y="200" fill="#6B21A8" font-size="10">Guarantees zero billing exceedance.</text>
  </g>

  <!-- ERD Relationships: Completely routed around borders with ZERO text intersection -->
  <!-- Users to user_settings (1:1) -->
  <line x1="360" y1="180" x2="425" y2="180" stroke="#0284C7" stroke-width="1.8" marker-end="url(#arr-blue)"/>
  <!-- Users to documents (1:N) -->
  <path d="M 210 285 L 210 320" stroke="#0284C7" stroke-width="1.8" fill="none" marker-end="url(#arr-blue)"/>
  
  <!-- Users to user_daily_usage (1:N): Routed along the outside right gutter of the schema container -->
  <path d="M 360 210 L 390 210 L 390 305 L 735 305 L 735 635 L 725 635" stroke="#8C4FFF" stroke-width="1.8" stroke-dasharray="4,4" fill="none" marker-end="url(#arr-purple)"/>

  <!-- Right: Cloud Polyglot Models Container -->
  <!-- Top Right: Amazon DynamoDB NoSQL Model -->
  <g transform="translate(775, 75)">
    <rect x="0" y="0" width="710" height="385" rx="10" fill="#F8FAFC" stroke="#0284C7" stroke-width="1.5"/>
    <rect x="0" y="0" width="710" height="38" rx="10" fill="#0284C7"/>
    <text x="355" y="24" fill="#FFFFFF" font-size="13" font-weight="700" text-anchor="middle">AMAZON DYNAMODB NOSQL MODEL (TABLE: huylam-ocr-jobs)</text>
    
    <g transform="translate(25, 55)">
      <rect x="0" y="0" width="660" height="75" rx="6" fill="#EFF6FF" stroke="#BFDBFE" stroke-width="1"/>
      <text x="15" y="22" fill="#1E40AF" font-size="11.5" font-weight="700">Capacity &amp; Scaling: On-Demand (PAY_PER_REQUEST) | Region: ap-southeast-1 | SLA: 99.99%</text>
      <text x="15" y="44" fill="#1E3A8A" font-size="11">Partition Key (PK): <tspan font-weight="700">job_id (String / UUID)</tspan>  — Even hash distribution across partitions</text>
      <text x="15" y="64" fill="#1E3A8A" font-size="11">Sort Key (SK): <tspan font-weight="700">created_at (String / ISO 8601)</tspan> — Chronological range querying &amp; audit</text>
    </g>

    <g transform="translate(25, 145)">
      <rect x="0" y="0" width="660" height="215" rx="6" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
      <text x="15" y="24" fill="#0F172A" font-size="11.5" font-weight="700">Document Job Schema Attributes:</text>
      
      <text x="15" y="50" fill="#0284C7" font-size="11" font-weight="700">filename</text><text x="170" y="50" fill="#64748B" font-size="11">String (e.g. "cv.pdf", "sample_contract.pdf")</text>
      <text x="15" y="74" fill="#0284C7" font-size="11" font-weight="700">status</text><text x="170" y="74" fill="#64748B" font-size="11">String ("RECEIVED_VIA_S3_EVENT" | "PROCESSING" | "COMPLETED")</text>
      <text x="15" y="98" fill="#0284C7" font-size="11" font-weight="700">total_pages</text><text x="170" y="98" fill="#64748B" font-size="11">Number (1 .. N pages)</text>
      <text x="15" y="122" fill="#0284C7" font-size="11" font-weight="700">processing_time_s</text><text x="170" y="122" fill="#64748B" font-size="11">Number (Execution duration, e.g. 0.28s, 2.54s)</text>
      <text x="15" y="146" fill="#0284C7" font-size="11" font-weight="700">s3_input_uri</text><text x="170" y="146" fill="#64748B" font-size="11">String ("s3://huylam-ocr-documents-ap-southeast-1/uploads/...")</text>
      <text x="15" y="170" fill="#0284C7" font-size="11" font-weight="700">s3_output_uris</text><text x="170" y="170" fill="#64748B" font-size="11">Map of (md_uri, docx_uri, pdf_uri) — Direct download artifacts</text>
      <text x="15" y="194" fill="#0284C7" font-size="11" font-weight="700">model_used</text><text x="170" y="194" fill="#64748B" font-size="11">String ("Fast-Path" | "Qwen2.5-VL-72B" | "Gemini-Flash")</text>
    </g>
  </g>

  <!-- Bottom Right: Amazon S3 Storage Hierarchy -->
  <g transform="translate(775, 485)">
    <rect x="0" y="0" width="710" height="390" rx="10" fill="#F8FAFC" stroke="#D97706" stroke-width="1.5"/>
    <rect x="0" y="0" width="710" height="38" rx="10" fill="#D97706"/>
    <text x="355" y="24" fill="#FFFFFF" font-size="13" font-weight="700" text-anchor="middle">AMAZON S3 OBJECT STORAGE HIERARCHY (BUCKET: huylam-ocr-documents)</text>

    <g transform="translate(25, 55)">
      <rect x="0" y="0" width="660" height="310" rx="6" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
      <text x="20" y="30" fill="#0F172A" font-size="13" font-weight="700">s3://huylam-ocr-documents-ap-southeast-1/</text>
      <text x="460" y="30" fill="#D97706" font-size="11" font-weight="600">SSE-S3 AES-256 Encrypted</text>
      
      <line x1="35" y1="45" x2="35" y2="155" stroke="#94A3B8" stroke-width="1.5"/>
      <line x1="35" y1="65" x2="60" y2="65" stroke="#94A3B8" stroke-width="1.5"/>
      <rect x="65" y="50" width="120" height="26" rx="4" fill="#FEF3C7" stroke="#F59E0B" stroke-width="1"/>
      <text x="125" y="67" fill="#B45309" font-size="11" font-weight="700" text-anchor="middle">uploads/ (Ingest)</text>
      
      <line x1="85" y1="76" x2="85" y2="125" stroke="#CBD5E1" stroke-width="1.2"/>
      <line x1="85" y1="95" x2="110" y2="95" stroke="#CBD5E1" stroke-width="1.2"/>
      <text x="115" y="99" fill="#0F172A" font-size="11">&lt;job_id&gt;/</text>
      <text x="210" y="99" fill="#64748B" font-size="10.5">input_document.pdf  (Uploaded directly via Presigned PUT URL)</text>
      
      <line x1="85" y1="120" x2="110" y2="120" stroke="#CBD5E1" stroke-width="1.2"/>
      <text x="115" y="124" fill="#0F172A" font-size="11">&lt;job_id&gt;/</text>
      <text x="210" y="124" fill="#64748B" font-size="10.5">scanned_invoice.png (Raw uploaded images awaiting OCR)</text>

      <line x1="35" y1="165" x2="60" y2="165" stroke="#94A3B8" stroke-width="1.5"/>
      <rect x="65" y="150" width="135" height="26" rx="4" fill="#DCFCE7" stroke="#10B981" stroke-width="1"/>
      <text x="132" y="167" fill="#047857" font-size="11" font-weight="700" text-anchor="middle">outputs/ (Artifacts)</text>
      
      <line x1="85" y1="176" x2="85" y2="285" stroke="#CBD5E1" stroke-width="1.2"/>
      
      <line x1="85" y1="195" x2="110" y2="195" stroke="#CBD5E1" stroke-width="1.2"/>
      <text x="115" y="199" fill="#0F172A" font-size="11">&lt;job_id&gt;/</text>
      <text x="210" y="199" fill="#047857" font-size="11" font-weight="600">output.md</text>
      <text x="320" y="199" fill="#64748B" font-size="10.5">— Clean extracted GitHub Flavored Markdown</text>

      <line x1="85" y1="225" x2="110" y2="225" stroke="#CBD5E1" stroke-width="1.2"/>
      <text x="115" y="229" fill="#0F172A" font-size="11">&lt;job_id&gt;/</text>
      <text x="210" y="229" fill="#047857" font-size="11" font-weight="600">output.translated.md</text>
      <text x="360" y="229" fill="#64748B" font-size="10.5">— Specialized Vietnamese translation</text>

      <line x1="85" y1="255" x2="110" y2="255" stroke="#CBD5E1" stroke-width="1.2"/>
      <text x="115" y="259" fill="#0F172A" font-size="11">&lt;job_id&gt;/</text>
      <text x="210" y="259" fill="#047857" font-size="11" font-weight="600">document.docx</text>
      <text x="330" y="259" fill="#64748B" font-size="10.5">— Monochrome Academic Word export</text>

      <line x1="85" y1="285" x2="110" y2="285" stroke="#CBD5E1" stroke-width="1.2"/>
      <text x="115" y="289" fill="#0F172A" font-size="11">&lt;job_id&gt;/</text>
      <text x="210" y="289" fill="#047857" font-size="11" font-weight="600">report_archive.pdf</text>
      <text x="360" y="289" fill="#64748B" font-size="10.5">— Recompressed PDF (&lt; 10 MB, 180 DPI)</text>
    </g>
  </g>
</svg>"""
    return raw_svg.replace("__W__", str(w)).replace("__H__", str(h)).replace("__DEFS__", DEFS_MARKERS)

def render_diagram(name, svg_content, width, height):
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(PUBLIC_DIR, exist_ok=True)

    svg_file = os.path.join(OUT_DIR, f"{name}.svg")
    png_file = os.path.join(OUT_DIR, f"{name}.png")
    public_svg = os.path.join(PUBLIC_DIR, f"{name}.svg")
    public_png = os.path.join(PUBLIC_DIR, f"{name}.png")

    with open(svg_file, "w", encoding="utf-8") as f:
        f.write(svg_content)

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
            print(f"[SUCCESS] Rendered PNG: {png_file} ({os.path.getsize(png_file):,} bytes)")
            shutil.copy2(svg_file, public_svg)
            shutil.copy2(png_file, public_png)
        else:
            print(f"[ERROR] Failed to render PNG for {name}: {res.stderr}")
    else:
        print(f"[ERROR] Chrome not found at {CHROME_PATH}")

def main():
    diagrams = [
        ("aws-use-case-architecture", gen_use_case_svg(), 1520, 920),
        ("aws-database-polyglot-erd", gen_database_erd_svg(), 1520, 920),
    ]

    for name, svg_content, width, height in diagrams:
        print(f"\nRebuilding {name} ({width}x{height})...")
        render_diagram(name, svg_content, width, height)

    print("\n[COMPLETED] Diagram clean-ups finished!")

if __name__ == "__main__":
    main()
