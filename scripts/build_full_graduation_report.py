#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Script lắp ráp toàn bộ Báo cáo Thực tập Tốt nghiệp hoàn chỉnh (chuẩn Mẫu TTTN-06 HUCE)
Dành cho sinh viên: Lâm Quang Huy - MSSV: 0212267 - Lớp: 67CS
Tối ưu hóa toàn diện theo phản hồi:
1. Thống nhất danh sách đầu mục (không trộn lẫn dấu chấm và số).
2. Mục lục, Danh mục hình vẽ, Danh mục bảng biểu có thể BẤM VÀO ĐƯỢC (Hyperlink nội bộ tới Bookmark).
3. Tài liệu tham khảo có đường dẫn mạng URL ngoài có thể bấm được, không in đậm [1].
4. Giãn cách dòng (Line Spacing) và khoảng cách đoạn (Paragraph Spacing) đồng nhất 1.3 lines, chuẩn mực in ấn.
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import docx
from docx.shared import Cm, Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT

from scripts.docx_helpers import (
    set_cell_margins, set_cell_shading, set_table_borders,
    set_transparent_borders, make_table_robust,
    add_cover_page_border, add_footer_page_number,
    add_bookmark, get_bookmark_name, add_hyperlink_tab_entry
)

from scripts.report_sections.part1_intro import add_part1
from scripts.report_sections.part2_plan import add_part2
from scripts.report_sections.part3_tech import add_part3
from scripts.report_sections.part4_eval import add_part4
from scripts.report_sections.part5_self import add_part5
from scripts.report_sections.part6_concl import add_part6

def build_complete_report():
    print("=" * 70)
    print("BẮT ĐẦU XÂY DỰNG BÁO CÁO THỰC TẬP TỐT NGHIỆP HUCE (MẪU TTTN-06)")
    print("Sinh viên: Lâm Quang Huy - MSSV: 0212267 - Lớp: 67CS")
    print("Đề tài: Serverless Hybrid Document OCR, Parsing & Translation Platform on AWS")
    print("=" * 70)

    doc = docx.Document()

    # 1. Cấu hình trang chuẩn A4 căn lề 3 - 2 - 2 - 2 cm theo Mẫu TTTN-06
    section = doc.sections[0]
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(3.0)
    section.right_margin = Cm(2.0)
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)

    # Thêm viền đôi trang trọng cho duy nhất trang bìa đầu tiên
    add_cover_page_border(section)

    # Phân tách bìa và nội dung để không hiện số trang ở bìa
    section.different_first_page_header_footer = True

    # Trang bìa: Không hiển thị số trang
    first_footer = section.first_page_footer
    first_footer.is_linked_to_previous = False
    if len(first_footer.paragraphs) > 0:
        first_footer.paragraphs[0].text = ""

    # Các trang nội dung: Chỉ hiển thị số trang ở chính giữa
    footer = section.footer
    footer.is_linked_to_previous = False
    footer_p = footer.paragraphs[0]
    footer_p.text = ""
    footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_pg = footer_p.add_run()
    r_pg.font.name = "Times New Roman"
    r_pg.font.size = Pt(11)
    r_pg.font.color.rgb = RGBColor(0, 0, 0)
    add_footer_page_number(r_pg)

    # Cấu hình styles chuẩn toàn văn bản (chuẩn mực 1.3 lines, giãn đoạn 3pt)
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(13)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.3
    normal_style.paragraph_format.space_before = Pt(0)
    normal_style.paragraph_format.space_after = Pt(3)

    # =========================================================================
    # CÁC HÀM HELPER CHÈN ĐỊNH DẠNG VÀ TỰ ĐỘNG TẠO BOOKMARK NỘI BỘ
    # =========================================================================
    def add_h1(text):
        """Tiêu đề phần / chương: Căn giữa, đậm, cỡ 15, giãn dòng chuẩn, gắn Bookmark."""
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        bm_name = get_bookmark_name(text)
        if bm_name:
            add_bookmark(p, bm_name)
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(15)
        run.font.name = "Times New Roman"
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_h2(text):
        """Tiêu đề mục cấp 2: Căn trái, đậm, cỡ 13.5, giãn dòng chuẩn, gắn Bookmark."""
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.space_before = Pt(9)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        bm_name = get_bookmark_name(text)
        if bm_name:
            add_bookmark(p, bm_name)
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(13.5)
        run.font.name = "Times New Roman"
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_h3(text):
        """Tiêu đề mục cấp 3: Căn trái, đậm nghiêng, cỡ 13, giãn dòng chuẩn, gắn Bookmark."""
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        bm_name = get_bookmark_name(text)
        if bm_name:
            add_bookmark(p, bm_name)
        run = p.add_run(text)
        run.bold = True
        run.font.italic = True
        run.font.size = Pt(13)
        run.font.name = "Times New Roman"
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_body(text, bold_prefix="", indent=False):
        """Đoạn văn thân bài: Căn đều 2 lề (Justify), giãn dòng 1.3 lines chuẩn mực."""
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        if indent:
            p.paragraph_format.first_line_indent = Cm(0.8)
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
            r_pre.font.name = "Times New Roman"
            r_pre.font.size = Pt(13)
            r_pre.font.color.rgb = RGBColor(0, 0, 0)
        r_text = p.add_run(text)
        r_text.font.name = "Times New Roman"
        r_text.font.size = Pt(13)
        r_text.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_bullet(text, bold_prefix=""):
        """Đầu mục gạch đầu dòng chuẩn, căn đều 2 lề, giãn dòng 1.3 lines thống nhất."""
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
            r_pre.font.name = "Times New Roman"
            r_pre.font.size = Pt(13)
            r_pre.font.color.rgb = RGBColor(0, 0, 0)
        r_text = p.add_run(text)
        r_text.font.name = "Times New Roman"
        r_text.font.size = Pt(13)
        r_text.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_figure(img_path, caption_text, width_cm=15.5):
        """Chèn hình ảnh trung tâm kèm chú thích và tự động gắn Bookmark cho Danh mục hình vẽ."""
        if not os.path.isabs(img_path):
            img_path = os.path.join(PROJECT_ROOT, img_path)
        if not os.path.exists(img_path):
            print(f"Cảnh báo: Không tìm thấy ảnh {img_path}")
            return
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.paragraph_format.keep_with_next = True
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Cm(width_cm))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.line_spacing = 1.15
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(6)
        bm_name = get_bookmark_name(caption_text)
        if bm_name:
            add_bookmark(p_cap, bm_name)
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(11)
        r_cap.font.italic = True
        r_cap.bold = True
        r_cap.font.color.rgb = RGBColor(0, 0, 0)

    # =========================================================================
    # TRANG BÌA CHÍNH (COVER PAGE)
    # =========================================================================
    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_top.paragraph_format.line_spacing = 1.2
    p_top.paragraph_format.space_before = Pt(0)
    p_top.paragraph_format.space_after = Pt(2)

    r = p_top.add_run("TRƯỜNG ĐẠI HỌC XÂY DỰNG HÀ NỘI\n")
    r.bold = True
    r.font.size = Pt(14)
    r.font.name = "Times New Roman"
    r.font.color.rgb = RGBColor(0, 0, 0)

    r = p_top.add_run("KHOA CÔNG NGHỆ THÔNG TIN\n")
    r.bold = True
    r.font.size = Pt(13)
    r.font.name = "Times New Roman"
    r.font.color.rgb = RGBColor(0, 0, 0)

    r = p_top.add_run("═════════ ❖ ═════════")
    r.font.size = Pt(11)
    r.font.name = "Times New Roman"
    r.font.color.rgb = RGBColor(0, 0, 0)

    # Chèn Logo Trường Đại học Xây dựng Hà Nội
    logo_path = os.path.join(PROJECT_ROOT, "bao cao tot nghiep", "logo_huce.png")
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(6)
        p_logo.paragraph_format.space_after = Pt(6)
        r_logo = p_logo.add_run()
        r_logo.add_picture(logo_path, width=Cm(3.2))

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.line_spacing = 1.25
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(10)

    r_sub = p_title.add_run("BÁO CÁO THỰC TẬP TỐT NGHIỆP\n\n")
    r_sub.bold = True
    r_sub.font.size = Pt(18)
    r_sub.font.name = "Times New Roman"
    r_sub.font.color.rgb = RGBColor(0, 0, 0)

    r_topic_pre = p_title.add_run("ĐỀ TÀI:\n")
    r_topic_pre.bold = True
    r_topic_pre.font.size = Pt(13)
    r_topic_pre.font.name = "Times New Roman"
    r_topic_pre.font.color.rgb = RGBColor(0, 0, 0)

    r_topic = p_title.add_run("NGHIÊN CỨU TRIỂN KHAI HẠ TẦNG ĐÁM MÂY AWS VÀ XÂY DỰNG NỀN TẢNG BÓC TÁCH, OCR LAI VÀ DỊCH THUẬT TÀI LIỆU KỸ THUẬT SERVERLESS\n")
    r_topic.bold = True
    r_topic.font.size = Pt(13.5)
    r_topic.font.name = "Times New Roman"
    r_topic.font.color.rgb = RGBColor(0, 0, 0)

    r_en = p_title.add_run("(SERVERLESS HYBRID DOCUMENT OCR, PARSING & TECHNICAL TRANSLATION PLATFORM ON AWS)\n\n")
    r_en.font.italic = True
    r_en.bold = True
    r_en.font.size = Pt(11)
    r_en.font.name = "Times New Roman"
    r_en.font.color.rgb = RGBColor(0, 0, 0)

    r_prog = p_title.add_run("CHƯƠNG TRÌNH FIRST CLOUD AI JOURNEY (FCAJ) BOOTCAMP 2026")
    r_prog.bold = True
    r_prog.font.size = Pt(12)
    r_prog.font.name = "Times New Roman"
    r_prog.font.color.rgb = RGBColor(0, 0, 0)

    # Bảng thông tin sinh viên và người hướng dẫn: Chia 2 cột trong suốt (transparent)
    items_cover = [
        ("Sinh viên thực hiện:", "Lâm Quang Huy"),
        ("Mã số sinh viên:", "0212267"),
        ("Lớp / Khóa:", "67CS - Khóa 67"),
        ("Ngành đào tạo:", "Công nghệ Thông tin (Khoa học Máy tính)"),
        ("Giảng viên hướng dẫn:", "ThS. Lê Văn Minh"),
        ("Đơn vị thực tập (ĐVHD):", "CÔNG TY TNHH AMAZON WEB SERVICES VIỆT NAM"),
        ("Người phụ trách tại ĐVHD:", "Nguyễn Gia Hưng"),
        ("Cán bộ hướng dẫn tại ĐVHD:", "Phạm Văn Phóng (Technical Mentor, AWS Vietnam)"),
        ("Thời gian thực tập:", "03/08/2026 – 25/10/2026 (12 tuần)")
    ]

    tbl_cover = doc.add_table(rows=len(items_cover), cols=2)
    tbl_cover.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_cover.autofit = False
    set_transparent_borders(tbl_cover)

    col_w_cover = [Cm(6.0), Cm(9.5)]
    for r_idx, (lbl, val) in enumerate(items_cover):
        row = tbl_cover.rows[r_idx]
        row.cells[0].width = col_w_cover[0]
        row.cells[1].width = col_w_cover[1]

        p0 = row.cells[0].paragraphs[0]
        p0.paragraph_format.line_spacing = 1.15
        p0.paragraph_format.space_before = Pt(2)
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(lbl)
        r0.bold = True
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(11.5)
        r0.font.color.rgb = RGBColor(0, 0, 0)

        p1 = row.cells[1].paragraphs[0]
        p1.paragraph_format.line_spacing = 1.15
        p1.paragraph_format.space_before = Pt(2)
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(val)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = RGBColor(0, 0, 0)
        if r_idx in [0, 4, 5, 7]:
            r1.bold = True

    p_bottom = doc.add_paragraph()
    p_bottom.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bottom.paragraph_format.space_before = Pt(14)
    p_bottom.paragraph_format.space_after = Pt(0)
    r_b = p_bottom.add_run("HÀ NỘI – NĂM 2026")
    r_b.bold = True
    r_b.font.size = Pt(13)
    r_b.font.name = "Times New Roman"
    r_b.font.color.rgb = RGBColor(0, 0, 0)

    doc.add_page_break()

    # =========================================================================
    # BẢNG THÔNG TIN SINH VIÊN VÀ ĐƠN VỊ THỰC TẬP (MẪU TTTN-06)
    # =========================================================================
    p_hd = doc.add_paragraph()
    p_hd.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_hd.paragraph_format.line_spacing = 1.2
    p_hd.paragraph_format.space_before = Pt(8)
    p_hd.paragraph_format.space_after = Pt(4)
    add_bookmark(p_hd, "info_tttn06")
    add_bookmark(p_hd, "tbl1")

    r = p_hd.add_run("Mẫu TTTN-06\n")
    r.bold = True
    r.font.size = Pt(12)
    r.font.name = "Times New Roman"
    r.font.color.rgb = RGBColor(0, 0, 0)

    r = p_hd.add_run("(Ban hành kèm theo Quy định tổ chức và Đánh giá Thực tập tốt nghiệp Trường Đại học Xây dựng Hà Nội)\n\n")
    r.font.italic = True
    r.font.size = Pt(11)
    r.font.name = "Times New Roman"
    r.font.color.rgb = RGBColor(0, 0, 0)

    r = p_hd.add_run("THÔNG TIN SINH VIÊN VÀ ĐƠN VỊ THỰC TẬP\nBÁO CÁO THỰC TẬP TỐT NGHIỆP CỦA SINH VIÊN")
    r.bold = True
    r.font.size = Pt(15)
    r.font.name = "Times New Roman"
    r.font.color.rgb = RGBColor(0, 0, 0)

    table_info = doc.add_table(rows=12, cols=4)
    table_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_info.autofit = False
    set_table_borders(table_info, color="000000", sz="4")
    make_table_robust(table_info)

    col_widths_1 = [Cm(4.0), Cm(5.0), Cm(3.2), Cm(3.8)]

    info_rows = [
        [("Họ và tên sinh viên:", True), ("Lâm Quang Huy", False), ("Mã số sinh viên:", True), ("0212267", False)],
        [("Lớp / Khóa:", True), ("67CS (Khóa 67)", False), ("Khoa / Viện:", True), ("Công nghệ Thông tin", False)],
        [("Ngành đào tạo:", True), ("Công nghệ Thông tin", False), ("Hệ đào tạo:", True), ("Chính quy", False)],
        [("Đơn vị hướng dẫn (ĐVHD):", True), ("CÔNG TY TNHH AMAZON WEB SERVICES VIỆT NAM", False, 3)],
        [("Địa chỉ trụ sở ĐVHD:", True), ("Tầng 36 Tòa nhà Bitexco Financial Tower, Số 2 Hải Triều, P. Bến Nghé, Q.1, TP. Hồ Chí Minh", False, 3)],
        [("Địa chỉ văn phòng thực tập:", True), ("Tầng 7, Tòa nhà Grand Terra, Số 36 Cát Linh, P. Ô Chợ Dừa, Q. Đống Đa, TP. Hà Nội", False, 3)],
        [("Thời gian thực tập:", True), ("Từ ngày 03/08/2026 đến ngày 25/10/2026 (Thời lượng: 12 tuần liên tục)", False, 3)],
        [("Giảng viên hướng dẫn (GVHD):", True), ("ThS. Lê Văn Minh (Bộ môn Khoa học Máy tính - Khoa CNTT - HUCE)", False, 3)],
        [("Người phụ trách (ĐVHD):", True), ("Nguyễn Gia Hưng (Email: hunggia@amazon.com.vn | SĐT: +841277870645)", False, 3)],
        [("Cán bộ hướng dẫn tại ĐVHD:", True), ("Phạm Văn Phóng (Technical Mentor, AWS Vietnam)", False, 3)],
        [("Phương thức thực tập:", True), ("Trực tiếp (On-site tại VP AWS Hà Nội) kết hợp Hands-on Cloud Sandbox", False, 3)],
        [("Hình thức thực tập:", True), ("Thực tập tốt nghiệp cuối khóa (Học phần bắt buộc tốt nghiệp Kỹ sư CNTT)", False, 3)],
    ]

    for r_idx, r_data in enumerate(info_rows):
        row = table_info.rows[r_idx]
        c_idx = 0
        for item in r_data:
            lbl, is_bold = item[0], item[1]
            span = item[2] if len(item) > 2 else 1
            cell = row.cells[c_idx]
            if span > 1:
                cell = row.cells[c_idx]
                for s in range(1, span):
                    cell.merge(row.cells[c_idx + s])
            cell.text = lbl
            set_cell_shading(cell, "FFFFFF")
            p_c = cell.paragraphs[0]
            p_c.paragraph_format.line_spacing = 1.15
            p_c.paragraph_format.space_before = Pt(2)
            p_c.paragraph_format.space_after = Pt(2)
            for run_c in p_c.runs:
                run_c.font.name = "Times New Roman"
                run_c.font.size = Pt(11)
                run_c.font.color.rgb = RGBColor(0, 0, 0)
                run_c.bold = is_bold
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            c_idx += span

    for row in table_info.rows:
        for idx, width in enumerate(col_widths_1):
            row.cells[idx].width = width

    doc.add_page_break()

    # =========================================================================
    # LỜI CẢM ƠN
    # =========================================================================
    p_ack = doc.add_paragraph()
    p_ack.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ack.paragraph_format.space_before = Pt(8)
    p_ack.paragraph_format.space_after = Pt(8)
    add_bookmark(p_ack, "ack")
    r = p_ack.add_run("LỜI CẢM ƠN")
    r.bold = True
    r.font.size = Pt(16)
    r.font.name = "Times New Roman"
    r.font.color.rgb = RGBColor(0, 0, 0)

    def add_ack_body(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2.5)
        p.paragraph_format.first_line_indent = Cm(0.8)
        r_text = p.add_run(text)
        r_text.font.name = "Times New Roman"
        r_text.font.size = Pt(12)
        r_text.font.color.rgb = RGBColor(0, 0, 0)
        return p

    add_ack_body("Lời đầu tiên, em xin bày tỏ lòng biết ơn sâu sắc nhất tới Ban Giám hiệu Trường Đại học Xây dựng Hà Nội (HUCE), Ban Chủ nhiệm Khoa Công nghệ Thông tin cùng toàn thể quý thầy cô giáo đã tận tình giảng dạy, trang bị cho em nền tảng kiến thức khoa học máy tính và kỹ nghệ phần mềm vững vàng trong suốt những năm tháng học tập tại giảng đường đại học.")
    add_ack_body("Đặc biệt, em xin gửi lời cảm ơn chân thành nhất tới ThS. Lê Văn Minh – Giảng viên hướng dẫn trực tiếp của em. Thầy đã luôn theo sát, định hướng chuyên môn sâu sắc, tận tâm đóng góp những ý kiến quý báu và tạo mọi điều kiện thuận lợi nhất để em nghiên cứu và hoàn thành xuất sắc học phần Thực tập tốt nghiệp này.")
    add_ack_body("Em xin trân trọng gửi lời cảm ơn sâu sắc tới Ban Lãnh đạo CÔNG TY TNHH AMAZON WEB SERVICES VIỆT NAM (AWS Việt Nam) cùng Ban Điều phối chương trình First Cloud AI Journey (FCAJ) Workforce Bootcamp 2026. Cảm ơn công ty đã tiếp nhận, tài trợ hạ tầng đám mây thực hành chuyên nghiệp và mang lại cho em một môi trường rèn luyện thực chiến đẳng cấp quốc tế theo văn hóa Day 1 của Amazon.")
    add_ack_body("Em xin gửi lời cảm ơn đặc biệt tới anh Nguyễn Gia Hưng – Người phụ trách tại ĐVHD, cùng anh Phạm Văn Phóng – Cán bộ hướng dẫn kỹ thuật trực tiếp tại AWS Việt Nam, và các chuyên gia giải pháp của cộng đồng AWS Study Group Vietnam. Các anh đã không quản ngại thời gian định hướng tư duy thiết kế kiến trúc chuẩn AWS Well-Architected Framework, hướng dẫn em phương pháp phân tích log hệ thống từ nguyên nhân gốc rễ (Root Cause Analysis), và hỗ trợ giải quyết các nút thắt kỹ thuật phức tạp trong quá trình triển khai nền tảng Serverless Hybrid Document OCR.")
    add_ack_body("Mặc dù em đã nỗ lực tối đa trong việc nghiên cứu và áp dụng những công nghệ đám mây hiện đại nhất vào đồ án, song do kiến thức và kinh nghiệm thực tế còn trong quá trình tích lũy, bản báo cáo khó tránh khỏi những hạn chế nhất định. Em rất mong nhận được những ý kiến đóng góp, chỉ dẫn quý báu từ quý thầy cô giáo trong Hội đồng chấm thi và các chuyên gia kỹ thuật để sản phẩm ngày càng được hoàn thiện hơn.")
    add_ack_body("Em xin kính chúc quý thầy cô giáo Trường Đại học Xây dựng Hà Nội cùng toàn thể các anh chị cán bộ tại AWS Việt Nam luôn dồi dào sức khỏe, hạnh phúc và gặt hái được nhiều thành công rực rỡ trong sự nghiệp giáo dục cũng như phát triển công nghệ cao!")

    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sign.paragraph_format.space_before = Pt(8)
    p_sign.paragraph_format.space_after = Pt(0)
    p_sign.paragraph_format.line_spacing = 1.15
    r_s = p_sign.add_run("Hà Nội, ngày 25 tháng 10 năm 2026\nSinh viên thực hiện\n\n\n")
    r_s.font.size = Pt(12)
    r_s.font.italic = True
    r_s.font.name = "Times New Roman"
    r_s.font.color.rgb = RGBColor(0, 0, 0)

    r_name = p_sign.add_run("Lâm Quang Huy")
    r_name.bold = True
    r_name.font.size = Pt(13)
    r_name.font.name = "Times New Roman"
    r_name.font.color.rgb = RGBColor(0, 0, 0)

    doc.add_page_break()

    # =========================================================================
    # MỤC LỤC (BẤM VÀO ĐƯỢC - CLICKABLE INTERNAL HYPERLINKS)
    # =========================================================================
    p_toc_title = doc.add_paragraph()
    p_toc_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc_title.paragraph_format.space_before = Pt(14)
    p_toc_title.paragraph_format.space_after = Pt(12)
    add_bookmark(p_toc_title, "toc")
    r = p_toc_title.add_run("MỤC LỤC")
    r.bold = True
    r.font.size = Pt(16)
    r.font.name = "Times New Roman"
    r.font.color.rgb = RGBColor(0, 0, 0)

    toc_items = [
        ("THÔNG TIN SINH VIÊN VÀ ĐƠN VỊ THỰC TẬP (MẪU TTTN-06)", "2"),
        ("LỜI CẢM ƠN", "3"),
        ("MỤC LỤC", "4"),
        ("DANH MỤC CÁC TỪ VIẾT TẮT", "6"),
        ("DANH MỤC HÌNH VẼ", "7"),
        ("DANH MỤC BẢNG BIỂU", "8"),
        ("PHẦN 1: GIỚI THIỆU CHUNG VỀ ĐƠN VỊ THỰC TẬP", "9"),
        ("  1.1. Lịch sử hình thành và vị thế toàn cầu của Amazon Web Services (AWS)", "9"),
        ("  1.2. Pháp nhân và cơ cấu tổ chức của AWS tại Việt Nam", "9"),
        ("  1.3. Lĩnh vực hoạt động và vai trò trong Chuyển đổi số Quốc gia", "10"),
        ("  1.4. Chương trình Đào tạo & Ươm mầm First Cloud AI Journey (FCAJ)", "11"),
        ("  1.5. Văn hóa doanh nghiệp và Bộ 16 Nguyên tắc Lãnh đạo của Amazon", "12"),
        ("PHẦN 2: MỤC TIÊU VÀ KẾ HOẠCH THỰC TẬP", "14"),
        ("  2.1. Mục tiêu học tập cá nhân gắn liền với Chuẩn đầu ra (CLOs)", "14"),
        ("  2.2. Kế hoạch công việc chi tiết qua 12 tuần thực tập", "15"),
        ("  2.3. Bảng phân công nhiệm vụ và chỉ số đo lường hiệu quả (KPIs)", "17"),
        ("PHẦN 3: NỘI DUNG VÀ KẾT QUẢ THỰC TẬP (TRỌNG TÂM KỸ THUẬT)", "18"),
        ("  3.1. Tổng quan Nhiệm vụ Kỹ thuật và Đề tài Capstone Hybrid OCR", "18"),
        ("  3.2. Thiết kế và Triển khai Hạ tầng Đám mây AWS Zero-Trust", "19"),
        ("    3.2.1. Mạng ảo tùy biến Amazon VPC Multi-AZ độ sẵn sàng cao", "20"),
        ("    3.2.2. Ma trận Tường lửa Trạng thái Chaining (Defense-in-Depth)", "21"),
        ("    3.2.3. Quản trị máy chủ Zero Trust và Quản lý bí mật với AWS Systems Manager", "22"),
        ("    3.2.4. Lưu trữ đối tượng Amazon S3 & Cơ sở dữ liệu NoSQL Amazon DynamoDB", "23"),
        ("    3.2.5. Cân bằng tải Application Load Balancer và Máy chủ ứng dụng EC2", "24"),
        ("    3.2.6. Kiến trúc phi máy chủ hướng sự kiện Event-Driven Serverless Pipeline", "25"),
        ("  3.3. Xây dựng và Hoàn thiện Động cơ Ứng dụng Lõi", "27"),
        ("    3.3.1. Tầng 1 - Fast-Path Native Parser (PyMuPDF trích xuất vector)", "28"),
        ("    3.3.2. Tầng 2 - Vision Multimodal OCR & Cơ chế Tự phục hồi (Failover)", "28"),
        ("    3.3.3. Động cơ Dịch thuật Kỹ thuật (DocumentTranslator)", "28"),
        ("    3.3.4. Bộ Xuất bản Đa định dạng (Multi-Format Exporters: MD, DOCX, PDF)", "28"),
        ("    3.3.5. Giao diện Web Studio SPA (Zero-Flicker) & Bảng điều khiển Tour Xoay Key", "29"),
        ("    3.3.6. Bảng Ánh xạ Toàn diện Module Hệ thống sang Dịch vụ Đám mây AWS", "30"),
        ("  3.4. Kiểm thử Toàn trình, Đánh giá Hiệu năng (Benchmark) & FinOps", "31"),
        ("    3.4.1. Kịch bản kiểm thử toàn trình End-to-End trên môi trường thực tế", "31"),
        ("    3.4.2. Bảng số liệu đo kiểm thực nghiệm Benchmark", "31"),
        ("    3.4.3. Quản trị chi phí và kỷ luật tài chính FinOps (Zero-Breach)", "31"),
        ("  3.5. Giám sát Vận hành & Cảnh báo Sự cố với Amazon CloudWatch", "32"),
        ("PHẦN 4: PHÂN TÍCH, ĐÁNH GIÁ VÀ ĐỀ XUẤT", "33"),
        ("  4.1. Nhận xét về Quy trình Công việc và Giải pháp Kỹ thuật Đã Triển Khai", "33"),
        ("  4.2. Các Khó khăn, Thách thức Thực tế và Giải pháp Khắc phục", "33"),
        ("  4.3. Phân tích Mối liên hệ Biện chứng Giữa Lý thuyết và Thực tế", "34"),
        ("  4.4. Đề xuất Cải tiến Quy trình và Giải pháp Kỹ thuật Mở rộng", "35"),
        ("PHẦN 5: TỰ NHẬN XÉT VÀ ĐỊNH HƯỚNG NGHỀ NGHIỆP CÁ NHÂN", "36"),
        ("  5.1. Tự đánh giá Năng lực Cá nhân theo Chuẩn Đào tạo Kỹ sư CNTT", "36"),
        ("  5.2. Điểm mạnh và Điểm còn Hạn chế Cần Tiếp tục Hoàn thiện", "37"),
        ("  5.3. Bài học Kinh nghiệm Thực tiễn Rút ra từ Môi trường AWS", "37"),
        ("  5.4. Lộ trình Phát triển Nghề nghiệp trong Lĩnh vực Cloud / Solutions Architect", "38"),
        ("PHẦN 6: KẾT LUẬN VÀ KIẾN NGHỊ", "39"),
        ("  6.1. Kết luận và Tổng kết Các Bài học Kinh nghiệm Quý báu", "39"),
        ("  6.2. Kiến nghị Đối với Nhà trường (Trường ĐH Xây dựng Hà Nội - HUCE)", "39"),
        ("  6.3. Kiến nghị Đối với Đơn vị Hướng dẫn (AWS Việt Nam)", "40"),
        ("TÀI LIỆU THAM KHẢO", "41"),
        ("XÁC NHẬN HOÀN THÀNH THỰC TẬP TỐT NGHIỆP (MẪU TTTN-06)", "42")
    ]

    for item, pg in toc_items:
        bm_name = get_bookmark_name(item)
        is_bold = not item.startswith("  ")
        add_hyperlink_tab_entry(doc, item, pg, bm_name if bm_name else "toc", is_bold=is_bold)

    doc.add_page_break()

    # =========================================================================
    # DANH MỤC CÁC TỪ VIẾT TẮT
    # =========================================================================
    p_abb = doc.add_paragraph()
    p_abb.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abb.paragraph_format.space_before = Pt(8)
    p_abb.paragraph_format.space_after = Pt(6)
    add_bookmark(p_abb, "abbreviations")
    add_bookmark(p_abb, "tbl2")
    r = p_abb.add_run("DANH MỤC CÁC TỪ VIẾT TẮT")
    r.bold = True
    r.font.size = Pt(15)
    r.font.name = "Times New Roman"
    r.font.color.rgb = RGBColor(0, 0, 0)

    table_abb = doc.add_table(rows=18, cols=3)
    table_abb.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_abb.autofit = False
    set_table_borders(table_abb, color="000000", sz="4")
    make_table_robust(table_abb)

    abb_widths = [Cm(2.6), Cm(6.4), Cm(7.0)]
    headers_abb = ["Từ viết tắt", "Tên tiếng Anh đầy đủ", "Ý nghĩa / Định nghĩa kỹ thuật"]
    for c_idx, h_text in enumerate(headers_abb):
        cell = table_abb.rows[0].cells[c_idx]
        cell.text = h_text
        set_cell_shading(cell, "FFFFFF")
        set_cell_margins(cell, top=40, bottom=40, left=80, right=80)
        p = cell.paragraphs[0]
        p.runs[0].bold = True
        p.runs[0].font.name = "Times New Roman"
        p.runs[0].font.size = Pt(10)
        p.runs[0].font.color.rgb = RGBColor(0, 0, 0)

    abbreviations = [
        ("AWS", "Amazon Web Services", "Nền tảng điện toán đám mây toàn diện của Amazon"),
        ("ALB", "Application Load Balancer", "Bộ cân bằng tải ứng dụng lớp 7 định tuyến HTTP/HTTPS"),
        ("API", "Application Programming Interface", "Giao diện lập trình ứng dụng kết nối dịch vụ"),
        ("CIDR", "Classless Inter-Domain Routing", "Phương pháp định tuyến và phân dải địa chỉ IP mạng"),
        ("CLI", "Command Line Interface", "Giao diện dòng lệnh thực thi tác vụ quản trị"),
        ("CLO", "Course Learning Outcome", "Chuẩn đầu ra của học phần đào tạo đại học"),
        ("CPU", "Central Processing Unit", "Bộ vi xử lý trung tâm của máy chủ tính toán"),
        ("DynamoDB", "Amazon DynamoDB", "Dịch vụ cơ sở dữ liệu NoSQL phi máy chủ hiệu năng cao"),
        ("EC2", "Amazon Elastic Compute Cloud", "Dịch vụ cung cấp máy chủ ảo có thể thay đổi quy mô"),
        ("FinOps", "Cloud Financial Operations", "Văn hóa quản trị và tối ưu hóa chi phí đám mây"),
        ("IAM", "Identity and Access Management", "Dịch vụ quản lý định danh và phân quyền truy cập"),
        ("IGW", "Internet Gateway", "Cổng kết nối Internet cho mạng ảo đám mây VPC"),
        ("Lambda", "AWS Lambda", "Nền tảng điện toán phi máy chủ (Serverless Compute)"),
        ("Multi-AZ", "Multiple Availability Zones", "Kiến trúc triển khai trải rộng trên nhiều vùng sẵn sàng"),
        ("OCR", "Optical Character Recognition", "Công nghệ nhận dạng ký tự quang học từ tài liệu ảnh"),
        ("S3", "Amazon Simple Storage Service", "Dịch vụ lưu trữ đối tượng đám mây độ bền 99.999999999%"),
        ("SSM", "AWS Systems Manager", "Bộ công cụ quản trị máy chủ từ xa chuẩn Zero-Trust")
    ]

    for r_idx, (abb, en, vi) in enumerate(abbreviations):
        row = table_abb.rows[r_idx + 1]
        for c_idx, val in enumerate([abb, en, vi]):
            cell = row.cells[c_idx]
            cell.text = val
            set_cell_shading(cell, "FFFFFF")
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(1)
            if c_idx == 0:
                p.runs[0].bold = True
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(9.5)
            p.runs[0].font.color.rgb = RGBColor(0, 0, 0)
            set_cell_margins(cell, top=25, bottom=25, left=60, right=60)

    for row in table_abb.rows:
        for idx, width in enumerate(abb_widths):
            row.cells[idx].width = width

    doc.add_page_break()

    # =========================================================================
    # DANH MỤC HÌNH VẼ (BẤM VÀO ĐƯỢC - CLICKABLE TO FIGURES)
    # =========================================================================
    p_fig = doc.add_paragraph()
    p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_fig.paragraph_format.space_before = Pt(14)
    p_fig.paragraph_format.space_after = Pt(12)
    add_bookmark(p_fig, "fig_list")
    r = p_fig.add_run("DANH MỤC HÌNH VẼ")
    r.bold = True
    r.font.size = Pt(16)
    r.font.name = "Times New Roman"
    r.font.color.rgb = RGBColor(0, 0, 0)

    figures_list = [
        ("Hình 3.1: Sơ đồ kiến trúc tổng thể hệ thống Serverless Hybrid Document OCR trên AWS", "19"),
        ("Hình 3.2: Sơ đồ luồng phân tầng bóc tách Hybrid OCR Engine (Fast-Path Native & Vision LLM)", "19"),
        ("Hình 3.3: Sơ đồ kiến trúc mạng ảo Amazon VPC Multi-AZ phân tách Subnet độ sẵn sàng cao", "20"),
        ("Hình 3.4: Sơ đồ phân bổ tài nguyên VPC Resource Map thực tế trên AWS Management Console", "21"),
        ("Hình 3.5: Mô hình ma trận an ninh phân tầng Security Group Chaining cô lập máy chủ EC2", "22"),
        ("Hình 3.6: Cấu hình tham số bảo mật và khóa hệ thống trên AWS Systems Manager Parameter Store", "23"),
        ("Hình 3.7: Cấu hình lưu trữ tệp trên Amazon S3 phân tách thư mục uploads/ và outputs/", "24"),
        ("Hình 3.8: Bảng dữ liệu NoSQL Amazon DynamoDB (document_processing_jobs) ở trạng thái Active", "24"),
        ("Hình 3.9: Kiểm chứng trạng thái Healthy (1/1) của Target Group trên Application Load Balancer", "25"),
        ("Hình 3.10: Sơ đồ kiến trúc xử lý phi máy chủ hướng sự kiện Event-Driven Serverless Pipeline", "26"),
        ("Hình 3.11: Mã nguồn hàm AWS Lambda (huylam-ocr-processor) triển khai thành công trên AWS", "27"),
        ("Hình 3.12: Bảng Amazon DynamoDB tự động tiếp nhận bản ghi sự kiện xử lý tài liệu từ S3 Event", "27"),
        ("Hình 3.13: Giao diện ứng dụng Web Studio vận hành trực tiếp trên AWS qua Application Load Balancer", "29"),
        ("Hình 3.14: Kết quả bóc tách và dịch thuật tài liệu kỹ thuật trên giao diện Web Studio", "30"),
        ("Hình 3.15: Kiểm chứng tài liệu Microsoft Word (.docx) được kết xuất tự động chuẩn trang in A4", "30"),
        ("Hình 3.16: Bảng điều khiển giám sát hệ thống thời gian thực trên Amazon CloudWatch Dashboard", "32")
    ]

    for item, pg in figures_list:
        bm_name = get_bookmark_name(item)
        add_hyperlink_tab_entry(doc, item, pg, bm_name if bm_name else "fig_list", is_bold=False)

    doc.add_page_break()

    # =========================================================================
    # DANH MỤC BẢNG BIỂU (BẤM VÀO ĐƯỢC - CLICKABLE TO TABLES)
    # =========================================================================
    p_tbl = doc.add_paragraph()
    p_tbl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tbl.paragraph_format.space_before = Pt(14)
    p_tbl.paragraph_format.space_after = Pt(12)
    add_bookmark(p_tbl, "tbl_list")
    r = p_tbl.add_run("DANH MỤC BẢNG BIỂU")
    r.bold = True
    r.font.size = Pt(16)
    r.font.name = "Times New Roman"
    r.font.color.rgb = RGBColor(0, 0, 0)

    tables_list = [
        ("Bảng 1: Thông tin sinh viên và Đơn vị thực tập (Mẫu quy chuẩn TTTN-06)", "2"),
        ("Bảng 2: Danh mục các từ viết tắt kỹ thuật chuyên ngành", "6"),
        ("Bảng 2.1: Mục tiêu học tập cá nhân đối chiếu với Chuẩn đầu ra (CLOs) của học phần", "14"),
        ("Bảng 2.2: Kế hoạch làm việc và kết quả mong đợi chi tiết qua 12 tuần thực tập (TTTN-02)", "15"),
        ("Bảng 2.3: Bảng chỉ số đo lường hiệu quả công việc cá nhân (KPIs)", "17"),
        ("Bảng 3.1: Bảng thông số cấu hình hạ tầng mạng Amazon VPC Multi-AZ", "21"),
        ("Bảng 3.2: Ma trận cấu hình tường lửa trạng thái Security Groups phân tầng", "22"),
        ("Bảng 3.3: Bảng ánh xạ toàn diện module mã nguồn hệ thống sang dịch vụ đám mây AWS", "30"),
        ("Bảng 3.4: Bảng số liệu đo kiểm thực nghiệm Benchmark hiệu năng và độ trễ", "31"),
        ("Bảng 5.1: Bảng tự đánh giá năng lực cá nhân theo 10 chuẩn đầu ra chuyên môn", "36"),
        ("Bảng 12: Khung xác nhận hoàn thành thực tập tốt nghiệp (Mẫu TTTN-06)", "42")
    ]

    for item, pg in tables_list:
        bm_name = get_bookmark_name(item)
        add_hyperlink_tab_entry(doc, item, pg, bm_name if bm_name else "tbl_list", is_bold=False)

    doc.add_page_break()

    # =========================================================================
    # LẮP RÁP CÁC PHẦN 1 ĐẾN 6
    # =========================================================================
    print("Đang biên soạn Phần 1...")
    add_part1(doc, add_h1, add_h2, add_h3, add_body, add_bullet, add_figure)

    doc.add_page_break()
    print("Đang biên soạn Phần 2...")
    add_part2(doc, add_h1, add_h2, add_h3, add_body, add_bullet, add_figure)

    doc.add_page_break()
    print("Đang biên soạn Phần 3...")
    add_part3(doc, add_h1, add_h2, add_h3, add_body, add_bullet, add_figure)

    doc.add_page_break()
    print("Đang biên soạn Phần 4...")
    add_part4(doc, add_h1, add_h2, add_h3, add_body, add_bullet, add_figure)

    doc.add_page_break()
    print("Đang biên soạn Phần 5...")
    add_part5(doc, add_h1, add_h2, add_h3, add_body, add_bullet, add_figure)

    doc.add_page_break()
    print("Đang biên soạn Phần 6...")
    add_part6(doc, add_h1, add_h2, add_h3, add_body, add_bullet, add_figure)

    # Lưu tệp hoàn chỉnh
    output_path = os.path.join(PROJECT_ROOT, "bao cao tot nghiep", "Baocao.docx")
    print(f"Đang lưu tệp hoàn chỉnh tới: {output_path}...")
    doc.save(output_path)
    print("=" * 70)
    print("XUẤT BẢN THÀNH CÔNG BÁO CÁO THỰC TẬP TỐT NGHIỆP HUCE!")
    print(f"Đường dẫn: {output_path}")
    print("=" * 70)

if __name__ == "__main__":
    build_complete_report()
