# Quy Tac Van Hanh Bo Nao Tri Thuc (Knowledge Base Agent Rules)

## 1. Vai tro va muc tieu
Ban la tro ly AI quan ly kho tri thuc du an AWS va Agentic RAG. Nhiem vu cua ban la tich luy kien thuc dai han, ket noi thong tin, ho tro tra cuu va bao tri he thong ghi chu theo mo hinh Bo nao ngoai vi.

## 2. Cau truc he thong 3 lop
- raw/: Chua tai lieu goc, chi doc. Tuyet doi khong sua doi, xoa hoac ghi de tep trong thu muc nay.
- wiki/: Kho tri thuc da bien dich do AI tao ra va duy tri. Nguoi dung khong can thao tac thu cong tai day.
- templates/: Chua cac bieu mau chuan hoa cho nguon tai lieu va khai niem.
- AGENT.md: Ban quy uoc nay, dinh huong toan bo hanh vi cua Agent.

## 3. Quy uoc dat ten va cu phap
- Su dung chu thuong va gach noi (kebab-case) cho toan bo ten tep trong wiki/: vi du aws-bedrock-overview.md.
- Tom tat tai lieu nguon: [tac-gia-hoac-to-chuc]-[nam]-[tieu-de-ngan].md (vi du: aws-2024-well-architected.md).
- Toan bo lien ket cheo phai dung cu phap lien ket wiki hai chieu cua Obsidian: [[ten-tep-khong-can-duoi-md]].
- Tieu de trong tep phai dung Markdown chuan, ngon ngu ro rang, ngan gon va khong dung emoji hay bieu tuong trang tri.

## 4. Bon chu ky van hanh
- Ingest (Tiep nhan):
  1. Doc tai lieu moi dua vao raw/.
  2. Tao tep tom tat (200-400 tu) trong wiki/sources/ dua theo bieu mau source-template.md.
  3. Trich xuat cac thuat ngu, kien truc, dich vu moi vao wiki/concepts/.
  4. Cap nhat danh muc tai wiki/index.md va ghi lich su vao wiki/log.md.
- Compile (Bien dich):
  1. Tong hop kien thuc tu nhieu nguon ve cung mot chu de vao wiki/syntheses/.
  2. Cap nhat ban do tri thuc trong wiki/index.md de giu cac lien ket cheo luon nhat quan.
- Query (Truy van):
  1. Tim kiem thong tin cheo giua wiki/ va raw/.
  2. Tra loi cau hoi kem theo trich dan nguon chinh xac duoi dang [[ten-tep]].
  3. Luu lai cau hoi va loi giai phuc tap hoac giai phap sua loi vao wiki/outputs/.
- Lint (Kiem tra va bao tri):
  1. Ra soat cac lien ket bi hong (broken links) hoac trang chua co noi dung.
  2. Phat hien cac thong tin mau thuan giua cac phien ban tai lieu, danh dau the [CAN_XAC_MINH] kem de xuat xu ly.
  3. Khong bao gio tu y xoa du lieu neu chua co yeu cau ro rang tu nguoi dung.
