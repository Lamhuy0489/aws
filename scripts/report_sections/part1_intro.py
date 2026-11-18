# -*- coding: utf-8 -*-
import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def add_part1(doc, add_h1, add_h2, add_h3, add_body, add_bullet, add_figure):
    add_h1("PHẦN 1: GIỚI THIỆU CHUNG VỀ ĐƠN VỊ THỰC TẬP")
    
    add_h2("1.1. Lịch sử hình thành và vị thế toàn cầu của Amazon Web Services (AWS)")
    add_body(
        "Điện toán đám mây (Cloud Computing) đã và đang trở thành xương sống của cuộc Cách mạng Công nghiệp lần thứ tư, "
        "thay đổi căn bản phương thức các tổ chức, doanh nghiệp và chính phủ trên toàn cầu xây dựng, triển khai và vận hành hệ thống thông tin [1]. "
        "Trong làn sóng chuyển dịch mang tính lịch sử này, Amazon Web Services (AWS) giữ vai trò là đơn vị tiên phong mở đường và "
        "liên tục dẫn đầu thị trường trong suốt gần hai thập kỷ qua.",
        indent=True
    )
    add_body(
        "Được thành lập chính thức vào năm 2006 trực thuộc tập đoàn thương mại điện tử Amazon.com, AWS đã khởi đầu với việc thương mại hóa "
        "các dịch vụ cơ sở hạ tầng tính toán cơ bản như Amazon Simple Storage Service (Amazon S3) và Amazon Elastic Compute Cloud (Amazon EC2). "
        "Ý tưởng đột phá của AWS bắt nguồn từ nhu cầu nội bộ của Amazon: biến toàn bộ tài nguyên tính toán, lưu trữ và mạng thành các khối dịch vụ "
        "được trừu tượng hóa cao, có thể cấp phát tức thì thông qua các giao diện lập trình ứng dụng (APIs) và thanh toán linh hoạt theo mức độ sử dụng "
        "(Pay-as-you-go). Mô hình này đã giải phóng các doanh nghiệp khỏi gánh nặng chi phí đầu tư ban đầu (CapEx) khổng lồ vào máy chủ vật lý, "
        "chuyển dịch sang chi phí vận hành biến đổi (OpEx) linh hoạt và tối ưu.",
        indent=True
    )
    add_body(
        "Trải qua 20 năm phát triển liên tục, AWS hiện cung cấp hơn 240 dịch vụ toàn diện và đầy đủ tính năng nhất trên thế giới, "
        "bao gồm từ điện toán, lưu trữ, cơ sở dữ liệu, mạng, phân tích dữ liệu lớn (Big Data), Internet vạn vật (IoT), học máy (Machine Learning) "
        "cho đến Trí tuệ nhân tạo tạo sinh (Generative AI). Theo báo cáo đánh giá định kỳ của tổ chức nghiên cứu công nghệ hàng đầu thế giới Gartner, "
        "AWS liên tục được vinh danh trong nhóm dẫn đầu (Leaders Quadrant) của Báo cáo Magic Quadrant dành cho Dịch vụ Cơ sở hạ tầng và Nền tảng Đám mây "
        "(Strategic Cloud Platform Services) trong hơn 13 năm liên tiếp nhờ cả tầm nhìn chiến lược xuất sắc và năng lực thực thi vượt trội [1].",
        indent=True
    )
    add_body(
        "Về mặt hạ tầng vật lý toàn cầu, AWS sở hữu mạng lưới trung tâm dữ liệu rộng khắp với hơn 34 Vùng địa lý (Regions) và 108 Vùng sẵn sàng "
        "(Availability Zones - AZs) kết nối với nhau qua mạng trục cáp quang riêng tốc độ cao terabit, phục vụ hàng triệu khách hàng tích cực "
        "tại hơn 190 quốc gia và vùng lãnh thổ trên toàn cầu.",
        indent=True
    )

    add_h2("1.2. Pháp nhân và cơ cấu tổ chức của AWS tại Việt Nam")
    add_body(
        "Nhận thấy tiềm năng tăng trưởng vượt bậc của nền kinh tế số Việt Nam và nhu cầu chuyển đổi số mạnh mẽ của các doanh nghiệp trong nước, "
        "tập đoàn Amazon Web Services đã chính thức hiện diện tại Việt Nam thông qua pháp nhân: CÔNG TY TNHH AMAZON WEB SERVICES VIỆT NAM.",
        indent=True
    )
    add_body("Hệ thống văn phòng đại diện và cơ sở hoạt động của AWS tại Việt Nam được đặt tại hai trung tâm kinh tế - chính trị trọng điểm:", indent=True)
    add_bullet(
        "Tầng 36, Tòa nhà Bitexco Financial Tower, Số 2 đường Hải Triều, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh. "
        "Đây là trung tâm điều hành kinh doanh, dịch vụ chuyên nghiệp (Professional Services) và quản trị đối tác chiến lược tại khu vực phía Nam.",
        bold_prefix="Trụ sở chính (TP. Hồ Chí Minh): "
    )
    add_bullet(
        "Tầng 7, Tòa nhà Grand Terra, Số 36 phố Cát Linh, Phường Ô Chợ Dừa, Quận Đống Đa, TP. Hà Nội (song song với các cơ sở "
        "hợp tác tại Tòa nhà Capital Place, 29 Liễu Giai, Ba Đình). Văn phòng Hà Nội đóng vai trò đầu não phụ trách các chương trình hợp tác Chính phủ, "
        "khối khách hàng doanh nghiệp Nhà nước, tài chính - ngân hàng và các chương trình phát triển giáo dục đại học tại miền Bắc.",
        bold_prefix="Văn phòng đại diện Hà Nội: "
    )
    add_body(
        "Cơ cấu tổ chức của AWS Việt Nam được phân bổ thành các khối chuyên trách bài bản nhằm hỗ trợ toàn diện vòng đời chuyển đổi số của khách hàng:",
        indent=True
    )
    add_bullet(
        "Tập hợp các chuyên gia kỹ thuật cấp cao (Principal/Senior Solutions Architects), "
        "chịu trách nhiệm tư vấn, thẩm định và thiết kế kiến trúc hệ thống đám mây theo chuẩn AWS Well-Architected Framework cho các khách hàng doanh nghiệp lớn [1].",
        bold_prefix="Khối Tư vấn Kiến trúc Giải pháp (Solutions Architecture - SA): "
    )
    add_bullet(
        "Trực tiếp tham gia cùng khách hàng trong các dự án di chuyển hạ tầng phức tạp "
        "(Large-Scale Cloud Migration), hiện đại hóa ứng dụng và xây dựng các nền tảng phân tích dữ liệu/AI quy mô lớn.",
        bold_prefix="Khối Dịch vụ Chuyên nghiệp (Professional Services - ProServe): "
    )
    add_bullet(
        "Quản lý và thúc đẩy mạng lưới đối tác AWS Partner Network (APN), "
        "hỗ trợ các công ty công nghệ trong nước trở thành các nhà cung cấp giải pháp đám mây chuyên nghiệp.",
        bold_prefix="Khối Phát triển Hệ sinh thái Đối tác & Khách hàng: "
    )
    add_bullet(
        "Tổ chức các khóa huấn luyện chuyên môn, tài trợ học liệu và phối hợp "
        "cùng cộng đồng công nghệ (AWS User Group Vietnam, AWS Study Group) nhằm ươm mầm nguồn nhân lực Cloud chất lượng cao cho đất nước.",
        bold_prefix="Khối Đào tạo và Chứng chỉ (AWS Training & Certification): "
    )

    add_h2("1.3. Lĩnh vực hoạt động và vai trò trong Chuyển đổi số Quốc gia")
    add_body(
        "Tại Việt Nam, AWS không đơn thuần là một nhà cung cấp hạ tầng tính toán quốc tế mà đã trở thành đối tác chiến lược tin cậy đồng hành cùng Chính phủ "
        "và cộng đồng doanh nghiệp trong chương trình Chuyển đổi số Quốc gia đến năm 2025, định hướng đến năm 2030.",
        indent=True
    )
    add_body(
        "Các lĩnh vực hoạt động trọng tâm và dấu ấn thực tế của AWS tại Việt Nam bao gồm:",
        indent=True
    )
    add_bullet(
        "Cung cấp nền tảng điện toán đám mây đạt tiêu chuẩn an ninh quốc tế PCI-DSS Level 1, ISO 27001 và hướng dẫn bảo mật "
        "của Ngân hàng Nhà nước Việt Nam. Hàng loạt ngân hàng thương mại và kỳ lân công nghệ tài chính hàng đầu (như Techcombank, VPBank, VNPAY, MoMo) "
        "đang vận hành các dịch vụ ngân hàng số thế hệ mới trên nền tảng AWS.",
        bold_prefix="Lĩnh vực Tài chính - Ngân hàng (BFSI): "
    )
    add_bullet(
        "Hỗ trợ các tập đoàn lớn (Vingroup, Masan Group) triển khai các hồ dữ liệu (Data Lake) và hệ thống phân tích "
        "thời gian thực, tối ưu hóa chuỗi cung ứng và cá nhân hóa trải nghiệm người tiêu dùng.",
        bold_prefix="Lĩnh vực Doanh nghiệp Sản xuất & Bán lẻ: "
    )
    add_bullet(
        "Thông qua chương trình AWS Activate, AWS đã tài trợ hàng triệu USD giá trị điểm tín dụng dịch vụ (Credits), "
        "hỗ trợ kỹ thuật chuyên sâu cho hàng trăm công ty khởi nghiệp công nghệ Việt Nam nhanh chóng ra mắt sản phẩm và vươn ra thị trường khu vực.",
        bold_prefix="Lĩnh vực Khởi nghiệp Đổi mới sáng tạo (Startups): "
    )
    add_bullet(
        "Triển khai chương trình AWS Academy và AWS Educate tại hàng chục trường đại học công nghệ hàng đầu "
        "(Đại học Quốc gia Hà Nội, Đại học Bách khoa Hà Nội, Đại học Xây dựng Hà Nội...), trang bị kỹ năng đám mây thực chiến cho hàng chục ngàn sinh viên.",
        bold_prefix="Lĩnh vực Giáo dục và Đào tạo nguồn nhân lực số: "
    )

    add_h2("1.4. Chương trình Đào tạo & Ươm mầm First Cloud AI Journey (FCAJ)")
    add_body(
        "Chương trình First Cloud AI Journey (FCAJ) Bootcamp 2026 là sáng kiến đào tạo và ươm mầm tài năng chuyên sâu (Workforce Development Bootcamp) "
        "được AWS Việt Nam phối hợp chặt chẽ cùng cộng đồng học thuật AWS Study Group thiết kế đặc quyền dành riêng cho các sinh viên năm cuối xuất sắc "
        "thuộc các trường đại học khối kỹ thuật và công nghệ thông tin tại Việt Nam.",
        indent=True
    )
    add_body(
        "Xuất phát từ thực trạng thị trường lao động đang thiếu hụt nghiêm trọng các kỹ sư đám mây có kỹ năng thực chiến (Hands-on Skills) và tư duy an ninh "
        "theo chuẩn doanh nghiệp, FCAJ được xây dựng theo triết lý 'Học từ việc làm thật' (Learning by Doing) với các mục tiêu cốt lõi:",
        indent=True
    )
    add_bullet(
        "Sinh viên được đào tạo bài bản về 6 trụ cột của khung kiến trúc AWS Well-Architected Framework [1]: "
        "Vận hành xuất sắc (Operational Excellence), An toàn bảo mật (Security), Độ tin cậy (Reliability), Hiệu năng vượt trội (Performance Efficiency), "
        "Tối ưu hóa chi phí (Cost Optimization / FinOps), và Tính bền vững (Sustainability).",
        bold_prefix="Rèn luyện tư duy kiến trúc chuẩn mực: "
    )
    add_bullet(
        "Toàn bộ các bài thực hành từ cấp phát mạng VPC [2], cấu hình cân bằng tải ALB [3], "
        "đóng gói Docker container, thiết lập cơ sở dữ liệu DynamoDB [5] đến các hàm phi máy chủ AWS Lambda [6] đều được thực thi trực tiếp trên tài khoản AWS Cloud thật, "
        "loại bỏ hoàn toàn tư duy mô phỏng lý thuyết sáo rỗng.",
        bold_prefix="Thực hành 100% trên môi trường đám mây thật (AWS Live Sandbox): "
    )
    add_bullet(
        "Mỗi thực tập sinh phải độc lập nghiên cứu, thiết kế kiến trúc và triển khai thành công "
        "một giải pháp phần mềm cấp doanh nghiệp có khả năng chạy thật trên Internet, đáp ứng các tiêu chuẩn khắt khe về an ninh mạng phân tầng, "
        "khả năng chịu lỗi cao và tối ưu chi phí vận hành ở mức 0.00 USD (FinOps Zero-Breach).",
        bold_prefix="Chinh phục đồ án tốt nghiệp thực chiến (Capstone Project): "
    )

    add_h2("1.5. Văn hóa doanh nghiệp và Bộ 16 Nguyên tắc Lãnh đạo của Amazon")
    add_body(
        "Nền tảng làm nên thành công phi thường và tốc độ đổi mới sáng tạo không ngừng của Amazon nói chung và AWS nói riêng chính là bộ văn hóa doanh nghiệp "
        "đặc thù, được đúc kết thành Bộ 16 Nguyên tắc Lãnh đạo (Amazon Leadership Principles - LPs). Tại AWS, các nguyên tắc này không phải là những khẩu hiệu "
        "treo trên tường mà là kim chỉ nam cho mọi quyết định kỹ thuật, mọi buổi thảo luận thiết kế và hành động hàng ngày của từng kỹ sư.",
        indent=True
    )
    add_body(
        "Trong suốt 12 tuần thực tập tại AWS Việt Nam, sinh viên đã được hòa mình, rèn luyện và trực tiếp áp dụng các nguyên tắc lãnh đạo cốt lõi vào quá trình "
        "phát triển đề tài tốt nghiệp:",
        indent=True
    )
    add_bullet(
        "Lãnh đạo luôn bắt đầu từ khách hàng và làm việc ngược trở lại (Working Backwards). Trong đề tài bóc tách tài liệu, "
        "sinh viên luôn trăn trở về nỗi đau của người dùng: tài liệu scan bị mờ, bảng biểu bị đứt gãy, chi phí OCR quá đắt đỏ và ứng dụng web bị giật lag khi tải lại trang. "
        "Chính sự ám ảnh vì trải nghiệm người dùng đã thúc đẩy sinh viên sáng tạo ra kiến trúc Fast-Path phân tầng và giao diện Single Page Application mượt mà.",
        bold_prefix="Customer Obsession (Ám ảnh vì khách hàng): "
    )
    add_bullet(
        "Các nhà lãnh đạo là những người chủ thực sự. Họ suy nghĩ dài hạn và không bao giờ hy sinh giá trị dài hạn vì kết quả ngắn hạn. "
        "Họ không bao giờ nói 'đó không phải là việc của tôi'. Thực tập sinh đã chủ động chịu trách nhiệm toàn diện từ khâu thiết kế sơ đồ mạng VPC [2], viết mã nguồn backend, "
        "xây dựng pipeline CI/CD, theo dõi chi phí FinOps đến việc tự sửa chữa sự cố máy chủ EC2 mà không ỷ lại vào người hướng dẫn.",
        bold_prefix="Ownership (Tinh thần làm chủ): "
    )
    add_bullet(
        "Lãnh đạo luôn yêu cầu sự đổi mới từ đội ngũ và luôn tìm cách đơn giản hóa vấn đề. Thay vì áp dụng những mô hình "
        "AI thị giác cồng kềnh, tốn kém cho toàn bộ tệp PDF, sinh viên đã nghiên cứu và ứng dụng giải thuật trích xuất trực tiếp luồng văn bản số của PyMuPDF [8], "
        "giúp giải quyết hơn 80% tài liệu chỉ trong 0.1 giây với chi phí 0 đồng.",
        bold_prefix="Invent and Simplify (Sáng tạo và Đơn giản hóa): "
    )
    add_bullet(
        "Tốc độ là yếu tố sống còn trong kinh doanh và công nghệ. Nhiều quyết định và hành động có thể đảo ngược được và không cần "
        "phải nghiên cứu quá mức. Sinh viên luôn chủ động xây dựng các bản mẫu chạy thử (PoC) ngay sau khi có ý tưởng, đo kiểm thực tế trên môi trường AWS Sandbox để "
        "rút ngắn chu kỳ phát triển.",
        bold_prefix="Bias for Action (Ưu tiên hành động): "
    )
    add_bullet(
        "Lãnh đạo hoạt động ở mọi cấp độ, gắn liền với các chi tiết, kiểm tra thường xuyên và luôn nghi ngờ khi các số liệu và câu chuyện "
        "có sự mâu thuẫn. Khi gặp lỗi Timeout 29 giây của API Gateway hay lỗi phân quyền AWS Bedrock, sinh viên không bỏ cuộc mà kiên trì truy vết mã lỗi trong CloudWatch Logs [7], "
        "phân tích các bản ghi JSON từ gốc rễ để tìm ra nguyên nhân cốt lõi và đưa ra giải pháp xử lý triệt để.",
        bold_prefix="Dive Deep (Đào sâu bản chất): "
    )
    add_bullet(
        "Hoàn thành nhiều việc hơn với ít nguồn lực hơn. Sự hạn chế nuôi dưỡng sự tháo vát, tự cung tự cấp và sáng tạo. "
        "Dưới áp lực ngân sách tài khoản thực tập Free Tier (0 USD), sinh viên đã tận dụng tối đa các tài nguyên tính toán miễn phí (Kaggle GPU [9], Google Tour Keys [10], "
        "DynamoDB On-Demand [5], Lambda scale-to-zero [6]) để xây dựng một hệ thống cấp doanh nghiệp mà không phát sinh bất kỳ khoản phí vượt ngưỡng nào.",
        bold_prefix="Frugality (Tiết kiệm và Tối ưu chi phí): "
    )

    print("Hoàn thành cập nhật PHẦN 1: Chuẩn hóa trích dẫn [1], bỏ double bullets.")
