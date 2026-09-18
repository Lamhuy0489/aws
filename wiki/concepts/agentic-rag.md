# Agentic RAG (Retrieval-Augmented Generation voi AI Agent)

- Danh muc: AI-ML
- Ngay tao: 2026-09-18

## 1. Dinh nghia va muc dich
Agentic RAG la kien truc nang cap cua he thong RAG truyen thong. Thay vi chi truy van vector roi tra ve ket qua mot cach thu dong, Agentic RAG su dung mot tac nhan tri tue nhan tao (AI Agent) co kha nang suy luan qua cac buoc (ReAct pattern): phan tich y dinh (Intent Routing), tu quyet dinh khi nao can tra cuu tai lieu, khi nao can thuc thi cong cu ngoai vi (Tool Execution), va tu danh gia lai ket qua truoc khi tra loi.

## 2. Dac diem ky thuat chinh
- Dinh tuyen y dinh: Phan loai cau hoi de tranh viec tra cuu vector lang phi khi gap cau hoi chao hoi hoac hoi dap don gian.
- Thuc thi cong cu: Co kha nang goi API, truy van co so du lieu thuc te (vi du: kiem tra trang thai don hang tren DynamoDB).
- Kiem soat phan anh (Self-Correction): Danh gia do lien quan cua ngu canh trich xuat va tinh chinh xac cua cau tra loi de han che ao giac (hallucination).

## 3. Cach ap dung trong du an
Trong du an nay ([project-agentic-rag-spec](file:///Users/huylam/Downloads/aws/docs/04_project_agentic_rag_spec.md)), Agentic RAG duoc thiet ke chay tren AWS Lambda lam bo dieu khien trung tam, tich hop Gemini Flash / Groq qua SSM Parameter Store de tiet kiem toi da chi phi.

## 4. Tai lieu nguon tham chieu
- [[rag-2026-spec]]
- [[aws-lambda-controller]]
- [[aws-bedrock-and-llm]]
