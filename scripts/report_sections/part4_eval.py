# -*- coding: utf-8 -*-
import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def add_part4(doc, add_h1, add_h2, add_h3, add_body, add_bullet, add_figure):
    add_h1("PHẦN 4: PHÂN TÍCH, ĐÁNH GIÁ VÀ ĐỀ XUẤT")

    add_h2("4.1. Nhận xét về Quy trình Công việc và Giải pháp Kỹ thuật Đã Triển Khai")
    add_body(
        "Nhìn lại toàn bộ quá trình 12 tuần thực tập tại AWS Việt Nam, quy trình làm việc được thiết lập bài bản, có sự gắn kết chặt chẽ "
        "giữa lý thuyết kiến trúc và thực hành thực chiến trên đám mây [1]. Về mặt giải pháp kỹ thuật, hệ thống Serverless Hybrid Document OCR "
        "đã chứng minh được tính đúng đắn và hiệu quả vượt trội so với các phương pháp tiếp cận truyền thống:",
        indent=True
    )
    add_bullet(
        "Việc phân loại tài liệu ngay từ cổng nạp thành văn bản số (Fast-Path [8]) "
        "và ảnh scan (Vision Multimodal [9], [10]) là một quyết định kiến trúc mang tính đột phá. Hệ thống đã giải quyết được hơn 80% khối lượng tài liệu văn phòng "
        "với tốc độ dưới 0.3 giây/trang và chi phí hoàn toàn bằng 0, chỉ kích hoạt các mô hình thị giác nhân tạo nặng nề khi thực sự cần thiết.",
        bold_prefix="Sự tối ưu của Kiến trúc Phân tầng Lai (Hybrid Multi-Tier): "
    )
    add_bullet(
        "Việc kết hợp giữa Amazon VPC Multi-AZ [2], Application Load Balancer [3] và chuỗi tường lửa "
        "Security Group Chaining đã giúp cô lập tuyệt đối máy chủ ứng dụng khỏi mạng Internet công cộng. Cùng với việc quản trị máy chủ qua "
        "AWS Systems Manager Session Manager (không mở cổng SSH 22 [4]) và quản lý bí mật qua Parameter Store [4], hệ thống đáp ứng trọn vẹn "
        "các tiêu chuẩn an ninh thông tin khắt khe nhất của môi trường doanh nghiệp.",
        bold_prefix="Tính an ninh vững chắc của Hạ tầng Mạng Zero-Trust: "
    )
    add_bullet(
        "Mô hình S3 Event Notification kết hợp AWS Lambda và DynamoDB [5], [6] cho phép hệ thống "
        "xử lý tài liệu nền không đồng bộ với độ trễ cực thấp (214 ms), không làm nghẽn máy chủ web và tự động co giãn theo nhu cầu thực tế.",
        bold_prefix="Tính linh hoạt của Kiến trúc Phi máy chủ Hướng sự kiện: "
    )

    add_h2("4.2. Các Khó khăn, Thách thức Thực tế và Giải pháp Khắc phục")
    add_body(
        "Trong quá trình hiện thực hóa giải pháp từ bản thiết kế trên giấy lên môi trường AWS Cloud thật, sinh viên đã đối mặt và vượt qua "
        "ba thách thức kỹ thuật lớn:",
        indent=True
    )
    add_bullet(
        "Khi người dùng tải lên các tệp tài liệu PDF nhiều trang (trên 15 trang), quá trình xử lý đồng bộ qua yêu cầu HTTP thường xuyên vượt quá giới hạn cứng 29 giây của API Gateway, dẫn tới lỗi đứt kết nối (504 Gateway Timeout). "
        "Giải pháp khắc phục: Sinh viên đã tái cấu trúc quy trình xử lý sang mô hình bất đồng bộ (Asynchronous Event-Driven Pipeline [6]). "
        "Tệp tài liệu được tải trực tiếp lên Amazon S3, kích hoạt AWS Lambda xử lý nền và lưu trạng thái vào Amazon DynamoDB [5], "
        "giúp giao diện người dùng phản hồi tức thì và loại bỏ hoàn toàn nguy cơ timeout.",
        bold_prefix="Thách thức về giới hạn thời gian chờ Timeout 29 giây của API Gateway: "
    )
    add_bullet(
        "Các tệp PDF phức tạp chứa bảng biểu nhiều dòng, căn lề không đồng nhất thường bị các thuật toán OCR thông thường làm rối loạn thứ tự cột. "
        "Giải pháp khắc phục: Xây dựng thuật toán phân tích tọa độ hình học (Bounding Box Analysis) trong FastNativeParser [8] để gom cụm dòng "
        "và phân tách ranh giới cột chuẩn xác; đồng thời tích hợp prompt kỹ thuật định hình cấu trúc bảng Markdown cho tầng Vision LLM [9], [10].",
        bold_prefix="Thách thức về xử lý đứt gãy cấu trúc bảng biểu và ký tự tiếng Việt có dấu: "
    )
    add_bullet(
        "Khi xử lý tài liệu lớn, việc gọi liên tục một API Key dễ dẫn tới lỗi HTTP 429 (Too Many Requests) hoặc tài khoản bị giới hạn chính sách. "
        "Giải pháp khắc phục: Phát triển module Quản lý Tour Xoay Key (Round-Robin Key Tour Manager). Hệ thống tự động phân bổ tải luân phiên "
        "qua danh sách các API Keys, tự động phát hiện key hỏng hoặc hết hạn mức để loại bỏ khỏi vòng xoay và chuyển tiếp sang key kế tiếp ngay lập tức.",
        bold_prefix="Thách thức về rào cản hạn ngạch (Rate Limit / Quota) của các nhà cung cấp API: "
    )

    add_h2("4.3. Phân tích Mối liên hệ Biện chứng Giữa Lý thuyết và Thực tế")
    add_body(
        "Kỳ thực tập tại AWS Việt Nam đã tạo cơ hội tuyệt vời để sinh viên đối chiếu, kiểm chứng và củng cố sâu sắc các khối kiến thức nền tảng "
        "đã được giảng dạy tại Trường Đại học Xây dựng Hà Nội (HUCE) [12]:",
        indent=True
    )
    add_bullet(
        "Các khái niệm lý thuyết về mô hình tham chiếu OSI 7 tầng, phân dải địa chỉ IP theo CIDR, chia mạng con "
        "(Subnetting), bảng định tuyến (Routing Table) và cơ chế tường lửa trạng thái (Stateful vs Stateless) đã được hiện thực hóa trực tiếp "
        "khi thiết kế mạng Amazon VPC tùy biến, cổng Internet Gateway, và ma trận Security Group Chaining [2], [3].",
        bold_prefix="Môn Mạng máy tính & An ninh mạng: "
    )
    add_bullet(
        "Lý thuyết về quản trị tiến trình (Process), luồng (Thread), quản lý bộ nhớ ảo, quyền người dùng Linux, "
        "và cơ chế dịch vụ nền (Daemon) đã được vận dụng khi cấu hình máy chủ Gunicorn chạy qua systemd daemon (huylam-ocr.service) trên Amazon Linux 2023.",
        bold_prefix="Môn Hệ điều hành & Kiến trúc máy tính: "
    )
    add_bullet(
        "Sự đối chiếu giữa cơ sở dữ liệu quan hệ (RDBMS) và cơ sở dữ liệu phi quan hệ (NoSQL) được thể hiện rõ ràng khi sinh viên "
        "lựa chọn Amazon DynamoDB [5] với mô hình Partition Key và Sort Key để lưu trữ trạng thái Job với tốc độ truy xuất mili-giây và khả năng co giãn vô hạn.",
        bold_prefix="Môn Cơ sở dữ liệu: "
    )
    add_bullet(
        "Các nguyên lý thiết kế Clean Architecture, kiến trúc RESTful API, kỹ thuật điều hướng máy khách "
        "(SPA Client-side Routing), quy trình quản lý mã nguồn Git và tự động hóa triển khai CI/CD đã giúp sinh viên xây dựng một sản phẩm phần mềm hoàn chỉnh, "
        "dễ bảo trì và sẵn sàng mở rộng.",
        bold_prefix="Môn Kỹ nghệ phần mềm & Công nghệ Web: "
    )

    add_h2("4.4. Đề xuất Cải tiến Quy trình và Giải pháp Kỹ thuật Mở rộng")
    add_body(
        "Để nền tảng Serverless Hybrid Document OCR tiếp tục phát triển và hoàn thiện thành một sản phẩm thương mại hóa cấp doanh nghiệp, "
        "sinh viên đề xuất ba hướng cải tiến kỹ thuật trọng tâm trong tương lai:",
        indent=True
    )
    add_bullet(
        "Khi tài khoản AWS hoàn tất xác thực quyền truy cập mô hình (Model Access), kích hoạt chính thức tính năng Amazon Textract AnalyzeDocument (chuyên trị Forms và Tables) "
        "và Amazon Bedrock (mô hình Amazon Nova / Claude 3.5 Sonnet) để tạo thành chu trình bóc tách khép kín 100% trong hạ tầng nội bộ của AWS.",
        bold_prefix="Đề xuất tích hợp toàn diện Amazon Textract và Amazon Bedrock: "
    )
    add_bullet(
        "Xây dựng thêm giao diện trò chuyện tương tác với tài liệu sau khi bóc tách. Người dùng có thể đặt câu hỏi tự nhiên (ví dụ: 'Tổng giá trị hợp đồng là bao nhiêu?', 'Điều khoản phạt chậm thanh toán gồm những gì?') "
        "để trợ lý AI trích xuất câu trả lời chính xác kèm trích dẫn số trang.",
        bold_prefix="Đề xuất nâng cấp tính năng Hỏi đáp tài liệu thông minh (Chat with Document): "
    )
    add_bullet(
        "Nâng cấp máy chủ Web Studio từ máy chủ EC2 đơn lẻ sang cụm container phi máy chủ Amazon ECS Fargate kết hợp Amazon ECR. "
        "Giải pháp này giúp tự động co giãn số lượng bản sao (Replicas) khi lưu lượng truy cập tăng đột biến, loại bỏ hoàn toàn công tác quản trị máy chủ cơ sở.",
        bold_prefix="Đề xuất chuyển dịch sang Container Orchestration với Amazon ECS Fargate: "
    )

    print("Hoàn thành biên soạn PHẦN 4: Phân tích, đánh giá và đề xuất.")
