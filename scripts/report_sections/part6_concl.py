# -*- coding: utf-8 -*-
import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from scripts.docx_helpers import (
    set_cell_margins, set_cell_shading, set_table_borders, make_table_robust,
    add_bookmark, add_external_hyperlink
)

def add_part6(doc, add_h1, add_h2, add_h3, add_body, add_bullet, add_figure):
    add_h1("PHẦN 6: KẾT LUẬN VÀ KIẾN NGHỊ")

    add_h2("6.1. Kết luận và Tổng kết Các Bài học Kinh nghiệm Quý báu")
    add_body(
        "Trải qua 12 tuần nỗ lực không ngừng nghỉ tại chương trình AWS First Cloud AI Journey Bootcamp 2026, sinh viên đã hoàn thành xuất sắc "
        "toàn bộ các mục tiêu học tập và nhiệm vụ kỹ thuật được giao. Kỳ thực tập tốt nghiệp không chỉ là một cột mốc quan trọng đánh dấu sự kết thúc "
        "của quãng đời sinh viên tại Trường Đại học Xây dựng Hà Nội, mà còn là bước đệm vững chắc đưa sinh viên bước vào thị trường lao động công nghệ cao [12].",
        indent=True
    )
    add_body(
        "Những thành quả kỹ thuật nổi bật nhất của đề tài tốt nghiệp bao gồm:",
        indent=True
    )
    add_bullet(
        "Nền tảng Serverless Hybrid Document OCR đã chứng minh tính ưu việt "
        "khi kết hợp hài hòa giữa tốc độ trích xuất vector tức thì của Fast-Path Native (PyMuPDF < 0.3s/trang [8]) với sức mạnh thị giác của mô hình AI đa phương thức "
        "(Vision Multimodal LLM [9], [10]), giải quyết bài toán bảo toàn cấu trúc bảng biểu và giảm thiểu 80% chi phí tính toán cho doanh nghiệp.",
        bold_prefix="Nghiên cứu và triển khai thành công mô hình kiến trúc lai tiên phong: "
    )
    add_bullet(
        "Triển khai thành công mạng ảo cô lập Amazon VPC Multi-AZ [2], "
        "ma trận tường lửa phân tầng Security Group Chaining [3], quản trị máy chủ Zero-Trust với AWS Systems Manager [4] và bộ cân bằng tải Application Load Balancer [3] "
        "vận hành ổn định với tên miền DNS thật trên toàn cầu.",
        bold_prefix="Làm chủ và hiện thực hóa hạ tầng đám mây cấp doanh nghiệp chuẩn Well-Architected: "
    )
    add_bullet(
        "Tự động hóa toàn trình quy trình tiếp nhận tệp "
        "từ Amazon S3, kích hoạt hàm AWS Lambda và ghi nhận dữ liệu vào Amazon DynamoDB với độ trễ phản hồi chỉ 214 ms [5], [6].",
        bold_prefix="Tích hợp xuất sắc kiến trúc phi máy chủ hướng sự kiện: "
    )
    add_bullet(
        "Vận hành toàn bộ hệ sinh thái thử nghiệm với chi phí phát sinh duy trì ở mức 0.00 USD, "
        "chứng minh tư duy tối ưu hóa tài nguyên xuất sắc của một Kỹ sư Giải pháp đám mây thực thụ.",
        bold_prefix="Tuyệt đối tuân thủ văn hóa quản trị chi phí FinOps: "
    )

    add_h2("6.2. Kiến nghị Đối với Nhà trường (Trường ĐH Xây dựng Hà Nội - HUCE)")
    add_body(
        "Để giúp các thế hệ sinh viên tiếp theo của Khoa Công nghệ Thông tin tiếp cận nhanh chóng hơn với các yêu cầu thực tiễn của ngành công nghiệp số, "
        "sinh viên xin trân trọng gửi tới Ban Giám hiệu Nhà trường và Ban Chủ nhiệm Khoa một số đề xuất tâm huyết:",
        indent=True
    )
    add_bullet(
        "Đề xuất xem xét đưa các học phần Điện toán đám mây (Cloud Computing), "
        "Ảo hóa Container (Docker/Kubernetes) và Hạ tầng dưới dạng mã nguồn (IaC) thành các môn học chuyên ngành bắt buộc hoặc tự chọn sớm hơn từ năm thứ 3 [12].",
        bold_prefix="Đưa các chuyên đề Điện toán đám mây và Container vào chương trình chính khóa: "
    )
    add_bullet(
        "Mở rộng liên kết với các chương trình như AWS Academy để cấp tài khoản "
        "thực hành đám mây (AWS Cloud Sandbox) có kinh phí tài trợ miễn phí cho sinh viên thực hành trong suốt các môn học chuyên ngành.",
        bold_prefix="Đẩy mạnh hợp tác giáo dục với các chương trình học viện công nghệ: "
    )
    add_bullet(
        "Thường xuyên phát động các cuộc thi thiết kế giải pháp đám mây, "
        "cuộc thi Hackathon và đấu trường Cloud GameDay nhằm kích thích tinh thần tự học và rèn luyện kỹ năng giải quyết sự cố của sinh viên.",
        bold_prefix="Tổ chức thêm các sân chơi học thuật và cuộc thi công nghệ thực chiến: "
    )

    add_h2("6.3. Kiến nghị Đối với Đơn vị Hướng dẫn (AWS Việt Nam)")
    add_body(
        "Sinh viên xin trân trọng gửi tới Ban Lãnh đạo Công ty TNHH Amazon Web Services Việt Nam và Ban Điều phối chương trình First Cloud AI Journey "
        "lời tri ân sâu sắc cùng một số kiến nghị đóng góp:",
        indent=True
    )
    add_bullet(
        "Đây là một chương trình ươm mầm vô cùng thiết thực và giá trị cao. "
        "Kính mong công ty tiếp tục duy trì và mở rộng quy mô chương trình tới nhiều trường đại học khối kỹ thuật hơn nữa trong các năm tiếp theo.",
        bold_prefix="Tiếp tục duy trì và nhân rộng chương trình First Cloud AI Journey (FCAJ): "
    )
    add_bullet(
        "Đề xuất tổ chức thêm các buổi sinh hoạt chuyên môn nhóm nhỏ định kỳ "
        "giữa thực tập sinh và các chuyên gia giải pháp cấp cao (Principal Solutions Architects) để giải đáp các nút thắt kỹ thuật hóc búa.",
        bold_prefix="Tăng cường các buổi giao lưu kỹ thuật chuyên sâu (Deep-Dive Check-in): "
    )
    add_bullet(
        "Tiếp tục là cầu nối uy tín giới thiệu các thực tập sinh xuất sắc tới mạng lưới khách hàng doanh nghiệp "
        "và các đối tác chiến lược của AWS tại Việt Nam.",
        bold_prefix="Hỗ trợ kết nối cơ hội nghề nghiệp: "
    )

    # =========================================================================
    # TÀI LIỆU THAM KHẢO
    # =========================================================================
    doc.add_page_break()
    p_ref = doc.add_paragraph()
    p_ref.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ref.paragraph_format.space_before = Pt(14)
    p_ref.paragraph_format.space_after = Pt(14)
    add_bookmark(p_ref, "references")
    r = p_ref.add_run("TÀI LIỆU THAM KHẢO")
    r.bold = True
    r.font.size = Pt(16)
    r.font.name = "Times New Roman"
    r.font.color.rgb = RGBColor(0, 0, 0)

    references = [
        ("[1]", "Amazon Web Services, 'AWS Well-Architected Framework: Reliability, Security, Operational Excellence and Cost Optimization Pillars', AWS Whitepapers, 2024.", "https://aws.amazon.com/architecture/well-architected/"),
        ("[2]", "Amazon Web Services, 'Amazon Virtual Private Cloud (VPC) User Guide: Multi-AZ Architecture, Subnetting and Route Tables', AWS Documentation, 2024.", "https://docs.aws.amazon.com/vpc/latest/userguide/"),
        ("[3]", "Amazon Web Services, 'Application Load Balancers User Guide: Target Groups, Health Checks and Security Group Chaining', AWS Documentation, 2024.", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/"),
        ("[4]", "Amazon Web Services, 'AWS Systems Manager User Guide: Session Manager, Parameter Store and Run Command', AWS Documentation, 2024.", "https://docs.aws.amazon.com/systems-manager/latest/userguide/"),
        ("[5]", "Amazon Web Services, 'Amazon DynamoDB Developer Guide: Core Components, Partition Keys and On-Demand Capacity Mode', AWS Documentation, 2024.", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/"),
        ("[6]", "Amazon Web Services, 'AWS Lambda Developer Guide: S3 Event Notifications and Serverless Execution Runtime', AWS Documentation, 2024.", "https://docs.aws.amazon.com/lambda/latest/dg/"),
        ("[7]", "Amazon Web Services, 'Amazon CloudWatch User Guide: CloudWatch Logs, Alarms and Monitoring Dashboards', AWS Documentation, 2024.", "https://docs.aws.amazon.com/cloudwatch/latest/monitoring/"),
        ("[8]", "PyMuPDF Development Team, 'PyMuPDF Documentation: Text and Table Extraction from PDF Documents', Artifex Software, 2024.", "https://pymupdf.readthedocs.io/"),
        ("[9]", "Qwen Team, Alibaba Cloud, 'Qwen2.5-VL: High-Resolution Vision-Language Model for Document Understanding and OCR', Technical Report, 2024.", "https://github.com/QwenLM/Qwen2.5-VL"),
        ("[10]", "Google DeepMind, 'Gemini 2.5 Flash API Documentation: Multimodal Vision and Structured Data Extraction', Google Cloud, 2024.", "https://ai.google.dev/gemini-api/docs"),
        ("[11]", "python-docx Authors, 'python-docx: Create and modify Word .docx documents with Python', Official Documentation, 2024.", "https://python-docx.readthedocs.io/"),
        ("[12]", "Trường Đại học Xây dựng Hà Nội, 'Đề cương chi tiết và Quy chuẩn Đánh giá học phần Thực tập Tốt nghiệp Kỹ sư CNTT', Khoa Công nghệ Thông tin, 2024.", "https://fit.huce.edu.vn/")
    ]

    for tag, content, url in references:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.left_indent = Cm(1.2)
        p.paragraph_format.first_line_indent = Cm(-1.2)

        # Người dùng yêu cầu: không cần in đậm cái [1] ở đầu tiêu đề
        r_tag = p.add_run(f"{tag}\t")
        r_tag.bold = False
        r_tag.font.name = "Times New Roman"
        r_tag.font.size = Pt(11.5)
        r_tag.font.color.rgb = RGBColor(0, 0, 0)

        r_text = p.add_run(content + " Đường dẫn: ")
        r_text.font.name = "Times New Roman"
        r_text.font.size = Pt(11.5)
        r_text.font.color.rgb = RGBColor(0, 0, 0)

        # Thêm liên kết mạng URL ngoài có thể bấm được trực tiếp (màu xanh chuẩn học thuật)
        add_external_hyperlink(p, url, url, color="1D4ED8", underline=True)

    # =========================================================================
    # XÁC NHẬN HOÀN THÀNH THỰC TẬP TỐT NGHIỆP (MẪU TTTN-06)
    # =========================================================================
    doc.add_page_break()
    p_cf = doc.add_paragraph()
    p_cf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cf.paragraph_format.space_before = Pt(14)
    p_cf.paragraph_format.space_after = Pt(16)
    add_bookmark(p_cf, "confirmation")
    add_bookmark(p_cf, "tbl12")
    r = p_cf.add_run("IV. XÁC NHẬN HOÀN THÀNH THỰC TẬP TỐT NGHIỆP\n")
    r.bold = True
    r.font.size = Pt(15)
    r.font.name = "Times New Roman"
    r.font.color.rgb = RGBColor(0, 0, 0)
    r = p_cf.add_run("(Theo biểu mẫu quy chuẩn TTTN-06 - Trường Đại học Xây dựng Hà Nội)")
    r.font.italic = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(0, 0, 0)

    table_sign = doc.add_table(rows=1, cols=2)
    table_sign.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_sign.autofit = False
    set_table_borders(table_sign, color="000000", sz="4")
    make_table_robust(table_sign)

    col_widths_sign = [Cm(8.0), Cm(8.0)]
    for row in table_sign.rows:
        for idx, width in enumerate(col_widths_sign):
            row.cells[idx].width = width

    cell_left = table_sign.rows[0].cells[0]
    cell_right = table_sign.rows[0].cells[1]
    set_cell_shading(cell_left, "FFFFFF")
    set_cell_shading(cell_right, "FFFFFF")
    set_cell_margins(cell_left, top=140, bottom=140, left=140, right=140)
    set_cell_margins(cell_right, top=140, bottom=140, left=140, right=140)

    # Cán bộ hướng dẫn ĐVHD
    p_l = cell_left.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_l.paragraph_format.line_spacing = 1.25
    r = p_l.add_run("XÁC NHẬN CỦA CÁN BỘ HƯỚNG DẪN\nTẠI ĐƠN VỊ THỰC TẬP (ĐVHD)\n\n")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)
    r.font.color.rgb = RGBColor(0, 0, 0)
    r = p_l.add_run("Tôi xác nhận sinh viên đã hoàn thành đúng kế hoạch thực tập, tuân thủ quy định và có kết quả đạt yêu cầu.\n\n")
    r.font.italic = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = RGBColor(0, 0, 0)
    r = p_l.add_run("Ký tên, ghi rõ họ tên, đóng dấu\n(nếu có)\n\n\n\n\n\n\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = RGBColor(0, 0, 0)
    r = p_l.add_run("Phạm Văn Phóng\n")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0, 0, 0)
    r = p_l.add_run("Cán bộ hướng dẫn (CBHD) / AWS Vietnam\n(Người phụ trách ĐVHD: Nguyễn Gia Hưng)\nNgày ….… tháng 10 năm 2026")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(0, 0, 0)

    # Giảng viên hướng dẫn HUCE
    p_r = cell_right.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_r.paragraph_format.line_spacing = 1.25
    r = p_r.add_run("XÁC NHẬN CỦA GIẢNG VIÊN HƯỚNG DẪN\nTRƯỜNG ĐH XÂY DỰNG HÀ NỘI\n\n")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)
    r.font.color.rgb = RGBColor(0, 0, 0)
    r = p_r.add_run("Tôi xác nhận báo cáo đạt yêu cầu, đủ điều kiện nộp và chấm điểm học phần.\n\n\n")
    r.font.italic = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = RGBColor(0, 0, 0)
    r = p_r.add_run("Ký tên, ghi rõ họ tên\n\n\n\n\n\n\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = RGBColor(0, 0, 0)
    r = p_r.add_run("ThS. Lê Văn Minh\n")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0, 0, 0)
    r = p_r.add_run("Giảng viên hướng dẫn (GVHD)\nKhoa Công nghệ Thông tin - HUCE\nNgày ……… tháng 10 năm 2026")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(0, 0, 0)

    print("Hoàn thành biên soạn PHẦN 6: Kết luận, kiến nghị, tài liệu tham khảo với liên kết mạng và Khung xác nhận Mẫu TTTN-06.")
