# Bo Dieu Phien Agent Tren AWS Lambda

- Danh muc: Compute / Serverless
- Ngay tao: 2026-09-18

## 1. Dinh nghia va muc dich
AWS Lambda la dich vu dien toan khong may chu (Serverless) cho phep chay ma nguon ma khong can khoi tao hay quan ly may chu. Trong he thong Agentic RAG, Lambda duoc su dung lam bo dieu khien trung tam (Agent Core Controller) de xu ly logic ReAct, goi cong cu, va giao tiep voi mo hinh ngon ngu lon.

## 2. Dac diem ky thuat chinh
- Mo hinh chi phi pay-per-use: Khong ton chi phi khi he thong o trang thai cho (idle), mien phi 1 trieu yeu cau moi thang qua AWS Free Tier.
- Tich hop chat che: Ket noi truc tiep voi Amazon API Gateway de nhan HTTPS request, ket noi DynamoDB de luu tru session, va lay khoa an toan tu SSM Parameter Store.
- Quan tri quyen han toi thieu: Cau hinh qua IAM Role chi cap quyen thao tac dung cac bang va bucket can thiet.

## 3. Cach ap dung trong du an
Toan bo ma nguon backend nam trong `src/backend/app.py` va cac module trong `src/backend/agents/` duoc dong goi de san sang trien khai len AWS Lambda.

## 4. Tai lieu nguon tham chieu
- [[rag-2026-spec]]
- [[agentic-rag]]
