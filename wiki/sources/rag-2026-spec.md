# Dac Ta Kien Truc Du An Agentic RAG Tren AWS

- Nguon: docs/04_project_agentic_rag_spec.md
- Phan loai: spec
- Ngay tiep nhan: 2026-09-18
- Tep goc trong raw: [[project-agentic-rag-spec]]

## 1. Tom tat noi dung (200 - 400 tu)
Dac ta he thong kien truc ky thuat hoan chinh cua ung dung Agentic RAG toi uu chi phi danh cho ky thuc tap. He thong khac phuc nhuoc diem cua Naive RAG bang cach su dung vong lap suy luan ReAct Agent:
- Frontend: Single Page Application luu tren Amazon S3, phan phoi qua CloudFront voi chung chi HTTPS tu ACM.
- API Gateway & Lambda: Dong vai tro Agent Core Controller, tiep nhan yeu cau va dieu phoi luong suy luan.
- Luu tru phien hoi thoai: Amazon DynamoDB luu session va chat history.
- Quan ly khoa bao mat: AWS Systems Manager Parameter Store luu API Key (Gemini Flash / OpenAI) duoi dang SecureString de giu chi phi o muc 0 USD.
- Tra cuu tri thuc: S3 Document Store ket hop voi Vector Index de trich xuat ngu canh phu hop.
- Cong cu ngoai (Tools): Lambda tool truy van don hang / ve ho tro tren DynamoDB.

Dac ta cung cap chi tiet cau truc ma nguon, luong du lieu, mo hinh bao mat IAM Least Privilege va ke hoach trien khai 4 sprint.

## 2. Cac khai niem cot loi
- [[agentic-rag]]: Kien truc tac nhan thong minh ket hop tra cuu tai lieu va thuc thi cong cu.
- [[aws-lambda-controller]]: Trung tam dieu phoi ReAct Agent tren AWS.
- [[aws-bedrock-and-llm]]: Tich hop mo hinh ngon ngu lon an toan va tiet kiem.

## 3. Diem can luu y va thuc hanh tot nhat
- Su dung Free Tier toi da (S3, CloudFront, Lambda 1M request/thang, DynamoDB 25GB).
- Tuyet doi khong hardcode API key trong ma nguon hoac Docker image.

## 4. Lien ket lien quan
- [[fcj-2026-roadmap]]
- [[agentic-rag]]
- [[aws-lambda-controller]]
