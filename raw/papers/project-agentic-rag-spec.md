# Đặc Tả Kiến Trúc Dự Án: Agentic RAG Trên AWS (Tối Ưu Chi Phí)

Tài liệu này mô tả chi tiết thiết kế kiến trúc, các thành phần kỹ thuật và phương án triển khai hệ thống **Agentic RAG (Retrieval-Augmented Generation kết hợp Trí tuệ Nhân tạo Tác nhân)** trên nền tảng đám mây AWS với chi phí tối ưu nhất cho kỳ thực tập.

---

## 1. Tổng quan bài toán và Mục tiêu

Hệ thống RAG truyền thống (Naive RAG) chỉ đơn thuần chuyển đổi câu hỏi thành vector, tìm các đoạn văn bản tương đồng nhất và yêu cầu mô hình ngôn ngữ lớn (LLM) trả lời. Cách tiếp cận này bộc lộ nhiều điểm yếu khi gặp câu hỏi phức tạp cần nhiều bước suy luận, câu hỏi không cần tra cứu tài liệu, hoặc yêu cầu thực hiện hành động (như truy vấn cơ sở dữ liệu thực tế, gọi API nghiệp vụ).

**Agentic RAG** giải quyết triệt để các vấn đề trên thông qua cơ chế Agent thông minh:
- Tự phân tích ý định câu hỏi (Intent Routing).
- Tự quyết định khi nào cần tra cứu tài liệu, khi nào cần gọi công cụ bên ngoài (Tool Execution).
- Tổng hợp thông tin đa nguồn và tự đánh giá chất lượng câu trả lời trước khi gửi lại cho người dùng.

---

## 2. Sơ đồ kiến trúc tổng thể (AWS Solution Architecture)

```text
[ Người Dùng / Trình Duyệt ]
           │
           ▼
[ Amazon CloudFront + S3 ] (Phân phối Giao diện Frontend Next.js/React)
           │
           ▼ (HTTPS Request)
[ Amazon API Gateway ] (Quản lý Endpoint, Rate Limiting, Throttling)
           │
           ▼ (Kích hoạt luồng)
[ AWS Lambda: Agent Core Controller ]
     │
     ├── 1. Lấy API Key an toàn ──────> [ AWS SSM Parameter Store (SecureString) ]
     │                                    (Chứa GEMINI_API_KEY / OPENAI_API_KEY)
     │
     ├── 2. Đọc/Ghi lịch sử hội thoại ──> [ Amazon DynamoDB (chat-sessions) ]
     │
     ├── 3. Quyết định hành động (ReAct Loop):
     │      │
     │      ├── [Nhánh A: Tra cứu tri thức] ─> [ S3 Document Store + Vector Index ]
     │      │                                    (Trích xuất tài liệu liên quan)
     │      │
     │      ├── [Nhánh B: Gọi Tool nghiệp vụ] ─> [ AWS Lambda: Query Order/Ticket ]
     │      │                                    (Truy vấn bảng nghiệp vụ DynamoDB)
     │      │
     │      └── [Nhánh C: Gửi thông báo] ──────> [ Amazon SNS / Webhook ]
     │
     └── 4. Gửi Prompt + Context + Tool Output ──> [ External LLM Provider ]
                                                   (Google Gemini Flash / Groq API)
           │
           ▼ (Kết quả hoàn chỉnh có kèm trích dẫn nguồn)
[ Người Dùng nhận câu trả lời dạng Streaming / JSON ]
```

---

## 3. Chi tiết các thành phần kỹ thuật

### a. Tầng Giao diện người dùng (Frontend)
- **Công nghệ**: Next.js hoặc React dạng Single Page Application (SPA), hoặc Streamlit container.
- **Lưu trữ & Phân phối**: Đóng gói thành file tĩnh (HTML/CSS/JS) tải lên **Amazon S3**, phân phối toàn cầu qua **Amazon CloudFront** với chứng chỉ bảo mật HTTPS miễn phí từ **AWS Certificate Manager (ACM)**.

### b. Tầng Cổng API & Bảo mật (API & Security Layer)
- **Amazon API Gateway**: Cung cấp endpoint REST API bảo mật tiếp nhận yêu cầu từ client.
- **AWS Systems Manager (SSM) Parameter Store**:
  - Lưu trữ API Key bên ngoài dưới dạng tham số mã hóa `SecureString`.
  - IAM Role của Lambda chỉ được cấp quyền `ssm:GetParameter` duy nhất cho tham số này.
  - Tuyệt đối không lưu key trong mã nguồn hoặc file `.env` trên Git.

### c. Tầng Điều phối Agent (Agent Engine Core)
- **Công nghệ thực thi**: **AWS Lambda** (Python 3.11/3.12).
- **Thư viện Agent**: Sử dụng LangChain, LangGraph hoặc LlamaIndex.
- **Nguyên lý hoạt động (ReAct Framework)**:
  1. *Reasoning (Suy luận)*: Agent nhận câu hỏi và lịch sử chat, phân tích xem cần thông tin gì.
  2. *Acting (Hành động)*: Nếu cần tìm tài liệu nội bộ, gọi hàm tìm kiếm Vector; nếu cần tra cứu dữ liệu khách hàng, gọi hàm Database Query.
  3. *Observation (Quan sát)*: Nhận kết quả từ công cụ và đánh giá xem đã đủ thông tin để trả lời chưa.
  4. *Final Response (Phản hồi)*: Định dạng câu trả lời hoàn chỉnh kèm chú thích nguồn tài liệu.

### d. Tầng Tri thức & Tìm kiếm Vector (Knowledge Base & Vector Store)
- **Amazon S3**: Lưu trữ tài liệu gốc (PDF, Word, Markdown quy trình).
- **Giải pháp Vector tối ưu chi phí**:
  - Đối với tập dữ liệu vừa và nhỏ (phù hợp thực tập/demo): Sử dụng thư viện vector nhúng nhẹ như **FAISS** hoặc **Chroma** lưu trữ file index trên Amazon S3, tải vào bộ nhớ đệm `/tmp` của Lambda khi chạy.
  - Đối với tập dữ liệu mở rộng: Sử dụng **Amazon Aurora PostgreSQL Serverless v2 với pgvector** hoặc dịch vụ Vector Cloud có gói miễn phí như Pinecone Serverless.

### e. Tầng Quản lý Phiên và Bộ nhớ (Session & Memory)
- **Amazon DynamoDB**:
  - Bảng `agent_chat_history` với Partition Key là `session_id` và Sort Key là `timestamp`.
  - Kích hoạt tính năng **Time to Live (TTL)**: Tự động dọn dẹp các đoạn chat sau 7 ngày để không làm phình dung lượng và tránh phát sinh chi phí lưu trữ.

### f. Tầng Giám sát & Nhật ký (Observability)
- **Amazon CloudWatch Logs**: Ghi lại lịch sử thực thi, số lượng token tiêu thụ, thời gian phản hồi (latency) của từng lần gọi mô hình.
- **CloudWatch Metrics & Alarms**: Báo động khi tỷ lệ lỗi 5xx của Lambda vượt ngưỡng quy định.

---

## 4. Phân tích chi phí (FinOps & Cost Efficiency)

Kiến trúc này được thiết kế để chi phí phát sinh gần như bằng 0 đồng trong tài khoản AWS cá nhân:

| Dịch vụ AWS | Hạn mức Free Tier / Chi phí thực tế | Đánh giá mức độ phát sinh chi phí |
| :--- | :--- | :--- |
| **AWS Lambda** | 1,000,000 request/tháng và 3.2 triệu giây tính toán miễn phí vĩnh viễn | 0 USD trong quá trình thực tập |
| **Amazon DynamoDB** | 25 GB lưu trữ miễn phí vĩnh viễn | 0 USD |
| **Amazon S3** | 5 GB lưu trữ tiêu chuẩn trong 12 tháng đầu | Gần như 0 USD |
| **Amazon API Gateway** | 1,000,000 cuộc gọi API miễn phí trong 12 tháng đầu | 0 USD |
| **SSM Parameter Store** | Lưu trữ tham số Standard hoàn toàn miễn phí | 0 USD |
| **LLM Provider (External)** | Google Gemini 1.5 Flash (Free Tier: 15 request/phút) hoặc Groq Free API | 0 USD |

---

## 5. Cấu trúc mã nguồn Backend mẫu

Tệp xử lý chính tại `src/backend/app.py`:

```python
import json
import os
import boto3
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool

# 1. Ham lay API Key an toan tu AWS SSM Parameter Store
def get_external_api_key():
    ssm = boto3.client("ssm", region_name=os.getenv("AWS_REGION", "ap-southeast-1"))
    param = ssm.get_parameter(
        Name="/agentic_rag/gemini_api_key",
        WithDecryption=True
    )
    return param["Parameter"]["Value"]

# 2. Khoi tao LLM
api_key = get_external_api_key()
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=api_key,
    temperature=0.2
)

# 3. Dinh nghia cac Tools cua Agent
def search_knowledge_base(query: str) -> str:
    # Logic truy xuat tu Vector DB hoac S3 Document
    return f"Ket qua tra cuu tai lieu ve: {query}"

def check_ticket_status(ticket_id: str) -> str:
    # Logic truy van bang DynamoDB
    return f"Ticket {ticket_id} dang o trang thai: Dang xu ly."

tools = [
    Tool(
        name="SearchInternalDocs",
        func=search_knowledge_base,
        description="Dung khi can tra cuu quy trinh, tai lieu ky thuat noi bo."
    ),
    Tool(
        name="CheckTicketStatus",
        func=check_ticket_status,
        description="Dung khi nguoi dung hoi ve trang thai cua ticket hoac don hang."
    )
]

# 4. Khoi tao Agent
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 5. Handler cho AWS Lambda
def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        user_prompt = body.get("message", "")
        
        response = agent_executor.run(user_prompt)
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"response": response})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
```
