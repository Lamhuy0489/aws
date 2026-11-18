# -*- coding: utf-8 -*-
import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from scripts.docx_helpers import (
    set_cell_margins, set_cell_shading, set_table_borders, make_table_robust,
    add_bookmark
)

def add_part2(doc, add_h1, add_h2, add_h3, add_body, add_bullet, add_figure):
    add_h1("PHẦN 2: MỤC TIÊU VÀ KẾ HOẠCH THỰC TẬP")

    add_h2("2.1. Mục tiêu học tập cá nhân gắn liền với Chuẩn đầu ra (CLOs)")
    add_body(
        "Căn cứ theo Đề cương chi tiết học phần Thực tập Tốt nghiệp của Khoa Công nghệ Thông tin – Trường Đại học Xây dựng Hà Nội (HUCE) [12] "
        "và yêu cầu chuẩn kỹ năng nghề nghiệp của chương trình AWS First Cloud AI Journey (FCAJ), sinh viên đã thiết lập bản kế hoạch học tập cá nhân "
        "nhằm đáp ứng trọn vẹn 3 nhóm Chuẩn đầu ra (Course Learning Outcomes - CLOs) cốt lõi của chương trình đào tạo Kỹ sư Công nghệ Thông tin:",
        indent=True
    )
    add_bullet(
        "Nắm vững và vận dụng linh hoạt các nguyên lý kiến trúc đám mây tiên tiến theo chuẩn AWS Well-Architected Framework [1]; "
        "hiểu rõ cơ chế hoạt động của mô hình mạng ảo cô lập (VPC [2]), cân bằng tải tầng ứng dụng (ALB [3]), bảo mật phân tầng (Security Group Chaining), "
        "mô hình tính toán phi máy chủ (Serverless Lambda [6]), cơ sở dữ liệu phi quan hệ (DynamoDB NoSQL [5]) và các giải pháp Trí tuệ nhân tạo đa phương thức (Vision Multimodal OCR [9], LLM [10]).",
        bold_prefix="Chuẩn đầu ra về Kiến thức (CLO 1): "
    )
    add_bullet(
        "Thành thạo kỹ năng thao tác trên giao diện AWS Management Console và tự động hóa qua giao diện dòng lệnh AWS CLI; "
        "có khả năng thiết kế, đóng gói container Docker, cấu hình tường lửa mạng đám mây, tích hợp cơ chế tự động kích hoạt hướng sự kiện (Event-Driven [6]), "
        "xây dựng ứng dụng web hiện đại (SPA), và thiết lập hệ thống giám sát cảnh báo sự cố tập trung bằng Amazon CloudWatch [7].",
        bold_prefix="Chuẩn đầu ra về Kỹ năng (CLO 2): "
    )
    add_bullet(
        "Rèn luyện tác phong kỷ luật kỹ thuật chuyên nghiệp, tinh thần làm chủ công việc (Ownership); "
        "tuân thủ nghiêm ngặt văn hóa quản trị chi phí đám mây FinOps (duy trì ngân sách 0.00 USD trong suốt 12 tuần); có năng lực phân tích nguyên nhân gốc rễ (RCA) "
        "để xử lý sự cố; và thành thạo kỹ năng viết tài liệu kỹ thuật, xây dựng workshop chuyên sâu phục vụ chuyển giao công nghệ [12].",
        bold_prefix="Chuẩn đầu ra về Năng lực tự chủ và Trách nhiệm (CLO 3): "
    )

    p_tbl_cap = doc.add_paragraph()
    p_tbl_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tbl_cap.paragraph_format.space_before = Pt(8)
    p_tbl_cap.paragraph_format.space_after = Pt(4)
    p_tbl_cap.paragraph_format.keep_with_next = True
    add_bookmark(p_tbl_cap, "tbl2_1")
    r = p_tbl_cap.add_run("Bảng 2.1: Mục tiêu học tập cá nhân đối chiếu với Chuẩn đầu ra (CLOs) của học phần")
    r.bold = True
    r.font.size = Pt(11)

    table_clo = doc.add_table(rows=4, cols=3)
    table_clo.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_clo.autofit = False
    set_table_borders(table_clo, color="000000", sz="4")
    make_table_robust(table_clo)

    clo_widths = [Cm(3.0), Cm(6.5), Cm(6.5)]
    headers_clo = ["Chuẩn đầu ra", "Mô tả chuẩn đầu ra học phần HUCE [12]", "Mục tiêu học tập & Minh chứng thực tế tại AWS"]
    for c_idx, h_text in enumerate(headers_clo):
        cell = table_clo.rows[0].cells[c_idx]
        cell.text = h_text
        set_cell_shading(cell, "FFFFFF")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        p.runs[0].bold = True
        p.runs[0].font.size = Pt(11)

    clos_data = [
        ("CLO 1 (Kiến thức)",
         "Vận dụng kiến thức khoa học máy tính, mạng máy tính và hệ thống phân tán để thiết kế giải pháp phần mềm doanh nghiệp.",
         "Thiết kế hoàn chỉnh kiến trúc đám mây 3 tầng Multi-AZ kết hợp Serverless Hybrid Document OCR chuẩn AWS Well-Architected Framework [1]."),
        ("CLO 2 (Kỹ năng)",
         "Làm chủ các công cụ lập trình, triển khai hệ thống, đóng gói container và tự động hóa quy trình kỹ nghệ phần mềm.",
         "Triển khai thực tế trên AWS: VPC [2], EC2, ALB [3], S3, DynamoDB [5], Lambda [6], Systems Manager [4], Docker; viết kịch bản deploy.sh tự động cập nhật hệ thống."),
        ("CLO 3 (Thái độ & Trách nhiệm)",
         "Thể hiện đạo đức nghề nghiệp, tính tự chủ, khả năng làm việc độc lập và quản lý rủi ro trong môi trường doanh nghiệp.",
         "Thực hiện kỷ luật FinOps nghiêm ngặt (0.00 USD phát sinh); duy trì 12 bài báo cáo nhật ký tuần; xây dựng Workshop song ngữ 12 chuyên đề trên GitHub Pages.")
    ]

    for r_idx, (clo, huce, aws_ev) in enumerate(clos_data):
        row = table_clo.rows[r_idx + 1]
        for c_idx, val in enumerate([clo, huce, aws_ev]):
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
            p.runs[0].font.size = Pt(10.5)
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)

    for row in table_clo.rows:
        for idx, width in enumerate(clo_widths):
            row.cells[idx].width = width

    add_h2("2.2. Kế hoạch công việc chi tiết qua 12 tuần thực tập")
    add_body(
        "Căn cứ theo Bản Kế hoạch học tập thực tập tốt nghiệp (mẫu TTTN-02) đã được Khoa Công nghệ Thông tin – Trường ĐH Xây dựng Hà Nội phê duyệt "
        "và nhật ký công việc thực tế (Worklog), lộ trình thực tập 12 tuần của sinh viên tại AWS Việt Nam được phân bổ khoa học, logic và thực hiện nghiêm túc như sau:",
        indent=True
    )

    p_tbl_cap2 = doc.add_paragraph()
    p_tbl_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tbl_cap2.paragraph_format.space_before = Pt(8)
    p_tbl_cap2.paragraph_format.space_after = Pt(4)
    p_tbl_cap2.paragraph_format.keep_with_next = True
    add_bookmark(p_tbl_cap2, "tbl2_2")
    r = p_tbl_cap2.add_run("Bảng 2.2: Kế hoạch làm việc và kết quả mong đợi chi tiết qua 12 tuần thực tập (chuẩn TTTN-02)")
    r.bold = True
    r.font.size = Pt(11)

    table_plan = doc.add_table(rows=13, cols=4)
    table_plan.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_plan.autofit = False
    set_table_borders(table_plan, color="000000", sz="4")
    make_table_robust(table_plan)

    plan_widths = [Cm(2.5), Cm(4.5), Cm(5.5), Cm(3.5)]
    headers_plan = ["Tuần / Thời gian", "Nội dung công việc trọng tâm", "Kết quả / Sản phẩm chuyển giao", "Minh chứng kỹ thuật"]
    for c_idx, h_text in enumerate(headers_plan):
        cell = table_plan.rows[0].cells[c_idx]
        cell.text = h_text
        set_cell_shading(cell, "FFFFFF")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.runs[0].bold = True
        p.runs[0].font.size = Pt(10.5)

    weeks_data = [
        ("Tuần 1\n(03/08–09/08)", "Làm quen với AWS: Thiết lập tài khoản, bảo mật Root MFA, tạo IAM User quản trị, cấu hình AWS Budgets và AWS CLI v2.", "Tài khoản bảo mật tuyệt đối, cấu hình ngân sách 0.00 USD, CLI kết nối thành công.", "Worklog Tuần 1, GitHub Pages Workshop."),
        ("Tuần 2\n(10/08–16/08)", "Lưu trữ đối tượng Amazon S3, S3 Bucket Policy (JSON), IAM Role phân quyền cho EC2, cài đặt Web Server tự động qua User Data.", "S3 Static Website hoạt động, máy chủ EC2 truy cập S3 an toàn không lộ Access Key.", "Worklog Tuần 2, ảnh Console IAM/S3."),
        ("Tuần 3\n(17/08–23/08)", "Thiết kế mạng ảo tùy biến Amazon VPC Multi-AZ (10.0.0.0/16, 4 Subnets [2]), gắn Internet Gateway, Route Tables, Security Groups, NACL.", "VPC tùy biến hoạt động ổn định, phân tách Public/Private Subnets chuẩn mực.", "Worklog Tuần 3, ảnh VPC Resource Map."),
        ("Tuần 4\n(24/08–30/08)", "Độ sẵn sàng cao và Co giãn linh hoạt: Cấu hình Two-Tier Security Groups, Launch Template, Target Group, Application Load Balancer [3], ASG.", "ALB cân bằng tải Round-Robin qua 2 AZs, Target Group đạt trạng thái 2/2 Healthy.", "Worklog Tuần 4, ảnh ALB DNS trên trình duyệt."),
        ("Tuần 5\n(31/08–06/09)", "Giám sát hệ thống với Amazon CloudWatch [7]: Thu thập CloudWatch Logs, cấu hình Alarm CPU >= 70% kích hoạt SNS gửi email, thiết kế Dashboard.", "Hệ thống cảnh báo tự động hoạt động, Dashboard huylam-monitoring-dashboard thời gian thực.", "Worklog Tuần 5, ảnh Stress Test CPU 100%."),
        ("Tuần 6\n(07/09–13/09)", "Quản trị máy chủ Zero Trust với AWS Systems Manager (SSM [4]): Fleet Manager, Session Manager (không mở cổng SSH), SSM Parameter Store mã hóa KMS.", "Kết nối shell Linux an toàn qua trình duyệt, quản lý tham số bí mật tập trung.", "Worklog Tuần 6, ảnh lệnh SSM get-parameter."),
        ("Tuần 7\n(14/09–20/09)", "Hạ tầng dưới dạng mã nguồn (IaC): Xây dựng CloudFormation Template (YAML) tự động hóa tạo VPC, EC2, UserData, thực thi Drift Detection.", "Ngăn xếp huylam-cfn-stack tạo thành công CREATE_COMPLETE, tự động hóa 100% triển khai.", "Worklog Tuần 7, mã nguồn Template YAML."),
        ("Tuần 8\n(21/09–27/09)", "Containerization và Điều phối Container: Đóng gói Docker container, đẩy image lên Amazon ECR, triển khai Amazon ECS Fargate phi máy chủ.", "Image lưu trữ an toàn trên ECR, ECS Service chạy thành công Task Apache mở cổng 80.", "Worklog Tuần 8, ảnh ECS Fargate Running."),
        ("Tuần 9\n(28/09–04/10)", "Nghiên cứu công nghệ và thiết kế kiến trúc đề tài tốt nghiệp: Nền tảng Serverless Hybrid Document OCR, Parsing & Technical Translation.", "Bản thiết kế kiến trúc phân tầng Fast-Path kết hợp Vision LLM và tài liệu đặc tả hệ thống.", "Worklog Tuần 9, sơ đồ kiến trúc draw.io."),
        ("Tuần 10\n(05/10–11/10)", "Khởi tạo hạ tầng đám mây cho đề tài: S3 bucket huylam-ocr-documents, DynamoDB table document_processing_jobs On-Demand [5], SSM Parameter [4].", "Kho lưu trữ và cơ sở dữ liệu NoSQL đám mây sẵn sàng tiếp nhận dữ liệu thực tế.", "Worklog Tuần 10, ảnh S3/DynamoDB Console."),
        ("Tuần 11\n(12/10–18/10)", "Phát triển động cơ ứng dụng lõi (PyMuPDF Fast-Path [8], Vision OCR [9], Translation, Exporters DOCX [11]/PDF); cấu hình Event-Driven S3 -> Lambda [6] -> DynamoDB [5].", "Ứng dụng xử lý bóc tách tài liệu tức thì, hàm Lambda huylam-ocr-processor phản hồi 214ms.", "Worklog Tuần 11, ảnh Lambda/DynamoDB Item."),
        ("Tuần 12\n(19/10–25/10)", "Triển khai kiến trúc 3 tầng trên AWS: EC2 huylam-ocr-web-server sau ALB Multi-AZ [3], chuỗi an ninh Chaining, nghiệm thu toàn trình qua Public DNS.", "Hệ thống live 100% trên Internet, xuất bản báo cáo tốt nghiệp và bộ minh chứng kỹ thuật.", "Worklog Tuần 12, URL ALB thật, Báo cáo DOCX.")
    ]

    for r_idx, (wk, task, res, ev) in enumerate(weeks_data):
        row = table_plan.rows[r_idx + 1]
        for c_idx, val in enumerate([wk, task, res, ev]):
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

    for row in table_plan.rows:
        for idx, width in enumerate(plan_widths):
            row.cells[idx].width = width

    add_h2("2.3. Bảng phân công nhiệm vụ và chỉ số đo lường hiệu quả (KPIs)")
    add_body(
        "Nhằm đảm bảo dự án thực tập hoàn thành đúng hạn với chất lượng kỹ thuật cao nhất, sinh viên làm việc dưới sự hướng dẫn chuyên môn "
        "trực tiếp của Technical Mentor AWS (anh Phạm Văn Phóng) và Giảng viên hướng dẫn HUCE (ThS. Lê Văn Minh). "
        "Tiến độ và kết quả thực tập được đo lường định lượng thông qua hệ thống chỉ số KPIs chặt chẽ như sau:",
        indent=True
    )

    p_tbl_cap3 = doc.add_paragraph()
    p_tbl_cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tbl_cap3.paragraph_format.space_before = Pt(8)
    p_tbl_cap3.paragraph_format.space_after = Pt(4)
    p_tbl_cap3.paragraph_format.keep_with_next = True
    add_bookmark(p_tbl_cap3, "tbl2_3")
    r = p_tbl_cap3.add_run("Bảng 2.3: Bảng chỉ số đo lường hiệu quả công việc cá nhân (KPIs)")
    r.bold = True
    r.font.size = Pt(11)

    table_kpi = doc.add_table(rows=6, cols=4)
    table_kpi.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_kpi.autofit = False
    set_table_borders(table_kpi, color="000000", sz="4")
    make_table_robust(table_kpi)

    kpi_widths = [Cm(1.5), Cm(5.0), Cm(4.5), Cm(5.0)]
    headers_kpi = ["STT", "Chỉ số KPI", "Chỉ tiêu cam kết", "Kết quả thực tế đạt được"]
    for c_idx, h_text in enumerate(headers_kpi):
        cell = table_kpi.rows[0].cells[c_idx]
        cell.text = h_text
        set_cell_shading(cell, "FFFFFF")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.runs[0].bold = True
        p.runs[0].font.size = Pt(10.5)

    kpis_data = [
        ("1", "Mức độ hoàn thành các bài thực hành AWS Cloud", "100% các bài Lab cốt lõi đạt trạng thái hoạt động trên môi trường thật", "Đạt 100% (Hoàn thành trọn vẹn 12 chuyên đề thực hành có ảnh kiểm chứng)."),
        ("2", "Tính sẵn sàng và độ ổn định của ứng dụng Capstone", "Hệ thống live trên Internet qua ALB, Target Group đạt Healthy", "Đạt 100% (ALB public DNS hoạt động ổn định, 1/1 Target Healthy)."),
        ("3", "Hiệu năng bóc tách tài liệu số (Fast-Path)", "Thời gian xử lý < 0.5 giây/trang, chi phí tính toán 0 đồng", "Vượt chỉ tiêu: Đạt 0.1s – 0.3s/trang (nhanh gấp 5 lần cam kết)."),
        ("4", "Kỷ luật quản trị chi phí đám mây (FinOps Zero-Breach)", "Chi phí phát sinh duy trì trong ngưỡng AWS Free Tier (0.00 USD)", "Đạt 100% (Không phát sinh bất kỳ khoản phí vượt ngưỡng nào ngoài ý muốn)."),
        ("5", "Chất lượng tài liệu bàn giao và báo cáo thực tập", "Website Workshop đầy đủ 12 tuần và Báo cáo tốt nghiệp chi tiết > 40 trang", "Vượt chỉ tiêu: Website Hugo song ngữ trên GitHub Pages và Báo cáo Word 50+ trang.")
    ]

    for r_idx, (stt, kpi, tgt, act) in enumerate(kpis_data):
        row = table_kpi.rows[r_idx + 1]
        for c_idx, val in enumerate([stt, kpi, tgt, act]):
            cell = row.cells[c_idx]
            cell.text = val
            set_cell_shading(cell, "FFFFFF")
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            if c_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.runs[0].bold = True
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(10)
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)

    for row in table_kpi.rows:
        for idx, width in enumerate(kpi_widths):
            row.cells[idx].width = width

    print("Hoàn thành cập nhật PHẦN 2: Bảng chữ đen nền trắng thuần khiết, bỏ màu xám.")
