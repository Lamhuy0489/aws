#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/build_defense_presentation_slides.py
Tự động khởi tạo bộ Slide thuyết trình Bảo vệ Thực tập Tốt nghiệp HUCE (18 Slides)
định dạng PowerPoint (.pptx) chuẩn 16:9 Widescreen, tích hợp đầy đủ sơ đồ kiến trúc,
ảnh chụp minh chứng thực tế, bảng số liệu Benchmark và lời thoại thuyết trình (Speaker Notes).
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(PROJECT_ROOT, "bao cao tot nghiep")
PPTX_PATH = os.path.join(OUT_DIR, "Slide_Bao_Cao_Tot_Nghiep_HUCE_Lam_Quang_Huy.pptx")
STATIC_DOWNLOADS_PPTX = os.path.join(PROJECT_ROOT, "workshop", "static", "downloads", "Slide_Bao_Cao_Tot_Nghiep_HUCE_Lam_Quang_Huy.pptx")

# Màu sắc thương hiệu kỹ thuật & AWS Well-Architected
COLOR_NAVY = RGBColor(35, 47, 62)       # AWS Squid Ink (#232F3E)
COLOR_ORANGE = RGBColor(255, 153, 0)     # AWS Smile Orange (#FF9900)
COLOR_DARK = RGBColor(30, 41, 59)        # Slate 800 (#1E293B)
COLOR_LIGHT_BG = RGBColor(248, 250, 252) # Slate 50 (#F8FAFC)
COLOR_BORDER = RGBColor(226, 232, 240)   # Slate 200 (#E2E8F0)
COLOR_MUTED = RGBColor(100, 116, 139)    # Slate 500 (#64748B)
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_BLUE = RGBColor(2, 132, 199)       # Sky 600 (#0284C7)

def create_slide_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_header(slide, tag_text, title_text, slide_num):
        # Header background banner
        header_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
        header_shape.fill.solid()
        header_shape.fill.fore_color.rgb = COLOR_NAVY
        header_shape.line.color.rgb = COLOR_NAVY

        # Orange Accent Line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.08), Inches(13.333), Inches(0.04))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_ORANGE
        line.line.color.rgb = COLOR_ORANGE

        # Header Text Frame
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.0), Inches(0.85))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_tag = tf.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.name = "Arial"
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = COLOR_ORANGE

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = "Arial"
        p_title.font.size = Pt(20)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_WHITE

        # Slide Number
        num_box = slide.shapes.add_textbox(Inches(11.8), Inches(0.3), Inches(1.0), Inches(0.5))
        ntf = num_box.text_frame
        p_num = ntf.paragraphs[0]
        p_num.text = f"{slide_num:02d} / 18"
        p_num.font.name = "Arial"
        p_num.font.size = Pt(12)
        p_num.font.bold = True
        p_num.font.color.rgb = COLOR_ORANGE
        p_num.alignment = PP_ALIGN.RIGHT

    def set_speaker_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # =========================================================================
    # SLIDE 1: BÌA BÁO CÁO (TITLE SLIDE)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_NAVY
    bg1.line.color.rgb = COLOR_NAVY

    # Orange Accent Bar on Top
    bar1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    bar1.fill.solid()
    bar1.fill.fore_color.rgb = COLOR_ORANGE
    bar1.line.color.rgb = COLOR_ORANGE

    # University Info
    tx1 = s1.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.333), Inches(1.0))
    tf1 = tx1.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "TRƯỜNG ĐẠI HỌC XÂY DỰNG HÀ NỘI (HUCE) — KHOA CÔNG NGHỆ THÔNG TIN"
    p1.font.name = "Arial"
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_ORANGE

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "BÁO CÁO THỰC TẬP TỐT NGHIỆP — BIỂU MẪU TTTN-06"
    p1_sub.font.name = "Arial"
    p1_sub.font.size = Pt(12)
    p1_sub.font.color.rgb = RGBColor(203, 213, 225)

    # Main Project Title
    tx_title = s1.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.333), Inches(2.2))
    tft = tx_title.text_frame
    tft.word_wrap = True
    pt = tft.paragraphs[0]
    pt.text = "NỀN TẢNG PHI MÁY CHỦ BÓC TÁCH VÀ DỊCH THUẬT\nTÀI LIỆU KỸ THUẬT HYBRID TRÊN ĐÁM MÂY AWS"
    pt.font.name = "Arial"
    pt.font.size = Pt(28)
    pt.font.bold = True
    pt.font.color.rgb = COLOR_WHITE

    pt_en = tft.add_paragraph()
    pt_en.text = "Serverless Hybrid Document OCR, Parsing & Technical Translation Platform on AWS"
    pt_en.font.name = "Arial"
    pt_en.font.size = Pt(15)
    pt_en.font.italic = True
    pt_en.font.color.rgb = COLOR_ORANGE

    # Student & Mentor Details Card
    card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.7), Inches(11.333), Inches(2.1))
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(45, 62, 80)
    card.line.color.rgb = RGBColor(71, 85, 105)

    tx_info = s1.shapes.add_textbox(Inches(1.3), Inches(4.85), Inches(10.7), Inches(1.8))
    tfi = tx_info.text_frame
    
    p_info1 = tfi.paragraphs[0]
    p_info1.text = "Sinh viên thực hiện:  LÂM QUANG HUY          MSSV: 0212267          Lớp: 67CS (Khoa học Máy tính)"
    p_info1.font.name = "Arial"
    p_info1.font.size = Pt(13)
    p_info1.font.bold = True
    p_info1.font.color.rgb = COLOR_WHITE

    p_info2 = tfi.add_paragraph()
    p_info2.text = "Giảng viên hướng dẫn: ThS. Lê Văn Minh (Khoa Công nghệ Thông tin - HUCE)"
    p_info2.font.name = "Arial"
    p_info2.font.size = Pt(12)
    p_info2.font.color.rgb = RGBColor(226, 232, 240)

    p_info3 = tfi.add_paragraph()
    p_info3.text = "Đơn vị thực tập:      CÔNG TY TNHH AMAZON WEB SERVICES VIỆT NAM"
    p_info3.font.name = "Arial"
    p_info3.font.size = Pt(12)
    p_info3.font.color.rgb = RGBColor(226, 232, 240)

    p_info4 = tfi.add_paragraph()
    p_info4.text = "Cán bộ hướng dẫn:     Nguyễn Gia Hưng (Email: hunggia@amazon.com.vn) — FCAJ Bootcamp 2026"
    p_info4.font.name = "Arial"
    p_info4.font.size = Pt(12)
    p_info4.font.color.rgb = COLOR_ORANGE

    set_speaker_notes(s1, "Kính thưa Thầy/Cô trong Hội đồng chấm thi, em xin phép được trình bày Báo cáo thực tập tốt nghiệp với đề tài: Xây dựng nền tảng phi máy chủ bóc tách và dịch thuật tài liệu kỹ thuật Hybrid trên đám mây AWS. Đề tài được hoàn thành trong kỳ thực tập tại Công ty TNHH Amazon Web Services Việt Nam dưới sự hướng dẫn của ThS. Lê Văn Minh và cán bộ hướng dẫn tại AWS là anh Nguyễn Gia Hưng.")

    # =========================================================================
    # SLIDE 2: ĐƠN VỊ THỰC TẬP (AWS VIETNAM)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Phần 1: Giới thiệu Đơn vị Thực tập", "Công ty TNHH Amazon Web Services Việt Nam & FCAJ Bootcamp", 2)
    
    # Left Content Box
    tx_l2 = s2.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(6.5), Inches(5.5))
    tf_l2 = tx_l2.text_frame
    tf_l2.word_wrap = True
    
    p = tf_l2.paragraphs[0]
    p.text = "Tổng quan Đơn vị Thực tập:"
    p.font.name = "Arial"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK

    bullets2 = [
        ("Vị thế hàng đầu", "AWS là nền tảng điện toán đám mây số 1 thế giới với hơn 200 dịch vụ hoàn chỉnh trên các trung tâm dữ liệu toàn cầu."),
        ("AWS Việt Nam", "Đồng hành thúc đẩy chuyển đổi số quốc gia, hỗ trợ xây dựng năng lực điện toán đám mây cho kỹ sư và sinh viên."),
        ("Chương trình FCAJ", "First Cloud AI Journey (Workforce Bootcamp 2026) — Đào tạo chuyên sâu về Cloud Architecture, DevOps và Generative AI."),
        ("Văn hóa Doanh nghiệp", "Tuân thủ nghiêm ngặt 16 Nguyên lý Lãnh đạo của Amazon (Leadership Principles: Customer Obsession, Ownership, Invent and Simplify, Deliver Results).")
    ]
    for b_title, b_desc in bullets2:
        p_b = tf_l2.add_paragraph()
        p_b.text = f"• {b_title}: {b_desc}"
        p_b.font.name = "Arial"
        p_b.font.size = Pt(12.5)
        p_b.font.color.rgb = COLOR_DARK

    # Right Card: Objectives
    rc2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.7), Inches(1.5), Inches(4.8), Inches(5.3))
    rc2.fill.solid()
    rc2.fill.fore_color.rgb = COLOR_LIGHT_BG
    rc2.line.color.rgb = COLOR_BORDER

    tx_rc2 = s2.shapes.add_textbox(Inches(8.0), Inches(1.7), Inches(4.2), Inches(4.9))
    tf_rc2 = tx_rc2.text_frame
    tf_rc2.word_wrap = True
    
    prc = tf_rc2.paragraphs[0]
    prc.text = "Mục tiêu 12 Tuần Thực tập:"
    prc.font.name = "Arial"
    prc.font.size = Pt(15)
    prc.font.bold = True
    prc.font.color.rgb = COLOR_BLUE

    rc_bullets = [
        "1. Làm chủ kiến trúc đám mây chuẩn AWS Well-Architected Framework (Multi-AZ, Zero-Trust).",
        "2. Phát triển Capstone Project hoàn chỉnh giải quyết bài toán xử lý tài liệu kỹ thuật thực tế.",
        "3. Áp dụng kỷ luật tài chính đám mây FinOps (vận hành toàn trình với chi phí 0.00 USD).",
        "4. Xây dựng tài liệu kỹ thuật chuẩn quốc tế và hoàn thành báo cáo tốt nghiệp 42 trang theo quy chuẩn HUCE."
    ]
    for b in rc_bullets:
        pb = tf_rc2.add_paragraph()
        pb.text = b
        pb.font.name = "Arial"
        pb.font.size = Pt(12)
        pb.font.color.rgb = COLOR_DARK

    set_speaker_notes(s2, "Tại AWS Việt Nam, chương trình First Cloud AI Journey kéo dài 12 tuần đặt mục tiêu giúp sinh viên cọ xát với văn hóa chuẩn mực toàn cầu của Amazon, đồng thời trực tiếp triển khai dự án Capstone với tiêu chuẩn kỹ thuật doanh nghiệp.")

    # =========================================================================
    # SLIDE 3: ĐẶT VẤN ĐỀ & BÀI TOÁN KỸ THUẬT
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Phần 2: Bối cảnh & Bài toán Kỹ thuật", "Thách thức trong Bóc tách & Dịch thuật Tài liệu Kỹ thuật", 3)

    challenges = [
        ("THÁCH THỨC 1: CẤU TRÚC PHỨC TẠP", "Tài liệu kỹ thuật, kiến trúc, xây dựng chứa nhiều bảng biểu số liệu, văn bản 2 cột, công thức toán và sơ đồ hình ảnh. Các công cụ OCR văn phòng thông thường làm vỡ hoàn toàn định dạng bảng.", COLOR_NAVY),
        ("THÁCH THỨC 2: CHI PHÍ & TỐC ĐỘ", "Việc gọi toàn bộ qua các Vision LLM thương mại lớn rất tốn kém (hàng chục USD/tài liệu) và độ trễ cao (hơn 10 giây/trang). Trong khi 80% tài liệu kỹ thuật là PDF số có sẵn văn bản vector.", COLOR_BLUE),
        ("THÁCH THỨC 3: GIỚI HẠN 10 MB PAYLOAD", "Amazon API Gateway có hạn mức cố định Payload tối đa 10 MB, gây lỗi 413 Payload Too Large khi tải lên các hồ sơ dự án hoặc sách hướng dẫn kỹ thuật lớn từ 15 MB đến 100 MB.", COLOR_ORANGE)
    ]

    for idx, (ch_title, ch_desc, ch_col) in enumerate(challenges):
        top_pos = 1.4 + idx * 1.8
        c_shape = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top_pos), Inches(11.7), Inches(1.55))
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = COLOR_LIGHT_BG
        c_shape.line.color.rgb = ch_col
        c_shape.line.width = Pt(1.5)

        tx_c = s3.shapes.add_textbox(Inches(1.1), Inches(top_pos + 0.15), Inches(11.1), Inches(1.25))
        tfc = tx_c.text_frame
        tfc.word_wrap = True
        pc1 = tfc.paragraphs[0]
        pc1.text = ch_title
        pc1.font.name = "Arial"
        pc1.font.size = Pt(13.5)
        pc1.font.bold = True
        pc1.font.color.rgb = ch_col

        pc2 = tfc.add_paragraph()
        pc2.text = ch_desc
        pc2.font.name = "Arial"
        pc2.font.size = Pt(12)
        pc2.font.color.rgb = COLOR_DARK

    set_speaker_notes(s3, "Khi tiếp cận bài toán xử lý tài liệu kỹ thuật, chúng ta gặp 3 rào cản lớn: vỡ cấu trúc bảng biểu, chi phí gọi mô hình AI quá cao và nghẽn băng thông do giới hạn 10MB của API Gateway. Dự án giải quyết triệt để cả 3 bài toán này.")

    # =========================================================================
    # SLIDE 4: TỔNG QUAN GIẢI PHÁP & KIẾN TRÚC TỔNG THỂ
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Phần 3: Kiến trúc Hệ thống", "Kiến trúc Tổng thể Serverless Hybrid Document OCR Platform", 4)

    # Left: Explanation
    tx_l4 = s4.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(4.5), Inches(5.8))
    tf_l4 = tx_l4.text_frame
    tf_l4.word_wrap = True

    p = tf_l4.paragraphs[0]
    p.text = "Các Thành phần Nòng cốt:"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    sol_bullets = [
        ("Hạ tầng chuẩn Enterprise", "Mạng ảo VPC Three-Tier Multi-AZ, cân bằng tải Application Load Balancer và máy chủ EC2 Gunicorn."),
        ("Động cơ Hybrid kép", "Tự động phân tầng: Fast-Path Native (0.28s/trang) cho PDF số và Multimodal Vision OCR cho ảnh scan."),
        ("Xử lý phi máy chủ", "Tải tệp qua S3 Presigned URL (vượt trần 10MB) và Lambda kích hoạt theo sự kiện ghi dữ liệu DynamoDB."),
        ("Dịch thuật chuyên sâu", "Tích hợp LLM với Key Tour Manager xoay vòng khóa API và bộ xuất bản Word, PDF chuẩn học thuật.")
    ]
    for b_title, b_desc in sol_bullets:
        pb = tf_l4.add_paragraph()
        pb.text = f"• {b_title}: {b_desc}"
        pb.font.name = "Arial"
        pb.font.size = Pt(11)
        pb.font.color.rgb = COLOR_DARK

    # Right: Architecture Image
    img_sys = os.path.join(PROJECT_ROOT, "workshop/static/images/architecture/aws-system-architecture.png")
    if os.path.exists(img_sys):
        s4.shapes.add_picture(img_sys, Inches(5.5), Inches(1.3), width=Inches(7.2))

    set_speaker_notes(s4, "Đây là sơ đồ kiến trúc tổng thể của hệ thống. Người dùng truy cập qua Application Load Balancer tới Web Studio. Tài liệu được tải trực tiếp lên S3 qua Presigned URL, kích hoạt luồng xử lý phi máy chủ Lambda và động cơ bóc tách kép.")

    # =========================================================================
    # SLIDE 5: SƠ ĐỒ USE CASE HỆ THỐNG
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Phần 3: Phân tích Ca sử dụng", "Sơ đồ Ca sử dụng Tổng thể (Use Case Architecture)", 5)

    tx_l5 = s5.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(5.8), Inches(5.8))
    tf_l5 = tx_l5.text_frame
    tf_l5.word_wrap = True

    p = tf_l5.paragraphs[0]
    p.text = "Phân rã Ca sử dụng theo Tác nhân (Actors):"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    uc_actors = [
        ("Người dùng cuối (End User)", "Đăng nhập/Đăng ký, cấu hình giao diện; Tải tài liệu qua Presigned URL; Xem kết quả bóc tách; Biên tập đối chiếu song ngữ; Tải tệp xuất bản DOCX, PDF, Markdown."),
        ("Hệ thống AWS Event (Lambda)", "Tự động lắng nghe sự kiện s3:ObjectCreated; Khởi tạo Job; Kích hoạt phân tích mật độ ký tự; Cập nhật trạng thái tiến trình vào DynamoDB."),
        ("AI Inference Engine", "Cung cấp năng lực Vision OCR (Qwen2.5-VL / Gemini) cho trang scan; Dịch thuật ngữ kỹ thuật chuyên ngành qua LLM."),
        ("Quản trị viên (Admin)", "Quản lý hạn mức người dùng; Cấu hình xoay vòng API Keys (Key Tour); Giám sát Telemetry trên CloudWatch Dashboard.")
    ]
    for act, desc in uc_actors:
        pb = tf_l5.add_paragraph()
        pb.text = f"• {act}: {desc}"
        pb.font.name = "Arial"
        pb.font.size = Pt(11)
        pb.font.color.rgb = COLOR_DARK

    # Right Card: 4 Major Functional Clusters
    rc5 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.0), Inches(1.4), Inches(5.5), Inches(5.6))
    rc5.fill.solid()
    rc5.fill.fore_color.rgb = COLOR_LIGHT_BG
    rc5.line.color.rgb = COLOR_BORDER

    tx_rc5 = s5.shapes.add_textbox(Inches(7.3), Inches(1.6), Inches(5.0), Inches(5.2))
    tf_rc5 = tx_rc5.text_frame
    tf_rc5.word_wrap = True

    prc5 = tf_rc5.paragraphs[0]
    prc5.text = "4 Nhóm Chức năng Trọng tâm:"
    prc5.font.name = "Arial"
    prc5.font.size = Pt(14)
    prc5.font.bold = True
    prc5.font.color.rgb = COLOR_BLUE

    clusters = [
        ("1. Quản lý Xác thực & Cấu hình", "JWT Token, phân quyền Role-based, lưu cấu hình ngôn ngữ đích và chế độ Fast-Path ưu tiên."),
        ("2. Tiếp nhận & Phân loại Thông minh", "Kiểm tra định dạng, phân tích mật độ ký tự số (Character Density) tự động phân nhánh."),
        ("3. Xử lý & Xuất bản Đa định dạng", "Bóc tách giữ nguyên bảng biểu, dịch thuật ngữ kỹ thuật, xuất Markdown, Word chuẩn học thuật, PDF in ấn."),
        ("4. Quản trị & Giám sát FinOps", "Bảo toàn số dư 0.00 USD, luân chuyển API keys chống Rate Limit, lưu vết CloudWatch Logs.")
    ]
    for c_title, c_desc in clusters:
        pb = tf_rc5.add_paragraph()
        pb.text = f"{c_title}\n{c_desc}"
        pb.font.name = "Arial"
        pb.font.size = Pt(11)
        pb.font.color.rgb = COLOR_DARK

    set_speaker_notes(s5, "Về mặt chức năng, hệ thống được thiết kế với 4 nhóm ca sử dụng lớn phục vụ hai đối tượng chính là Người dùng cuối và Quản trị viên, cùng sự phối hợp tự động của tác nhân phi máy chủ AWS và AI Engine.")

    # =========================================================================
    # SLIDE 6: KIẾN TRÚC MẠNG AWS VPC MULTI-AZ
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Phần 3: Hạ tầng Đám mây", "Mạng ảo Amazon VPC Three-Tier Multi-AZ Độ Sẵn Sàng Cao", 6)

    tx_l6 = s6.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(4.5), Inches(5.8))
    tf_l6 = tx_l6.text_frame
    tf_l6.word_wrap = True

    p = tf_l6.paragraphs[0]
    p.text = "Thông số Mạng Doanh nghiệp:"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    vpc_bullets = [
        ("Khu vực triển khai", "ap-southeast-1 (Singapore) với 2 Availability Zones độc lập (1a và 1b)."),
        ("Dải mạng tùy biến", "Custom VPC CIDR 10.0.0.0/16 (huylam-vpc), không sử dụng Default VPC."),
        ("Public Subnets", "2 Subnets (10.0.0.0/20 & 10.0.16.0/20) chứa Application Load Balancer và Internet Gateway."),
        ("Private Subnets", "2 Subnets (10.0.128.0/20 & 10.0.144.0/20) cô lập máy chủ tính toán EC2."),
        ("Cơ chế dự phòng", "Standby Target Group tự động chuyển mạch khi phát hiện sự cố vùng.")
    ]
    for b_title, b_desc in vpc_bullets:
        pb = tf_l6.add_paragraph()
        pb.text = f"• {b_title}: {b_desc}"
        pb.font.name = "Arial"
        pb.font.size = Pt(11)
        pb.font.color.rgb = COLOR_DARK

    img_vpc = os.path.join(PROJECT_ROOT, "workshop/static/images/architecture/aws-vpc-network-architecture.png")
    if os.path.exists(img_vpc):
        s6.shapes.add_picture(img_vpc, Inches(5.5), Inches(1.3), width=Inches(7.2))

    set_speaker_notes(s6, "Mô hình mạng VPC Three-Tier Multi-AZ giúp cô lập máy chủ EC2 trong phân vùng mạng riêng (Private Subnet), hoàn toàn không gán IP công cộng. Chỉ có Application Load Balancer nằm ở Public Subnet mới được tiếp nhận kết nối Internet.")

    # =========================================================================
    # SLIDE 7: BẢO MẬT ZERO-TRUST & SECURITY GROUP CHAINING
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Phần 3: An ninh Đám mây", "Cơ chế Bảo mật Zero-Trust & Security Group Chaining", 7)

    tx_l7 = s7.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(4.5), Inches(5.8))
    tf_l7 = tx_l7.text_frame
    tf_l7.word_wrap = True

    p = tf_l7.paragraphs[0]
    p.text = "Chuỗi An ninh Phân tầng:"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    sec_bullets = [
        ("ALB Security Group", "Chỉ mở cổng Inbound HTTP 80 cho dải 0.0.0.0/0 tiếp nhận người dùng."),
        ("EC2 Security Group", "Chỉ cho phép Inbound cổng 5000 tham chiếu trực tiếp ID của ALB Security Group. Chặn 100% kết nối trực tiếp từ Internet."),
        ("Zero Open Port 22", "Đóng hoàn toàn cổng SSH 22. Quản trị máy chủ thông qua AWS Systems Manager (SSM) Session Manager qua kênh TLS 443 an toàn."),
        ("Mã hóa Dữ liệu", "Mã hóa đường truyền TLS và mã hóa tại chỗ SSE-S3 AES-256 cho toàn bộ tài liệu lưu trữ.")
    ]
    for b_title, b_desc in sec_bullets:
        pb = tf_l7.add_paragraph()
        pb.text = f"• {b_title}: {b_desc}"
        pb.font.name = "Arial"
        pb.font.size = Pt(11)
        pb.font.color.rgb = COLOR_DARK

    img_sec = os.path.join(PROJECT_ROOT, "workshop/static/images/architecture/aws-security-group-chaining.png")
    if os.path.exists(img_sec):
        s7.shapes.add_picture(img_sec, Inches(5.5), Inches(1.3), width=Inches(7.2))

    set_speaker_notes(s7, "Cơ chế Security Group Chaining loại bỏ hoàn toàn khả năng máy chủ EC2 bị tấn công trực tiếp từ bên ngoài. Thêm vào đó, việc loại bỏ cổng SSH 22 và thay thế bằng AWS Systems Manager đảm bảo quản trị an toàn tuyệt đối mà không cần quản lý private keys.")

    # =========================================================================
    # SLIDE 8: ĐỘNG CƠ BÓC TÁCH KÉP HYBRID OCR ENGINE
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Phần 3: Trọng tâm Kỹ thuật", "Động cơ Bóc tách Kép Thông minh (Dual-Engine Hybrid Parser)", 8)

    tx_l8 = s8.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(4.5), Inches(5.8))
    tf_l8 = tx_l8.text_frame
    tf_l8.word_wrap = True

    p = tf_l8.paragraphs[0]
    p.text = "Thuật toán Phân tầng Tối ưu:"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    engine_bullets = [
        ("Tầng 1 (Fast-Path Native)", "Phân tích cấu trúc vector của PDF bằng PyMuPDF. Tốc độ 0.28s/trang, chi phí 0.00 USD, giữ 100% bảng biểu."),
        ("Ngưỡng Mật độ Ký tự", "Kiểm tra Character Density Threshold (0.05). Nếu trang có mật độ chữ cao -> kích hoạt Fast-Path tức thì."),
        ("Tầng 2 (Vision Multimodal OCR)", "Kích hoạt với trang scan hoặc chữ viết tay. Sử dụng Qwen2.5-VL 72B (Kaggle GPU) kết hợp tự động Failover sang Gemini Flash."),
        ("Hiệu quả Đột phá", "85% tài liệu số được xử lý tức thì, giảm 90% chi phí và thời gian so với phương pháp gọi AI truyền thống.")
    ]
    for b_title, b_desc in engine_bullets:
        pb = tf_l8.add_paragraph()
        pb.text = f"• {b_title}: {b_desc}"
        pb.font.name = "Arial"
        pb.font.size = Pt(11)
        pb.font.color.rgb = COLOR_DARK

    img_ocr = os.path.join(PROJECT_ROOT, "workshop/static/images/architecture/aws-hybrid-ocr-engine-architecture.png")
    if os.path.exists(img_ocr):
        s8.shapes.add_picture(img_ocr, Inches(5.5), Inches(1.3), width=Inches(7.2))

    set_speaker_notes(s8, "Đây là đóng góp kỹ thuật trọng tâm của đề tài. Nhờ thuật toán nhận diện mật độ ký tự số, hệ thống giải phóng 85% tài liệu số qua tầng Fast-Path native chỉ mất 0.28 giây/trang với chi phí 0 đồng, chỉ chuyển các trang scan thực sự sang tầng Vision OCR.")

    # =========================================================================
    # SLIDE 9: ĐƯỜNG ỐNG PHI MÁY CHỦ (SERVERLESS EVENT PIPELINE)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Phần 3: Tối ưu Băng thông", "Đường ống Phi máy chủ Hướng sự kiện (Event-Driven Pipeline)", 9)

    tx_l9 = s9.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(4.5), Inches(5.8))
    tf_l9 = tx_l9.text_frame
    tf_l9.word_wrap = True

    p = tf_l9.paragraphs[0]
    p.text = "Khắc phục Trần 10MB API Gateway:"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    pipe_bullets = [
        ("S3 Presigned URL", "Trình duyệt gửi yêu cầu ký URL SigV4. Trình duyệt đẩy trực tiếp tệp PDF/ảnh lên S3 Bucket mà không qua API Gateway."),
        ("S3 Event Notification", "Khi tệp ghi thành công, sự kiện s3:ObjectCreated kích hoạt hàm AWS Lambda huylam-ocr-processor."),
        ("AWS Lambda Siêu tốc", "Hàm Lambda khởi chạy trong 214 ms, bộ nhớ tiêu thụ chỉ 88 MB / 128 MB, phân tích metadata."),
        ("Amazon DynamoDB", "Tự động ghi nhận bản ghi tiến trình với trạng thái PROCESSING và chuyển giao tác vụ bóc tách.")
    ]
    for b_title, b_desc in pipe_bullets:
        pb = tf_l9.add_paragraph()
        pb.text = f"• {b_title}: {b_desc}"
        pb.font.name = "Arial"
        pb.font.size = Pt(11)
        pb.font.color.rgb = COLOR_DARK

    img_pipe = os.path.join(PROJECT_ROOT, "workshop/static/images/architecture/aws-serverless-event-pipeline.png")
    if os.path.exists(img_pipe):
        s9.shapes.add_picture(img_pipe, Inches(5.5), Inches(1.3), width=Inches(7.2))

    set_speaker_notes(s9, "Bằng việc ứng dụng cơ chế S3 Presigned URL, hệ thống hoàn toàn vượt qua rào cản 10MB của API Gateway, cho phép người dùng kéo thả tài liệu dung lượng lớn lên tới 100MB một cách mượt mà và an toàn.")

    # =========================================================================
    # SLIDE 10: THIẾT KẾ CƠ SỞ DỮ LIỆU (POLYGLOT PERSISTENCE & ERD)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Phần 3: Thiết kế Dữ liệu", "Mô hình Dữ liệu Đa công nghệ (Polyglot Persistence & ERD)", 10)

    # 3 Database Cards
    db_cards = [
        ("AMAZON DYNAMODB (NoSQL)", "Bảng huylam-ocr-jobs (On-Demand Mode)\n• Partition Key: job_id (UUID duy nhất)\n• Sort Key: created_at (Timestamp ISO 8601)\n• Thuộc tính: filename, status, total_pages, digital_pages, scanned_pages, processing_time_seconds, s3_uris.\n• Vai trò: Lưu trạng thái xử lý phi máy chủ, hỗ trợ hàng triệu truy vấn với độ trễ < 10ms, chi phí 0.00 USD.", COLOR_BLUE),
        ("AMAZON S3 OBJECT STORAGE", "Bucket huylam-ocr-documents (Singapore)\n• uploads/{job_id}/: Chứa tài liệu gốc (PDF/ảnh) từ Presigned URL.\n• outputs/{job_id}/: Chứa kết quả trích xuất Markdown, bản dịch tiếng Việt, tệp Word (.docx) và PDF (.pdf).\n• Vai trò: Kho dữ liệu phi cấu trúc an toàn, độ bền 99.999999999% (11 số 9), mã hóa SSE-S3 AES-256.", COLOR_ORANGE),
        ("CƠ SỞ DỮ LIỆU QUAN HỆ (SQL)", "Schema 5 bảng quan hệ chuẩn hóa:\n• users: id (PK), username, email, password_hash, role.\n• documents: id (PK), user_id (FK), filename, status, markdown, processing_time.\n• api_keys: id (PK), provider, key_value, usage_count.\n• user_settings: user_id (PK, FK), theme, default_model.\n• user_daily_usage: (user_id, usage_date) (PK, FK).", COLOR_NAVY)
    ]

    for idx, (dbc_title, dbc_desc, dbc_col) in enumerate(db_cards):
        left_pos = 0.8 + idx * 4.0
        c_shape = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_pos), Inches(1.4), Inches(3.7), Inches(5.5))
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = COLOR_LIGHT_BG
        c_shape.line.color.rgb = dbc_col
        c_shape.line.width = Pt(1.5)

        tx_c = s10.shapes.add_textbox(Inches(left_pos + 0.15), Inches(1.55), Inches(3.4), Inches(5.2))
        tfc = tx_c.text_frame
        tfc.word_wrap = True
        
        pc1 = tfc.paragraphs[0]
        pc1.text = dbc_title
        pc1.font.name = "Arial"
        pc1.font.size = Pt(12)
        pc1.font.bold = True
        pc1.font.color.rgb = dbc_col

        pc2 = tfc.add_paragraph()
        pc2.text = dbc_desc
        pc2.font.name = "Arial"
        pc2.font.size = Pt(10.5)
        pc2.font.color.rgb = COLOR_DARK

    set_speaker_notes(s10, "Hệ thống kết hợp mô hình lưu trữ đa công nghệ Polyglot Persistence: DynamoDB lưu vết trạng thái công việc phi máy chủ, S3 lưu trữ đối tượng dung lượng lớn và Relational SQL quản lý tài khoản, phân quyền và xoay vòng API keys.")

    # =========================================================================
    # SLIDE 11: MODULE DỊCH THUẬT & KEY TOUR MANAGER
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Phần 3: Trí tuệ Nhân tạo", "Module Dịch thuật Thuật ngữ Kỹ thuật & Key Tour Manager", 11)

    tx_l11 = s11.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(5.8), Inches(5.5))
    tf_l11 = tx_l11.text_frame
    tf_l11.word_wrap = True

    p = tf_l11.paragraphs[0]
    p.text = "Thuật toán Dịch thuật Kỹ thuật:"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    trans_bullets = [
        ("Bảo toàn Thuật ngữ", "Sử dụng Prompt Engineering chuyên sâu bảo toàn nguyên vẹn tên dịch vụ AWS, mã lệnh shell, tham số cấu hình và công thức KaTeX."),
        ("Dịch thuật Bảng biểu", "Dịch chính xác từng ô trong bảng Markdown mà không phá vỡ liên kết dòng và cột."),
        ("Đối chiếu Đoạn văn", "Tự động phân đoạn (Chunking) theo ranh giới đoạn văn logic, đảm bảo ngữ cảnh liền mạch."),
        ("Tốc độ xử lý", "Thời gian dịch trung bình chỉ 2.80 giây cho một trang tài liệu đầy đủ.")
    ]
    for b_title, b_desc in trans_bullets:
        pb = tf_l11.add_paragraph()
        pb.text = f"• {b_title}: {b_desc}"
        pb.font.name = "Arial"
        pb.font.size = Pt(11.5)
        pb.font.color.rgb = COLOR_DARK

    # Right Card: Key Tour Rotation
    rc11 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.0), Inches(1.4), Inches(5.5), Inches(5.5))
    rc11.fill.solid()
    rc11.fill.fore_color.rgb = COLOR_LIGHT_BG
    rc11.line.color.rgb = COLOR_BORDER

    tx_rc11 = s11.shapes.add_textbox(Inches(7.3), Inches(1.6), Inches(5.0), Inches(5.1))
    tf_rc11 = tx_rc11.text_frame
    tf_rc11.word_wrap = True

    prc = tf_rc11.paragraphs[0]
    prc.text = "Cơ chế Xoay vòng Khóa (Key Tour Manager):"
    prc.font.name = "Arial"
    prc.font.size = Pt(14)
    prc.font.bold = True
    prc.font.color.rgb = COLOR_ORANGE

    kt_bullets = [
        ("Phân phối Tải Round-Robin", "Xoay vòng thông minh qua danh sách API keys của nhiều nhà cung cấp (Kaggle GPU, Google Gemini, Groq)."),
        ("Chống nghẽn Rate Limit", "Theo dõi số lượt gọi usage_count và tự động chuyển sang key kế tiếp khi đạt ngưỡng tải."),
        ("Cơ chế Exponential Backoff", "Tự động lùi thời gian thử lại khi gặp mã lỗi 429 Too Many Requests, đảm bảo tỷ lệ gọi thành công 99.99%."),
        ("Quản trị Động", "Cho phép thêm, xóa, bật/tắt khóa trực tiếp từ bảng điều khiển quản trị mà không cần khởi động lại máy chủ.")
    ]
    for b_title, b_desc in kt_bullets:
        pb = tf_rc11.add_paragraph()
        pb.text = f"• {b_title}: {b_desc}"
        pb.font.name = "Arial"
        pb.font.size = Pt(11)
        pb.font.color.rgb = COLOR_DARK

    set_speaker_notes(s11, "Module dịch thuật được trang bị cơ chế Key Tour Manager giúp xoay vòng các API key miễn phí, tự động lùi thời gian khi chạm hạn ngạch, đảm bảo ứng dụng luôn sẵn sàng phục vụ mà không bị gián đoạn.")

    # =========================================================================
    # SLIDE 12: BỘ XUẤT BẢN ĐA ĐỊNH DẠNG CHUẨN HỌC THUẬT
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Phần 3: Xuất bản Tài liệu", "Bộ Xuất bản Đa định dạng Chuẩn Học thuật (Multi-Format Exporters)", 12)

    exp_cards = [
        ("MARKDOWN EXPORTER (.md)", "Chuẩn hóa GitHub-Flavored Markdown\n• Hỗ trợ công thức toán học KaTeX ($...$ và $$...$$).\n• Bảo toàn bảng biểu Markdown chuẩn căn lề.\n• Nhúng hình ảnh sơ đồ kỹ thuật và khối mã nguồn có định dạng cú pháp.", COLOR_NAVY),
        ("MICROSOFT WORD (.docx)", "Monochrome Academic Style\n• Cỡ chữ Times New Roman 13pt, dãn dòng 1.2pt chuẩn in ấn.\n• Bảng biểu viền đen 0.5pt, tiêu đề in đậm nền trong suốt.\n• Căn đều 2 lề (Justified), thụt đầu dòng 1.27 cm chuẩn mực.\n• Siêu liên kết (hyperlinks) giữ nguyên màu xanh bấm được.", COLOR_BLUE),
        ("ADOBE PDF EXPORTER (.pdf)", "Chuẩn Nộp Lưu chiểu (< 10 MB)\n• Tái nén ảnh thông minh PyMuPDF chất lượng cao (quality=92, 180 DPI).\n• Giảm dung lượng từ 10.36 MB xuống 5.11 MB (-50.7%).\n• Bảo toàn 100% 42 trang in và 94 siêu liên kết hoạt động hoàn hảo.", COLOR_ORANGE)
    ]

    for idx, (ec_title, ec_desc, ec_col) in enumerate(exp_cards):
        left_pos = 0.8 + idx * 4.0
        c_shape = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_pos), Inches(1.4), Inches(3.7), Inches(5.5))
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = COLOR_LIGHT_BG
        c_shape.line.color.rgb = ec_col
        c_shape.line.width = Pt(1.5)

        tx_c = s12.shapes.add_textbox(Inches(left_pos + 0.15), Inches(1.55), Inches(3.4), Inches(5.2))
        tfc = tx_c.text_frame
        tfc.word_wrap = True
        
        pc1 = tfc.paragraphs[0]
        pc1.text = ec_title
        pc1.font.name = "Arial"
        pc1.font.size = Pt(12)
        pc1.font.bold = True
        pc1.font.color.rgb = ec_col

        pc2 = tfc.add_paragraph()
        pc2.text = ec_desc
        pc2.font.name = "Arial"
        pc2.font.size = Pt(11)
        pc2.font.color.rgb = COLOR_DARK

    set_speaker_notes(s12, "Bộ xuất bản của hệ thống tạo ra 3 định dạng hoàn chỉnh. Đặc biệt bản Word tuân thủ phong cách học thuật đơn sắc và bản PDF được nén xuống 5.11 MB, sẵn sàng nộp lưu chiểu và in ấn mà không vượt ngưỡng 10MB.")

    # =========================================================================
    # SLIDE 13: GIAO DIỆN WEB STUDIO THỰC TẾ
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Phần 3: Kiểm chứng Ứng dụng", "Giao diện Web Studio & Trình Soạn thảo Đối chiếu Song ngữ", 13)

    img_studio = os.path.join(PROJECT_ROOT, "workshop/static/images/week11/03-studio-cv-extracted-translated.png")
    if os.path.exists(img_studio):
        s13.shapes.add_picture(img_studio, Inches(0.8), Inches(1.3), width=Inches(7.2))

    tx_r13 = s13.shapes.add_textbox(Inches(8.2), Inches(1.3), Inches(4.4), Inches(5.8))
    tf_r13 = tx_r13.text_frame
    tf_r13.word_wrap = True

    p = tf_r13.paragraphs[0]
    p.text = "Tính năng Nổi bật trên Giao diện:"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    studio_bullets = [
        ("Kéo thả Trực quan", "Hỗ trợ kéo thả PDF, PNG, JPG lên tới 50 MB."),
        ("Tùy chọn Chế độ Xử lý", "Tự động phân loại hoặc ép buộc Fast-Path / Vision OCR theo mong muốn."),
        ("Bilingual Side-by-Side", "Trình soạn thảo song ngữ cho phép đọc văn bản gốc bên trái và bản dịch tiếng Việt bên phải song song."),
        ("Xem trước Thời gian thực", "Xem ngay kết quả định dạng và tải về Word, PDF tức thì chỉ với một cú nhấp chuột.")
    ]
    for b_title, b_desc in studio_bullets:
        pb = tf_r13.add_paragraph()
        pb.text = f"• {b_title}: {b_desc}"
        pb.font.name = "Arial"
        pb.font.size = Pt(11.5)
        pb.font.color.rgb = COLOR_DARK

    set_speaker_notes(s13, "Trên màn hình là giao diện Web Studio thực tế đang chạy trên hạ tầng AWS. Người dùng có thể kéo thả tài liệu, xem tiến trình bóc tách và đối chiếu bản gốc - bản dịch song song theo thời gian thực.")

    # =========================================================================
    # SLIDE 14: KẾT QUẢ ĐO KIỂM THỰC NGHIỆM (BENCHMARK)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Phần 3: Đo kiểm Thực nghiệm", "Số liệu Thực nghiệm Hiệu năng & So sánh Động cơ (Benchmark)", 14)

    # Table
    rows, cols = 6, 5
    table_shape = s14.shapes.add_table(rows, cols, Inches(0.8), Inches(1.4), Inches(11.7), Inches(3.2))
    table = table_shape.table

    # Column widths
    table.columns[0].width = Inches(2.8)
    table.columns[1].width = Inches(2.2)
    table.columns[2].width = Inches(2.7)
    table.columns[3].width = Inches(2.0)
    table.columns[4].width = Inches(2.0)

    headers = ["Tác vụ Thực nghiệm", "Tài liệu Kiểm thử", "Động cơ Thực thi", "Thời gian Xử lý", "Chi phí AWS"]
    for c_idx, h in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        p = cell.text_frame.paragraphs[0]
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

    data = [
        ["Bóc tách PDF văn bản số", "cv.pdf (1 trang)", "Fast-Path (PyMuPDF)", "0.31 giây", "0.00 USD"],
        ["Bóc tách bài báo khoa học", "28_Bai_Bao.pdf (11 trang)", "Fast-Path (PyMuPDF)", "3.07 giây (0.28s/trang)", "0.00 USD"],
        ["Bóc tách ảnh scan biểu mẫu", "Ảnh scan hóa đơn", "Vision OCR (Kaggle/Gemini)", "2.54 giây", "0.00 USD"],
        ["Dịch thuật ngữ kỹ thuật", "cv.pdf (Anh -> Việt)", "DocumentTranslator (LLM)", "2.80 giây", "0.00 USD"],
        ["Kết xuất tài liệu Word", "Tệp sau khi dịch", "DocxExporter Module", "0.15 giây", "0.00 USD"]
    ]

    for r_idx, row_data in enumerate(data):
        for c_idx, val in enumerate(row_data):
            cell = table.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_WHITE if r_idx % 2 == 0 else COLOR_LIGHT_BG
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Arial"
            p.font.size = Pt(10.5)
            p.font.color.rgb = COLOR_DARK
            if c_idx >= 3:
                p.alignment = PP_ALIGN.CENTER
                p.font.bold = True
                if c_idx == 4:
                    p.font.color.rgb = RGBColor(16, 149, 193)

    # Bottom Highlight Card
    bot_card = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.9), Inches(11.7), Inches(2.0))
    bot_card.fill.solid()
    bot_card.fill.fore_color.rgb = COLOR_LIGHT_BG
    bot_card.line.color.rgb = COLOR_BLUE

    tx_bot = s14.shapes.add_textbox(Inches(1.0), Inches(5.05), Inches(11.3), Inches(1.7))
    tf_bot = tx_bot.text_frame
    tf_bot.word_wrap = True

    pb1 = tf_bot.paragraphs[0]
    pb1.text = "ĐÁNH GIÁ CHỈ SỐ KỸ THUẬT QUAN TRỌNG:"
    pb1.font.name = "Arial"
    pb1.font.size = Pt(12.5)
    pb1.font.bold = True
    pb1.font.color.rgb = COLOR_BLUE

    eval_bullets = [
        "• Độ chính xác cấu trúc bảng biểu: Đạt 99.4% đối với PDF số thông qua Fast-Path Native.",
        "• Tốc độ bóc tách trung bình: Chỉ 0.28 giây/trang, nhanh hơn gấp 10 lần so với OCR truyền thống.",
        "• Thời gian phản hồi Lambda s3-trigger: Thực thi xong trong 214.37 ms với bộ nhớ tiêu thụ chỉ 88 MB.",
        "• Chi phí toàn trình: Duy trì mức tuyệt đối 0.00 USD xuyên suốt toàn bộ quá trình kiểm thử tải."
    ]
    for b in eval_bullets:
        pb = tf_bot.add_paragraph()
        pb.text = b
        pb.font.name = "Arial"
        pb.font.size = Pt(11)
        pb.font.color.rgb = COLOR_DARK

    set_speaker_notes(s14, "Bảng đo kiểm thực nghiệm cho thấy Fast-Path bóc tách 11 trang tài liệu chỉ mất 3.07 giây (0.28 giây/trang), nhanh gấp 10 lần các giải pháp OCR truyền thống, trong khi vẫn bảo toàn tuyệt đối 99.4% cấu trúc bảng biểu.")

    # =========================================================================
    # SLIDE 15: KỶ LUẬT TÀI CHÍNH ĐÁM MÂY (FINOPS ZERO-BREACH)
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Phần 3: Quản trị Tài chính", "Kỷ luật Tài chính Đám mây (FinOps Zero-Breach 0.00 USD)", 15)

    tx_l15 = s15.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(6.0), Inches(5.5))
    tf_l15 = tx_l15.text_frame
    tf_l15.word_wrap = True

    p = tf_l15.paragraphs[0]
    p.text = "Chiến lược Tối ưu Hóa Chi phí:"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    finops_bullets = [
        ("Tận dụng AWS Free Tier", "Sử dụng EC2 t3.micro (750 giờ/tháng miễn phí), S3 Standard (5 GB miễn phí), DynamoDB (25 GB miễn phí trọn đời)."),
        ("Kiến trúc Serverless Scale-to-Zero", "AWS Lambda miễn phí 1 triệu lượt gọi/tháng; không phát sinh bất kỳ chi phí tính toán nào khi hệ thống không có yêu cầu."),
        ("Tận dụng Cụm GPU Ngoại vi", "Chạy mô hình thị giác Qwen2.5-VL 72B trên cụm GPU Kaggle miễn phí (30 giờ/tuần), kết hợp Cloudflare Tunnel an toàn."),
        ("Giám sát Ngân sách Chủ động", "Thiết lập AWS Budgets cảnh báo ngưỡng chi phí 0.01 USD và CloudWatch Billing Alarm tự động gửi thông báo qua SNS.")
    ]
    for b_title, b_desc in finops_bullets:
        pb = tf_l15.add_paragraph()
        pb.text = f"• {b_title}: {b_desc}"
        pb.font.name = "Arial"
        pb.font.size = Pt(11.5)
        pb.font.color.rgb = COLOR_DARK

    # Right Card: Zero Cost Stamp
    rc15 = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.2), Inches(1.4), Inches(5.3), Inches(5.5))
    rc15.fill.solid()
    rc15.fill.fore_color.rgb = COLOR_NAVY
    rc15.line.color.rgb = COLOR_ORANGE
    rc15.line.width = Pt(2)

    tx_rc15 = s15.shapes.add_textbox(Inches(7.5), Inches(1.8), Inches(4.7), Inches(4.8))
    tf_rc15 = tx_rc15.text_frame
    tf_rc15.word_wrap = True

    prc = tf_rc15.paragraphs[0]
    prc.text = "KẾT QUẢ FINOPS SAU 12 TUẦN"
    prc.font.name = "Arial"
    prc.font.size = Pt(16)
    prc.font.bold = True
    prc.font.color.rgb = COLOR_ORANGE
    prc.alignment = PP_ALIGN.CENTER

    p_cost = tf_rc15.add_paragraph()
    p_cost.text = "0.00 USD"
    p_cost.font.name = "Arial"
    p_cost.font.size = Pt(44)
    p_cost.font.bold = True
    p_cost.font.color.rgb = COLOR_WHITE
    p_cost.alignment = PP_ALIGN.CENTER

    p_sub = tf_rc15.add_paragraph()
    p_sub.text = "(Kiểm chứng 100% qua AWS Cost Explorer)"
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(12)
    p_sub.font.italic = True
    p_sub.font.color.rgb = RGBColor(203, 213, 225)
    p_sub.alignment = PP_ALIGN.CENTER

    p_detail = tf_rc15.add_paragraph()
    p_detail.text = "\nKhông phát sinh bất kỳ hóa đơn ngoài ý muốn nào trong suốt 12 tuần thực nghiệm, minh chứng cho năng lực thiết kế kiến trúc chuẩn mực và tối ưu tài nguyên tối đa."
    p_detail.font.name = "Arial"
    p_detail.font.size = Pt(11.5)
    p_detail.font.color.rgb = COLOR_WHITE

    set_speaker_notes(s15, "Kỷ luật FinOps là một trong những điểm sáng nhất của đề tài. Sau 12 tuần liên tục phát triển và kiểm thử toàn diện trên AWS, hóa đơn thực tế được kiểm chứng qua AWS Cost Explorer là đúng 0.00 USD.")

    # =========================================================================
    # SLIDE 16: HƯỚNG MỞ RỘNG (ROADMAP & ADVANCED ARCHITECTURE)
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "Phần 4: Đề xuất Giải pháp", "Kế hoạch Phát triển Mở rộng (Advanced Roadmap)", 16)

    tx_l16 = s16.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(4.5), Inches(5.8))
    tf_l16 = tx_l16.text_frame
    tf_l16.word_wrap = True

    p = tf_l16.paragraphs[0]
    p.text = "3 Định hướng Nâng cấp Chính:"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    road_bullets = [
        ("Container hóa ECS Fargate", "Đóng gói ứng dụng thành Microservices triển khai trên Amazon ECS Fargate phi máy chủ, tự động co giãn theo số lượng người dùng."),
        ("Agentic RAG với Bedrock", "Tích hợp Amazon Bedrock Knowledge Bases và OpenSearch Serverless, hỗ trợ tra cứu hỏi đáp thông minh dựa trên nội dung tài liệu."),
        ("Tự động hóa CI/CD Toàn trình", "Xây dựng quy trình tự động kiểm thử và triển khai với AWS CodePipeline và AWS CodeBuild.")
    ]
    for b_title, b_desc in road_bullets:
        pb = tf_l16.add_paragraph()
        pb.text = f"• {b_title}: {b_desc}"
        pb.font.name = "Arial"
        pb.font.size = Pt(11.5)
        pb.font.color.rgb = COLOR_DARK

    img_ecs = os.path.join(PROJECT_ROOT, "workshop/static/images/architecture/aws-ecs-fargate-architecture.png")
    if os.path.exists(img_ecs):
        s16.shapes.add_picture(img_ecs, Inches(5.5), Inches(1.3), width=Inches(7.2))

    set_speaker_notes(s16, "Trong giai đoạn phát triển tiếp theo, hệ thống sẵn sàng được container hóa và chuyển dịch lên Amazon ECS Fargate để tự động co giãn không giới hạn, đồng thời kết hợp Agentic RAG với Amazon Bedrock Knowledge Bases.")

    # =========================================================================
    # SLIDE 17: TỰ ĐÁNH GIÁ & ĐỊNH HƯỚNG NGHỀ NGHIỆP
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "Phần 5: Đánh giá & Định hướng", "Kết quả Đạt được & Định hướng Nghề nghiệp Cá nhân", 17)

    tx_l17 = s17.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(5.8), Inches(5.5))
    tf_l17 = tx_l17.text_frame
    tf_l17.word_wrap = True

    p = tf_l17.paragraphs[0]
    p.text = "Kết quả Đạt được sau Kỳ Thực tập:"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    achieve_bullets = [
        ("Hoàn thành 100% Khối lượng", "Đạt toàn bộ mục tiêu đề ra trong đề cương kế hoạch 12 tuần theo quy định của HUCE."),
        ("Hồ sơ Báo cáo Chuẩn mực", "Hoàn thiện cuốn báo cáo dày 42 trang theo Biểu mẫu TTTN-06, 16 sơ đồ kỹ thuật và 11 bảng biểu chuẩn hóa."),
        ("Kỹ năng Kỹ thuật Đột phá", "Làm chủ thiết kế kiến trúc đám mây AWS Well-Architected, an ninh mạng Zero-Trust, Serverless, AI Multimodal và FinOps."),
        ("Tác phong Kỹ sư Quốc tế", "Rèn luyện tính chủ động, tư duy phân tích nguyên nhân gốc rễ (Root Cause Analysis) và tinh thần Ownership.")
    ]
    for b_title, b_desc in achieve_bullets:
        pb = tf_l17.add_paragraph()
        pb.text = f"• {b_title}: {b_desc}"
        pb.font.name = "Arial"
        pb.font.size = Pt(11.5)
        pb.font.color.rgb = COLOR_DARK

    # Right Card: Career Goals
    rc17 = s17.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.0), Inches(1.4), Inches(5.5), Inches(5.5))
    rc17.fill.solid()
    rc17.fill.fore_color.rgb = COLOR_LIGHT_BG
    rc17.line.color.rgb = COLOR_BORDER

    tx_rc17 = s17.shapes.add_textbox(Inches(7.3), Inches(1.6), Inches(5.0), Inches(5.1))
    tf_rc17 = tx_rc17.text_frame
    tf_rc17.word_wrap = True

    prc = tf_rc17.paragraphs[0]
    prc.text = "Định hướng Nghề nghiệp Cá nhân:"
    prc.font.name = "Arial"
    prc.font.size = Pt(14)
    prc.font.bold = True
    prc.font.color.rgb = COLOR_BLUE

    career_bullets = [
        ("Mục tiêu Chuyên môn", "Phát triển theo hướng Cloud Solutions Architect & AI/ML Solutions Engineer chuyên nghiệp."),
        ("Lộ trình Chứng chỉ Quốc tế", "Hoàn thành chứng chỉ AWS Certified Solutions Architect - Associate và hướng tới cấp độ Professional."),
        ("Đóng góp Cộng đồng", "Xuất bản tài liệu hướng dẫn kỹ thuật mở (Open Workshop) trên nền tảng GitHub Pages chia sẻ cho sinh viên và cộng đồng kỹ sư."),
        ("Ứng dụng vào Khóa luận", "Tiếp tục phát triển hệ thống làm nền tảng cho Đồ án Tốt nghiệp chuyên sâu trong học kỳ tới.")
    ]
    for b_title, b_desc in career_bullets:
        pb = tf_rc17.add_paragraph()
        pb.text = f"• {b_title}: {b_desc}"
        pb.font.name = "Arial"
        pb.font.size = Pt(11)
        pb.font.color.rgb = COLOR_DARK

    set_speaker_notes(s17, "Kỳ thực tập không chỉ giúp em hoàn thành xuất sắc đồ án báo cáo tốt nghiệp mà còn định hình rõ nét con đường sự nghiệp tương lai hướng tới vị trí Kỹ sư Kiến trúc Đám mây và AI chuyên nghiệp.")

    # =========================================================================
    # SLIDE 18: LỜI CẢM ƠN & PHIÊN HỎI ĐÁP (Q&A)
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    bg18 = s18.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg18.fill.solid()
    bg18.fill.fore_color.rgb = COLOR_NAVY
    bg18.line.color.rgb = COLOR_NAVY

    bar18 = s18.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    bar18.fill.solid()
    bar18.fill.fore_color.rgb = COLOR_ORANGE
    bar18.line.color.rgb = COLOR_ORANGE

    tx18 = s18.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.333), Inches(4.5))
    tf18 = tx18.text_frame
    tf18.word_wrap = True

    p = tf18.paragraphs[0]
    p.text = "CHÂN THÀNH CẢM ƠN QUÝ THẦY CÔ VÀ HỘI ĐỒNG!"
    p.font.name = "Arial"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = COLOR_ORANGE
    p.alignment = PP_ALIGN.CENTER

    p_sub = tf18.add_paragraph()
    p_sub.text = "Em xin trân trọng cảm ơn ThS. Lê Văn Minh, các Thầy/Cô Khoa Công nghệ Thông tin - HUCE\ncùng các Chuyên gia hướng dẫn tại Công ty TNHH Amazon Web Services Việt Nam."
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(14)
    p_sub.font.color.rgb = RGBColor(226, 232, 240)
    p_sub.alignment = PP_ALIGN.CENTER

    p_qa = tf18.add_paragraph()
    p_qa.text = "\nPHIÊN HỎI ĐÁP & CHẤT VẤN (Q&A)\nKính mời Quý Thầy/Cô trong Hội đồng đặt câu hỏi đóng góp cho đề tài!"
    p_qa.font.name = "Arial"
    p_qa.font.size = Pt(18)
    p_qa.font.bold = True
    p_qa.font.color.rgb = COLOR_WHITE
    p_qa.alignment = PP_ALIGN.CENTER

    p_links = tf18.add_paragraph()
    p_links.text = "\nKho mã nguồn dự án: github.com/Lamhuy0489/aws   |   Website Workshop: lamhuy0489.github.io/workshop/"
    p_links.font.name = "Arial"
    p_links.font.size = Pt(12)
    p_links.font.color.rgb = RGBColor(148, 163, 184)
    p_links.alignment = PP_ALIGN.CENTER

    set_speaker_notes(s18, "Em xin chân thành cảm ơn Quý Thầy/Cô đã chú ý lắng nghe bài trình bày. Em rất mong nhận được những câu hỏi và ý kiến đóng góp quý báu từ Hội đồng để đề tài được hoàn thiện tốt hơn nữa!")

    # Lưu tệp PowerPoint
    os.makedirs(OUT_DIR, exist_ok=True)
    prs.save(PPTX_PATH)
    print("=" * 70)
    print(f"XUAT BAN THANH CONG BO SLIDE THUYET TRINH (18 SLIDES)!")
    print(f"Duong dan: {PPTX_PATH}")
    
    # Đồng bộ sang workshop/static/downloads nếu cần
    os.makedirs(os.path.dirname(STATIC_DOWNLOADS_PPTX), exist_ok=True)
    prs.save(STATIC_DOWNLOADS_PPTX)
    print(f"Dong bo tai ve sang: {STATIC_DOWNLOADS_PPTX}")
    print("=" * 70)

if __name__ == "__main__":
    create_slide_deck()
