# Ket Qua Thuc Hanh: Lab 000007 - Quan Ly Chi Phi Voi AWS Budgets

- Nguoi thuc hien: Lam Huy
- Ngay hoan thanh: 2026-09-18
- AWS Account ID: 677994024390

---

## 1. Muc tieu
- Cấu hình công cụ kiểm soát và cảnh báo chi phí tự động AWS Budgets.
- Ngăn ngừa rủi ro phát sinh chi phí ngoài ý muốn trong quá trình thực tập và triển khai các dịch vụ cloud.

## 2. Thong so Budget da xac thuc qua AWS CLI
He thong da xac nhan 2 Budget dang hoat dong o trang thai `HEALTHY`:

1. **Budget 1**: `My Monthly Cost Budget`
   - Han muc: `100.0 USD` / thang (Monthly).
   - Chi phi thuc te hien tai (Actual Spend): `0.001 USD`.
   - Du bao chi phi (Forecasted Spend): `0.051 USD`.
   - Trang thai suc khoe: `HEALTHY`.
   - Billing View ARN: `arn:aws:billing::677994024390:billingview/primary`.

2. **Budget 2**: `My-200$-budget`
   - Han muc: `200.0 USD` / thang (Monthly).
   - Chi phi thuc te hien tai: `0.0 USD`.
   - Du bao chi phi: `0.051 USD`.
   - Trang thai suc khoe: `HEALTHY`.

## 3. Khuyen nghi FinOps bo sung
- Han muc 100 USD va 200 USD la nguong an toan cao. De can than hon khi thuc tap, nen bo sung them mot canh bao o nguong nho: **5.0 USD** hoac **10.0 USD** de nhan email canh bao ngay khi co bat ky tai nguyen nao bat dau tinh phi.
