#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Điền thông tin, điểm đánh giá CLO và minh chứng vào biểu mẫu TTTN-08b
(Phiếu phản hồi của sinh viên - Đánh giá TTTN Trường Đại học Xây dựng Hà Nội)
Sinh viên: Lâm Quang Huy - MSSV: 0212267 - Lớp: 67CS
Đơn vị thực tập: Chi nhánh Công ty TNHH Amazon Web Services Việt Nam tại TP Hà Nội
Định dạng: Chuẩn học thuật Monochrome Academic Style, đúng 3 trang tròn trịa, không tràn dòng.
"""

import os
import shutil
import docx
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=40, bottom=40, left=80, right=80):
    """Thiết lập padding lề cho ô trong bảng (đơn vị dxa: 20 dxa = 1 pt)."""
    tcPr = cell._tc.get_or_add_tcPr()
    old_tcMar = tcPr.find(qn('w:tcMar'))
    if old_tcMar is not None:
        tcPr.remove(old_tcMar)
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex="FFFFFF"):
    """Tô nền ô."""
    tcPr = cell._tc.get_or_add_tcPr()
    old_shd = tcPr.find(qn('w:shd'))
    if old_shd is not None:
        tcPr.remove(old_shd)
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def set_table_borders(table, color="000000", sz="4"):
    """Thiết lập đường viền bảng đen trang trọng."""
    tblPr = table._tbl.tblPr
    old_borders = tblPr.find(qn('w:tblBorders'))
    if old_borders is not None:
        tblPr.remove(old_borders)
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def set_table_col_widths(table, col_widths_cm):
    """Thiết lập độ rộng cột chuẩn xác bằng XML."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    total_dxa = int(sum(col_widths_cm) * 567)
    tblPr = table._tbl.tblPr
    old_tblW = tblPr.find(qn('w:tblW'))
    if old_tblW is not None:
        tblPr.remove(old_tblW)
    tblW = parse_xml(f'<w:tblW {nsdecls("w")} w:w="{total_dxa}" w:type="dxa"/>')
    tblPr.append(tblW)

    for row in table.rows:
        trPr = row._tr.get_or_add_trPr()
        if trPr.find(qn('w:cantSplit')) is None:
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
            
        for idx, width_cm in enumerate(col_widths_cm):
            cell = row.cells[idx]
            cell_dxa = int(width_cm * 567)
            tcPr = cell._tc.get_or_add_tcPr()
            old_tcW = tcPr.find(qn('w:tcW'))
            if old_tcW is not None:
                tcPr.remove(old_tcW)
            tcW = parse_xml(f'<w:tcW {nsdecls("w")} w:w="{cell_dxa}" w:type="dxa"/>')
            tcPr.append(tcW)

def set_cell_text(cell, text, font_name="Times New Roman", font_size=9.0, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.LEFT, line_spacing=1.05):
    """Điền văn bản vào ô với định dạng chuẩn."""
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_before = Pt(0.5)
    p.paragraph_format.space_after = Pt(0.5)
    
    lines = text.split("\n")
    for idx, line in enumerate(lines):
        if idx > 0:
            p = cell.add_paragraph()
            p.alignment = align
            p.paragraph_format.line_spacing = line_spacing
            p.paragraph_format.space_before = Pt(0.5)
            p.paragraph_format.space_after = Pt(0.5)
        run = p.add_run(line)
        run.font.name = font_name
        run.font.size = Pt(font_size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = RGBColor(0, 0, 0)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

def format_paragraph(p, text, font_name="Times New Roman", font_size=9.5, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=1, space_after=2, line_spacing=1.05):
    """Định dạng đoạn văn."""
    p.text = ""
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    
    lines = text.split("\n")
    for idx, line in enumerate(lines):
        if idx > 0:
            p.add_run("\n")
        run = p.add_run(line)
        run.font.name = font_name
        run.font.size = Pt(font_size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = RGBColor(0, 0, 0)

def set_page_break_before(p):
    """Đặt ngắt trang trước đoạn văn."""
    pPr = p._p.get_or_add_pPr()
    if pPr.find(qn('w:pageBreakBefore')) is None:
        pPr.append(parse_xml(f'<w:pageBreakBefore {nsdecls("w")}/>'))

def fill_tttn_08b(doc_path):
    print(f"Bắt đầu tinh chỉnh tệp: {doc_path}")
    doc = docx.Document(doc_path)
    
    # -------------------------------------------------------------------------
    # 0. BẢNG 0: Thông tin sinh viên (tối ưu lề và font)
    # -------------------------------------------------------------------------
    t0 = doc.tables[0]
    set_table_col_widths(t0, [5.5, 11.0])
    for row in t0.rows:
        for cell in row.cells:
            set_cell_margins(cell, top=30, bottom=30, left=70, right=70)
            for p in cell.paragraphs:
                p.paragraph_format.line_spacing = 1.05
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(9.5)

    # -------------------------------------------------------------------------
    # 1. BẢNG 1: Đánh giá chất lượng đợt thực tập (Mức độ 1-5 & Ghi chú)
    # -------------------------------------------------------------------------
    t1 = doc.tables[1]
    set_table_borders(t1, color="000000", sz="4")
    set_table_col_widths(t1, [6.0, 2.2, 8.3])  # Tổng: 16.5 cm
    
    # Header styling
    for cell in t1.rows[0].cells:
        set_cell_margins(cell, top=50, bottom=50, left=70, right=70)
        set_cell_shading(cell, "F2F2F2")
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(9.0)
                r.font.bold = True

    table1_data = [
        (
            "Sự phù hợp giữa nội dung thực tập và chuyên ngành đào tạo",
            "5",
            "Nội dung thực tập về Điện toán đám mây và Trí tuệ nhân tạo (GenAI/RAG) hoàn toàn phù hợp và phát huy tối đa kiến thức ngành Khoa học máy tính."
        ),
        (
            "Mức độ hỗ trợ từ giảng viên hướng dẫn",
            "5",
            "ThS. Lê Văn Minh định hướng phương pháp luận nghiên cứu khoa học chuẩn mực, theo sát tiến độ qua các mốc CLO và phản hồi báo cáo tỉ mỉ."
        ),
        (
            "Mức độ hỗ trợ và hướng dẫn từ người hướng dẫn tại ĐVHD",
            "5",
            "Anh Phạm Văn Phóng (AWS Việt Nam) hướng dẫn tận tình, chia sẻ kiến trúc hệ thống chuẩn Well-Architected và tạo điều kiện thực hành trên môi trường AWS thực tế."
        ),
        (
            "Điều kiện làm việc và an toàn tại nơi thực tập",
            "5",
            "Môi trường làm việc chuyên nghiệp, trang thiết bị và hạ tầng mạng hiện đại, bảo đảm tuyệt đối quy định an toàn thông tin và văn hóa doanh nghiệp AWS."
        ),
        (
            "Cơ hội học hỏi và phát triển nghề nghiệp",
            "5",
            "Học hỏi toàn diện về các dịch vụ AWS Bedrock, Lambda, DynamoDB, kiến trúc Serverless, quy trình FinOps và mở rộng định hướng trở thành Cloud/AI Architect."
        ),
        (
            "Tính hiệu quả của quy trình đánh giá CLO (4 tuần/lần)",
            "5",
            "Quy trình kiểm tra định kỳ 2 chặng giúp sinh viên lượng hóa năng lực chuẩn đầu ra, kịp thời điều chỉnh kế hoạch và hoàn thành xuất sắc đồ án."
        )
    ]
    
    for row_idx, (crit, score, note) in enumerate(table1_data, start=1):
        set_cell_text(t1.rows[row_idx].cells[0], crit, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell_text(t1.rows[row_idx].cells[1], score, font_size=9.0, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_text(t1.rows[row_idx].cells[2], note, font_size=8.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        for c in t1.rows[row_idx].cells:
            set_cell_margins(c, top=35, bottom=35, left=70, right=70)

    # -------------------------------------------------------------------------
    # 2. ĐOẠN VĂN: Ý kiến khác & Phản hồi mở
    # -------------------------------------------------------------------------
    for p in doc.paragraphs:
        txt = p.text.strip()
        if txt.startswith("Mức 1: Rất không hài lòng"):
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.0
            for r in p.runs:
                r.font.size = Pt(8.0)
                r.font.italic = True
        elif txt.startswith("Các ý kiến khác:"):
            format_paragraph(
                p,
                "Các ý kiến khác: Đợt thực tập tại AWS Việt Nam mang lại trải nghiệm thực tiễn quý báu, giúp sinh viên làm quen với môi trường công nghệ cao chuẩn quốc tế và tự tin ứng dụng kiến thức vào các bài toán thực tế.",
                font_size=9.0,
                space_before=1,
                space_after=1
            )
        elif txt.startswith("2. Phản hồi mở và đề xuất cải tiến"):
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(1)
            for r in p.runs:
                r.font.size = Pt(9.5)
                r.font.bold = True

    # Chèn đoạn văn phản hồi mở vào giữa đề mục 2 và Mục B
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip().startswith("2. Phản hồi mở và đề xuất cải tiến"):
            if i + 1 < len(doc.paragraphs):
                next_p = doc.paragraphs[i+1]
                if next_p.text.strip().startswith("B. BẢNG TỰ ĐÁNH GIÁ CLO"):
                    new_p = next_p.insert_paragraph_before()
                    format_paragraph(
                        new_p,
                        "Khoa CNTT và Nhà trường đã xây dựng quy chế thực tập rất bài bản, phân định rõ chuẩn đầu ra CLO. Đề xuất Khoa tiếp tục mở rộng mạng lưới hợp tác với các doanh nghiệp công nghệ hàng đầu như AWS để tạo thêm nhiều cơ hội thực tập chuyên sâu cho sinh viên các khóa sau.",
                        font_size=9.0,
                        space_before=1,
                        space_after=1
                    )
                elif "Khoa CNTT và Nhà trường" in next_p.text:
                    format_paragraph(
                        next_p,
                        "Khoa CNTT và Nhà trường đã xây dựng quy chế thực tập rất bài bản, phân định rõ chuẩn đầu ra CLO. Đề xuất Khoa tiếp tục mở rộng mạng lưới hợp tác với các doanh nghiệp công nghệ hàng đầu như AWS để tạo thêm nhiều cơ hội thực tập chuyên sâu cho sinh viên các khóa sau.",
                        font_size=9.0,
                        space_before=1,
                        space_after=1
                    )
            break

    # -------------------------------------------------------------------------
    # 3. MỤC B & BẢNG 2: Bắt đầu ở TRANG 2 (Page break before)
    # -------------------------------------------------------------------------
    for p in doc.paragraphs:
        if p.text.strip().startswith("B. BẢNG TỰ ĐÁNH GIÁ CLO"):
            set_page_break_before(p)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(1)
            for r in p.runs:
                r.font.size = Pt(10.5)
                r.font.bold = True
        elif p.text.strip().startswith("Mức độ (0 – 4):"):
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(1)

    t2 = doc.tables[2]
    set_table_borders(t2, color="000000", sz="4")
    set_table_col_widths(t2, [0.8, 1.4, 4.4, 1.8, 8.1])  # Tổng: 16.5 cm
    
    # Header styling
    for cell in t2.rows[0].cells:
        set_cell_margins(cell, top=40, bottom=40, left=50, right=50)
        set_cell_shading(cell, "F2F2F2")
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(8.5)
                r.font.bold = True

    table2_data = [
        (
            "1", "CLO1", "Áp dụng kiến thức chuyên môn vào nhiệm vụ thực tế",
            "4",
            "Thiết kế và triển khai hoàn chỉnh hệ thống AWS Agentic RAG xử lý hồ sơ thầu tự động. Ứng dụng tích hợp pipeline xử lý đa định dạng (PyMuPDF, python-docx), hybrid search và Amazon Bedrock LLM."
        ),
        (
            "2", "CLO2", "Phân tích và giải quyết vấn đề kỹ thuật tại nơi thực tập",
            "4",
            "Phân tích bài toán phân đoạn tài liệu phức tạp, giải quyết triệt để lỗi phân giải token vượt ngưỡng qua kỹ thuật Recursive Token Chunking (overlap 10%), xử lý cold start trên AWS Lambda và tối ưu hiệu năng DynamoDB."
        ),
        (
            "3", "CLO3", "Trình bày, báo cáo, thuyết trình chuyên môn hiệu quả",
            "4",
            "Hoàn thiện Báo cáo tổng kết TTTN 42 trang đúng quy chuẩn kỹ thuật; xây dựng bộ slide bảo vệ chuyên nghiệp 20 trang kèm sơ đồ kiến trúc chuẩn AWS; thuyết trình báo cáo tiến độ tuần và phản biện kỹ thuật rõ ràng."
        ),
        (
            "4", "CLO4", "Tuân thủ đạo đức nghề nghiệp và quy định an toàn lao động",
            "4",
            "Tuân thủ tuyệt đối thỏa thuận bảo mật dữ liệu doanh nghiệp (NDA), áp dụng chuẩn bảo mật AWS IAM Least Privilege, mã hóa dữ liệu tại chỗ (KMS/AES-256) và chấp hành nghiêm nội quy lao động công ty."
        ),
        (
            "5", "CLO5", "Làm việc nhóm, giao tiếp và hợp tác với đồng nghiệp",
            "4",
            "Tương tác chặt chẽ với mentor và đồng nghiệp qua Jira, Slack và standup hàng ngày; phối hợp rà soát mã nguồn (code review) qua Git Pull Request; tích cực hỗ trợ các thành viên trong nhóm dự án."
        ),
        (
            "6", "CLO6", "Sử dụng thành thạo công cụ kỹ thuật, phần mềm chuyên ngành",
            "4",
            "Sử dụng thành thạo hệ sinh thái AWS (Bedrock, Lambda, DynamoDB, S3, IAM, CloudWatch), ngôn ngữ Python, Docker, Postman, Git CLI, kiến trúc hạ tầng dạng mã (IaC CDK/CloudFormation)."
        ),
        (
            "7", "CLO7", "Tự đánh giá năng lực bản thân, xác định định hướng nghề nghiệp",
            "4",
            "Tự đánh giá định kỳ qua nhật ký thực tập 8 tuần; nhận diện rõ điểm mạnh và kỹ năng cần cải thiện; hoàn thành 02 chứng chỉ AWS Certified Cloud Practitioner / Solutions Architect Associate và định hướng làm Cloud/AI Solutions Architect."
        )
    ]
    
    for row_idx, (stt, clo, desc, rating, evidence) in enumerate(table2_data, start=1):
        set_cell_text(t2.rows[row_idx].cells[0], stt, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_text(t2.rows[row_idx].cells[1], clo, font_size=8.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_text(t2.rows[row_idx].cells[2], desc, font_size=8.0, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell_text(t2.rows[row_idx].cells[3], rating, font_size=9.0, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_text(t2.rows[row_idx].cells[4], evidence, font_size=8.0, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        for c in t2.rows[row_idx].cells:
            set_cell_margins(c, top=30, bottom=30, left=60, right=60)

    # Bảng 3: Thang đo 0-4
    t3 = doc.tables[3]
    set_table_borders(t3, color="000000", sz="4")
    set_table_col_widths(t3, [3.3, 3.3, 3.3, 3.3, 3.3])
    for c in t3.rows[0].cells:
        set_cell_margins(c, top=20, bottom=20, left=30, right=30)
        for p in c.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.size = Pt(8.0)

    # -------------------------------------------------------------------------
    # 4. MỤC C: Bắt đầu ở TRANG 3 (Page break before)
    # -------------------------------------------------------------------------
    for p in doc.paragraphs:
        txt = p.text.strip()
        if txt.startswith("C.  NHỮNG TRAO ĐỔI TỰ THÂN"):
            set_page_break_before(p)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(1)
            for r in p.runs:
                r.font.size = Pt(10.5)
                r.font.bold = True
        elif txt.startswith("Những kỹ năng hoặc kiến thức tôi đã học được nhiều nhất"):
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(0.5)
            for r in p.runs:
                r.font.size = Pt(9.0)
                r.font.bold = True
        elif txt.startswith("Những khó khăn hoặc hạn chế tôi gặp phải:"):
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(0.5)
            for r in p.runs:
                r.font.size = Pt(9.0)
                r.font.bold = True
        elif txt.startswith("Kế hoạch cá nhân để cải thiện năng lực chuyên môn hoặc kỹ năng mềm:"):
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(0.5)
            for r in p.runs:
                r.font.size = Pt(9.0)
                r.font.bold = True
        elif txt.startswith("Đề xuất của tôi cho việc cải thiện học phần Thực tập tốt nghiệp:"):
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(0.5)
            for r in p.runs:
                r.font.size = Pt(9.0)
                r.font.bold = True
        elif txt.startswith("D. TỰ TÍNH ĐIỂM TRUNG BÌNH HỌC PHẦN"):
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(1)
            for r in p.runs:
                r.font.size = Pt(10.0)
                r.font.bold = True
        elif txt.startswith("II. CAM KẾT CỦA SINH VIÊN"):
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(0.5)
            for r in p.runs:
                r.font.size = Pt(9.5)
                r.font.bold = True
        elif txt.startswith("Tôi xin cam kết rằng các thông tin"):
            format_paragraph(
                p,
                "Tôi xin cam kết rằng các thông tin, số liệu và minh chứng trong phiếu này là trung thực, phản ánh đúng năng lực và kết quả thực tế trong quá trình thực tập tốt nghiệp. Tôi đồng ý cho phép Nhà trường sử dụng dữ liệu này phục vụ mục đích đánh giá, kiểm định và cải tiến chất lượng đào tạo.",
                font_size=8.0,
                space_before=0.5,
                space_after=1,
                line_spacing=1.0
            )
        elif txt.startswith("III – TỔNG HỢP VÀ LƯU TRỮ"):
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(0.5)
            for r in p.runs:
                r.font.size = Pt(9.5)
                r.font.bold = True
        elif txt.startswith("Ghi chú:") and "CQI" in txt:
            format_paragraph(
                p,
                "Ghi chú: Dữ liệu tự đánh giá được thu thập qua Hệ thống đào tạo và lưu trữ tối thiểu 5 năm tại Khoa. Chỉ số tự nhận thức năng lực (Self-awareness index) phục vụ công tác CQI theo tiêu chuẩn kiểm định AUN-QA và ABET.",
                font_size=7.5,
                italic=True,
                space_before=0.5,
                space_after=1,
                line_spacing=1.0
            )

    # Câu trả lời Section C súc tích
    for i, p in enumerate(doc.paragraphs):
        txt = p.text.strip()
        if txt.startswith("Những kỹ năng hoặc kiến thức tôi đã học được nhiều nhất"):
            if i + 1 < len(doc.paragraphs):
                ans = (
                    "- Kiến thức chuyên sâu về Điện toán đám mây và Generative AI/RAG trên AWS (Bedrock, Lambda, DynamoDB, S3, IAM).\n"
                    "- Kỹ năng thiết kế hệ thống Serverless chịu tải cao, tối ưu chi phí FinOps (0.00 USD Free Tier) và chuẩn Well-Architected.\n"
                    "- Kỹ năng làm việc chuyên nghiệp: quy trình Agile/Scrum, kiểm thử tự động, chuẩn hóa mã nguồn Git và tài liệu kỹ thuật."
                )
                format_paragraph(doc.paragraphs[i+1], ans, font_size=8.0, space_before=0.5, space_after=1, line_spacing=1.0)
        elif txt.startswith("Những khó khăn hoặc hạn chế tôi gặp phải:"):
            if i + 1 < len(doc.paragraphs):
                ans = (
                    "- Thời gian đầu cần làm quen với ma trận phân quyền IAM chi tiết và hạn ngạch tài nguyên (service quotas) của Bedrock LLM.\n"
                    "- Việc xử lý tài liệu thầu phức tạp với nhiều bảng biểu đòi hỏi thử nghiệm nhiều giải pháp chunking. Nhờ sự hỗ trợ kịp thời của mentor doanh nghiệp và GVHD, các khó khăn đều được tháo gỡ triệt để."
                )
                format_paragraph(doc.paragraphs[i+1], ans, font_size=8.0, space_before=0.5, space_after=1, line_spacing=1.0)
        elif txt.startswith("Kế hoạch cá nhân để cải thiện năng lực chuyên môn hoặc kỹ năng mềm:"):
            if i + 1 < len(doc.paragraphs):
                ans = (
                    "- Hoàn thành chứng chỉ chuyên nghiệp AWS Solutions Architect - Associate và hướng tới AWS AI Practitioner trong năm 2026.\n"
                    "- Nghiên cứu sâu về kiến trúc Multi-Agent Systems và tối ưu chi phí vận hành cho mô hình ngôn ngữ lớn (LLM).\n"
                    "- Rèn luyện kỹ năng tiếng Anh chuyên ngành và khả năng thuyết trình, bảo vệ giải pháp kỹ thuật trước hội đồng."
                )
                format_paragraph(doc.paragraphs[i+1], ans, font_size=8.0, space_before=0.5, space_after=1, line_spacing=1.0)
        elif txt.startswith("Đề xuất của tôi cho việc cải thiện học phần Thực tập tốt nghiệp:"):
            if i + 1 < len(doc.paragraphs):
                ans = (
                    "- Đề xuất Khoa tổ chức thêm workshop tiền thực tập nhằm định hướng cho sinh viên về văn hóa doanh nghiệp và quy trình chuẩn công nghiệp.\n"
                    "- Duy trì mô hình theo dõi đánh giá CLO 2 chặng vì mô hình này giúp sinh viên tự định lượng năng lực và cải thiện liên tục."
                )
                format_paragraph(doc.paragraphs[i+1], ans, font_size=8.0, space_before=0.5, space_after=1, line_spacing=1.0)

    # -------------------------------------------------------------------------
    # 5. BẢNG 4: Tự tính điểm trung bình học phần
    # -------------------------------------------------------------------------
    t4 = doc.tables[4]
    set_table_borders(t4, color="000000", sz="4")
    set_table_col_widths(t4, [5.5, 2.5, 2.8, 2.5, 3.2])  # Tổng: 16.5 cm
    
    for r_idx in [0, 1]:
        for cell in t4.rows[r_idx].cells:
            set_cell_margins(cell, top=25, bottom=25, left=40, right=40)
            set_cell_shading(cell, "F2F2F2")
            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(8.0)
                    r.font.bold = True

    clo_scores = [
        ("1", "4", "9.5", "0.20", "1.90"),
        ("2", "4", "9.5", "0.20", "1.90"),
        ("3", "4", "9.0", "0.15", "1.35"),
        ("4", "4", "9.5", "0.10", "0.95"),
        ("5", "4", "9.0", "0.10", "0.90"),
        ("6", "4", "9.5", "0.15", "1.43"),
        ("7", "4", "9.5", "0.10", "0.95")
    ]
    
    for row_idx, (clo_num, rating, score_10, weight, weighted_score) in enumerate(clo_scores, start=2):
        set_cell_text(t4.rows[row_idx].cells[0], clo_num, font_size=8.0, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_text(t4.rows[row_idx].cells[1], rating, font_size=8.0, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_text(t4.rows[row_idx].cells[2], score_10, font_size=8.0, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_text(t4.rows[row_idx].cells[3], weight, font_size=8.0, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_text(t4.rows[row_idx].cells[4], weighted_score, font_size=8.0, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        for c in t4.rows[row_idx].cells:
            set_cell_margins(c, top=20, bottom=20, left=40, right=40)
            
    # Row 9: HPself
    set_cell_text(t4.rows[9].cells[0], "Điểm học phần tự đánh giá (HPself) (5)", font_size=8.0, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT)
    set_cell_text(t4.rows[9].cells[1], "4", font_size=8.0, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(t4.rows[9].cells[2], "", font_size=8.0, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(t4.rows[9].cells[3], "1.00", font_size=8.0, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(t4.rows[9].cells[4], "9.38", font_size=8.0, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    for c in t4.rows[9].cells:
        set_cell_margins(c, top=25, bottom=25, left=40, right=40)
        set_cell_shading(c, "EAEAEA")

    # Ghi chú (1)-(5) dưới Table 4
    for p in doc.paragraphs:
        txt = p.text.strip()
        if any(txt.startswith(k) for k in ["(1) –", "(2) –", "(3) –", "(5) -"]):
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            for r in p.runs:
                r.font.size = Pt(7.0)
                r.font.italic = True

    # -------------------------------------------------------------------------
    # 6. BẢNG 5: Chữ ký sinh viên
    # -------------------------------------------------------------------------
    t5 = doc.tables[5]
    set_table_col_widths(t5, [8.0, 8.5])
    sig_text = "Hà Nội, ngày 28 tháng 09 năm 2026\nSinh viên ký tên\n(Ký và ghi rõ họ tên)\n\nLâm Quang Huy"
    set_cell_text(t5.rows[0].cells[1], sig_text, font_size=9.0, align=WD_ALIGN_PARAGRAPH.CENTER)

    # -------------------------------------------------------------------------
    # 7. BẢNG 6: Người thu thập & Đơn vị
    # -------------------------------------------------------------------------
    t6 = doc.tables[6]
    set_table_borders(t6, color="000000", sz="4")
    set_table_col_widths(t6, [3.8, 5.2, 2.5, 5.0])
    for c in t6.rows[0].cells:
        set_cell_margins(c, top=20, bottom=20, left=30, right=30)
        set_cell_shading(c, "F2F2F2")
        for p in c.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(7.5)
                r.font.bold = True

    set_cell_text(t6.rows[1].cells[0], "Cán bộ phụ trách tập hợp", font_size=7.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(t6.rows[1].cells[1], "Khoa CNTT / CTĐT Khoa học máy tính", font_size=7.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(t6.rows[1].cells[2], "28/09/2026", font_size=7.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_text(t6.rows[1].cells[3], "Hệ thống CSDL đào tạo / Bản giấy", font_size=7.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    for c in t6.rows[1].cells:
        set_cell_margins(c, top=20, bottom=20, left=30, right=30)

    # Lưu tài liệu
    doc.save(doc_path)
    print(f"Hoàn tất tinh chỉnh và lưu tài liệu tại: {doc_path}")

if __name__ == "__main__":
    src_path = "/Users/huylam/Downloads/thuc tap/TTTN-08b-lam-quang-huy.docx"
    fill_tttn_08b(src_path)
