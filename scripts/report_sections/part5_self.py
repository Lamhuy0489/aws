# -*- coding: utf-8 -*-
import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from scripts.docx_helpers import (
    set_cell_margins, set_cell_shading, set_table_borders, make_table_robust,
    add_bookmark
)

def add_part5(doc, add_h1, add_h2, add_h3, add_body, add_bullet, add_figure):
    add_h1("PHẦN 5: TỰ NHẬN XÉT VÀ ĐỊNH HƯỚNG NGHỀ NGHIỆP CÁ NHÂN")

    add_h2("5.1. Tự đánh giá Năng lực Cá nhân theo Chuẩn Đào tạo Kỹ sư CNTT")
    add_body(
        "Đối chiếu với Chuẩn đầu ra của chương trình đào tạo Kỹ sư Công nghệ Thông tin – Trường Đại học Xây dựng Hà Nội (HUCE) "
        "và các tiêu chí đánh giá khắt khe của chương trình AWS First Cloud AI Journey Bootcamp 2026, sinh viên tự đánh giá mức độ hoàn thành nhiệm vụ "
        "và năng lực chuyên môn đạt được sau 12 tuần thực tập thực chiến như sau:",
        indent=True
    )

    p_tbl_cap_self = doc.add_paragraph()
    p_tbl_cap_self.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tbl_cap_self.paragraph_format.space_before = Pt(8)
    p_tbl_cap_self.paragraph_format.space_after = Pt(4)
    p_tbl_cap_self.paragraph_format.keep_with_next = True
    add_bookmark(p_tbl_cap_self, "tbl5_1")
    r = p_tbl_cap_self.add_run("Bảng 5.1: Bảng tự đánh giá năng lực cá nhân theo 10 chuẩn đầu ra chuyên môn")
    r.bold = True
    r.font.size = Pt(11)

    table_self = doc.add_table(rows=11, cols=6)
    table_self.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_self.autofit = False
    set_table_borders(table_self, color="000000", sz="4")
    make_table_robust(table_self)

    self_widths = [Cm(1.2), Cm(5.2), Cm(1.6), Cm(1.4), Cm(1.4), Cm(5.2)]
    headers_self = ["STT", "Tiêu chí đánh giá chuyên môn", "Xuất sắc", "Tốt", "Đạt", "Nội dung minh chứng thực tế tại AWS"]
    for c_idx, h_text in enumerate(headers_self):
        cell = table_self.rows[0].cells[c_idx]
        cell.text = h_text
        set_cell_shading(cell, "FFFFFF")
        set_cell_margins(cell, top=80, bottom=80, left=60, right=60)
        p = cell.paragraphs[0]
        p.runs[0].bold = True
        p.runs[0].font.size = Pt(10)
        if c_idx in [0, 2, 3, 4]:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    self_data = [
        ("1", "Thiết kế kiến trúc đám mây AWS", "[x]", "[ ]", "[ ]", "Hoàn thành kiến trúc Three-Tier Multi-AZ kết hợp Serverless chuẩn Well-Architected [1]."),
        ("2", "Kỹ năng mạng & an ninh VPC / SG", "[x]", "[ ]", "[ ]", "Triển khai Custom VPC 10.0.0.0/16, 2 Subnet Multi-AZ, Internet Gateway và Security Group Chaining [2], [3]."),
        ("3", "Bảo mật máy chủ Zero-Trust (SSM)", "[x]", "[ ]", "[ ]", "Triệt tiêu cổng SSH 22; kết nối an toàn qua Session Manager và quản lý khóa bằng SSM Parameter Store [4]."),
        ("4", "Đóng gói Container & Docker/ECR", "[x]", "[ ]", "[ ]", "Xây dựng Dockerfile python:3.11-slim, xuất bản image lên Amazon ECR huylam-web-app."),
        ("5", "Tự động hóa Serverless Event-Driven", "[x]", "[ ]", "[ ]", "Tích hợp luồng S3 Event s3:ObjectCreated:* kích hoạt AWS Lambda huylam-ocr-processor (214 ms) [5], [6]."),
        ("6", "Quản lý chi phí đám mây FinOps", "[x]", "[ ]", "[ ]", "Kiểm soát chi phí lũy kế 0.00 USD trong AWS Free Tier suốt 12 tuần (Zero-Breach)."),
        ("7", "Xây dựng tài liệu kỹ thuật & Workshop", "[x]", "[ ]", "[ ]", "Biên soạn website tài liệu Hugo song ngữ 12 chuyên đề và Báo cáo tốt nghiệp chi tiết 50+ trang [12]."),
        ("8", "Khả năng tự nghiên cứu & giải quyết bài toán", "[x]", "[ ]", "[ ]", "Tự thiết kế giải thuật Fast-Path PyMuPDF (< 0.3s/trang [8]) và cơ chế Tour Xoay API Key tự phục hồi."),
        ("9", "Tinh thần kỷ luật & tiến độ công việc", "[x]", "[ ]", "[ ]", "Cập nhật đầy đủ 12 bài báo cáo Worklog tuần đúng hạn, hoàn thành 100% các mốc đánh giá."),
        ("10", "Tác phong kỹ thuật chuyên nghiệp", "[x]", "[ ]", "[ ]", "Quản lý mã nguồn trên Git, xây dựng kịch bản One-Click Deploy và tuân thủ chuẩn Enterprise.")
    ]

    for r_idx, (stt, crit, xs, tot, dat, ev) in enumerate(self_data):
        row = table_self.rows[r_idx + 1]
        for c_idx, val in enumerate([stt, crit, xs, tot, dat, ev]):
            cell = row.cells[c_idx]
            cell.text = val
            set_cell_shading(cell, "FFFFFF")
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            if c_idx in [0, 2, 3, 4]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                if c_idx == 0:
                    p.runs[0].bold = True
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(9.5)
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)

    for row in table_self.rows:
        for idx, width in enumerate(self_widths):
            row.cells[idx].width = width

    add_h2("5.2. Điểm mạnh và Điểm còn Hạn chế Cần Tiếp tục Hoàn thiện")
    add_body("Về các điểm mạnh nổi bật:", indent=True)
    add_bullet("Có khả năng nhìn nhận bài toán từ góc độ thiết kế hệ thống phân tán, cân bằng giữa hiệu năng, tính sẵn sàng cao và chi phí vận hành [1].", bold_prefix="Tư duy kiến trúc hệ thống tổng thể tốt: ")
    add_bullet("Chủ động tìm tòi, đọc tài liệu kỹ thuật tiếng Anh chính thống của AWS và áp dụng thành công các công nghệ mới (Fast-Path OCR [8], Cloudflare Tunnel, Serverless Event-Driven [6]).", bold_prefix="Khả năng tự học và thích ứng công nghệ cực nhanh: ")
    add_bullet("Thành thạo cả lập trình Backend (Python, Flask, FastAPI, Boto3 SDK) và xây dựng giao diện người dùng hiện đại (SPA, Vanilla JS, CSS Glassmorphism).", bold_prefix="Kỹ năng lập trình Fullstack vững vàng: ")
    add_bullet("Luôn kiểm tra kỹ các quy tắc tường lửa mạng trước khi áp dụng, cấu hình bảo vệ tài nguyên và duy trì kỷ luật ghi chép tài liệu hàng tuần.", bold_prefix="Tác phong làm việc cẩn trọng và kỷ luật cao: ")

    add_body("Về các điểm còn hạn chế cần tiếp tục hoàn thiện:", indent=True)
    add_bullet("Mặc dù đã làm chủ kiến trúc Multi-AZ cho ứng dụng đơn lẻ, sinh viên cần tiếp tục tích lũy kinh nghiệm quản trị các cụm Kubernetes/EKS phân tán đa vùng lãnh thổ (Multi-Region).", bold_prefix="Kinh nghiệm vận hành hạ tầng ở quy mô siêu lớn (Hyperscale): ")
    add_bullet("Cần rèn luyện thêm sự tự tin khi trình bày các giải pháp kiến trúc chuyên sâu trước các hội đồng chuyên gia quốc tế.", bold_prefix="Kỹ năng giao tiếp và thuyết trình kỹ thuật bằng tiếng Anh: ")

    add_h2("5.3. Bài học Kinh nghiệm Thực tiễn Rút ra từ Môi trường AWS")
    add_body(
        "Kỳ thực tập tại AWS Việt Nam đã mang lại cho sinh viên những bài học nghề nghiệp vô cùng giá trị, vượt xa các kiến thức sách vở thông thường [1]:",
        indent=True
    )
    add_bullet(
        "Trong điện toán đám mây, an ninh không phải là một tính năng gắn thêm "
        "mà phải được tích hợp vào từng lớp kiến trúc. Nguyên tắc đặc quyền tối thiểu (Least Privilege) và cô lập mạng phân tầng phải luôn là ưu tiên số một [2], [4].",
        bold_prefix="Tư duy thiết kế an ninh ngay từ đầu (Security by Design): "
    )
    add_bullet(
        "Đám mây mang lại sự linh hoạt vô tận nhưng cũng có thể gây thảm họa tài chính nếu không được giám sát. "
        "Mọi kỹ sư đám mây đều phải là một nhà quản lý tài chính thông thái, luôn bật cảnh báo ngân sách AWS Budgets và chọn mô hình định giá phù hợp nhất.",
        bold_prefix="Kỷ luật tài chính đám mây (FinOps Discipline): "
    )
    add_bullet(
        "Khi hệ thống gặp sự cố, kỹ sư chuyên nghiệp không sửa chữa mò mẫm "
        "mà phải bình tĩnh đọc log hệ thống từ CloudWatch [7], tái lập lỗi và triệt tiêu nguyên nhân gốc rễ để sự cố không bao giờ lặp lại.",
        bold_prefix="Tư duy phân tích nguyên nhân gốc rễ (Root Cause Analysis - RCA): "
    )
    add_bullet(
        "Mọi thứ đều có thể hỏng hóc vào bất kỳ lúc nào ('Everything fails, all the time' - Werner Vogels). "
        "Hệ thống xuất sắc là hệ thống luôn có cơ chế chuyển mạch dự phòng tự động (Failover) và có khả năng tự phục hồi mà người dùng không hề hay biết [1].",
        bold_prefix="Thiết kế hệ thống chịu lỗi (Fault-Tolerant Architecture): "
    )

    add_h2("5.4. Lộ trình Phát triển Nghề nghiệp trong Lĩnh vực Cloud / Solutions Architect")
    add_body(
        "Xác định rõ đam mê và tiềm năng phát triển to lớn của ngành công nghiệp đám mây, sinh viên đã xây dựng lộ trình phát triển sự nghiệp "
        "cho bản thân trong các giai đoạn tiếp theo:",
        indent=True
    )
    add_bullet(
        "Ôn tập chuyên sâu và thi đỗ chứng chỉ quốc tế AWS Certified Solutions Architect – Associate (SAA-C03); "
        "hoàn thành xuất sắc khóa luận tốt nghiệp Kỹ sư CNTT tại Trường Đại học Xây dựng Hà Nội với đề tài ứng dụng điện toán đám mây và AI [12].",
        bold_prefix="Mục tiêu ngắn hạn (6 tháng tới): "
    )
    add_bullet(
        "Gia nhập các tập đoàn công nghệ hàng đầu hoặc các đối tác cao cấp của AWS (AWS Premier Partners) "
        "với vai trò Kỹ sư Kiến trúc Đám mây (Cloud Solutions Architect) hoặc Kỹ sư DevOps; tiếp tục chinh phục chứng chỉ chuyên gia cao cấp "
        "AWS Certified Solutions Architect – Professional (SAP-C02) và AWS Certified Security – Specialty.",
        bold_prefix="Mục tiêu trung hạn (1 – 2 năm tới): "
    )
    add_bullet(
        "Trở thành Chuyên gia Kiến trúc Giải pháp Cấp cao (Lead Cloud Solutions Architect), "
        "trực tiếp dẫn dắt các dự án chuyển đổi số quy mô lớn cho khối tài chính - ngân hàng và chính phủ; tích cực tham gia diễn thuyết, "
        "chia sẻ kiến thức kỹ thuật và đóng góp cho cộng đồng công nghệ AWS User Group Vietnam.",
        bold_prefix="Mục tiêu dài hạn (3 – 5 năm tới): "
    )

    print("Hoàn thành biên soạn PHẦN 5: Tự nhận xét và định hướng nghề nghiệp cá nhân.")
