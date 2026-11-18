#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/build_light_defense_slides.py
Tạo bộ Slide thuyết trình Bảo vệ Thực tập Tốt nghiệp HUCE (20 Slides)
theo phong cách GIAO DIỆN MÀU SÁNG (LIGHT THEME) chuẩn mực, thanh lịch,
tích hợp đầy đủ các sơ đồ kỹ thuật Retina 2x đã kiểm chứng và lời thoại thuyết trình (Speaker Notes).
"""

import os
import subprocess
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(PROJECT_ROOT, "bao cao tot nghiep")
PPTX_PATH = os.path.join(OUT_DIR, "Slide_Bao_Cao_Tot_Nghiep_HUCE_Lam_Quang_Huy.pptx")
PDF_PATH = os.path.join(OUT_DIR, "Slide_Bao_Cao_Tot_Nghiep_HUCE_Lam_Quang_Huy.pdf")
STATIC_DOWNLOADS_PPTX = os.path.join(PROJECT_ROOT, "workshop", "static", "downloads", "Slide_Bao_Cao_Tot_Nghiep_HUCE_Lam_Quang_Huy.pptx")
STATIC_DOWNLOADS_PDF = os.path.join(PROJECT_ROOT, "workshop", "static", "downloads", "Slide_Bao_Cao_Tot_Nghiep_HUCE_Lam_Quang_Huy.pdf")

# =============================================================================
# BẢNG MÀU CHUẨN MỰC HỌC THUẬT & CÔNG NGHỆ AWS (LIGHT THEME)
# =============================================================================
COLOR_BG_WHITE = RGBColor(255, 255, 255)
COLOR_BG_LIGHT = RGBColor(248, 250, 252)       # Slate 50 (#F8FAFC)
COLOR_BG_CARD = RGBColor(255, 255, 255)        # Pure White (#FFFFFF)
COLOR_BORDER = RGBColor(226, 232, 240)         # Slate 200 (#E2E8F0)
COLOR_BORDER_STRONG = RGBColor(203, 213, 225)  # Slate 300 (#CBD5E1)

COLOR_TITLE = RGBColor(15, 23, 42)             # Slate 900 (#0F172A)
COLOR_TEXT_BODY = RGBColor(30, 41, 59)         # Slate 800 (#1E293B)
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)     # Slate 500 (#64748B)

COLOR_AWS_NAVY = RGBColor(35, 47, 62)          # AWS Squid Ink (#232F3E)
COLOR_AWS_ORANGE = RGBColor(255, 153, 0)       # AWS Smile Orange (#FF9900)
COLOR_TAG_ORANGE = RGBColor(217, 119, 6)       # Amber 600 (#D97706)
COLOR_TAG_BG_ORANGE = RGBColor(254, 243, 199)  # Amber 100 (#FEF3C7)

COLOR_BLUE = RGBColor(2, 132, 199)             # Sky 600 (#0284C7)
COLOR_BLUE_BG = RGBColor(240, 249, 255)        # Sky 50 (#F0F9FF)
COLOR_GREEN = RGBColor(22, 163, 74)            # Green 600 (#16A34A)
COLOR_GREEN_BG = RGBColor(240, 253, 244)       # Green 50 (#F0FDF4)
COLOR_PURPLE = RGBColor(126, 34, 206)          # Purple 700 (#7E22CE)
COLOR_PURPLE_BG = RGBColor(250, 245, 255)      # Purple 50 (#FAF5FF)

def create_light_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Helper: Banner tiêu đề Light Theme
    def add_light_header(slide, tag_text, title_text, slide_num, total_slides=20):
        # Header background banner (Light Theme)
        h_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        h_bg.fill.solid()
        h_bg.fill.fore_color.rgb = COLOR_BG_LIGHT
        h_bg.line.color.rgb = COLOR_BORDER
        h_bg.line.width = Pt(1)

        # Orange accent line at bottom of header
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.12), Inches(13.333), Inches(0.03))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_AWS_ORANGE
        line.line.color.rgb = COLOR_AWS_ORANGE

        # Header Text Frame
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.0), Inches(0.9))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_tag = tf.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.name = "Arial"
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = COLOR_TAG_ORANGE

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = "Arial"
        p_title.font.size = Pt(20)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_TITLE

        # Slide Number Indicator
        num_box = slide.shapes.add_textbox(Inches(11.7), Inches(0.3), Inches(1.0), Inches(0.5))
        ntf = num_box.text_frame
        p_num = ntf.paragraphs[0]
        p_num.text = f"{slide_num:02d} / {total_slides:02d}"
        p_num.font.name = "Arial"
        p_num.font.size = Pt(12)
        p_num.font.bold = True
        p_num.font.color.rgb = COLOR_TEXT_MUTED
        p_num.alignment = PP_ALIGN.RIGHT

    # Helper: Lời thoại thuyết trình
    def set_speaker_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # Helper: Khối hộp Card phong cách Executive sắc nét (không lỗi bo góc thừa)
    def add_card(slide, x, y, w, h, bg_color=COLOR_BG_CARD, border_color=COLOR_BORDER, accent_bar_color=None):
        from pptx.oxml import parse_xml
        card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        try:
            card._element.spPr.append(parse_xml('<a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'))
        except Exception:
            pass

        if accent_bar_color:
            strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(0.06))
            strip.fill.solid()
            strip.fill.fore_color.rgb = accent_bar_color
            strip.line.color.rgb = accent_bar_color
            strip.line.width = Pt(0)
            try:
                strip._element.spPr.append(parse_xml('<a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'))
            except Exception:
                pass
        return card

    # Helper: Chèn sơ đồ kỹ thuật căn chỉnh tỷ lệ chính xác (Zero Whitespace)
    def add_diagram_image(slide, image_path, x, y_min, y_max, target_width):
        if not os.path.exists(image_path):
            return None
        with Image.open(image_path) as im:
            orig_w, orig_h = im.size
        aspect = orig_w / orig_h
        target_h = target_width / aspect
        avail_h = y_max - y_min
        if target_h > avail_h:
            target_h = avail_h
            target_width = target_h * aspect
        y = y_min + (avail_h - target_h) / 2

        # Viền khung tinh tế bám sát đúng kích thước ảnh
        frame = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x - 0.02), Inches(y - 0.02), Inches(target_width + 0.04), Inches(target_h + 0.04))
        frame.fill.solid()
        frame.fill.fore_color.rgb = COLOR_BORDER
        frame.line.color.rgb = COLOR_BORDER
        frame.line.width = Pt(1)

        pic = slide.shapes.add_picture(image_path, Inches(x), Inches(y), width=Inches(target_width), height=Inches(target_h))
        return pic

    # Helper: Thêm một khối thông tin trong cột giải thích (Explanation Item)
    def add_info_block(tf, title, desc, bullet_color=COLOR_TITLE, title_color=COLOR_TITLE, pt_size=10.0):
        p = tf.add_paragraph()
        p.text = f"• {title}: {desc}"
        p.font.name = "Arial"
        p.font.size = Pt(pt_size)
        p.font.color.rgb = COLOR_TEXT_BODY
        p.line_spacing = 1.15

    # =========================================================================
    # SLIDE 1: BÌA BÁO CÁO (TITLE SLIDE)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_BG_WHITE
    bg1.line.color.rgb = COLOR_BG_WHITE

    # Dải cam AWS trên đỉnh
    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.18))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = COLOR_AWS_ORANGE
    top_bar.line.color.rgb = COLOR_AWS_ORANGE

    # Tiêu đề Khoa và Trường
    tx1_header = s1.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(10.5), Inches(0.8))
    tf1_h = tx1_header.text_frame
    p1_u = tf1_h.paragraphs[0]
    p1_u.text = "TRƯỜNG ĐẠI HỌC XÂY DỰNG HÀ NỘI (HUCE) — KHOA CÔNG NGHỆ THÔNG TIN"
    p1_u.font.name = "Arial"
    p1_u.font.size = Pt(12)
    p1_u.font.bold = True
    p1_u.font.color.rgb = COLOR_TAG_ORANGE

    p1_rep = tf1_h.add_paragraph()
    p1_rep.text = "HỘI ĐỒNG ĐÁNH GIÁ BÁO CÁO THỰC TẬP TỐT NGHIỆP — BIỂU MẪU TTTN-06"
    p1_rep.font.name = "Arial"
    p1_rep.font.size = Pt(11)
    p1_rep.font.color.rgb = COLOR_TEXT_MUTED

    # Logo HUCE góc phải trên
    logo_path = os.path.join(PROJECT_ROOT, "bao cao tot nghiep", "logo_huce.png")
    if os.path.exists(logo_path):
        s1.shapes.add_picture(logo_path, Inches(11.5), Inches(0.45), width=Inches(1.05))

    # Hộp Tiêu đề Đề tài
    tx1_title = s1.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.733), Inches(2.2))
    tf1_t = tx1_title.text_frame
    tf1_t.word_wrap = True

    p1_main = tf1_t.paragraphs[0]
    p1_main.text = "NỀN TẢNG PHI MÁY CHỦ BÓC TÁCH VÀ DỊCH THUẬT\nTÀI LIỆU KỸ THUẬT HYBRID TRÊN ĐÁM MÂY AWS"
    p1_main.font.name = "Arial"
    p1_main.font.size = Pt(28)
    p1_main.font.bold = True
    p1_main.font.color.rgb = COLOR_TITLE

    p1_en = tf1_t.add_paragraph()
    p1_en.text = "Serverless Hybrid Document OCR, Parsing & Technical Translation Platform on AWS"
    p1_en.font.name = "Arial"
    p1_en.font.size = Pt(15)
    p1_en.font.italic = True
    p1_en.font.color.rgb = COLOR_BLUE

    # 3 Khối Thông tin Cấu trúc rõ ràng ở phía dưới
    col_w = 3.733
    cards_y = 4.0
    cards_h = 2.8

    # Box 1: Sinh viên
    add_card(s1, 0.8, cards_y, col_w, cards_h, bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER_STRONG, accent_bar_color=COLOR_AWS_ORANGE)
    tx_s1 = s1.shapes.add_textbox(Inches(1.05), Inches(cards_y + 0.15), Inches(col_w - 0.35), Inches(cards_h - 0.3))
    tf_s1 = tx_s1.text_frame
    tf_s1.word_wrap = True
    p = tf_s1.paragraphs[0]
    p.text = "SINH VIÊN THỰC HIỆN"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TAG_ORANGE

    p2 = tf_s1.add_paragraph()
    p2.text = "LÂM QUANG HUY"
    p2.font.name = "Arial"
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TITLE

    details1 = [
        "Mã số sinh viên: 0212267",
        "Lớp: 67CS (Khoa học Máy tính)",
        "Khoa: Công nghệ Thông tin",
        "Trường: ĐH Xây dựng Hà Nội"
    ]
    for d in details1:
        pd = tf_s1.add_paragraph()
        pd.text = d
        pd.font.name = "Arial"
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = COLOR_TEXT_BODY

    # Box 2: Giảng viên & Cán bộ hướng dẫn
    add_card(s1, 4.8, cards_y, col_w, cards_h, bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER_STRONG, accent_bar_color=COLOR_BLUE)
    tx_s2 = s1.shapes.add_textbox(Inches(5.05), Inches(cards_y + 0.15), Inches(col_w - 0.35), Inches(cards_h - 0.3))
    tf_s2 = tx_s2.text_frame
    tf_s2.word_wrap = True
    p = tf_s2.paragraphs[0]
    p.text = "HƯỚNG DẪN KHOA HỌC"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE

    p2 = tf_s2.add_paragraph()
    p2.text = "ThS. LÊ VĂN MINH"
    p2.font.name = "Arial"
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TITLE

    p3 = tf_s2.add_paragraph()
    p3.text = "Giảng viên Khoa CNTT — HUCE"
    p3.font.name = "Arial"
    p3.font.size = Pt(10.5)
    p3.font.color.rgb = COLOR_TEXT_MUTED

    p4 = tf_s2.add_paragraph()
    p4.text = "\nCán bộ ĐVHD: Nguyễn Gia Hưng"
    p4.font.name = "Arial"
    p4.font.size = Pt(11)
    p4.font.bold = True
    p4.font.color.rgb = COLOR_TITLE

    p5 = tf_s2.add_paragraph()
    p5.text = "hunggia@amazon.com.vn (AWS)"
    p5.font.name = "Arial"
    p5.font.size = Pt(10.5)
    p5.font.color.rgb = COLOR_TEXT_MUTED

    # Box 3: Đơn vị Thực tập
    add_card(s1, 8.8, cards_y, col_w, cards_h, bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER_STRONG, accent_bar_color=COLOR_AWS_NAVY)
    tx_s3 = s1.shapes.add_textbox(Inches(9.05), Inches(cards_y + 0.15), Inches(col_w - 0.35), Inches(cards_h - 0.3))
    tf_s3 = tx_s3.text_frame
    tf_s3.word_wrap = True
    p = tf_s3.paragraphs[0]
    p.text = "ĐƠN VỊ THỰC TẬP"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_AWS_NAVY

    p2 = tf_s3.add_paragraph()
    p2.text = "AWS VIỆT NAM"
    p2.font.name = "Arial"
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TITLE

    details3 = [
        "Chương trình: FCAJ Bootcamp 2026",
        "First Cloud AI Journey (12 tuần)",
        "Thời gian: 03/08 — 25/10/2026",
        "Tiêu chuẩn: AWS Well-Architected"
    ]
    for d in details3:
        pd = tf_s3.add_paragraph()
        pd.text = d
        pd.font.name = "Arial"
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = COLOR_TEXT_BODY

    set_speaker_notes(s1, "Kính thưa Thầy/Cô trong Hội đồng chấm thi, em xin phép được trình bày Báo cáo thực tập tốt nghiệp với đề tài: Xây dựng nền tảng phi máy chủ bóc tách và dịch thuật tài liệu kỹ thuật Hybrid trên đám mây AWS. Đề tài được hoàn thành trong kỳ thực tập tại Công ty TNHH Amazon Web Services Việt Nam dưới sự hướng dẫn của ThS. Lê Văn Minh và cán bộ hướng dẫn tại AWS là anh Nguyễn Gia Hưng.")

    # =========================================================================
    # SLIDE 2: ĐƠN VỊ THỰC TẬP (AWS VIETNAM & FCAJ BOOTCAMP)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_light_header(s2, "Phần 1: Giới thiệu Đơn vị Thực tập", "Công ty TNHH Amazon Web Services Việt Nam & FCAJ Bootcamp", 2)

    card_y = 1.35
    card_h = 5.65
    half_w = 5.7

    # Left Top Card
    add_card(s2, 0.8, card_y, half_w, 3.85, bg_color=COLOR_BG_WHITE, border_color=COLOR_BORDER, accent_bar_color=COLOR_AWS_NAVY)
    tx2_l = s2.shapes.add_textbox(Inches(1.05), Inches(card_y + 0.15), Inches(half_w - 0.35), Inches(3.55))
    tf2_l = tx2_l.text_frame
    tf2_l.word_wrap = True

    p = tf2_l.paragraphs[0]
    p.text = "TỔNG QUAN ĐƠN VỊ THỰC TẬP"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_AWS_NAVY

    b2_list = [
        ("Vị thế Tiên phong Toàn cầu", "AWS là nền tảng điện toán đám mây số 1 thế giới với hơn 200 dịch vụ hoàn chỉnh trên các cụm Data Center toàn cầu."),
        ("Sứ mệnh tại Việt Nam", "Đồng hành thúc đẩy Chuyển đổi số Quốc gia, đào tạo nguồn nhân lực Cloud chất lượng cao."),
        ("AWS FCAJ Bootcamp 2026", "First Cloud AI Journey huấn luyện chuyên sâu về Cloud Architecture, Serverless, DevOps và Generative AI.")
    ]
    for b_title, b_desc in b2_list:
        add_info_block(tf2_l, b_title, b_desc, pt_size=10.0)

    # Left Bottom Card
    add_card(s2, 0.8, card_y + 4.05, half_w, 1.6, bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER_STRONG, accent_bar_color=COLOR_TAG_ORANGE)
    tx2_lb = s2.shapes.add_textbox(Inches(1.05), Inches(card_y + 4.15), Inches(half_w - 0.35), Inches(1.4))
    tf2_lb = tx2_lb.text_frame
    tf2_lb.word_wrap = True
    p = tf2_lb.paragraphs[0]
    p.text = "VĂN HÓA DOANH NGHIỆP AMAZON"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TAG_ORANGE
    p2 = tf2_lb.add_paragraph()
    p2.text = "• 16 Leadership Principles: Customer Obsession, Ownership, Invent & Simplify\n• Tác phong kỹ sư chuyên nghiệp, tư duy giải quyết vấn đề từ gốc rễ (Root Cause)"
    p2.font.name = "Arial"
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_TEXT_BODY

    # Right Top Card
    add_card(s2, 6.8, card_y, half_w, 3.85, bg_color=COLOR_BG_WHITE, border_color=COLOR_BORDER, accent_bar_color=COLOR_BLUE)
    tx2_r = s2.shapes.add_textbox(Inches(7.05), Inches(card_y + 0.15), Inches(half_w - 0.35), Inches(3.55))
    tf2_r = tx2_r.text_frame
    tf2_r.word_wrap = True

    pr = tf2_r.paragraphs[0]
    pr.text = "MỤC TIÊU 12 TUẦN THỰC TẬP (03/08 — 25/10/2026)"
    pr.font.name = "Arial"
    pr.font.size = Pt(13)
    pr.font.bold = True
    pr.font.color.rgb = COLOR_BLUE

    r2_bullets = [
        ("Làm chủ Kiến trúc AWS Enterprise", "Nắm vững Well-Architected Framework: Multi-AZ High Availability, Zero-Trust và Serverless."),
        ("Phát triển Đề tài Capstone Thực tế", "Xây dựng nền tảng Hybrid OCR & Translation giải quyết triệt để rào cản bóc tách bảng biểu kỹ thuật."),
        ("Kỷ luật Tài chính FinOps", "Thiết lập giám sát thời gian thực, vận hành toàn bộ hệ thống với chi phí 0.00 USD trong suốt 12 tuần.")
    ]
    for b_title, b_desc in r2_bullets:
        add_info_block(tf2_r, b_title, b_desc, pt_size=10.0)

    # Right Bottom Card
    add_card(s2, 6.8, card_y + 4.05, half_w, 1.6, bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER_STRONG, accent_bar_color=COLOR_GREEN)
    tx2_rb = s2.shapes.add_textbox(Inches(7.05), Inches(card_y + 4.15), Inches(half_w - 0.35), Inches(1.4))
    tf2_rb = tx2_rb.text_frame
    tf2_rb.word_wrap = True
    p = tf2_rb.paragraphs[0]
    p.text = "KẾT QUẢ ĐO LƯỜNG HOÀN THÀNH"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN
    p2 = tf2_rb.add_paragraph()
    p2.text = "• Hoàn thành 100% khối lượng đề cương theo quy định Khoa CNTT HUCE\n• Báo cáo thực tập 42 trang Biểu mẫu TTTN-06 + Website Workshop GitHub Pages"
    p2.font.name = "Arial"
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_TEXT_BODY

    set_speaker_notes(s2, "Tại AWS Việt Nam, chương trình First Cloud AI Journey kéo dài 12 tuần đặt mục tiêu giúp sinh viên cọ xát với văn hóa chuẩn mực toàn cầu của Amazon, đồng thời trực tiếp triển khai dự án Capstone với tiêu chuẩn kỹ thuật doanh nghiệp.")

    # =========================================================================
    # SLIDE 3: BỐI CẢNH & 3 THÁCH THỨC KỸ THUẬT
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_light_header(s3, "Phần 2: Bối cảnh & Bài toán Kỹ thuật", "3 Thách thức Trọng tâm trong Xử lý Tài liệu Kỹ thuật Lớn", 3)

    challenges = [
        ("THÁCH THỨC 1: CẤU TRÚC PHỨC TẠP & VỠ BẢNG BIỂU",
         "Tài liệu kỹ thuật, tiêu chuẩn xây dựng, hồ sơ dự án chứa dày đặc bảng biểu số liệu, văn bản 2 cột, công thức toán và sơ đồ bản vẽ.\n"
         "Các công cụ OCR văn phòng thông thường làm vỡ hoàn toàn định dạng bảng và mất quan hệ dòng/cột logic.",
         "Hệ quả thực tế: Người dùng mất 40% thời gian chỉnh sửa lại định dạng thủ công.",
         COLOR_AWS_NAVY),
        ("THÁCH THỨC 2: CHI PHÍ & ĐỘ TRỄ KHI GỌI VISION LLM",
         "Việc đưa toàn bộ các trang tài liệu qua các Vision Multimodal LLM thương mại gây tốn kém chi phí cực lớn (hàng chục USD/tài liệu) và độ trễ cao (> 10s/trang).\n"
         "Trong khi thực tế hơn 85% tài liệu kỹ thuật lưu hành là PDF số có sẵn văn bản vector sắc nét.",
         "Hệ quả thực tế: Lãng phí tài nguyên tính toán và chi phí API không cần thiết.",
         COLOR_BLUE),
        ("THÁCH THỨC 3: GIỚI HẠN 10 MB PAYLOAD CỦA API GATEWAY",
         "Amazon API Gateway có hạn mức cố định Payload tối đa 10 MB, gây lỗi 413 Payload Too Large khi người dùng tải lên hồ sơ dự án lớn (15 MB đến 100 MB).\n"
         "Máy chủ Web bị nghẽn băng thông do phải trung chuyển luồng tệp nhị phân dung lượng lớn.",
         "Hệ quả thực tế: Hệ thống bị treo khi nhiều người dùng tải tệp cùng lúc.",
         COLOR_TAG_ORANGE)
    ]

    c_w = 11.733
    c_h = 1.65
    for idx, (ch_title, ch_desc, ch_sub, ch_col) in enumerate(challenges):
        top_pos = 1.35 + idx * 1.9
        add_card(s3, 0.8, top_pos, c_w, c_h, bg_color=COLOR_BG_WHITE, border_color=COLOR_BORDER, accent_bar_color=ch_col)

        tx_c = s3.shapes.add_textbox(Inches(1.15), Inches(top_pos + 0.12), Inches(c_w - 0.45), Inches(c_h - 0.24))
        tfc = tx_c.text_frame
        tfc.word_wrap = True

        pc1 = tfc.paragraphs[0]
        pc1.text = ch_title
        pc1.font.name = "Arial"
        pc1.font.size = Pt(12.5)
        pc1.font.bold = True
        pc1.font.color.rgb = ch_col

        for line in ch_desc.split("\n"):
            pc2 = tfc.add_paragraph()
            pc2.text = f"• {line}"
            pc2.font.name = "Arial"
            pc2.font.size = Pt(10.0)
            pc2.font.color.rgb = COLOR_TEXT_BODY

        pc3 = tfc.add_paragraph()
        pc3.text = f"   >> {ch_sub}"
        pc3.font.name = "Arial"
        pc3.font.size = Pt(10.0)
        pc3.font.italic = True
        pc3.font.color.rgb = COLOR_TEXT_MUTED

    set_speaker_notes(s3, "Khi tiếp cận bài toán xử lý tài liệu kỹ thuật, chúng ta gặp 3 rào cản lớn: vỡ cấu trúc bảng biểu, chi phí gọi mô hình AI quá cao và nghẽn băng thông do giới hạn 10MB của API Gateway. Dự án giải quyết triệt để cả 3 bài toán này.")

    # =========================================================================
    # SLIDE 4: TỔNG QUAN KIẾN TRÚC 5 PHÂN TẦNG
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_light_header(s4, "Phần 3: Kiến trúc Hệ thống", "Mô hình 5 Phân tầng Nền tảng Serverless Hybrid Platform", 4)

    left_w = 4.0
    right_w = 7.5
    img_sys = os.path.join(PROJECT_ROOT, "workshop/static/images/architecture/aws-system-architecture.png")

    # Left top card: 5 layers
    add_card(s4, 0.8, 1.35, left_w, 4.2, bg_color=COLOR_BG_WHITE, border_color=COLOR_BORDER, accent_bar_color=COLOR_AWS_NAVY)
    tx4_l = s4.shapes.add_textbox(Inches(1.05), Inches(1.5), Inches(left_w - 0.35), Inches(3.9))
    tf4_l = tx4_l.text_frame
    tf4_l.word_wrap = True

    p = tf4_l.paragraphs[0]
    p.text = "5 PHÂN TẦNG KIẾN TRÚC DOANH NGHIỆP"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_AWS_NAVY

    layers = [
        ("1. Presentation Layer", "Web Studio SPA, trình soạn thảo đối chiếu song ngữ Side-by-Side thời gian thực."),
        ("2. Ingress & Routing", "VPC Three-Tier Multi-AZ, Application Load Balancer và Security Group Chaining."),
        ("3. Compute & Event", "Máy chủ EC2 AL2023 Gunicorn kết hợp AWS Lambda s3-trigger phản hồi trong 214 ms."),
        ("4. Hybrid AI Engine", "Fast-Path Native (0.28s/trang) cho PDF số và Multimodal Vision OCR cho ảnh scan."),
        ("5. Polyglot Persistence", "DynamoDB (Jobs), Amazon S3 (Files) và SQLite (Auth & API Key Tour).")
    ]
    for l_title, l_desc in layers:
        add_info_block(tf4_l, l_title, l_desc, pt_size=9.5)

    # Left bottom highlight card
    add_card(s4, 0.8, 5.7, left_w, 1.3, bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER_STRONG, accent_bar_color=COLOR_BLUE)
    tx4_b = s4.shapes.add_textbox(Inches(1.05), Inches(5.8), Inches(left_w - 0.35), Inches(1.1))
    tf4_b = tx4_b.text_frame
    tf4_b.word_wrap = True
    pb = tf4_b.paragraphs[0]
    pb.text = "CHỈ SỐ THIẾT KẾ ĐÁM MÂY"
    pb.font.name = "Arial"
    pb.font.size = Pt(11)
    pb.font.bold = True
    pb.font.color.rgb = COLOR_BLUE

    pb2 = tf4_b.add_paragraph()
    pb2.text = "• Độ sẵn sàng cao: Multi-AZ High Availability\n• Tối ưu chi phí: Scale-to-Zero phi máy chủ\n• Khắc phục 100% trần 10MB của API Gateway"
    pb2.font.name = "Arial"
    pb2.font.size = Pt(9.5)
    pb2.font.color.rgb = COLOR_TEXT_BODY

    # Right Diagram
    add_diagram_image(s4, img_sys, 5.0, 1.35, 7.0, right_w)

    set_speaker_notes(s4, "Hệ thống được thiết kế theo 5 phân tầng chuẩn mực Enterprise. Người dùng truy cập qua Application Load Balancer tới Web Studio. Tài liệu được tải trực tiếp lên S3 qua Presigned URL, kích hoạt luồng xử lý phi máy chủ Lambda và động cơ bóc tách kép.")

    # =========================================================================
    # SLIDE 5: SƠ ĐỒ USE CASE KIẾN TRÚC
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_light_header(s5, "Phần 3: Phân tích Chức năng", "Sơ đồ Ca sử dụng Tổng thể & Mô hình Tác nhân (Use Case Architecture)", 5)

    img_uc = os.path.join(PROJECT_ROOT, "workshop/static/images/architecture/aws-use-case-architecture.png")

    # Left top card
    add_card(s5, 0.8, 1.35, left_w, 4.2, bg_color=COLOR_BG_WHITE, border_color=COLOR_BORDER, accent_bar_color=COLOR_BLUE)
    tx5_l = s5.shapes.add_textbox(Inches(1.05), Inches(1.5), Inches(left_w - 0.35), Inches(3.9))
    tf5_l = tx5_l.text_frame
    tf5_l.word_wrap = True

    p = tf5_l.paragraphs[0]
    p.text = "PHÂN RÃ 13 CA SỬ DỤNG THEO 4 TÁC NHÂN"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE

    uc_summary = [
        ("End User (6 UCs)", "Đăng nhập; Thiết lập theme & model; Tải tệp lớn qua Presigned URL; Biên tập song ngữ; Xuất bản MD/DOCX/PDF; Tra cứu lịch sử."),
        ("Administrator (3 UCs)", "Quản lý xoay vòng API Keys (Key Tour); Giám sát Telemetry trên CloudWatch; Kiểm soát trần FinOps 0.00 USD."),
        ("AWS Event System (2 UCs)", "Bắt sự kiện s3:ObjectCreated; Tự động kích hoạt Lambda (214ms); Đồng bộ tiến trình DynamoDB Jobs."),
        ("AI Inference (2 UCs)", "Cung cấp Vision OCR (Qwen2.5-VL / Gemini) và dịch thuật ngữ kỹ thuật chuyên ngành.")
    ]
    for act, desc in uc_summary:
        add_info_block(tf5_l, act, desc, pt_size=9.5)

    # Left bottom highlight card
    add_card(s5, 0.8, 5.7, left_w, 1.3, bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER_STRONG, accent_bar_color=COLOR_GREEN)
    tx5_b = s5.shapes.add_textbox(Inches(1.05), Inches(5.8), Inches(left_w - 0.35), Inches(1.1))
    tf5_b = tx5_b.text_frame
    tf5_b.word_wrap = True
    pb = tf5_b.paragraphs[0]
    pb.text = "KIỂM CHỨNG THIẾT KẾ (ZERO COLLISION)"
    pb.font.name = "Arial"
    pb.font.size = Pt(11)
    pb.font.bold = True
    pb.font.color.rgb = COLOR_GREEN

    pb2 = tf5_b.add_paragraph()
    pb2.text = "• 100% đường nối Actor-to-UC là đường thẳng ngang\n• Phân tách ranh giới Human vs System Actors rõ ràng\n• Đảm bảo tính toàn vẹn chức năng chuẩn UML 2.5"
    pb2.font.name = "Arial"
    pb2.font.size = Pt(9.5)
    pb2.font.color.rgb = COLOR_TEXT_BODY

    add_diagram_image(s5, img_uc, 5.0, 1.35, 7.0, right_w)

    set_speaker_notes(s5, "Sơ đồ Use Case thể hiện rõ 13 ca sử dụng cốt lõi được phân bổ logic cho 4 tác nhân. Đường liên kết được bố trí gọn gàng, thể hiện tính độc lập giữa luồng tương tác người dùng và luồng xử lý sự kiện phi máy chủ ở backend.")

    # =========================================================================
    # SLIDE 6: KIẾN TRÚC TỔNG THỂ HỆ THỐNG TRÊN AWS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_light_header(s6, "Phần 3: Hạ tầng Đám mây AWS", "Sơ đồ Kiến trúc Tổng thể Hệ thống trên Nền tảng Đám mây AWS", 6)

    add_card(s6, 0.8, 1.35, left_w, 4.2, bg_color=COLOR_BG_WHITE, border_color=COLOR_BORDER, accent_bar_color=COLOR_AWS_NAVY)
    tx6_l = s6.shapes.add_textbox(Inches(1.05), Inches(1.5), Inches(left_w - 0.35), Inches(3.9))
    tf6_l = tx6_l.text_frame
    tf6_l.word_wrap = True

    p = tf6_l.paragraphs[0]
    p.text = "ĐẶC TẢ TRIỂN KHAI AWS MULTI-AZ"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_AWS_NAVY

    aws_sys_bullets = [
        ("Vùng Triển khai", "Khu vực ap-southeast-1 (Singapore) trải rộng trên 2 Vùng sẵn sàng ap-southeast-1a và 1b."),
        ("Tài khoản Quản trị", "Account ID: 677994024390, IAM User: dev_admin tuân thủ Least Privilege."),
        ("Cân bằng tải ALB", "Application Load Balancer định tuyến lưu lượng vào Target Group EC2 AL2023 Gunicorn."),
        ("Lưu trữ Đối tượng S3", "Bucket: huylam-ocr-documents-ap-southeast-1, mã hóa SSE-S3 AES-256."),
        ("Cơ sở Dữ liệu NoSQL", "Amazon DynamoDB On-Demand huylam-ocr-jobs lưu vết trạng thái với độ trễ < 8 ms.")
    ]
    for b_title, b_desc in aws_sys_bullets:
        add_info_block(tf6_l, b_title, b_desc, pt_size=9.5)

    add_card(s6, 0.8, 5.7, left_w, 1.3, bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER_STRONG, accent_bar_color=COLOR_TAG_ORANGE)
    tx6_b = s6.shapes.add_textbox(Inches(1.05), Inches(5.8), Inches(left_w - 0.35), Inches(1.1))
    tf6_b = tx6_b.text_frame
    tf6_b.word_wrap = True
    pb = tf6_b.paragraphs[0]
    pb.text = "AWS WELL-ARCHITECTED ALIGNMENT"
    pb.font.name = "Arial"
    pb.font.size = Pt(11)
    pb.font.bold = True
    pb.font.color.rgb = COLOR_TAG_ORANGE

    pb2 = tf6_b.add_paragraph()
    pb2.text = "• Trụ cột Bảo mật: 100% dữ liệu mã hóa tĩnh & động\n• Trụ cột Tin cậy: Tự động chuyển mạch khi sự cố\n• Trụ cột Tối ưu: Vận hành không phát sinh chi phí"
    pb2.font.name = "Arial"
    pb2.font.size = Pt(9.5)
    pb2.font.color.rgb = COLOR_TEXT_BODY

    add_diagram_image(s6, img_sys, 5.0, 1.35, 7.0, right_w)

    set_speaker_notes(s6, "Sơ đồ kiến trúc tổng thể trên AWS tuân thủ nghiêm ngặt khung Well-Architected Framework, bảo đảm đầy đủ các trụ cột về độ tin cậy, an ninh bảo mật và tối ưu chi phí.")

    # =========================================================================
    # SLIDE 7: MẠNG ẢO AMAZON VPC MULTI-AZ
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_light_header(s7, "Phần 3: An ninh Mạng", "Mạng ảo Amazon VPC Three-Tier Multi-AZ Phân tách Subnet Độ Sẵn Sàng Cao", 7)

    img_vpc = os.path.join(PROJECT_ROOT, "workshop/static/images/architecture/aws-vpc-network-architecture.png")

    add_card(s7, 0.8, 1.35, left_w, 4.2, bg_color=COLOR_BG_WHITE, border_color=COLOR_BORDER, accent_bar_color=COLOR_BLUE)
    tx7_l = s7.shapes.add_textbox(Inches(1.05), Inches(1.5), Inches(left_w - 0.35), Inches(3.9))
    tf7_l = tx7_l.text_frame
    tf7_l.word_wrap = True

    p = tf7_l.paragraphs[0]
    p.text = "CẤU TRÚC PHÂN VÙNG MẠNG ẢO VPC"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE

    vpc_bullets = [
        ("Custom VPC", "huylam-vpc CIDR dải mạng 10.0.0.0/16 tại khu vực Singapore (ap-southeast-1)."),
        ("Public Subnets", "2 Subnets (10.0.0.0/20 & 10.0.16.0/20) chứa ALB và Internet Gateway."),
        ("Private Subnets", "2 Subnets (10.0.128.0/20 & 10.0.144.0/20) cô lập hoàn toàn máy chủ EC2."),
        ("Isolated Subnets", "Phân vùng Database không có Internet Ingress lẫn Egress, an toàn tuyệt đối."),
        ("High Availability", "Standby Route Table và Target Group sẵn sàng kích hoạt chuyển mạch khi có sự cố.")
    ]
    for b_title, b_desc in vpc_bullets:
        add_info_block(tf7_l, b_title, b_desc, pt_size=9.5)

    add_card(s7, 0.8, 5.7, left_w, 1.3, bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER_STRONG, accent_bar_color=COLOR_AWS_NAVY)
    tx7_b = s7.shapes.add_textbox(Inches(1.05), Inches(5.8), Inches(left_w - 0.35), Inches(1.1))
    tf7_b = tx7_b.text_frame
    tf7_b.word_wrap = True
    pb = tf7_b.paragraphs[0]
    pb.text = "NGUYÊN LÝ CÔ LẬP MẠNG"
    pb.font.name = "Arial"
    pb.font.size = Pt(11)
    pb.font.bold = True
    pb.font.color.rgb = COLOR_AWS_NAVY

    pb2 = tf7_b.add_paragraph()
    pb2.text = "• Không gán Public IP cho máy chủ EC2 Backend\n• Chỉ cho phép truy cập web thông qua Load Balancer\n• Loại bỏ hoàn toàn nguy cơ quét cổng diện rộng"
    pb2.font.name = "Arial"
    pb2.font.size = Pt(9.5)
    pb2.font.color.rgb = COLOR_TEXT_BODY

    add_diagram_image(s7, img_vpc, 5.0, 1.35, 7.0, right_w)

    set_speaker_notes(s7, "Mô hình mạng VPC Three-Tier Multi-AZ giúp cô lập máy chủ EC2 trong phân vùng mạng riêng (Private Subnet), hoàn toàn không gán IP công cộng. Chỉ có Application Load Balancer nằm ở Public Subnet mới tiếp nhận lưu lượng Internet.")

    # =========================================================================
    # SLIDE 8: BẢO MẬT ZERO-TRUST & SECURITY GROUP CHAINING
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_light_header(s8, "Phần 3: An ninh Mạng", "Cơ chế Bảo mật Zero-Trust & Security Group Chaining Phân tầng", 8)

    img_sec = os.path.join(PROJECT_ROOT, "workshop/static/images/architecture/aws-security-group-chaining.png")

    add_card(s8, 0.8, 1.35, left_w, 4.2, bg_color=COLOR_BG_WHITE, border_color=COLOR_BORDER, accent_bar_color=COLOR_PURPLE)
    tx8_l = s8.shapes.add_textbox(Inches(1.05), Inches(1.5), Inches(left_w - 0.35), Inches(3.9))
    tf8_l = tx8_l.text_frame
    tf8_l.word_wrap = True

    p = tf8_l.paragraphs[0]
    p.text = "CHUỖI LIÊN KẾT NHÓM BẢO MẬT"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_PURPLE

    sec_bullets = [
        ("ALB Security Group", "Chỉ mở cổng Inbound HTTP 80 tiếp nhận yêu cầu từ địa chỉ IP của người dùng."),
        ("EC2 Security Group", "Chỉ cho phép Inbound cổng 5000 tham chiếu trực tiếp Security Group ID của ALB. Chặn 100% traffic ngoài."),
        ("Đóng cổng SSH 22", "Không mở cổng 22. Quản trị máy chủ thông qua AWS Systems Manager (SSM) Session Manager an toàn."),
        ("Mã hóa Kênh truyền", "Toàn bộ phiên làm việc quản trị được mã hóa TLS 443 và ghi nhật ký giám sát đầy đủ.")
    ]
    for b_title, b_desc in sec_bullets:
        add_info_block(tf8_l, b_title, b_desc, pt_size=9.5)

    add_card(s8, 0.8, 5.7, left_w, 1.3, bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER_STRONG, accent_bar_color=COLOR_GREEN)
    tx8_b = s8.shapes.add_textbox(Inches(1.05), Inches(5.8), Inches(left_w - 0.35), Inches(1.1))
    tf8_b = tx8_b.text_frame
    tf8_b.word_wrap = True
    pb = tf8_b.paragraphs[0]
    pb.text = "LỢI ÍCH AN NINH ZERO-TRUST"
    pb.font.name = "Arial"
    pb.font.size = Pt(11)
    pb.font.bold = True
    pb.font.color.rgb = COLOR_GREEN

    pb2 = tf8_b.add_paragraph()
    pb2.text = "• Loại bỏ hoàn toàn việc quản lý tệp SSH Key (.pem)\n• Kiểm soát quyền hạn máy chủ theo IAM Role Instance\n• Ghi nhận 100% lịch sử phiên lệnh trên CloudWatch"
    pb2.font.name = "Arial"
    pb2.font.size = Pt(9.5)
    pb2.font.color.rgb = COLOR_TEXT_BODY

    add_diagram_image(s8, img_sec, 5.0, 1.35, 7.0, right_w)

    set_speaker_notes(s8, "Cơ chế Security Group Chaining loại bỏ hoàn toàn khả năng máy chủ EC2 bị tấn công trực tiếp từ bên ngoài. Thêm vào đó, việc loại bỏ cổng SSH 22 và thay thế bằng AWS Systems Manager đảm bảo quản trị an toàn tuyệt đối mà không cần quản lý private keys.")

    # =========================================================================
    # SLIDE 9: ĐỘNG CƠ BÓC TÁCH KÉP (HYBRID OCR ENGINE)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_light_header(s9, "Phần 3: Trọng tâm Kỹ thuật", "Động cơ Bóc tách Kép Thông minh (Dual-Engine Hybrid Parser)", 9)

    img_ocr = os.path.join(PROJECT_ROOT, "workshop/static/images/architecture/aws-hybrid-ocr-engine-architecture.png")

    add_card(s9, 0.8, 1.35, left_w, 4.2, bg_color=COLOR_BG_WHITE, border_color=COLOR_BORDER, accent_bar_color=COLOR_GREEN)
    tx9_l = s9.shapes.add_textbox(Inches(1.05), Inches(1.5), Inches(left_w - 0.35), Inches(3.9))
    tf9_l = tx9_l.text_frame
    tf9_l.word_wrap = True

    p = tf9_l.paragraphs[0]
    p.text = "THUẬT TOÁN PHÂN LUỒNG TỐI ƯU"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN

    engine_bullets = [
        ("Tầng 1: Fast-Path Native", "Phân tích cấu trúc vector của PDF bằng PyMuPDF. Tốc độ 0.28s/trang, chi phí 0.00 USD, giữ 100% cấu trúc bảng."),
        ("Ngưỡng Mật độ Ký tự", "Kiểm tra Character Density Threshold (0.05). Nếu trang có mật độ chữ cao -> kích hoạt Fast-Path ngay lập tức."),
        ("Tầng 2: Multimodal OCR", "Kích hoạt khi trang scan có mật độ chữ thấp. Sử dụng Qwen2.5-VL 72B (Kaggle GPU) kết hợp failover sang Gemini Flash."),
        ("Hiệu quả Toàn diện", "85% tài liệu số được bóc tách tức thì, giảm hơn 90% chi phí và thời gian xử lý so với OCR truyền thống.")
    ]
    for b_title, b_desc in engine_bullets:
        add_info_block(tf9_l, b_title, b_desc, pt_size=9.5)

    add_card(s9, 0.8, 5.7, left_w, 1.3, bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER_STRONG, accent_bar_color=COLOR_BLUE)
    tx9_b = s9.shapes.add_textbox(Inches(1.05), Inches(5.8), Inches(left_w - 0.35), Inches(1.1))
    tf9_b = tx9_b.text_frame
    tf9_b.word_wrap = True
    pb = tf9_b.paragraphs[0]
    pb.text = "CHỈ SỐ THỰC NGHIỆM ĐỘNG CƠ"
    pb.font.name = "Arial"
    pb.font.size = Pt(11)
    pb.font.bold = True
    pb.font.color.rgb = COLOR_BLUE

    pb2 = tf9_b.add_paragraph()
    pb2.text = "• Tốc độ Fast-Path: 0.28 giây / trang PDF số\n• Độ chính xác cấu trúc bảng biểu: Đạt 99.4%\n• Độ trễ Vision OCR: ~2.54 giây / trang scan"
    pb2.font.name = "Arial"
    pb2.font.size = Pt(9.5)
    pb2.font.color.rgb = COLOR_TEXT_BODY

    add_diagram_image(s9, img_ocr, 5.0, 1.35, 7.0, right_w)

    set_speaker_notes(s9, "Đây là đóng góp kỹ thuật trọng tâm của đề tài. Nhờ thuật toán nhận diện mật độ ký tự số, hệ thống giải phóng 85% tài liệu số qua tầng Fast-Path native chỉ mất 0.28 giây/trang với chi phí 0 đồng, chỉ chuyển các trang scan thực sự sang tầng Vision OCR.")

    # =========================================================================
    # SLIDE 10: ĐƯỜNG ỐNG PHI MÁY CHỦ (SERVERLESS EVENT PIPELINE)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_light_header(s10, "Phần 3: Tối ưu Băng thông", "Đường ống Phi máy chủ Hướng sự kiện (Event-Driven Pipeline)", 10)

    img_pipe = os.path.join(PROJECT_ROOT, "workshop/static/images/architecture/aws-serverless-event-pipeline.png")

    add_card(s10, 0.8, 1.35, left_w, 4.2, bg_color=COLOR_BG_WHITE, border_color=COLOR_BORDER, accent_bar_color=COLOR_TAG_ORANGE)
    tx10_l = s10.shapes.add_textbox(Inches(1.05), Inches(1.5), Inches(left_w - 0.35), Inches(3.9))
    tf10_l = tx10_l.text_frame
    tf10_l.word_wrap = True

    p = tf10_l.paragraphs[0]
    p.text = "VƯỢT TRẦN 10MB API GATEWAY"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TAG_ORANGE

    pipe_bullets = [
        ("S3 Presigned URL", "Trình duyệt nhận URL ký bảo mật SigV4, tải trực tiếp tệp nhị phân lên S3 Bucket mà không qua API Gateway."),
        ("S3 Event Notification", "Sự kiện s3:ObjectCreated tự động kích hoạt hàm AWS Lambda huylam-ocr-processor trong 214 ms."),
        ("Xử lý Bất đồng bộ", "Hàm Lambda kiểm tra metadata, tạo bản ghi tiến trình trên DynamoDB với trạng thái PROCESSING."),
        ("Giải phóng Web Server", "Máy chủ web hoàn toàn không phải gánh luồng upload nặng, triệt tiêu 100% lỗi nghẽn I/O.")
    ]
    for b_title, b_desc in pipe_bullets:
        add_info_block(tf10_l, b_title, b_desc, pt_size=9.5)

    add_card(s10, 0.8, 5.7, left_w, 1.3, bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER_STRONG, accent_bar_color=COLOR_GREEN)
    tx10_b = s10.shapes.add_textbox(Inches(1.05), Inches(5.8), Inches(left_w - 0.35), Inches(1.1))
    tf10_b = tx10_b.text_frame
    tf10_b.word_wrap = True
    pb = tf10_b.paragraphs[0]
    pb.text = "THÔNG SỐ THỰC THI LAMBDA"
    pb.font.name = "Arial"
    pb.font.size = Pt(11)
    pb.font.bold = True
    pb.font.color.rgb = COLOR_GREEN

    pb2 = tf10_b.add_paragraph()
    pb2.text = "• Thời gian thực thi: 214.37 ms\n• Bộ nhớ tiêu thụ: 88 MB / 128 MB định mức\n• Chi phí thực thi: Nằm trọn trong Free Tier (1M reqs)"
    pb2.font.name = "Arial"
    pb2.font.size = Pt(9.5)
    pb2.font.color.rgb = COLOR_TEXT_BODY

    add_diagram_image(s10, img_pipe, 5.0, 1.35, 7.0, right_w)

    set_speaker_notes(s10, "Bằng việc ứng dụng cơ chế S3 Presigned URL, hệ thống hoàn toàn vượt qua rào cản 10MB của API Gateway, cho phép người dùng kéo thả tài liệu dung lượng lớn lên tới 100MB một cách mượt mà và an toàn.")

    # =========================================================================
    # SLIDE 11: THIẾT KẾ CƠ SỞ DỮ LIỆU ĐA CÔNG NGHỆ (POLYGLOT ERD)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_light_header(s11, "Phần 3: Thiết kế Dữ liệu", "Mô hình Cơ sở Dữ liệu Đa công nghệ (Polyglot Persistence & ERD)", 11)

    img_erd = os.path.join(PROJECT_ROOT, "workshop/static/images/architecture/aws-database-polyglot-erd.png")

    add_card(s11, 0.8, 1.35, left_w, 4.2, bg_color=COLOR_BG_WHITE, border_color=COLOR_BORDER, accent_bar_color=COLOR_BLUE)
    tx11_l = s11.shapes.add_textbox(Inches(1.05), Inches(1.5), Inches(left_w - 0.35), Inches(3.9))
    tf11_l = tx11_l.text_frame
    tf11_l.word_wrap = True

    p = tf11_l.paragraphs[0]
    p.text = "3 TẦNG LƯU TRỮ CHUYÊN BIỆT"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE

    db_bullets = [
        ("DynamoDB NoSQL", "Bảng huylam-ocr-jobs (On-Demand). PK: job_id (UUID), SK: created_at. Lưu vết trạng thái phi máy chủ với độ trễ < 8 ms."),
        ("Amazon S3 Object Storage", "Bucket huylam-ocr-documents: thư mục uploads/ lưu tệp gốc; thư mục outputs/ lưu MD, DOCX, PDF xuất bản."),
        ("Relational SQL Schema", "5 bảng quan hệ chuẩn hóa (users, documents, user_settings, api_keys, user_daily_usage) với ràng buộc CASCADE."),
        ("Toàn vẹn Dữ liệu", "Phân định rõ ranh giới giữa dữ liệu giao dịch và lưu trữ tệp lớn, tối ưu hóa triệt để chi phí I/O.")
    ]
    for b_title, b_desc in db_bullets:
        add_info_block(tf11_l, b_title, b_desc, pt_size=9.5)

    add_card(s11, 0.8, 5.7, left_w, 1.3, bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER_STRONG, accent_bar_color=COLOR_AWS_NAVY)
    tx11_b = s11.shapes.add_textbox(Inches(1.05), Inches(5.8), Inches(left_w - 0.35), Inches(1.1))
    tf11_b = tx11_b.text_frame
    tf11_b.word_wrap = True
    pb = tf11_b.paragraphs[0]
    pb.text = "KIỂM CHỨNG LIÊN KẾT NGOẠI (FK)"
    pb.font.name = "Arial"
    pb.font.size = Pt(11)
    pb.font.bold = True
    pb.font.color.rgb = COLOR_AWS_NAVY

    pb2 = tf11_b.add_paragraph()
    pb2.text = "• 100% đường liên kết FK bo viền không cắt chữ\n• Ràng buộc toàn vẹn ON DELETE CASCADE chuẩn mực\n• Hỗ trợ quản trị xoay vòng API Keys an toàn"
    pb2.font.name = "Arial"
    pb2.font.size = Pt(9.5)
    pb2.font.color.rgb = COLOR_TEXT_BODY

    add_diagram_image(s11, img_erd, 5.0, 1.35, 7.0, right_w)

    set_speaker_notes(s11, "Hệ thống kết hợp mô hình lưu trữ đa công nghệ Polyglot Persistence: DynamoDB lưu vết trạng thái công việc phi máy chủ, S3 lưu trữ đối tượng dung lượng lớn và Relational SQL quản lý tài khoản, phân quyền và xoay vòng API keys.")

    # =========================================================================
    # SLIDE 12: SƠ ĐỒ TUẦN TỰ XỬ LÝ TOÀN TRÌNH (SEQUENCE EVENT FLOW)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_light_header(s12, "Phần 3: Luồng Dữ liệu", "Sơ đồ Tuần tự Xử lý Toàn trình Hướng sự kiện (Sequence Event Flow)", 12)

    img_seq = os.path.join(PROJECT_ROOT, "workshop/static/images/architecture/aws-sequence-event-flow.png")

    add_card(s12, 0.8, 1.35, left_w, 4.2, bg_color=COLOR_BG_WHITE, border_color=COLOR_BORDER, accent_bar_color=COLOR_GREEN)
    tx12_l = s12.shapes.add_textbox(Inches(1.05), Inches(1.5), Inches(left_w - 0.35), Inches(3.9))
    tf12_l = tx12_l.text_frame
    tf12_l.word_wrap = True

    p = tf12_l.paragraphs[0]
    p.text = "11 BƯỚC XỬ LÝ TOÀN TRÌNH"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN

    seq_bullets = [
        ("Bước 1 — 3: Ingestion", "Web Studio xin URL ký SigV4, tải nhị phân trực tiếp lên S3 qua HTTP PUT mà không qua EC2."),
        ("Bước 4 — 6: Trigger", "S3 Notification kích hoạt AWS Lambda (214 ms), ghi DynamoDB Jobs và gọi bóc tách."),
        ("Bước 7: ALT Flow", "Tự động rẽ nhánh: Fast-Path Native (0.28s) cho PDF số hoặc Vision OCR (Kaggle GPU) cho scan."),
        ("Bước 8 — 9: Translate", "Dịch thuật qua LLM và kết xuất đa định dạng ghi vào outputs/ trên S3."),
        ("Bước 10 — 11: Render", "Cập nhật DynamoDB COMPLETED và giao diện Web Studio hiển thị song ngữ tức thì.")
    ]
    for b_title, b_desc in seq_bullets:
        add_info_block(tf12_l, b_title, b_desc, pt_size=9.5)

    add_card(s12, 0.8, 5.7, left_w, 1.3, bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER_STRONG, accent_bar_color=COLOR_BLUE)
    tx12_b = s12.shapes.add_textbox(Inches(1.05), Inches(5.8), Inches(left_w - 0.35), Inches(1.1))
    tf12_b = tx12_b.text_frame
    tf12_b.word_wrap = True
    pb = tf12_b.paragraphs[0]
    pb.text = "ĐO KIỂM TELEMETRY TOÀN TRÌNH"
    pb.font.name = "Arial"
    pb.font.size = Pt(11)
    pb.font.bold = True
    pb.font.color.rgb = COLOR_BLUE

    pb2 = tf12_b.add_paragraph()
    pb2.text = "• Thời gian kích hoạt Lambda: 214.37 ms\n• Ghi nhận DynamoDB state: < 8 ms\n• Tổng thời gian phản hồi: Gần như tức thì cho người dùng"
    pb2.font.name = "Arial"
    pb2.font.size = Pt(9.5)
    pb2.font.color.rgb = COLOR_TEXT_BODY

    add_diagram_image(s12, img_seq, 5.0, 1.35, 7.0, right_w)

    set_speaker_notes(s12, "Sơ đồ tuần tự minh họa chi tiết chu trình 11 bước xử lý. Bất đồng bộ hóa qua sự kiện S3 giúp ứng dụng phản hồi mượt mà mà không làm treo trình duyệt người dùng.")

    # =========================================================================
    # SLIDE 13: DỊCH THUẬT & KEY TOUR MANAGER
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_light_header(s13, "Phần 3: Trí tuệ Nhân tạo", "Module Dịch thuật Thuật ngữ Kỹ thuật & Key Tour Manager Chống Nghẽn", 13)

    add_card(s13, 0.8, card_y, half_w, card_h, bg_color=COLOR_BG_WHITE, border_color=COLOR_BORDER, accent_bar_color=COLOR_PURPLE)
    tx13_l = s13.shapes.add_textbox(Inches(1.1), Inches(card_y + 0.2), Inches(half_w - 0.4), Inches(card_h - 0.4))
    tf13_l = tx13_l.text_frame
    tf13_l.word_wrap = True

    p = tf13_l.paragraphs[0]
    p.text = "THUẬT TOÁN DỊCH THUẬT KỸ THUẬT CHUYÊN SÂU"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_PURPLE

    trans_bullets = [
        ("Bảo toàn Thuật ngữ AWS", "Prompt Engineering chuyên sâu bảo toàn nguyên vẹn tên dịch vụ AWS, mã lệnh bash/shell, tham số cấu hình và cú pháp KaTeX."),
        ("Dịch thuật Bảng biểu Toàn vẹn", "Dịch chính xác từng ô trong bảng Markdown mà không phá vỡ liên kết dòng và cột."),
        ("Phân đoạn Ngữ cảnh Thông minh", "Tự động phân đoạn (Chunking) theo ranh giới đoạn văn logic, đảm bảo mạch văn dịch trôi chảy và tự nhiên."),
        ("Hiệu năng Thực tế", "Thời gian dịch trung bình chỉ 2.80 giây cho một trang tài liệu đầy đủ nội dung chuyên môn.")
    ]
    for b_title, b_desc in trans_bullets:
        add_info_block(tf13_l, b_title, b_desc, pt_size=10.5)

    add_card(s13, 6.8, card_y, half_w, card_h, bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER_STRONG, accent_bar_color=COLOR_TAG_ORANGE)
    tx13_r = s13.shapes.add_textbox(Inches(7.1), Inches(card_y + 0.2), Inches(half_w - 0.4), Inches(card_h - 0.4))
    tf13_r = tx13_r.text_frame
    tf13_r.word_wrap = True

    pr = tf13_r.paragraphs[0]
    pr.text = "CƠ CHẾ XOAY VÒNG KHÓA (KEY TOUR MANAGER)"
    pr.font.name = "Arial"
    pr.font.size = Pt(13)
    pr.font.bold = True
    pr.font.color.rgb = COLOR_TAG_ORANGE

    kt_bullets = [
        ("Phân phối Tải Round-Robin", "Xoay vòng thông minh qua danh sách API keys của nhiều nhà cung cấp (Kaggle GPU, Google Gemini, Groq)."),
        ("Chống nghẽn Rate Limit", "Theo dõi số lượt gọi usage_count và tự động chuyển sang key kế tiếp khi đạt ngưỡng tải."),
        ("Exponential Backoff", "Tự động lùi thời gian thử lại khi gặp mã lỗi 429 Too Many Requests, đảm bảo tỷ lệ gọi thành công 99.99%."),
        ("Quản trị Động Không Downtime", "Cho phép thêm, xóa, bật/tắt khóa trực tiếp từ bảng điều khiển quản trị mà không cần khởi động lại máy chủ.")
    ]
    for b_title, b_desc in kt_bullets:
        add_info_block(tf13_r, b_title, b_desc, pt_size=10.5)

    set_speaker_notes(s13, "Module dịch thuật được trang bị cơ chế Key Tour Manager giúp xoay vòng các API key miễn phí, tự động lùi thời gian khi chạm hạn ngạch, đảm bảo ứng dụng luôn sẵn sàng phục vụ mà không bị gián đoạn.")

    # =========================================================================
    # SLIDE 14: BỘ XUẤT BẢN ĐA ĐỊNH DẠNG CHUẨN HỌC THUẬT
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_light_header(s14, "Phần 3: Xuất bản Tài liệu", "Bộ Xuất bản Đa định dạng Chuẩn Học thuật (Multi-Format Exporters)", 14)

    exp_cards = [
        ("MARKDOWN EXPORTER (.md)",
         "Chuẩn hóa GitHub-Flavored Markdown\n"
         "• Hỗ trợ công thức toán học KaTeX ($...$ và $$...$$).\n"
         "• Bảo toàn 100% bảng biểu Markdown chuẩn căn lề.\n"
         "• Nhúng hình ảnh sơ đồ kỹ thuật và khối mã nguồn có định dạng cú pháp chuyên nghiệp.",
         "Đặc tả: UTF-8 Encoding, GFM Specification",
         COLOR_AWS_NAVY),
        ("MICROSOFT WORD (.docx)",
         "Monochrome Academic Style (Chuẩn In ấn)\n"
         "• Cỡ chữ Times New Roman 13pt, dãn dòng 1.2pt chuẩn mực.\n"
         "• Bảng biểu viền đen 0.5pt, tiêu đề in đậm nền trong suốt.\n"
         "• Căn đều 2 lề (Justified), thụt đầu dòng 1.27 cm.\n"
         "• Siêu liên kết (hyperlinks) giữ nguyên màu xanh bấm được.",
         "Đặc tả: Biểu mẫu TTTN-06 HUCE, 0.15s Export",
         COLOR_BLUE),
        ("ADOBE PDF EXPORTER (.pdf)",
         "Chuẩn Nộp Lưu chiểu (< 10 MB)\n"
         "• Tái nén ảnh thông minh PyMuPDF chất lượng cao (quality=92, 180 DPI).\n"
         "• Giảm dung lượng từ 10.36 MB xuống 5.11 MB (-50.7%).\n"
         "• Bảo toàn 100% 42 trang in và 94 siêu liên kết hoạt động hoàn hảo.",
         "Đặc tả: 5.11 MB / 42 trang, Thỏa mãn trần 10MB",
         COLOR_TAG_ORANGE)
    ]

    card_3w = 3.733
    for idx, (ec_title, ec_desc, ec_spec, ec_col) in enumerate(exp_cards):
        left_pos = 0.8 + idx * 4.0
        # Top Card
        add_card(s14, left_pos, card_y, card_3w, 3.85, bg_color=COLOR_BG_WHITE, border_color=COLOR_BORDER, accent_bar_color=ec_col)
        tx_c = s14.shapes.add_textbox(Inches(left_pos + 0.2), Inches(card_y + 0.15), Inches(card_3w - 0.35), Inches(3.55))
        tfc = tx_c.text_frame
        tfc.word_wrap = True

        pc1 = tfc.paragraphs[0]
        pc1.text = ec_title
        pc1.font.name = "Arial"
        pc1.font.size = Pt(12)
        pc1.font.bold = True
        pc1.font.color.rgb = ec_col

        for line in ec_desc.split("\n"):
            pc2 = tfc.add_paragraph()
            pc2.text = line
            pc2.font.name = "Arial"
            pc2.font.size = Pt(9.5)
            pc2.font.color.rgb = COLOR_TEXT_BODY

        # Bottom Spec Card
        add_card(s14, left_pos, card_y + 4.05, card_3w, 1.6, bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER_STRONG, accent_bar_color=ec_col)
        tx_cb = s14.shapes.add_textbox(Inches(left_pos + 0.2), Inches(card_y + 4.15), Inches(card_3w - 0.35), Inches(1.4))
        tfcb = tx_cb.text_frame
        tfcb.word_wrap = True
        pb = tfcb.paragraphs[0]
        pb.text = "TIÊU CHUẨN ĐẶC TẢ"
        pb.font.name = "Arial"
        pb.font.size = Pt(11)
        pb.font.bold = True
        pb.font.color.rgb = ec_col
        pb2 = tfcb.add_paragraph()
        pb2.text = f"• {ec_spec}\n• Tương thích 100% nộp lưu chiểu và in ấn"
        pb2.font.name = "Arial"
        pb2.font.size = Pt(9.5)
        pb2.font.color.rgb = COLOR_TEXT_BODY

    set_speaker_notes(s14, "Bộ xuất bản của hệ thống tạo ra 3 định dạng hoàn chỉnh. Đặc biệt bản Word tuân thủ phong cách học thuật đơn sắc và bản PDF được nén xuống 5.11 MB, sẵn sàng nộp lưu chiểu và in ấn mà không vượt ngưỡng 10MB.")

    # =========================================================================
    # SLIDE 15: KIỂM CHỨNG GIAO DIỆN WEB STUDIO THỰC TẾ
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_light_header(s15, "Phần 3: Kiểm chứng Ứng dụng", "Giao diện Web Studio Thực tế & Trình Soạn thảo Đối chiếu Song ngữ", 15)

    img_studio = os.path.join(PROJECT_ROOT, "workshop/static/images/week11/03-studio-cv-extracted-translated.png")
    studio_img_w = 7.4

    # Left: Real UI screenshot
    add_diagram_image(s15, img_studio, 0.8, 1.35, 7.0, studio_img_w)

    # Right: Features Card
    right_x = 8.5
    right_cw = 4.0
    add_card(s15, right_x, 1.35, right_cw, 4.2, bg_color=COLOR_BG_WHITE, border_color=COLOR_BORDER, accent_bar_color=COLOR_BLUE)
    tx15_r = s15.shapes.add_textbox(Inches(right_x + 0.25), Inches(1.5), Inches(right_cw - 0.4), Inches(3.9))
    tf15_r = tx15_r.text_frame
    tf15_r.word_wrap = True

    p = tf15_r.paragraphs[0]
    p.text = "TÍNH NĂNG NỔI BẬT TRÊN WEB STUDIO"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE

    studio_bullets = [
        ("Kéo thả Trực quan", "Hỗ trợ kéo thả PDF, PNG, JPG lên tới 50 MB."),
        ("Tùy chọn Chế độ Xử lý", "Tự động phân loại hoặc ép buộc Fast-Path / Vision OCR."),
        ("Bilingual Side-by-Side", "Trình soạn thảo song ngữ cho phép đọc văn bản gốc bên trái và bản dịch tiếng Việt bên phải song song."),
        ("Xem trước Thời gian thực", "Xem ngay kết quả định dạng và tải về Word, PDF tức thì chỉ với một cú nhấp chuột.")
    ]
    for b_title, b_desc in studio_bullets:
        add_info_block(tf15_r, b_title, b_desc, pt_size=9.5)

    # Right bottom card
    add_card(s15, right_x, 5.7, right_cw, 1.3, bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER_STRONG, accent_bar_color=COLOR_TAG_ORANGE)
    tx15_b = s15.shapes.add_textbox(Inches(right_x + 0.25), Inches(5.8), Inches(right_cw - 0.4), Inches(1.1))
    tf15_b = tx15_b.text_frame
    tf15_b.word_wrap = True
    pb = tf15_b.paragraphs[0]
    pb.text = "TRẢI NGHIỆM NGƯỜI DÙNG TỐI ƯU"
    pb.font.name = "Arial"
    pb.font.size = Pt(11)
    pb.font.bold = True
    pb.font.color.rgb = COLOR_TAG_ORANGE

    pb2 = tf15_b.add_paragraph()
    pb2.text = "• Giao diện Web Responsive hiện đại\n• Đồng bộ cuộn trang Side-by-Side tự động\n• Phù hợp với kỹ sư, giảng viên và sinh viên"
    pb2.font.name = "Arial"
    pb2.font.size = Pt(9.5)
    pb2.font.color.rgb = COLOR_TEXT_BODY

    set_speaker_notes(s15, "Trên màn hình là giao diện Web Studio thực tế đang chạy trên hạ tầng AWS. Người dùng có thể kéo thả tài liệu, xem tiến trình bóc tách và đối chiếu bản gốc - bản dịch song song theo thời gian thực.")

    # =========================================================================
    # SLIDE 16: SỐ LIỆU ĐO KIỂM THỰC NGHIỆM (BENCHMARK)
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_light_header(s16, "Phần 3: Đo kiểm Thực nghiệm", "Số liệu Thực nghiệm Hiệu năng Toàn trình & So sánh Động cơ (Benchmark)", 16)

    # Table
    rows, cols = 6, 5
    table_shape = s16.shapes.add_table(rows, cols, Inches(0.8), Inches(1.35), Inches(11.733), Inches(3.2))
    table = table_shape.table

    table.columns[0].width = Inches(2.8)
    table.columns[1].width = Inches(2.2)
    table.columns[2].width = Inches(2.733)
    table.columns[3].width = Inches(2.0)
    table.columns[4].width = Inches(2.0)

    headers = ["Tác vụ Thực nghiệm", "Tài liệu Kiểm thử", "Động cơ Thực thi", "Thời gian Xử lý", "Chi phí AWS"]
    for c_idx, h in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_AWS_NAVY
        p = cell.text_frame.paragraphs[0]
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
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
            cell.fill.fore_color.rgb = COLOR_BG_WHITE if r_idx % 2 == 0 else COLOR_BG_LIGHT
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Arial"
            p.font.size = Pt(10.5)
            p.font.color.rgb = COLOR_TEXT_BODY
            if c_idx >= 3:
                p.alignment = PP_ALIGN.CENTER
                p.font.bold = True
                if c_idx == 4:
                    p.font.color.rgb = COLOR_GREEN

    # Highlight Card Below Table
    add_card(s16, 0.8, 4.8, 11.733, 2.2, bg_color=COLOR_BG_WHITE, border_color=COLOR_BORDER_STRONG, accent_bar_color=COLOR_BLUE)
    tx16_bot = s16.shapes.add_textbox(Inches(1.15), Inches(4.95), Inches(11.2), Inches(1.9))
    tf16_b = tx16_bot.text_frame
    tf16_b.word_wrap = True

    pb1 = tf16_b.paragraphs[0]
    pb1.text = "KẾT LUẬN TỪ ĐO KIỂM THỰC NGHIỆM:"
    pb1.font.name = "Arial"
    pb1.font.size = Pt(12)
    pb1.font.bold = True
    pb1.font.color.rgb = COLOR_BLUE

    eval_bullets = [
        "1. Độ chính xác cấu trúc bảng biểu đạt 99.4% đối với tài liệu số nhờ công nghệ Fast-Path Native.",
        "2. Tốc độ bóc tách trung bình 0.28 giây/trang, nhanh hơn gấp 10 lần so với các giải pháp OCR truyền thống.",
        "3. Thời gian phản hồi Lambda s3-trigger chỉ 214.37 ms với bộ nhớ tiêu thụ khiêm tốn 88 MB / 128 MB.",
        "4. Chi phí toàn trình duy trì mức 0.00 USD tuyệt đối xuyên suốt toàn bộ quá trình kiểm thử tải và vận hành."
    ]
    for b in eval_bullets:
        pb = tf16_b.add_paragraph()
        pb.text = f"• {b}"
        pb.font.name = "Arial"
        pb.font.size = Pt(10.5)
        pb.font.color.rgb = COLOR_TEXT_BODY

    set_speaker_notes(s16, "Bảng đo kiểm thực nghiệm cho thấy Fast-Path bóc tách 11 trang tài liệu chỉ mất 3.07 giây (0.28 giây/trang), nhanh gấp 10 lần các giải pháp OCR truyền thống, trong khi vẫn bảo toàn tuyệt đối 99.4% cấu trúc bảng biểu.")

    # =========================================================================
    # SLIDE 17: KỶ LUẬT TÀI CHÍNH ĐÁM MÂY (FINOPS ZERO-BREACH)
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_light_header(s17, "Phần 3: Quản trị Tài chính", "Kỷ luật Tài chính Đám mây (FinOps Zero-Breach 0.00 USD)", 17)

    # Left Card
    add_card(s17, 0.8, card_y, 6.2, card_h, bg_color=COLOR_BG_WHITE, border_color=COLOR_BORDER, accent_bar_color=COLOR_GREEN)
    tx17_l = s17.shapes.add_textbox(Inches(1.1), Inches(card_y + 0.2), Inches(5.7), Inches(card_h - 0.4))
    tf17_l = tx17_l.text_frame
    tf17_l.word_wrap = True

    p = tf17_l.paragraphs[0]
    p.text = "CHIẾN LƯỢC QUẢN TRỊ CHI PHÍ FINOPS CHỦ ĐỘNG"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_TITLE

    finops_bullets = [
        ("Tận dụng AWS Free Tier", "Sử dụng EC2 t3.micro (750 giờ/tháng), S3 Standard (5 GB), DynamoDB (25 GB miễn phí trọn đời)."),
        ("Kiến trúc Serverless Scale-to-Zero", "AWS Lambda miễn phí 1 triệu lượt gọi/tháng; không phát sinh bất kỳ chi phí tính toán nào khi hệ thống không có yêu cầu."),
        ("Cụm GPU Ngoại vi Bảo mật", "Chạy mô hình thị giác Qwen2.5-VL 72B trên cụm GPU Kaggle miễn phí (30 giờ/tuần), kết hợp Cloudflare Tunnel an toàn."),
        ("Cảnh báo Ngân sách Tự động", "Thiết lập AWS Budgets cảnh báo ngưỡng chi phí 0.01 USD và CloudWatch Billing Alarm tự động gửi thông báo qua SNS.")
    ]
    for b_title, b_desc in finops_bullets:
        add_info_block(tf17_l, b_title, b_desc, pt_size=10.5)

    # Right Top Card: Metric Display
    add_card(s17, 7.3, card_y, 5.233, 2.3, bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER_STRONG, accent_bar_color=COLOR_GREEN)
    tx17_rt = s17.shapes.add_textbox(Inches(7.5), Inches(card_y + 0.15), Inches(4.8), Inches(2.0))
    tf17_rt = tx17_rt.text_frame
    tf17_rt.word_wrap = True

    prc = tf17_rt.paragraphs[0]
    prc.text = "KẾT QUẢ FINOPS SAU 12 TUẦN"
    prc.font.name = "Arial"
    prc.font.size = Pt(13)
    prc.font.bold = True
    prc.font.color.rgb = COLOR_GREEN
    prc.alignment = PP_ALIGN.CENTER

    p_cost = tf17_rt.add_paragraph()
    p_cost.text = "0.00 USD"
    p_cost.font.name = "Arial"
    p_cost.font.size = Pt(38)
    p_cost.font.bold = True
    p_cost.font.color.rgb = COLOR_TITLE
    p_cost.alignment = PP_ALIGN.CENTER

    p_sub = tf17_rt.add_paragraph()
    p_sub.text = "(Kiểm chứng 100% qua AWS Cost Explorer)"
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(11)
    p_sub.font.italic = True
    p_sub.font.color.rgb = COLOR_TEXT_MUTED
    p_sub.alignment = PP_ALIGN.CENTER

    # Right Bottom Card: Detailed Cost Breakdown
    add_card(s17, 7.3, card_y + 2.5, 5.233, 3.15, bg_color=COLOR_BG_WHITE, border_color=COLOR_BORDER, accent_bar_color=COLOR_BLUE)
    tx17_rb = s17.shapes.add_textbox(Inches(7.5), Inches(card_y + 2.65), Inches(4.8), Inches(2.85))
    tf17_rb = tx17_rb.text_frame
    tf17_rb.word_wrap = True

    p_h = tf17_rb.paragraphs[0]
    p_h.text = "CHI TIẾT HÓA ĐƠN DỊCH VỤ AWS"
    p_h.font.name = "Arial"
    p_h.font.size = Pt(12)
    p_h.font.bold = True
    p_h.font.color.rgb = COLOR_BLUE

    breakdown_items = [
        ("Amazon EC2 (t3.micro)", "$0.00 (AWS Free Tier 750h)"),
        ("Amazon S3 Documents", "$0.00 (< 5 GB Standard Storage)"),
        ("Amazon DynamoDB", "$0.00 (25 GB NoSQL On-Demand)"),
        ("AWS Lambda Trigger", "$0.00 (1M Lượt gọi / tháng)"),
        ("Application Load Balancer", "$0.00 (750h Free Trial)")
    ]
    for svc, cost in breakdown_items:
        add_info_block(tf17_rb, svc, cost, pt_size=9.5)

    p_total = tf17_rb.add_paragraph()
    p_total.text = "• TỔNG PHÁT SINH: 0.00 USD (ZERO-BREACH GUARANTEE)"
    p_total.font.name = "Arial"
    p_total.font.size = Pt(10)
    p_total.font.bold = True
    p_total.font.color.rgb = COLOR_GREEN

    set_speaker_notes(s17, "Kỷ luật FinOps là một trong những điểm sáng nhất của đề tài. Sau 12 tuần liên tục phát triển và kiểm thử toàn diện trên AWS, hóa đơn thực tế được kiểm chứng qua AWS Cost Explorer là đúng 0.00 USD.")

    # =========================================================================
    # SLIDE 18: HƯỚNG PHÁT TRIỂN MỞ RỘNG (ROADMAP & ECS FARGATE)
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    add_light_header(s18, "Phần 4: Đề xuất Giải pháp", "Kế hoạch Phát triển Mở rộng (Advanced Roadmap & Containerization)", 18)

    img_ecs = os.path.join(PROJECT_ROOT, "workshop/static/images/architecture/aws-ecs-fargate-architecture.png")

    add_card(s18, 0.8, 1.35, left_w, 4.2, bg_color=COLOR_BG_WHITE, border_color=COLOR_BORDER, accent_bar_color=COLOR_AWS_NAVY)
    tx18_l = s18.shapes.add_textbox(Inches(1.05), Inches(1.5), Inches(left_w - 0.35), Inches(3.9))
    tf18_l = tx18_l.text_frame
    tf18_l.word_wrap = True

    p = tf18_l.paragraphs[0]
    p.text = "3 HƯỚNG NÂNG CẤP HỆ THỐNG"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_AWS_NAVY

    road_bullets = [
        ("Container hóa ECS Fargate", "Đóng gói ứng dụng thành Microservices triển khai trên Amazon ECS Fargate phi máy chủ, tự động co giãn theo số lượng người dùng."),
        ("Agentic RAG với Bedrock", "Tích hợp Amazon Bedrock Knowledge Bases và OpenSearch Serverless, hỗ trợ tra cứu hỏi đáp thông minh theo ngữ cảnh."),
        ("Tự động hóa CI/CD Toàn trình", "Xây dựng pipeline kiểm thử và triển khai liên tục tự động với AWS CodePipeline và AWS CodeBuild.")
    ]
    for b_title, b_desc in road_bullets:
        add_info_block(tf18_l, b_title, b_desc, pt_size=9.5)

    add_card(s18, 0.8, 5.7, left_w, 1.3, bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER_STRONG, accent_bar_color=COLOR_BLUE)
    tx18_b = s18.shapes.add_textbox(Inches(1.05), Inches(5.8), Inches(left_w - 0.35), Inches(1.1))
    tf18_b = tx18_b.text_frame
    tf18_b.word_wrap = True
    pb = tf18_b.paragraphs[0]
    pb.text = "LỘ TRÌNH ĐỒ ÁN TỐT NGHIỆP"
    pb.font.name = "Arial"
    pb.font.size = Pt(11)
    pb.font.bold = True
    pb.font.color.rgb = COLOR_BLUE

    pb2 = tf18_b.add_paragraph()
    pb2.text = "• Mở rộng quy mô phục vụ hàng trăm ngàn tài liệu\n• Tích hợp mô hình AI Claude 3.5 Sonnet qua Bedrock\n• Triển khai Infrastructure as Code (Terraform / CDK)"
    pb2.font.name = "Arial"
    pb2.font.size = Pt(9.5)
    pb2.font.color.rgb = COLOR_TEXT_BODY

    add_diagram_image(s18, img_ecs, 5.0, 1.35, 7.0, right_w)

    set_speaker_notes(s18, "Trong giai đoạn phát triển tiếp theo, hệ thống sẵn sàng được container hóa và chuyển dịch lên Amazon ECS Fargate để tự động co giãn không giới hạn, đồng thời kết hợp Agentic RAG với Amazon Bedrock Knowledge Bases.")

    # =========================================================================
    # SLIDE 19: TỰ ĐÁNH GIÁ KẾT QUẢ & ĐỊNH HƯỚNG NGHỀ NGHIỆP
    # =========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    add_light_header(s19, "Phần 5: Đánh giá & Định hướng", "Kết quả Đạt được sau Kỳ Thực tập & Định hướng Nghề nghiệp Cá nhân", 19)

    add_card(s19, 0.8, card_y, half_w, card_h, bg_color=COLOR_BG_WHITE, border_color=COLOR_BORDER, accent_bar_color=COLOR_BLUE)
    tx19_l = s19.shapes.add_textbox(Inches(1.1), Inches(card_y + 0.2), Inches(half_w - 0.4), Inches(card_h - 0.4))
    tf19_l = tx19_l.text_frame
    tf19_l.word_wrap = True

    p = tf19_l.paragraphs[0]
    p.text = "KẾT QUẢ THU NHẬN ĐƯỢC SAU 12 TUẦN"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_TITLE

    achieve_bullets = [
        ("Hoàn thành 100% Khối lượng", "Đạt toàn bộ mục tiêu đề ra trong đề cương kế hoạch 12 tuần theo quy định của Khoa CNTT — HUCE."),
        ("Hồ sơ Báo cáo Chuẩn mực", "Hoàn thiện cuốn báo cáo dày 42 trang theo Biểu mẫu TTTN-06, tích hợp 16 sơ đồ kỹ thuật và 11 bảng biểu chuẩn hóa."),
        ("Kỹ năng Kỹ thuật Đột phá", "Làm chủ thiết kế kiến trúc đám mây AWS Well-Architected, an ninh mạng Zero-Trust, Serverless, AI Multimodal và FinOps."),
        ("Tác phong Kỹ sư Toàn cầu", "Rèn luyện tính chủ động, tư duy phân tích nguyên nhân gốc rễ (Root Cause Analysis) và tinh thần Ownership tuyệt đối.")
    ]
    for b_title, b_desc in achieve_bullets:
        add_info_block(tf19_l, b_title, b_desc, pt_size=10.5)

    add_card(s19, 6.8, card_y, half_w, card_h, bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER_STRONG, accent_bar_color=COLOR_TAG_ORANGE)
    tx19_r = s19.shapes.add_textbox(Inches(7.1), Inches(card_y + 0.2), Inches(half_w - 0.4), Inches(card_h - 0.4))
    tf19_r = tx19_r.text_frame
    tf19_r.word_wrap = True

    pr = tf19_r.paragraphs[0]
    pr.text = "ĐỊNH HƯỚNG NGHỀ NGHIỆP CÁ NHÂN"
    pr.font.name = "Arial"
    pr.font.size = Pt(13)
    pr.font.bold = True
    pr.font.color.rgb = COLOR_TAG_ORANGE

    career_bullets = [
        ("Mục tiêu Chuyên môn", "Phát triển theo hướng Cloud Solutions Architect & AI/ML Solutions Engineer chuyên nghiệp."),
        ("Lộ trình Chứng chỉ Quốc tế", "Hoàn thành chứng chỉ AWS Certified Solutions Architect - Associate (SAA) và hướng tới cấp độ Professional (SAP)."),
        ("Đóng góp Cộng đồng Kỹ thuật", "Xuất bản tài liệu hướng dẫn kỹ thuật mở (Open Workshop) trên nền tảng GitHub Pages chia sẻ cho sinh viên và cộng đồng."),
        ("Nền tảng Đồ án Tốt nghiệp", "Tiếp tục phát triển hệ thống làm đề tài Đồ án Tốt nghiệp chuyên sâu trong học kỳ tới tại HUCE.")
    ]
    for b_title, b_desc in career_bullets:
        add_info_block(tf19_r, b_title, b_desc, pt_size=10.5)

    set_speaker_notes(s19, "Kỳ thực tập không chỉ giúp em hoàn thành xuất sắc đồ án báo cáo tốt nghiệp mà còn định hình rõ nét con đường sự nghiệp tương lai hướng tới vị trí Kỹ sư Kiến trúc Đám mây và AI chuyên nghiệp.")

    # =========================================================================
    # SLIDE 20: LỜI CẢM ƠN & PHIÊN HỎI ĐÁP (Q&A)
    # =========================================================================
    s20 = prs.slides.add_slide(blank_layout)
    bg20 = s20.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg20.fill.solid()
    bg20.fill.fore_color.rgb = COLOR_BG_WHITE
    bg20.line.color.rgb = COLOR_BG_WHITE

    bar20 = s20.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.18))
    bar20.fill.solid()
    bar20.fill.fore_color.rgb = COLOR_AWS_ORANGE
    bar20.line.color.rgb = COLOR_AWS_ORANGE

    # Center card
    card_20w = 11.733
    add_card(s20, 0.8, 0.8, card_20w, 5.9, bg_color=COLOR_BG_LIGHT, border_color=COLOR_BORDER_STRONG, accent_bar_color=COLOR_AWS_ORANGE)

    tx20 = s20.shapes.add_textbox(Inches(1.2), Inches(1.1), Inches(card_20w - 0.8), Inches(5.3))
    tf20 = tx20.text_frame
    tf20.word_wrap = True

    p = tf20.paragraphs[0]
    p.text = "CHÂN THÀNH CẢM ƠN QUÝ THẦY CÔ VÀ HỘI ĐỒNG ĐÁNH GIÁ!"
    p.font.name = "Arial"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = COLOR_TITLE
    p.alignment = PP_ALIGN.CENTER

    p_sub = tf20.add_paragraph()
    p_sub.text = (
        "\nEm xin bày tỏ lòng biết ơn sâu sắc đến ThS. Lê Văn Minh cùng các Thầy/Cô Khoa Công nghệ Thông tin — HUCE\n"
        "và các Chuyên gia hướng dẫn tại Công ty TNHH Amazon Web Services Việt Nam (AWS Vietnam)\n"
        "đã tận tình chỉ dẫn và tạo mọi điều kiện thuận lợi nhất để em hoàn thành kỳ thực tập."
    )
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(12)
    p_sub.font.color.rgb = COLOR_TEXT_BODY
    p_sub.alignment = PP_ALIGN.CENTER

    p_qa = tf20.add_paragraph()
    p_qa.text = "\n\nPHIÊN HỎI ĐÁP & CHẤT VẤN KHOA HỌC (Q&A)\nKính mời Quý Thầy/Cô trong Hội đồng đặt câu hỏi đóng góp cho đề tài!"
    p_qa.font.name = "Arial"
    p_qa.font.size = Pt(16)
    p_qa.font.bold = True
    p_qa.font.color.rgb = COLOR_TAG_ORANGE
    p_qa.alignment = PP_ALIGN.CENTER

    p_links = tf20.add_paragraph()
    p_links.text = (
        "\n\nKho mã nguồn dự án: https://github.com/Lamhuy0489/aws\n"
        "Website Workshop Kỹ thuật: https://lamhuy0489.github.io/workshop/\n"
        "Email liên hệ: huylam0489@gmail.com   |   hunggia@amazon.com.vn"
    )
    p_links.font.name = "Arial"
    p_links.font.size = Pt(11)
    p_links.font.color.rgb = COLOR_TEXT_MUTED
    p_links.alignment = PP_ALIGN.CENTER

    set_speaker_notes(s20, "Em xin chân thành cảm ơn Quý Thầy/Cô đã chú ý lắng nghe bài trình bày. Em rất mong nhận được những câu hỏi và ý kiến đóng góp quý báu từ Hội đồng để đề tài được hoàn thiện tốt hơn nữa!")

    # =========================================================================
    # LƯU FILE PPTX & XUẤT BẢN PDF
    # =========================================================================
    os.makedirs(OUT_DIR, exist_ok=True)
    prs.save(PPTX_PATH)
    print("=" * 70)
    print(f"1. Xuat ban PPTX thanh cong tai: {PPTX_PATH}")

    os.makedirs(os.path.dirname(STATIC_DOWNLOADS_PPTX), exist_ok=True)
    prs.save(STATIC_DOWNLOADS_PPTX)
    print(f"2. Dong bo PPTX tai ve sang: {STATIC_DOWNLOADS_PPTX}")

    # Xuất bản PDF thông qua AppleScript (PowerPoint)
    print("3. Dang xuat ban ban PDF qua Microsoft PowerPoint...")
    applescript_cmd = f'''
    tell application "Microsoft PowerPoint"
        open POSIX file "{PPTX_PATH}"
        delay 2
        save active presentation in POSIX file "{PDF_PATH}" as save as PDF
        delay 1
        close active presentation saving no
    end tell
    '''
    try:
        res = subprocess.run(["osascript", "-e", applescript_cmd], capture_output=True, text=True, timeout=30)
        if res.returncode == 0 and os.path.exists(PDF_PATH):
            pdf_size = os.path.getsize(PDF_PATH) / (1024 * 1024)
            print(f"   Xuat ban PDF thanh cong ({pdf_size:.2f} MB) tai: {PDF_PATH}")
            # Đồng bộ sang workshop/static/downloads/
            import shutil
            shutil.copy2(PDF_PATH, STATIC_DOWNLOADS_PDF)
            print(f"   Dong bo PDF tai ve sang: {STATIC_DOWNLOADS_PDF}")
        else:
            print("   Luu y: AppleScript PowerPoint PDF export khong hoan tat, kiem tra lai.")
            print("   Stderr:", res.stderr)
    except Exception as e:
        print("   Loi khi xuat PDF:", e)

    print("=" * 70)
    print("HOAN TAT TOAN BO 20 SLIDE GIAO DIEN MAU SANG CHUAN MUC!")
    print("=" * 70)

if __name__ == "__main__":
    create_light_presentation()
