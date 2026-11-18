# -*- coding: utf-8 -*-
import os
import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from scripts.docx_helpers import (
    set_cell_margins, set_cell_shading, set_table_borders, make_table_robust,
    add_bookmark
)

def add_part3(doc, add_h1, add_h2, add_h3, add_body, add_bullet, add_figure):
    add_h1("PHẦN 3: NỘI DUNG VÀ KẾT QUẢ THỰC TẬP (TRỌNG TÂM KỸ THUẬT)")

    add_h2("3.1. Tổng quan Nhiệm vụ Kỹ thuật và Đề tài Capstone Hybrid OCR")
    add_body(
        "Trong kỷ nguyên chuyển đổi số và bùng nổ Trí tuệ nhân tạo (AI), dữ liệu tài liệu dạng văn bản không có cấu trúc "
        "(như hồ sơ kỹ thuật, báo cáo khoa học, hợp đồng thương mại, hóa đơn tài chính và bản scan biểu mẫu) chiếm hơn 80% tổng khối lượng "
        "thông tin trong các doanh nghiệp và tổ chức. Tuy nhiên, việc khai thác và tự động hóa xử lý nguồn tri thức khổng lồ này đang đối mặt "
        "với ba thách thức công nghệ nan giải:",
        indent=True
    )
    add_bullet(
        "Các công cụ nhận dạng ký tự quang học (OCR) truyền thống dựa trên xử lý ảnh "
        "thường xuyên làm đứt gãy cấu trúc bảng biểu phức tạp, mất định dạng phân cấp tiêu đề, và phát sinh lỗi chính tả nghiêm trọng khi xử lý tiếng Việt có dấu.",
        bold_prefix="Nút thắt về độ chính xác và bảo toàn cấu trúc bảng biểu: "
    )
    add_bullet(
        "Việc gửi toàn bộ các trang tài liệu (kể cả các trang PDF văn bản số vốn dĩ đã có sẵn luồng text) "
        "qua các API thị giác đám mây thương mại (như Google Cloud Vision, Azure OCR hay AWS Textract) làm gia tăng chi phí theo cấp số nhân "
        "(từ 0.015 đến 0.05 USD mỗi trang) và tạo ra độ trễ mạng lớn từ 3 đến 8 giây mỗi trang.",
        bold_prefix="Gánh nặng chi phí tính toán đám mây và độ trễ cao: "
    )
    add_bullet(
        "Khi đưa văn bản bóc tách vào các mô hình dịch thuật thông thường, cấu trúc Markdown, "
        "các ký hiệu toán học và bảng biểu bị xáo trộn hoàn toàn, đòi hỏi nhân sự phải mất hàng giờ định dạng lại thủ công.",
        bold_prefix="Rào cản ngôn ngữ và mất định dạng khi chuyển ngữ: "
    )
    add_body(
        "Nhằm giải quyết triệt để các bài toán thực tiễn nêu trên, đề tài thực tập tốt nghiệp của sinh viên tập trung vào việc nghiên cứu, "
        "thiết kế kiến trúc và triển khai thực tế trên đám mây AWS một nền tảng bóc tách, OCR lai và dịch thuật tài liệu kỹ thuật toàn diện mang tên: "
        "Serverless Hybrid Document OCR, Parsing & Technical Translation Platform on AWS.",
        indent=True
    )
    add_body(
        "Giải pháp kỹ thuật đột phá của đề tài là kiến trúc phân tầng lai thông minh (Multi-Tier Hybrid Architecture): "
        "Hệ thống tự động phân loại bản chất từng trang tài liệu ngay tại cổng nạp:",
        indent=True
    )
    add_bullet(
        "Trích xuất trực tiếp luồng văn bản số của tệp PDF với tốc độ mili-giây (< 0.1s/trang) bằng giải thuật PyMuPDF [8], "
        "bảo toàn 100% bảng biểu có cấu trúc và phát sinh chi phí tính toán là 0.00 USD.",
        bold_prefix="Tầng 1 - Fast-Path Native (PyMuPDF): "
    )
    add_bullet(
        "Tự động phát hiện các trang scan, ảnh chụp hoặc bản vẽ có mật độ ký tự thấp để định tuyến sang "
        "các mô hình thị giác nhân tạo chuyên sâu (Qwen2.5-VL-7B [9] trên cụm GPU Kaggle ngoại vi kết hợp cơ chế tự phục hồi Failover sang Google Gemini Flash [10] "
        "và tùy chọn AWS Bedrock Nova/Textract).",
        bold_prefix="Tầng 2 - Vision Multimodal OCR: "
    )

    add_figure(
        "workshop/static/images/architecture/aws-system-architecture.png",
        "Hình 3.1: Sơ đồ kiến trúc tổng thể hệ thống Serverless Hybrid Document OCR trên nền tảng đám mây AWS",
        width_cm=15.5
    )

    add_figure(
        "workshop/static/images/architecture/aws-hybrid-ocr-engine-architecture.png",
        "Hình 3.2: Sơ đồ luồng phân tầng bóc tách Hybrid OCR Engine (Fast-Path Native kết hợp Vision Multimodal OCR)",
        width_cm=15.5
    )

    add_h2("3.2. Thiết kế và Triển khai Hạ tầng Đám mây AWS Zero-Trust")
    add_body(
        "Toàn bộ hạ tầng đám mây phục vụ hệ thống được thiết kế và triển khai tuân thủ nghiêm ngặt khung kiến trúc AWS Well-Architected Framework [1], "
        "kết hợp mô hình an ninh mạng Zero-Trust và kiến trúc mạng doanh nghiệp 3 tầng (Three-Tier Enterprise Cloud Architecture).",
        indent=True
    )

    add_h3("3.2.1. Mạng ảo tùy biến Amazon VPC Multi-AZ độ sẵn sàng cao")
    add_body(
        "Hệ thống không sử dụng mạng VPC mặc định (Default VPC) mà khởi tạo một mạng ảo đám mây cô lập chuyên biệt (Custom VPC [2]) "
        "mang tên huylam-vpc với dải mạng CIDR 10.0.0.0/16 tại khu vực Singapore (ap-southeast-1). "
        "Mạng được phân chia thành 2 Public Subnets Multi-AZ nằm trên 2 Vùng sẵn sàng độc lập:",
        indent=True
    )
    add_bullet(
        "Dải mạng CIDR 10.0.0.0/20 thuộc Vùng sẵn sàng ap-southeast-1a (subnet-0efa7c3a5818035dc).",
        bold_prefix="Public Subnet 1 (huylam-public-subnet-1a): "
    )
    add_bullet(
        "Dải mạng CIDR 10.0.16.0/20 thuộc Vùng sẵn sàng ap-southeast-1b (subnet-0e07eb2fd44d1ac91).",
        bold_prefix="Public Subnet 2 (huylam-public-subnet-2a): "
    )
    add_bullet(
        "Dải mạng CIDR 10.0.128.0/20 thuộc Vùng sẵn sàng ap-southeast-1a (subnet-08563e499271091ab).",
        bold_prefix="Private Subnet 1 (huylam-private-subnet-1a): "
    )
    add_bullet(
        "Dải mạng CIDR 10.0.144.0/20 thuộc Vùng sẵn sàng ap-southeast-1b (subnet-07e20dc44c40fac46).",
        bold_prefix="Private Subnet 2 (huylam-private-subnet-2a): "
    )
    add_body(
        "Cổng Internet Gateway (huylam-igw) được khởi tạo và liên kết trực tiếp với huylam-vpc. Bảng định tuyến công khai (Public Route Table) "
        "được cấu hình chuyển tiếp toàn bộ lưu lượng ngoại vi đích 0.0.0.0/0 tới Internet Gateway, đồng thời kích hoạt tính năng tự động gán địa chỉ "
        "IP công cộng (Auto-assign Public IPv4) cho các máy chủ tính toán trong mạng [2].",
        indent=True
    )

    add_figure(
        "workshop/static/images/architecture/aws-vpc-network-architecture.png",
        "Hình 3.3: Sơ đồ kiến trúc mạng ảo Amazon VPC Multi-AZ phân tách Subnet độ sẵn sàng cao",
        width_cm=15.5
    )

    add_figure(
        "workshop/static/images/week3/03-vpc-resource-map.png",
        "Hình 3.4: Sơ đồ phân bổ tài nguyên VPC Resource Map thực tế trên AWS Management Console",
        width_cm=15.5
    )

    p_tbl_cap_vpc = doc.add_paragraph()
    p_tbl_cap_vpc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tbl_cap_vpc.paragraph_format.space_before = Pt(8)
    p_tbl_cap_vpc.paragraph_format.space_after = Pt(4)
    p_tbl_cap_vpc.paragraph_format.keep_with_next = True
    add_bookmark(p_tbl_cap_vpc, "tbl3_1")
    r = p_tbl_cap_vpc.add_run("Bảng 3.1: Bảng thông số cấu hình hạ tầng mạng Amazon VPC Multi-AZ")
    r.bold = True
    r.font.size = Pt(11)

    table_vpc = doc.add_table(rows=8, cols=4)
    table_vpc.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_vpc.autofit = False
    set_table_borders(table_vpc, color="000000", sz="4")
    make_table_robust(table_vpc)

    vpc_widths = [Cm(3.5), Cm(4.0), Cm(4.0), Cm(4.5)]
    headers_vpc = ["Tài nguyên mạng", "Định danh / Tên", "Dải mạng CIDR / Vùng", "Mục đích sử dụng"]
    for c_idx, h_text in enumerate(headers_vpc):
        cell = table_vpc.rows[0].cells[c_idx]
        cell.text = h_text
        set_cell_shading(cell, "FFFFFF")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        p.runs[0].bold = True
        p.runs[0].font.size = Pt(10.5)

    vpc_data = [
        ("Virtual Private Cloud", "huylam-vpc (vpc-0125f4d6db3fbffa6)", "10.0.0.0/16", "Không gian mạng ảo cô lập cấp doanh nghiệp"),
        ("Public Subnet AZ-1", "huylam-public-subnet-1a", "10.0.0.0/20 (ap-southeast-1a)", "Phân bổ ALB và máy chủ ứng dụng EC2"),
        ("Public Subnet AZ-2", "huylam-public-subnet-2a", "10.0.16.0/20 (ap-southeast-1b)", "Phân bổ ALB phục vụ dự phòng Multi-AZ"),
        ("Private Subnet AZ-1", "huylam-private-subnet-1a", "10.0.128.0/20 (ap-southeast-1a)", "Phân vùng cô lập nội bộ dữ liệu"),
        ("Private Subnet AZ-2", "huylam-private-subnet-2a", "10.0.144.0/20 (ap-southeast-1b)", "Phân vùng cô lập dự phòng dữ liệu"),
        ("Internet Gateway", "huylam-igw (igw-0b9db3a6eac29ede9)", "Attached to huylam-vpc", "Cổng giao tiếp Internet hai chiều"),
        ("Public Route Table", "huylam-public-rt (rtb-01c05a18a99a80eb9)", "0.0.0.0/0 -> huylam-igw", "Định tuyến lưu lượng truy cập công khai")
    ]

    for r_idx, (res, name, cidr, purp) in enumerate(vpc_data):
        row = table_vpc.rows[r_idx + 1]
        for c_idx, val in enumerate([res, name, cidr, purp]):
            cell = row.cells[c_idx]
            cell.text = val
            set_cell_shading(cell, "FFFFFF")
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            if c_idx == 0:
                p.runs[0].bold = True
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(10)
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)

    for row in table_vpc.rows:
        for idx, width in enumerate(vpc_widths):
            row.cells[idx].width = width

    add_h3("3.2.2. Ma trận Tường lửa Trạng thái Chaining (Defense-in-Depth)")
    add_body(
        "Nhằm loại bỏ triệt để nguy cơ máy chủ ứng dụng bị tấn công trực diện hoặc quét cổng từ Internet, hệ thống thiết lập cơ chế "
        "chuỗi tường lửa liên kết (Security Group Chaining [3]). Thay vì mở dải IP rộng (0.0.0.0/0) vào máy chủ ứng dụng, hệ thống phân tách thành 2 tầng bảo vệ:",
        indent=True
    )
    add_bullet(
        "Đóng vai trò là lá chắn biên giới tiếp nhận lưu lượng HTTP (TCP cổng 80) từ toàn bộ người dùng Internet công cộng (0.0.0.0/0).",
        bold_prefix="Tầng 1 - ALB Security Group (huylam-alb-sg): "
    )
    add_bullet(
        "Bảo vệ trực tiếp máy chủ ứng dụng EC2. Security Group này chỉ cho phép lưu lượng truy cập "
        "vào cổng TCP 5000 khi và chỉ khi nguồn gốc kết nối xuất phát từ chính định danh Security Group của ALB (Source: huylam-alb-sg). "
        "Mọi nỗ lực truy cập trực tiếp từ Internet vào cổng 5000 của EC2 đều bị tường lửa hủy gói tin tức thì (Drop Packet).",
        bold_prefix="Tầng 2 - Web Server Security Group (huylam-web-sg): "
    )
    add_bullet(
        "Không mở cổng 22 trên bất kỳ Security Group nào, triệt tiêu 100% bề mặt tấn công vét cạn mật khẩu (Brute-force) [4].",
        bold_prefix="Triệt tiêu hoàn toàn cổng SSH 22 (Zero Inbound SSH): "
    )

    add_figure(
        "workshop/static/images/architecture/aws-security-group-chaining.png",
        "Hình 3.5: Mô hình chuỗi an ninh phân tầng Security Group Chaining cô lập máy chủ EC2",
        width_cm=15.0
    )

    p_tbl_cap_sg = doc.add_paragraph()
    p_tbl_cap_sg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tbl_cap_sg.paragraph_format.space_before = Pt(8)
    p_tbl_cap_sg.paragraph_format.space_after = Pt(4)
    p_tbl_cap_sg.paragraph_format.keep_with_next = True
    add_bookmark(p_tbl_cap_sg, "tbl3_2")
    r = p_tbl_cap_sg.add_run("Bảng 3.2: Ma trận cấu hình tường lửa trạng thái Security Groups phân tầng")
    r.bold = True
    r.font.size = Pt(11)

    table_sg = doc.add_table(rows=3, cols=5)
    table_sg.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_sg.autofit = False
    set_table_borders(table_sg, color="000000", sz="4")
    make_table_robust(table_sg)

    sg_widths = [Cm(3.5), Cm(2.5), Cm(2.5), Cm(4.0), Cm(3.5)]
    headers_sg = ["Tên Security Group", "Giao thức", "Cổng mạng", "Nguồn truy cập (Source)", "Ý nghĩa an ninh"]
    for c_idx, h_text in enumerate(headers_sg):
        cell = table_sg.rows[0].cells[c_idx]
        cell.text = h_text
        set_cell_shading(cell, "FFFFFF")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        p.runs[0].bold = True
        p.runs[0].font.size = Pt(10.5)

    sg_data = [
        ("huylam-alb-sg", "TCP", "80 (HTTP)", "0.0.0.0/0 (Internet)", "Tiếp nhận người dùng công khai"),
        ("huylam-web-sg", "TCP", "5000 (App)", "huylam-alb-sg (Chained)", "Cô lập EC2, chỉ nhận từ ALB")
    ]

    for r_idx, (name, proto, port, src, desc) in enumerate(sg_data):
        row = table_sg.rows[r_idx + 1]
        for c_idx, val in enumerate([name, proto, port, src, desc]):
            cell = row.cells[c_idx]
            cell.text = val
            set_cell_shading(cell, "FFFFFF")
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            if c_idx == 0:
                p.runs[0].bold = True
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(10)
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)

    for row in table_sg.rows:
        for idx, width in enumerate(sg_widths):
            row.cells[idx].width = width

    add_h3("3.2.3. Quản trị máy chủ Zero Trust và Quản lý bí mật với AWS Systems Manager")
    add_body(
        "Thay vì duy trì các khóa bí mật SSH (.pem) có rủi ro thất lạc cao và mở cổng 22, hệ thống ứng dụng giải pháp quản trị "
        "AWS Systems Manager (SSM [4]) theo mô hình Zero-Trust. Máy chủ EC2 được gắn IAM Role chuyên dụng (huylam-ssm-role) đính kèm các chính sách "
        "AmazonSSMManagedInstanceCore, AmazonS3FullAccess và AmazonDynamoDBFullAccess.",
        indent=True
    )
    add_body(
        "Thông qua SSM Session Manager [4], quản trị viên có thể truy cập shell tương tác trực tiếp trên giao diện trình duyệt web mà không cần mở cổng mạng Inbound nào. "
        "Đồng thời, toàn bộ các cấu hình nhạy cảm (ngưỡng phân loại trang scan, tham số xoay vòng API Keys, thông tin dịch vụ) được lưu trữ tập trung "
        "trên AWS Systems Manager Parameter Store dưới dạng tham số mã hóa bảo mật cao (SecureString) sử dụng khóa AWS KMS (alias/aws/ssm) tại đường dẫn /huylam-ocr/config.",
        indent=True
    )

    add_figure(
        "workshop/static/images/week10/05-ssm-parameter-details.png",
        "Hình 3.6: Cấu hình tham số bảo mật và khóa hệ thống trên AWS Systems Manager Parameter Store",
        width_cm=15.5
    )

    add_h3("3.2.4. Lưu trữ đối tượng Amazon S3 & Cơ sở dữ liệu NoSQL Amazon DynamoDB")
    add_body(
        "Hệ thống lưu trữ và quản lý trạng thái tài liệu được xây dựng hoàn toàn trên các dịch vụ đám mây có độ bền và tính sẵn sàng cao:",
        indent=True
    )
    add_bullet(
        "Khởi tạo bucket huylam-ocr-documents-ap-southeast-1 được mã hóa Server-Side Encryption (SSE-S3 AES-256). "
        "Cấu trúc lưu trữ được phân tách khoa học thành 2 phân vùng độc lập: uploads/ (tiếp nhận các tệp PDF và ảnh scan gốc của người dùng) và "
        "outputs/ (lưu trữ kết quả bóc tách Markdown, tệp Word .docx và PDF đã chuyển ngữ). Cấu hình chia sẻ tài nguyên nguồn gốc chéo (CORS) cho phép tải tệp trực tiếp an toàn.",
        bold_prefix="Kho lưu trữ đối tượng Amazon S3: "
    )
    add_bullet(
        "Khởi tạo bảng document_processing_jobs với khóa chính hỗn hợp gồm Partition Key job_id (String) "
        "và Sort Key created_at (String) [5]. Bảng được cấu hình chế độ định mức năng lực theo yêu cầu (On-Demand Capacity Mode - PAY_PER_REQUEST), "
        "đảm bảo tự động co giãn tức thì theo tải và duy trì chi phí 0.00 USD khi hệ thống ở trạng thái nhàn rỗi.",
        bold_prefix="Cơ sở dữ liệu NoSQL Amazon DynamoDB: "
    )

    add_figure(
        "workshop/static/images/week10/01-s3-create-bucket-config.png",
        "Hình 3.7: Cấu hình lưu trữ tệp trên Amazon S3 phân tách thư mục uploads/ và outputs/",
        width_cm=15.5
    )

    add_figure(
        "workshop/static/images/week10/04-dynamodb-table-active-overview.png",
        "Hình 3.8: Bảng dữ liệu NoSQL Amazon DynamoDB (document_processing_jobs) ở trạng thái Active",
        width_cm=15.5
    )

    add_h3("3.2.5. Cân bằng tải Application Load Balancer và Máy chủ ứng dụng EC2")
    add_body(
        "Tầng điện toán và phân phối lưu lượng của nền tảng được vận hành bởi sự kết hợp giữa bộ cân bằng tải và máy chủ ảo tối ưu hóa [3]:",
        indent=True
    )
    add_bullet(
        "Phiên bản huylam-ocr-web-server (Instance ID: i-0566e1eedaacea52d) sử dụng hệ điều hành Amazon Linux 2023, "
        "loại phần cứng t2.micro thuộc gói AWS Free Tier, chạy máy chủ WSGI Gunicorn dưới dạng một daemon hệ thống (huylam-ocr.service) trên cổng 5000.",
        bold_prefix="Máy chủ ứng dụng Amazon EC2: "
    )
    add_bullet(
        "huylam-ocr-tg đăng ký trực tiếp phiên bản máy chủ EC2 trên cổng 5000, thiết lập cơ chế tự động kiểm tra sức khỏe "
        "(Health Check) định kỳ qua đường dẫn /login, xác nhận trạng thái đạt chuẩn 1/1 Healthy.",
        bold_prefix="Nhóm mục tiêu (Target Group): "
    )
    add_bullet(
        "Khởi tạo ALB huylam-ocr-alb kết nối Internet (Internet-facing), phân bổ lưu lượng qua 2 Public Subnet Multi-AZ, "
        "lắng nghe cổng HTTP 80 và chuyển tiếp lưu lượng vào Target Group với tên miền DNS công khai [3]:",
        bold_prefix="Application Load Balancer: "
    )
    add_body("http://huylam-ocr-alb-1284818160.ap-southeast-1.elb.amazonaws.com", bold_prefix="Tên miền công khai ALB: ")

    add_figure(
        "workshop/static/images/week12/08-target-group-healthy-status.png",
        "Hình 3.9: Kiểm chứng trạng thái Healthy (1/1) của Target Group trên Application Load Balancer",
        width_cm=15.5
    )

    add_h3("3.2.6. Kiến trúc phi máy chủ hướng sự kiện Event-Driven Serverless Pipeline")
    add_body(
        "Một trong những điểm nhấn kiến trúc nâng cao của đồ án là việc tích hợp mô hình xử lý phi máy chủ hướng sự kiện (Event-Driven Serverless Architecture [6]). "
        "Mô hình này giúp giải quyết triệt để vấn đề quá tải cho máy chủ web khi người dùng nạp các tài liệu lớn, đồng thời mở rộng quy mô tự động:",
        indent=True
    )
    add_bullet(
        "Khi người dùng tải một tệp PDF vào thư mục uploads/ của Amazon S3, S3 Event Notification tự động phát sinh sự kiện "
        "s3:ObjectCreated:* và chuyển tiếp trực tiếp tới hàm phi máy chủ AWS Lambda huylam-ocr-processor [6].",
        bold_prefix="Quy trình kích hoạt tự động: "
    )
    add_bullet(
        "Hàm Lambda tự động tải tệp từ S3, kích hoạt động cơ bóc tách lai Hybrid Document Engine, tự động xuất bản kết quả "
        "ra định dạng Markdown (.md) và Word (.docx [11]) rồi lưu trữ trở lại thư mục outputs/ của S3.",
        bold_prefix="Thực thi xử lý phi máy chủ: "
    )
    add_bullet(
        "Lambda tự động ghi nhận bản ghi nhật ký tiến trình (Job Record) gồm thông tin số trang, thời gian xử lý, "
        "đường dẫn S3 URI đầu ra vào bảng Amazon DynamoDB document_processing_jobs [5] và đồng bộ nhật ký sang Amazon CloudWatch Logs [7] với độ trễ chỉ 214 ms.",
        bold_prefix="Cập nhật trạng thái tự động vào CSDL: "
    )

    add_figure(
        "workshop/static/images/architecture/aws-serverless-event-pipeline.png",
        "Hình 3.10: Sơ đồ kiến trúc xử lý phi máy chủ hướng sự kiện (Event-Driven Serverless Pipeline)",
        width_cm=15.5
    )

    add_figure(
        "workshop/static/images/week11/10-lambda-code-deployed-success.png",
        "Hình 3.11: Mã nguồn hàm AWS Lambda (huylam-ocr-processor) được triển khai thành công trên AWS",
        width_cm=15.5
    )

    add_figure(
        "workshop/static/images/week11/13-dynamodb-items-received-s3-event.png",
        "Hình 3.12: Bảng Amazon DynamoDB tự động tiếp nhận bản ghi sự kiện xử lý tài liệu từ S3 Event Notification",
        width_cm=15.5
    )

    add_h2("3.3. Xây dựng và Hoàn thiện Động cơ Ứng dụng Lõi")
    add_body(
        "Bên cạnh hạ tầng điện toán đám mây vững chắc, phần mềm ứng dụng được xây dựng theo kiến trúc mô-đun hóa cao (Modular Clean Architecture), "
        "bao gồm các thành phần công nghệ độc lập:",
        indent=True
    )

    add_h3("3.3.1. Tầng 1 - Fast-Path Native Parser (PyMuPDF trích xuất vector)")
    add_body(
        "Động cơ FastNativeParser khai thác trực tiếp luồng đối tượng đồ họa và font chữ vector của tài liệu PDF bằng thư viện PyMuPDF [8]. "
        "Thuật toán phân tích tọa độ không gian (Bounding Box) của từng từ và ký tự để tái tạo chính xác các bảng biểu dữ liệu thành cú pháp bảng Markdown "
        "(| Cột 1 | Cột 2 |).",
        indent=True
    )
    add_body(
        "Khi một trang tài liệu chứa từ 50 ký tự số trở lên, hệ thống xác định đây là trang văn bản số và xử lý ngay tại tầng này. "
        "Tốc độ xử lý trung bình đạt 0.1s đến 0.3s mỗi trang mà không tiêu tốn bất kỳ chi phí API nào.",
        indent=True
    )

    add_h3("3.3.2. Tầng 2 - Vision Multimodal OCR & Cơ chế Tự phục hồi (Failover)")
    add_body(
        "Đối với các trang văn bản quét scan hoặc ảnh chụp mờ (mật độ ký tự < 50), bộ điều phối OCRDispatcher sẽ tự động kích hoạt Tầng 2:",
        indent=True
    )
    add_bullet(
        "Gửi ảnh tới máy chủ FastAPI chạy mô hình thị giác tiên tiến Qwen2.5-VL-7B [9] trên 2x NVIDIA T4 GPU "
        "thông qua đường hầm bảo mật Cloudflare Tunnel với chi phí tính toán 0.00 USD.",
        bold_prefix="Ưu tiên 1 - Cụm GPU Kaggle ngoại vi: "
    )
    add_bullet(
        "Khi endpoint Kaggle phản hồi chậm quá 5 giây hoặc mất kết nối, bộ điều phối tự động chuyển mạch dự phòng "
        "sang mô hình Google Gemini Flash [10] thông qua hệ thống Tour Xoay API Key mà không làm gián đoạn tiến trình của người dùng.",
        bold_prefix="Cơ chế tự phục hồi tức thì (Self-Healing Failover): "
    )
    add_bullet(
        "Hệ thống tích hợp sẵn driver Boto3 cho phép quản trị viên kích hoạt mô hình Amazon Bedrock (Nova/Claude) hoặc "
        "Amazon Textract khi doanh nghiệp yêu cầu dữ liệu khép kín hoàn toàn trong môi trường AWS.",
        bold_prefix="Tùy chọn AWS Native AI: "
    )

    add_h3("3.3.3. Động cơ Dịch thuật Kỹ thuật (DocumentTranslator)")
    add_body(
        "Module dịch thuật DocumentTranslator được thiết kế chuyên biệt để chuyển ngữ các tài liệu kỹ thuật phức tạp (hỗ trợ Tiếng Anh, Tiếng Nhật, "
        "Tiếng Hàn, Tiếng Trung, Tiếng Pháp, Tiếng Đức và Tiếng Việt) thông qua mô hình ngôn ngữ lớn [10].",
        indent=True
    )
    add_body(
        "Hệ thống áp dụng thuật toán phân đoạn thông minh (Smart Semantic Chunking): chia nhỏ tài liệu theo ranh giới đoạn văn và bảng biểu, "
        "đảm bảo không vượt quá ngữ cảnh token của mô hình, đồng thời ép buộc mô hình giữ nguyên 100% cấu trúc Markdown, mã code và các nhãn cột trong bảng.",
        indent=True
    )

    add_h3("3.3.4. Bộ Xuất bản Đa định dạng (Multi-Format Exporters)")
    add_body(
        "Sau khi hoàn tất bóc tách hoặc dịch thuật, hệ thống cho phép xuất bản tài liệu ra ba định dạng chuẩn mực:",
        indent=True
    )
    add_bullet("Định dạng văn bản thuần có cấu trúc tiêu chuẩn phục vụ lưu trữ số và tích hợp vào các hệ thống tri thức (RAG/Wiki).", bold_prefix="Định dạng Markdown (.md): ")
    add_bullet("Tự động chuyển đổi bảng Markdown thành bảng Word thực thụ bằng python-docx [11], áp dụng kiểu dáng tiêu đề và căn lề chuyên nghiệp.", bold_prefix="Định dạng Microsoft Word (.docx): ")
    add_bullet("Sử dụng động cơ PyMuPDF Story [8] để kết xuất tài liệu ra tệp PDF chuẩn trang in A4 sắc nét.", bold_prefix="Định dạng PDF chuẩn in ấn (.pdf): ")

    add_h3("3.3.5. Giao diện Web Studio SPA (Zero-Flicker) & Bảng điều khiển Tour Xoay Key")
    add_body(
        "Trải nghiệm người dùng được tối ưu hóa toàn diện với giao diện ứng dụng đơn trang (Single Page Application - SPA) được điều hướng bằng spa_router.js, "
        "loại bỏ hoàn toàn hiện tượng tải lại toàn bộ trang (Zero-Flicker). Hệ thống quản lý trạng thái hai lớp (Dual-Layer State Persistence) trên cả máy chủ "
        "(Flask Session + SQLite) và bộ nhớ cục bộ trình duyệt (localStorage), ngăn chặn tuyệt đối tình trạng mất dữ liệu khi làm mới trang.",
        indent=True
    )
    add_body(
        "Bảng điều khiển quản trị (/admin) cho phép giám sát chỉ số KPI, xem nhật ký tiến trình, thêm mới hoặc bật/tắt tạm dừng các khóa API trong Tour Xoay vòng [10].",
        indent=True
    )

    add_figure(
        "workshop/static/images/week12/10-browser-alb-studio-live.png",
        "Hình 3.13: Giao diện ứng dụng Web Studio vận hành trực tiếp trên hạ tầng AWS thông qua Application Load Balancer",
        width_cm=12.2
    )

    add_figure(
        "workshop/static/images/week11/03-studio-cv-extracted-translated.png",
        "Hình 3.14: Kết quả bóc tách và dịch thuật tài liệu kỹ thuật trên giao diện Web Studio",
        width_cm=12.2
    )

    add_figure(
        "workshop/static/images/week11/04-word-cv-exported-verification.png",
        "Hình 3.15: Kiểm chứng tài liệu Microsoft Word (.docx) được kết xuất tự động với định dạng chuẩn mực",
        width_cm=12.2
    )

    add_h3("3.3.6. Bảng Ánh xạ Toàn diện Module Hệ thống sang Dịch vụ Đám mây AWS")
    add_body(
        "Bảng dưới đây tổng hợp chi tiết sự gắn kết và ánh xạ giữa từng thành phần trong mã nguồn của nền tảng với các dịch vụ đám mây AWS tương ứng:",
        indent=True
    )

    p_tbl_cap_map = doc.add_paragraph()
    p_tbl_cap_map.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tbl_cap_map.paragraph_format.space_before = Pt(8)
    p_tbl_cap_map.paragraph_format.space_after = Pt(4)
    p_tbl_cap_map.paragraph_format.keep_with_next = True
    add_bookmark(p_tbl_cap_map, "tbl3_3")
    r = p_tbl_cap_map.add_run("Bảng 3.3: Bảng ánh xạ toàn diện module mã nguồn hệ thống sang dịch vụ đám mây AWS")
    r.bold = True
    r.font.size = Pt(11)

    table_map = doc.add_table(rows=8, cols=3)
    table_map.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_map.autofit = False
    set_table_borders(table_map, color="000000", sz="4")
    make_table_robust(table_map)

    map_widths = [Cm(4.8), Cm(4.5), Cm(6.7)]
    headers_map = ["Thành phần trong mã nguồn", "Dịch vụ đám mây AWS", "Vai trò và chức năng đảm nhiệm"]
    for c_idx, h_text in enumerate(headers_map):
        cell = table_map.rows[0].cells[c_idx]
        cell.text = h_text
        set_cell_shading(cell, "FFFFFF")
        set_cell_margins(cell, top=40, bottom=40, left=70, right=70)
        p = cell.paragraphs[0]
        p.runs[0].bold = True
        p.runs[0].font.size = Pt(9.5)

    map_data = [
        ("Cân bằng tải & Điều hướng", "Application Load Balancer (ALB [3])", "Tiếp nhận lưu lượng HTTP cổng 80, cân bằng tải Multi-AZ và chuyển tiếp vào Target Group."),
        ("Máy chủ Web Studio Gunicorn", "Amazon EC2 (Amazon Linux 2023)", "Vận hành ứng dụng web Python 3.11, xử lý điều hướng SPA và bóc tách Fast-Path [8]."),
        ("Kho lưu trữ tệp gốc & kết quả", "Amazon Simple Storage Service (S3)", "Lưu trữ tệp tải lên (uploads/) và tệp kết xuất (outputs/) với mã hóa SSE-S3 AES-256."),
        ("Quản lý tiến trình xử lý", "Amazon DynamoDB (On-Demand [5])", "Cơ sở dữ liệu NoSQL lưu trữ trạng thái Job, số trang, thời gian xử lý và metadata."),
        ("Bóc tách bất đồng bộ hướng sự kiện", "AWS Lambda (Serverless [6])", "Hàm huylam-ocr-processor tự động kích hoạt bởi S3 Event Notification khi có tệp mới."),
        ("Quản lý bí mật & Cấu hình", "AWS Systems Manager (SSM [4])", "Lưu trữ tham số /huylam-ocr/config mã hóa KMS và điều khiển máy chủ qua Session Manager."),
        ("Giám sát & Cảnh báo thời gian thực", "Amazon CloudWatch & SNS [7]", "Thu thập nhật ký, giám sát chỉ số tải CPU máy chủ và gửi cảnh báo sự cố qua email.")
    ]

    for r_idx, (comp, svc, role) in enumerate(map_data):
        row = table_map.rows[r_idx + 1]
        for c_idx, val in enumerate([comp, svc, role]):
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
            set_cell_margins(cell, top=25, bottom=25, left=60, right=60)

    for row in table_map.rows:
        for idx, width in enumerate(map_widths):
            row.cells[idx].width = width

    add_h2("3.4. Kiểm thử Toàn trình, Đánh giá Hiệu năng (Benchmark) & FinOps")
    add_h3("3.4.1. Kịch bản kiểm thử toàn trình End-to-End trên môi trường thực tế")
    add_body(
        "Nhằm đánh giá khách quan năng lực vận hành thực tế của giải pháp, hệ thống đã trải qua quy trình kiểm thử toàn trình "
        "trên môi trường AWS Cloud thật với đa dạng các tập dữ liệu mẫu:",
        indent=True
    )
    add_bullet(
        "Sử dụng bài báo khoa học 28_Bai_Bao.pdf (11 trang định dạng PDF số). "
        "Hệ thống kích hoạt Tầng 1 Fast-Path Native [8], hoàn thành toàn bộ 11 trang chỉ trong 3.07 giây (trung bình 0.28s/trang), "
        "bảo toàn trọn vẹn 100% cấu trúc các bảng biểu số liệu phức tạp với chi phí tính toán là 0.00 USD.",
        bold_prefix="Kiểm thử bóc tách tài liệu số nhiều trang: "
    )
    add_bullet(
        "Tải lên ảnh chụp scan biểu mẫu thực tập có chất lượng mờ. "
        "Hệ thống tự động kích hoạt Tầng 2 Vision OCR [9], trích xuất chính xác tiếng Việt có dấu trong 2.54 giây với chi phí 0 đồng.",
        bold_prefix="Kiểm thử ảnh quét scan và cơ chế Failover: "
    )
    add_bullet(
        "Chuyển ngữ hồ sơ kỹ thuật tiếng Anh sang tiếng Việt, "
        "hệ thống mất 2.80 giây để hoàn thành và xuất ra tệp Word (.docx [11]) chuẩn mực trong 0.15 giây.",
        bold_prefix="Kiểm thử dịch thuật và xuất bản Word: "
    )

    add_h3("3.4.2. Bảng số liệu đo kiểm thực nghiệm Benchmark")
    p_tbl_cap_bm = doc.add_paragraph()
    p_tbl_cap_bm.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tbl_cap_bm.paragraph_format.space_before = Pt(8)
    p_tbl_cap_bm.paragraph_format.space_after = Pt(4)
    p_tbl_cap_bm.paragraph_format.keep_with_next = True
    add_bookmark(p_tbl_cap_bm, "tbl3_4")
    r = p_tbl_cap_bm.add_run("Bảng 3.4: Bảng số liệu đo kiểm thực nghiệm Benchmark hiệu năng và độ trễ")
    r.bold = True
    r.font.size = Pt(11)

    table_bm = doc.add_table(rows=6, cols=5)
    table_bm.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_bm.autofit = False
    set_table_borders(table_bm, color="000000", sz="4")
    make_table_robust(table_bm)

    bm_widths = [Cm(3.5), Cm(3.0), Cm(3.5), Cm(3.0), Cm(3.0)]
    headers_bm = ["Tác vụ thực nghiệm", "Tài liệu mẫu", "Động cơ thực thi", "Thời gian xử lý", "Chi phí vận hành"]
    for c_idx, h_text in enumerate(headers_bm):
        cell = table_bm.rows[0].cells[c_idx]
        cell.text = h_text
        set_cell_shading(cell, "FFFFFF")
        set_cell_margins(cell, top=40, bottom=40, left=70, right=70)
        p = cell.paragraphs[0]
        p.runs[0].bold = True
        p.runs[0].font.size = Pt(9.5)

    bm_data = [
        ("Bóc tách PDF văn bản số", "cv.pdf (1 trang)", "Fast-Path Native [8]", "0.31 giây", "0.00 USD"),
        ("Bóc tách bài báo khoa học", "28_Bai_Bao.pdf (11 trang)", "Fast-Path Native [8]", "3.07 giây (~0.28s/trang)", "0.00 USD"),
        ("Bóc tách ảnh scan biểu mẫu", "Ảnh chụp scan hóa đơn", "Vision OCR (Kaggle [9] / Gemini [10])", "2.54 giây", "0.00 USD (Free Tier)"),
        ("Dịch thuật tài liệu kỹ thuật", "cv.pdf (Anh -> Việt)", "DocumentTranslator [10]", "2.80 giây", "0.00 USD (Free Tier)"),
        ("Xuất bản Microsoft Word", "Tệp kết quả sau dịch", "DocxExporter Module [11]", "0.15 giây", "0.00 USD")
    ]

    for r_idx, (task, doc_s, eng, time_s, cost) in enumerate(bm_data):
        row = table_bm.rows[r_idx + 1]
        for c_idx, val in enumerate([task, doc_s, eng, time_s, cost]):
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
            set_cell_margins(cell, top=25, bottom=25, left=60, right=60)

    for row in table_bm.rows:
        for idx, width in enumerate(bm_widths):
            row.cells[idx].width = width

    add_h3("3.4.3. Quản trị chi phí và kỷ luật tài chính FinOps (Zero-Breach)")
    add_body(
        "Về mặt quản trị tài chính đám mây (FinOps [1]): Thông qua việc thiết lập ngân sách AWS Budgets tự động cảnh báo và tối ưu hóa tài nguyên "
        "(sử dụng EC2 t2.micro, DynamoDB On-Demand [5], Lambda serverless [6], S3 Standard kết hợp tận dụng cụm GPU Kaggle ngoại vi), "
        "chi phí phát sinh thực tế lũy kế trong suốt kỳ thực tập được kiểm soát tuyệt đối ở mức 0.00 USD, tuân thủ nguyên tắc Zero-Breach.",
        indent=True
    )

    add_h2("3.5. Giám sát Vận hành & Cảnh báo Sự cố với Amazon CloudWatch")
    add_body(
        "Nhằm đảm bảo hệ thống vận hành liên tục và phát hiện sớm các sự cố tiềm ẩn, sinh viên đã xây dựng hệ thống giám sát tập trung bằng Amazon CloudWatch [7]:",
        indent=True
    )
    add_bullet(
        "Thiết lập Log Group /aws/lambda/huylam-ocr-processor và /huylam/cloudwatch/system-logs, "
        "thu thập toàn bộ nhật ký truy cập web, thời gian thực thi của từng trang bóc tách và các mã lỗi ngoại lệ.",
        bold_prefix="Quản lý nhật ký tập trung (CloudWatch Logs): "
    )
    add_bullet(
        "Thiết lập cảnh báo tĩnh khi mức sử dụng CPU của máy chủ EC2 vượt ngưỡng 70% trong 1 phút, "
        "tự động kích hoạt thông báo Amazon SNS gửi email cảnh báo tới quản trị viên (huyngu127@gmail.com). "
        "Quy trình chuyển đổi trạng thái từ OK sang ALARM và tự động phục hồi đã được kiểm chứng thực tế qua bài ép tải CPU 100%.",
        bold_prefix="Cơ chế cảnh báo tự động (CloudWatch Alarms & SNS): "
    )
    add_bullet(
        "Xây dựng bảng điều khiển huylam-monitoring-dashboard tích hợp 4 loại widget chuyên sâu: "
        "trạng thái cảnh báo, chỉ số tải CPU trung bình, biểu đồ lưu lượng mạng và số lượng Healthy Host của Target Group.",
        bold_prefix="Bảng điều khiển giám sát trực quan (CloudWatch Dashboard): "
    )

    add_figure(
        "workshop/static/images/week5/11-cloudwatch-monitoring-dashboard.png",
        "Hình 3.16: Bảng điều khiển giám sát hệ thống thời gian thực trên Amazon CloudWatch Dashboard",
        width_cm=11.5
    )

    print("Hoàn thành cập nhật PHẦN 3: Bảng nền trắng, chữ đen, chuẩn hóa trích dẫn [1]-[11], bỏ double bullets.")
