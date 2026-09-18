---
name: aws-knowledge-brain
description: >-
  Manage and operate the external knowledge base (Obsidian vault) for the AWS Internship and Agentic RAG project. Use this skill whenever the user wants to ingest new AWS documents or lab notes into raw/, compile concepts and syntheses into wiki/, query the knowledge base with cross-citations, or lint wiki integrity and broken links.
---

# AWS Knowledge Brain Skill

Ky nang chuyen biet de van hanh bo nao tri thuc ngoai vi (External AI Brain) cho du an AWS va Agentic RAG theo phuong phap Karpathy / Obsidian.

## 1. Tong quan kien truc
- raw/: Du lieu nguon tho, chi doc. Chua cac bai viet, paper kien truc, workshop lab.
- wiki/: Tri thuc da duoc bien dich gom index.md, log.md, concepts/, sources/, syntheses/, outputs/.
- templates/: Mau tom tat tai lieu (source-template.md) va mau khai niem (concept-template.md).
- AGENT.md: Quy tac van hanh cot loi cua du an.

## 2. Quy trinh van hanh 4 chu ky

### a. Chu ky Ingest (Tiep nhan tai lieu moi)
Kich hoat khi: Nguoi dung them tai lieu moi vao raw/labs/, raw/articles/, raw/papers/ hoac yeu cau Ingest.
Cac buoc thuc hien:
1. Doc toan bo noi dung tai lieu moi trong raw/.
2. Tao ban tom tat theo bieu mau templates/source-template.md va luu tai wiki/sources/[tac-gia-hoac-to-chuc]-[nam]-[tieu-de-ngan].md.
3. Trich xuat cac thuat ngu, kien truc, dich vu AWS moi vao wiki/concepts/[ten-khai-niem].md theo bieu mau templates/concept-template.md.
4. Cap nhat ban do tri thuc tai wiki/index.md, bo sung cac lien ket hai chieu [[ten-tep]].
5. Ghi nhat ky hoat dong vao wiki/log.md kem ngay thang.

### b. Chu ky Query (Truy van va tich luy)
Kich hoat khi: Nguoi dung hoi ve kien thuc AWS, huong dan lam lab, kien truc Agentic RAG hoac cach sua loi.
Cac buoc thuc hien:
1. Tim kiem cheo tren wiki/ va raw/ de tong hop thong tin chinh xac nhat.
2. Tra loi cau hoi kem theo trich dan ro rang toi cac trang lien quan duoi dang [[ten-tep]].
3. Neu cau tra loi mang tinh giai phap ky thuat phuc tap hoac giai quyet loi quan trong, luu lai vao wiki/outputs/[YYYY-MM-DD]-[ten-chu-de].md de tai su dung.

### c. Chu ky Compile (Bien dich chuyen sau)
Kich hoat khi: Nguoi dung muon tong hop nhieu bai lab hoac dich vu thanh mot chuyen de hoan chinh.
Cac buoc thuc hien:
1. Tong hop kien thuc tu cac bai viet rieng le trong wiki/sources/ va wiki/concepts/.
2. Viet bai tong quan he thong vao wiki/syntheses/[ten-chuyen-de].md.
3. Cap nhat wiki/index.md vao muc "Bai tong hop chuyen sau".

### d. Chu ky Lint (Kiem tra va bao tri)
Kich hoat khi: Nguoi dung yeu cau ra soat hoac kiem tra tinh toan ven cua wiki.
Cac buoc thuc hien:
1. Quet toan bo wiki/ de tim cac lien ket hong (cac the [[...]] tro toi tep khong ton tai).
2. Phat hien thong tin xung dot hoac mau thuan giua cac phien ban tai lieu.
3. Danh dau the [CAN_XAC_MINH] tai vi tri co nghi van kem theo de xuat giai quyet.
4. Khong tu y xoa du lieu goc.

## 3. Tieu chuan trinh bay
- Dat ten tep: Kebab-case (chu thuong ngan cach bang dau gach ngang).
- Lien ket: Cu phap wiki link [[ten-tep]].
- Ngon ngu: Tieng Viet chuan co dau day du, ro rang, ngan gon, chuyen nghiep.
- Khong su dung emoji hoac bieu tuong trang tri.
