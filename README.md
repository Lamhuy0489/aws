# Kho Lưu Trữ Tri Thức Thực Tập AWS & Dự Án Agentic RAG

Kho tài liệu này được tổng hợp và xây dựng nhằm phục vụ toàn bộ lộ trình thực tập Cloud/AWS, bám sát khung chương trình **The First Cloud Journey (FCJ)** của cộng đồng AWS Study Group Vietnam, kết hợp đặc tả kỹ thuật dự án **Agentic RAG on AWS**.

- **Website Báo cáo thực tập (Live trên GitHub Pages)**: [https://lamhuy0489.github.io/workshop/](https://lamhuy0489.github.io/workshop/)
- **Kho lưu trữ Website Báo cáo**: [https://github.com/Lamhuy0489/workshop](https://github.com/Lamhuy0489/workshop)
- **Đề xuất dự án trực tuyến (Proposal)**: [https://lamhuy0489.github.io/workshop/2-proposal/](https://lamhuy0489.github.io/workshop/2-proposal/)

---

## 1. Mục lục tài liệu tri thức

Hệ thống tài liệu hướng dẫn chi tiết được lưu trong thư mục `docs/`:

- [docs/01_aws_cloud_journey_curriculum.md](file:///Users/huylam/Downloads/aws/docs/01_aws_cloud_journey_curriculum.md): Toàn bộ danh mục 7 module kỹ thuật và hơn 100 workshop thực hành từ Cloud Journey kèm liên kết trực tiếp.
- [docs/02_internship_roadmap.md](file:///Users/huylam/Downloads/aws/docs/02_internship_roadmap.md): Lộ trình thực tập chi tiết theo từng giai đoạn, các yêu cầu và tiêu chí tốt nghiệp của chương trình FCJ Workforce Program.
- [docs/03_hands_on_checklist.md](file:///Users/huylam/Downloads/aws/docs/03_hands_on_checklist.md): Bảng kiểm tra tiến độ các bài lab thực hành cốt lõi cần hoàn thành theo thứ tự ưu tiên.
- [docs/04_project_hybrid_ocr_spec.md](file:///Users/huylam/Downloads/aws/docs/04_project_hybrid_ocr_spec.md): Thiết kế kiến trúc kỹ thuật chi tiết của dự án Serverless Hybrid Document OCR & Parsing Platform trên AWS.

---

## 2. Cấu trúc thư mục dự án

Toàn bộ mã nguồn, cấu hình hạ tầng và tài liệu được tổ chức theo cấu trúc chuẩn như sau:

```text
/Users/huylam/Downloads/aws/
├── README.md                           # Tổng quan kho tài liệu và hướng dẫn bắt đầu
├── docs/                               # Thư mục lưu trữ tri thức và lộ trình thực tập
│   ├── 01_aws_cloud_journey_curriculum.md
│   ├── 02_internship_roadmap.md
│   ├── 03_hands_on_checklist.md
│   └── 04_project_hybrid_ocr_spec.md
├── src/                                # Mã nguồn ứng dụng
│   ├── backend/                        # Backend xử lý tài liệu và Lambda Handler
│   │   ├── app.py                      # AWS Lambda Handler & API Router
│   │   ├── config/                     # Cấu hình môi trường và tham số AWS SSM
│   │   ├── parsers/                    # Tầng 1: Fast-Path Parser & Tầng 2: OCR Dispatcher
│   │   ├── exporters/                  # Xuất kết quả Markdown (.md) và Word (.docx)
│   │   └── requirements.txt            # Thư viện Python phụ thuộc
│   ├── kaggle/                         # Kịch bản FastAPI phục vụ mô hình trên Kaggle GPU/TPU
│   │   └── serve_ocr.py
│   └── frontend/                       # Giao diện người dùng xem kết quả song song
├── infrastructure/                     # Quản lý hạ tầng bằng mã (IaC)
│   ├── terraform/                      # Kịch bản Terraform triển khai AWS
│   └── cdk/                            # (Tùy chọn) AWS CDK scripts
├── data/                               # Dữ liệu phục vụ kiểm thử
│   └── sample_documents/               # Tài liệu PDF và ảnh mẫu
└── tests/                              # Unit test và kiểm thử tích hợp
```

---

## 3. Các bước tiếp theo

1. Đọc tài liệu `docs/02_internship_roadmap.md` để nắm rõ các mốc thời gian và yêu cầu đầu ra của kỳ thực tập.
2. Thiết lập tài khoản AWS cá nhân và cấu hình cảnh báo chi phí theo hướng dẫn tại bài lab 000001 và 000007.
3. Thực hiện các bài lab nền tảng theo bảng kiểm tra `docs/03_hands_on_checklist.md`.
4. Triển khai và kiểm thử hệ thống bóc tách tài liệu theo đặc tả `docs/04_project_hybrid_ocr_spec.md`.
