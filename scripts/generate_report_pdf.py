import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# 1. Register Vietnamese Unicode Fonts
font_dir = '/System/Library/Fonts/Supplemental'
pdfmetrics.registerFont(TTFont('Arial', os.path.join(font_dir, 'Arial.ttf')))
pdfmetrics.registerFont(TTFont('Arial-Bold', os.path.join(font_dir, 'Arial Bold.ttf')))
pdfmetrics.registerFont(TTFont('Arial-Italic', os.path.join(font_dir, 'Arial Italic.ttf')))
pdfmetrics.registerFont(TTFont('Arial-BoldItalic', os.path.join(font_dir, 'Arial Bold Italic.ttf')))

pdfmetrics.registerFontFamily(
    'Arial',
    normal='Arial',
    bold='Arial-Bold',
    italic='Arial-Italic',
    boldItalic='Arial-BoldItalic'
)

# 2. Numbered Canvas for Header/Footer
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Arial", 8)
        self.setFillColor(colors.HexColor("#4B5563"))
        
        # Header (Pages 2+)
        if self._pageNumber > 1:
            self.drawString(45, A4[1] - 30, "AWS FIRST CLOUD JOURNEY BOOTCAMP 2026 | BÁO CÁO THỰC TẬP TỐT NGHIỆP")
            self.drawRightString(A4[0] - 45, A4[1] - 30, "Serverless Hybrid OCR Platform on AWS")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(45, A4[1] - 34, A4[0] - 45, A4[1] - 34)

        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(45, 38, A4[0] - 45, 38)
        
        self.drawString(45, 26, "Học viên: Lâm Quang Huy (MSSV: 0212267) - AWS Account: 677994024390 (huylam)")
        page_text = f"Trang {self._pageNumber} / {page_count}"
        self.drawRightString(A4[0] - 45, 26, page_text)
        self.restoreState()

def build_pdf(filename="Bao_Cao_Thuc_Tap_AWS_Lam_Quang_Huy.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=45,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#1E293B")     # Slate 800
    c_aws_blue = colors.HexColor("#0F172A")    # Deep Navy
    c_accent = colors.HexColor("#D97706")      # Amber / Gold accent
    c_text = colors.HexColor("#1F2937")        # Gray 800
    c_muted = colors.HexColor("#4B5563")       # Gray 600
    c_bg_light = colors.HexColor("#F8FAFC")    # Slate 50
    c_border = colors.HexColor("#CBD5E1")      # Slate 300

    # Typography styles
    styles.add(ParagraphStyle(
        'DocSuperTitle',
        fontName='Arial-Bold',
        fontSize=10,
        leading=14,
        textColor=c_accent,
        alignment=0,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'DocTitle',
        fontName='Arial-Bold',
        fontSize=17,
        leading=21,
        textColor=c_aws_blue,
        alignment=0,
        spaceAfter=5
    ))
    styles.add(ParagraphStyle(
        'DocSubTitle',
        fontName='Arial',
        fontSize=10.5,
        leading=14.5,
        textColor=c_muted,
        alignment=0,
        spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        'SecHeading',
        fontName='Arial-Bold',
        fontSize=12,
        leading=16,
        textColor=c_aws_blue,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'BodyCustom',
        fontName='Arial',
        fontSize=8.8,
        leading=13,
        textColor=c_text,
        spaceAfter=5
    ))
    styles.add(ParagraphStyle(
        'TableHead',
        fontName='Arial-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.white,
        alignment=0
    ))
    styles.add(ParagraphStyle(
        'TableCell',
        fontName='Arial',
        fontSize=8,
        leading=11,
        textColor=c_text
    ))
    styles.add(ParagraphStyle(
        'TableCellBold',
        fontName='Arial-Bold',
        fontSize=8,
        leading=11,
        textColor=c_text
    ))
    styles.add(ParagraphStyle(
        'CalloutText',
        fontName='Arial',
        fontSize=8.5,
        leading=12.5,
        textColor=c_primary
    ))

    story = []

    # ==================== TRANG 1 ====================
    story.append(Paragraph("AWS FIRST CLOUD JOURNEY BOOTCAMP 2026 | BÁO CÁO THỰC TẬP TỐT NGHIỆP", styles['DocSuperTitle']))
    story.append(Paragraph("Serverless Hybrid Document OCR, Parsing & Technical Translation Platform on AWS", styles['DocTitle']))
    story.append(Paragraph("Đề tài: Nền tảng Bóc tách, OCR Lai & Dịch thuật Tài liệu Kỹ thuật Đa tầng trên Điện toán Đám mây AWS", styles['DocSubTitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=0, spaceAfter=8))

    # Student Info Table
    info_data = [
        [
            Paragraph("<b>Học viên:</b> Lâm Quang Huy", styles['TableCell']),
            Paragraph("<b>Mã sinh viên:</b> 0212267", styles['TableCell']),
            Paragraph("<b>Cơ sở đào tạo:</b> ĐH Xây dựng Hà Nội (HUCE)", styles['TableCell'])
        ],
        [
            Paragraph("<b>Lớp chuyên ngành:</b> 67CS - CNTT", styles['TableCell']),
            Paragraph("<b>AWS Account ID:</b> 677994024390", styles['TableCell']),
            Paragraph("<b>Account Name:</b> huylam (ap-southeast-1)", styles['TableCell'])
        ],
        [
            Paragraph("<b>Live ALB URL:</b> huylam-ocr-alb-1284818160.ap-southeast-1.elb.amazonaws.com", styles['TableCell']),
            Paragraph("<b>Workshop Site:</b> Lamhuy0489.github.io/workshop", styles['TableCell']),
            Paragraph("<b>GitHub:</b> github.com/Lamhuy0489/aws", styles['TableCell'])
        ]
    ]
    info_table = Table(info_data, colWidths=[175, 150, 180])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('BOX', (0,0), (-1,-1), 0.8, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.4, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 8))

    # 1. Executive Summary
    story.append(Paragraph("1. Tóm Tắt Dự Án (Executive Summary)", styles['SecHeading']))
    p1 = (
        "<b>Serverless Hybrid Document OCR, Parsing & Technical Translation Platform on AWS</b> là nền tảng điện toán đám mây cấp doanh nghiệp "
        "được thiết kế nhằm giải quyết bài toán số hóa, bóc tách cấu trúc và chuyển ngữ các tài liệu kỹ thuật phức tạp (hồ sơ thiết kế, hợp đồng, "
        "báo cáo tài chính, bài báo khoa học PDF/ảnh scan đa ngôn ngữ) với độ chính xác cao, thời gian phản hồi tức thì và chi phí vận hành tối ưu tuyệt đối (0.00 USD trong suốt kỳ thực tập). "
        "Hệ thống vận hành thực tế qua Application Load Balancer Multi-AZ công khai Internet kết nối máy chủ EC2 Gunicorn, tích hợp dịch vụ lưu trữ bền vững S3, "
        "cơ sở dữ liệu NoSQL DynamoDB On-Demand, quản trị cấu hình bảo mật AWS Systems Manager Parameter Store, và xác thực danh tính liên kết Amazon Cognito với Google OAuth 2.0."
    )
    story.append(Paragraph(p1, styles['BodyCustom']))

    # Callout Box: 3 Core Pillars
    callout_data = [[
        Paragraph(
            "<b>Ba Trụ Cột Đột Phá Cốt Lõi Của Giải Pháp:</b><br/>"
            "1. <b>Two-Stage Hybrid Engine:</b> Tầng 1 Fast-Path Native (PyMuPDF) trích xuất trực tiếp văn bản số trong 0.1s - 0.3s/trang với chi phí 0 USD (xử lý 80%+ tài liệu văn phòng). "
            "Tầng 2 Selective OCR tự động định tuyến trang scan/ảnh tới cụm GPU Qwen2.5-VL hoặc Google Gemini Flash với cơ chế tự phục hồi Failover an toàn.<br/>"
            "2. <b>Markdown-Preserving Technical Translation Engine:</b> Dịch thuật tài liệu kỹ thuật bảo toàn 100% cú pháp Markdown, bảng biểu số liệu, công thức toán LaTeX.<br/>"
            "3. <b>Multi-Format Export Engine:</b> Xuất bản đa định dạng sang Markdown (.md), Microsoft Word (.docx chuẩn quốc tế), và PDF in ấn chuẩn A4.",
            styles['CalloutText']
        )
    ]]
    callout_table = Table(callout_data, colWidths=[505])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#F59E0B")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 8))

    # 1.1 Highlights Box
    highlights_data = [[
        Paragraph(
            "<b>Điểm Nhấn Vận Hành Thực Tế & Nghiệm Thu:</b><br/>"
            "• <b>Live Production URL:</b> <code>http://huylam-ocr-alb-1284818160.ap-southeast-1.elb.amazonaws.com</code> (ALB Listener HTTP 80 &rarr; Target Group cổng 5000).<br/>"
            "• <b>Cổng Đăng Nhập Doanh Nghiệp:</b> Tích hợp SSO Google OAuth 2.0 qua Amazon Cognito User Pool (50,000 MAU Always Free).<br/>"
            "• <b>Bảo Mật Phân Tầng:</b> Security Group Chaining cô lập máy chủ EC2 khỏi Internet; quản trị Shell từ xa qua SSM Session Manager (zero open SSH ports).<br/>"
            "• <b>FinOps Zero Cost:</b> Chi phí vận hành toàn bộ vòng đời thực tập được kiểm soát ở mức 0.00 USD.",
            styles['CalloutText']
        )
    ]]
    highlights_table = Table(highlights_data, colWidths=[505])
    highlights_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#3B82F6")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(highlights_table)

    story.append(PageBreak())

    # ==================== TRANG 2 ====================
    # 2. Cloud Infrastructure Architecture
    story.append(Paragraph("2. Kiến Trúc Hạ Tầng Đám Mây AWS (Enterprise Three-Tier Architecture)", styles['SecHeading']))
    p2 = (
        "Hệ thống tuân thủ nghiêm ngặt chuẩn <b>AWS Well-Architected Framework</b>, kết hợp giữa mô hình mạng doanh nghiệp 3 tầng "
        "(Three-Tier Enterprise Cloud Networking) và kiến trúc phi máy chủ hướng sự kiện (Event-Driven Serverless):"
    )
    story.append(Paragraph(p2, styles['BodyCustom']))

    infra_headers = [Paragraph("<b>Tầng Kiến Trúc</b>", styles['TableHead']),
                     Paragraph("<b>Tài Nguyên AWS</b>", styles['TableHead']),
                     Paragraph("<b>Định Danh Kỹ Thuật (ID / ARN)</b>", styles['TableHead']),
                     Paragraph("<b>Vai Trò & Cấu Hình An Ninh</b>", styles['TableHead'])]
    
    infra_rows = [
        infra_headers,
        [
            Paragraph("<b>Phân phối & Cân bằng tải</b>", styles['TableCellBold']),
            Paragraph("Application Load Balancer (ALB)", styles['TableCell']),
            Paragraph("<code>huylam-ocr-alb</code>", styles['TableCell']),
            Paragraph("Multi-AZ (1a & 1b), Listener HTTP:80, Health check <code>/login</code> (Healthy 1/1).", styles['TableCell'])
        ],
        [
            Paragraph("<b>Chuỗi an ninh phân tầng</b>", styles['TableCellBold']),
            Paragraph("Security Group Chaining", styles['TableCell']),
            Paragraph("<code>huylam-alb-sg</code><br/>&rarr; <code>huylam-web-sg</code>", styles['TableCell']),
            Paragraph("ALB SG mở cổng 80 cho Internet. Web SG chỉ mở cổng 5000 cho nguồn từ ALB SG, cô lập EC2.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Máy chủ ứng dụng</b>", styles['TableCellBold']),
            Paragraph("Amazon EC2 (t2.micro)", styles['TableCell']),
            Paragraph("<code>i-0566e1eedaacea52d</code><br/>(huylam-ocr-web-server)", styles['TableCell']),
            Paragraph("Amazon Linux 2023, IP 10.0.8.15. Chạy daemon systemd Gunicorn cổng 5000. Quản trị qua SSM.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Lưu trữ đối tượng</b>", styles['TableCellBold']),
            Paragraph("Amazon S3 Bucket", styles['TableCell']),
            Paragraph("<code>huylam-ocr-documents-ap-southeast-1</code>", styles['TableCell']),
            Paragraph("Độ bền 99.999999999%. Phân cấp thư mục <code>uploads/</code> và <code>outputs/</code>. Mã hóa SSE-S3.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Cơ sở dữ liệu trạng thái</b>", styles['TableCellBold']),
            Paragraph("Amazon DynamoDB", styles['TableCell']),
            Paragraph("<code>document_processing_jobs</code>", styles['TableCell']),
            Paragraph("NoSQL On-Demand (PAY_PER_REQUEST). Partition Key <code>job_id</code>, Sort Key <code>created_at</code>.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Quản trị cấu hình bảo mật</b>", styles['TableCellBold']),
            Paragraph("SSM Parameter Store", styles['TableCell']),
            Paragraph("<code>/huylam-ocr/config</code>", styles['TableCell']),
            Paragraph("Loại <code>SecureString</code> mã hóa KMS. Quản trị API key tập trung, không hardcode mã nguồn.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Quản lý danh tính & SSO</b>", styles['TableCellBold']),
            Paragraph("Amazon Cognito User Pool", styles['TableCell']),
            Paragraph("<code>huylam-ocr-user-pool</code><br/>(User pool - qp0rmn)", styles['TableCell']),
            Paragraph("Federated IdP Google OAuth 2.0. Miền <code>kc4iwg.auth.ap-southeast-1.amazoncognito.com</code>.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Tự động hóa phi máy chủ</b>", styles['TableCellBold']),
            Paragraph("AWS Lambda (Python 3.11)", styles['TableCell']),
            Paragraph("<code>huylam-ocr-processor</code>", styles['TableCell']),
            Paragraph("S3 Event Notification kích hoạt Lambda tạo bản ghi DynamoDB tức thì trong 214 ms.", styles['TableCell'])
        ]
    ]

    t_infra = Table(infra_rows, colWidths=[85, 105, 125, 190])
    t_infra.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('GRID', (0,0), (-1,-1), 0.4, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_infra)
    story.append(Spacer(1, 10))

    # 3. Two-Stage Hybrid Engine
    story.append(Paragraph("3. Động Cơ Xử Lý Bóc Tách Lai Đa Tầng (Two-Stage Hybrid Engine)", styles['SecHeading']))
    p3 = (
        "Nền tảng triển khai giải thuật lai phân tầng nhằm tối ưu hóa triệt để hiệu năng và kinh tế đám mây:<br/>"
        "• <b>Tầng 1 - Fast-Path Native Extraction:</b> Đối với tài liệu định dạng PDF có sẵn lớp ký tự (chiếm hơn 80% tài liệu kỹ thuật, báo cáo, hợp đồng), "
        "PyMuPDF trực tiếp bóc tách văn bản, tọa độ bảng và phân đoạn trang chỉ mất <b>0.1s - 0.3s/trang</b> với chi phí 0.00 USD.<br/>"
        "• <b>Tầng 2 - Selective Vision OCR:</b> Chỉ những trang có mật độ văn bản thấp hơn ngưỡng hoặc là ảnh quét scan mới được kích hoạt bộ điều phối OCR. "
        "Hệ thống tích hợp mô hình thị giác AI Kaggle Qwen2.5-VL ($0) mở qua Cloudflare Tunnel, tự động chuyển đổi dự phòng (Failover) sang Google Gemini 3.6 Flash / Flash Lite "
        "kèm thuật toán xoay vòng API Keys tự động (Key Tour Manager) và tùy chọn AWS Bedrock Nova.<br/>"
        "• <b>Chuyển ngữ bảo toàn Markdown & Đa định dạng:</b> Hệ thống dịch thuật chuyên ngành bảo toàn 100% cú pháp tiêu đề, ma trận bảng biểu số liệu, "
        "công thức toán học, và hỗ trợ xuất bản tức thì sang tệp Microsoft Word (.docx) và PDF in ấn."
    )
    story.append(Paragraph(p3, styles['BodyCustom']))

    story.append(PageBreak())

    # ==================== TRANG 3 ====================
    # 4. Benchmark Empirical Metrics
    story.append(Paragraph("4. Bảng Số Liệu Đo Kiểm Thực Nghiệm (Benchmark Empirical Metrics)", styles['SecHeading']))
    
    bench_headers = [
        Paragraph("<b>Hạng Mục Kiểm Thử</b>", styles['TableHead']),
        Paragraph("<b>Mẫu Dữ Liệu</b>", styles['TableHead']),
        Paragraph("<b>Động Cơ Thực Thi</b>", styles['TableHead']),
        Paragraph("<b>Thời Gian Xử Lý</b>", styles['TableHead']),
        Paragraph("<b>Chi Phí Vận Hành</b>", styles['TableHead']),
        Paragraph("<b>Đánh Giá Kết Quả</b>", styles['TableHead'])
    ]
    bench_rows = [
        bench_headers,
        [
            Paragraph("Bóc tách văn bản số", styles['TableCellBold']),
            Paragraph("<code>cv.pdf</code> (1 trang)", styles['TableCell']),
            Paragraph("Fast-Path Native", styles['TableCell']),
            Paragraph("<b>0.31 giây</b>", styles['TableCellBold']),
            Paragraph("0.00 USD", styles['TableCell']),
            Paragraph("Hoàn hảo, tức thì", styles['TableCell'])
        ],
        [
            Paragraph("Bóc tách bài báo KH", styles['TableCellBold']),
            Paragraph("<code>28_Bai_Bao.pdf</code> (11 trang)", styles['TableCell']),
            Paragraph("Fast-Path Native", styles['TableCell']),
            Paragraph("<b>3.07 giây</b> (~0.28s/trang)", styles['TableCellBold']),
            Paragraph("0.00 USD", styles['TableCell']),
            Paragraph("Bảo toàn bảng biểu", styles['TableCell'])
        ],
        [
            Paragraph("Bóc tách ảnh quét scan", styles['TableCellBold']),
            Paragraph("Ảnh scan biểu mẫu", styles['TableCell']),
            Paragraph("Kaggle Qwen2.5-VL / Gemini", styles['TableCell']),
            Paragraph("<b>2.54 giây</b>", styles['TableCellBold']),
            Paragraph("0.00 USD (Free Tier)", styles['TableCell']),
            Paragraph("Tiếng Việt có dấu 100%", styles['TableCell'])
        ],
        [
            Paragraph("Tùy chọn AWS Native", styles['TableCellBold']),
            Paragraph("Ảnh scan hóa đơn", styles['TableCell']),
            Paragraph("Amazon Bedrock (Nova)", styles['TableCell']),
            Paragraph("<b>4.61s - 6.99s</b>", styles['TableCellBold']),
            Paragraph("Pay-as-you-go", styles['TableCell']),
            Paragraph("Bóc tách chính xác", styles['TableCell'])
        ],
        [
            Paragraph("Dịch thuật bảo toàn MD", styles['TableCellBold']),
            Paragraph("<code>cv.pdf</code> (Anh &rarr; Việt)", styles['TableCell']),
            Paragraph("Gemini Flash Translator", styles['TableCell']),
            Paragraph("<b>2.80 giây</b>", styles['TableCellBold']),
            Paragraph("0.00 USD (Free Tier)", styles['TableCell']),
            Paragraph("Giữ 100% format bảng", styles['TableCell'])
        ],
        [
            Paragraph("Xuất Word (.docx)", styles['TableCellBold']),
            Paragraph("Tệp kết quả dịch", styles['TableCell']),
            Paragraph("DocxExporter Module", styles['TableCell']),
            Paragraph("<b>0.15 giây</b>", styles['TableCellBold']),
            Paragraph("0.00 USD", styles['TableCell']),
            Paragraph("Tệp 38.2 KB mở chuẩn", styles['TableCell'])
        ],
        [
            Paragraph("Kích hoạt S3 &rarr; Lambda", styles['TableCellBold']),
            Paragraph("Upload vào <code>uploads/</code>", styles['TableCell']),
            Paragraph("Lambda (Python 3.11)", styles['TableCell']),
            Paragraph("<b>214 - 257 ms</b>", styles['TableCellBold']),
            Paragraph("0.00 USD (Free Tier)", styles['TableCell']),
            Paragraph("Tạo record DynamoDB", styles['TableCell'])
        ],
        [
            Paragraph("Độ trễ ALB Production", styles['TableCellBold']),
            Paragraph("Public DNS Ingress", styles['TableCell']),
            Paragraph("Application Load Balancer", styles['TableCell']),
            Paragraph("<b>15 - 25 ms</b>", styles['TableCellBold']),
            Paragraph("0.00 USD (Free Tier)", styles['TableCell']),
            Paragraph("HTTP 200 OK mượt mà", styles['TableCell'])
        ]
    ]

    t_bench = Table(bench_rows, colWidths=[90, 85, 100, 75, 75, 80])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('GRID', (0,0), (-1,-1), 0.4, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 8))

    # 5. 12-Week Roadmap Summary
    story.append(Paragraph("5. Lộ Trình Triển Khai 12 Tuần Thực Tập (Worklog Milestones)", styles['SecHeading']))
    
    road_headers = [
        Paragraph("<b>Giai Đoạn / Tuần</b>", styles['TableHead']),
        Paragraph("<b>Mục Tiêu Trọng Tâm</b>", styles['TableHead']),
        Paragraph("<b>Dịch Vụ AWS & Sản Phẩm Đạt Được</b>", styles['TableHead'])
    ]
    road_rows = [
        road_headers,
        [
            Paragraph("<b>Tuần 1 - 2</b><br/>(Khởi đầu)", styles['TableCellBold']),
            Paragraph("Thiết lập môi trường, an toàn tài khoản AWS, quản trị chi phí", styles['TableCell']),
            Paragraph("Kích hoạt MFA Root, IAM Users/Groups, cấu hình AWS Budgets khóa chi phí, cài đặt AWS CLI v2.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Tuần 3 - 4</b><br/>(Hạ tầng cốt lõi)", styles['TableCellBold']),
            Paragraph("Mạng ảo VPC phân tầng, máy chủ ảo EC2, lưu trữ Amazon S3", styles['TableCell']),
            Paragraph("Khởi tạo VPC, Public/Private Subnets, Internet Gateway, IAM Role S3 Full Access, kết nối máy chủ Linux.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Tuần 5 - 6</b><br/>(Giám sát & Mã hóa)", styles['TableCellBold']),
            Paragraph("Hạ tầng dạng mã (IaC), giám sát CloudWatch và mã hóa KMS", styles['TableCell']),
            Paragraph("Tự động hóa với AWS CloudFormation, cấu hình CloudWatch Alarms, thiết lập khóa mã hóa AWS KMS.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Tuần 7 - 8</b><br/>(Containerization)", styles['TableCellBold']),
            Paragraph("Đóng gói ứng dụng Docker Container và lưu trữ Amazon ECR", styles['TableCell']),
            Paragraph("Dockerfile OCI Container đa tầng trên Python 3.11, kho ECR Repository lưu trữ và kiểm soát phiên bản.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Tuần 9 - 10</b><br/>(Serverless & Dữ liệu)", styles['TableCellBold']),
            Paragraph("Thiết kế Serverless, DynamoDB On-Demand, SSM Parameter Store", styles['TableCell']),
            Paragraph("Bucket S3 với CORS an toàn, bảng DynamoDB <code>document_processing_jobs</code>, tham số mã hóa <code>/huylam-ocr/config</code>.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Tuần 11</b><br/>(Event-Driven)", styles['TableCellBold']),
            Paragraph("Đo kiểm Benchmark thực nghiệm, S3 Event Notification & Lambda", styles['TableCell']),
            Paragraph("Kiến trúc hướng sự kiện tự động S3 &rarr; Lambda &rarr; DynamoDB &rarr; CloudWatch phản hồi trong 214 ms.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Tuần 12</b><br/>(Production Live)", styles['TableCellBold']),
            Paragraph("Triển khai kiến trúc mạng 3 tầng, cân bằng tải ALB, cấp link thật", styles['TableCell']),
            Paragraph("ALB Multi-AZ công khai Internet, chuỗi Security Group Chaining, Gunicorn systemd, tích hợp Cognito Google SSO.", styles['TableCell'])
        ]
    ]

    t_road = Table(road_rows, colWidths=[80, 195, 230])
    t_road.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('GRID', (0,0), (-1,-1), 0.4, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_road)
    story.append(Spacer(1, 8))

    # 6. FinOps & Conclusion
    story.append(Paragraph("6. Quản Trị Tài Chính FinOps & Cam Kết Tốt Nghiệp", styles['SecHeading']))
    p4 = (
        "<b>Chiến Lược Tối Ưu Chi Phí 0.00 USD (FinOps Governance):</b> "
        "Toàn bộ các dịch vụ cốt lõi đều được thiết kế tận dụng triệt để hạn ngạch AWS Free Tier và cơ chế Serverless On-Demand: "
        "DynamoDB không tính cước khi nhàn rỗi, Lambda trong giới hạn 1 triệu request miễn phí/tháng, Cognito miễn phí tới 50,000 MAU. "
        "Tầng bóc tách Fast-Path bản địa triệt tiêu 80%+ chi phí GPU suy luận thị giác. "
        "Học viên có kế hoạch xóa ALB và dừng máy chủ EC2 khi hoàn tất phiên nghiệm thu để đảm bảo không phát sinh chi phí ngoài ý muốn.<br/>"
        "<b>Kết luận:</b> Đề tài đã hoàn thành xuất sắc 100% mục tiêu đề ra, khẳng định năng lực làm chủ kiến trúc điện toán đám mây AWS, "
        "kết hợp hài hòa giữa kỹ năng hạ tầng DevOps, mô hình trí tuệ nhân tạo thị giác AI và văn hóa kỹ thuật chuẩn mực."
    )
    story.append(Paragraph(p4, styles['BodyCustom']))

    # Build the document using NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Xuat file PDF thanh cong: {filename}")

if __name__ == '__main__':
    build_pdf()
