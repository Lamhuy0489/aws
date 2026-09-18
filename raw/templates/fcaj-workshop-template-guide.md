# Huong Dan Su Dung FCAJ Workshop Template

Nguon: https://github.com/AWS-First-Cloud-Journey/Workshop-template

---

## 1. Tong quan
Workshop-template la bo khung website tao tai lieu ky thuat va bao cao thuc tap dua tren Static Site Generator Hugo, su dung giao dien Hugo Learn Theme.

## 2. Cau truc thu muc cua Template
```text
Workshop-template/
├── config.toml           # Tep cau hinh website (title, baseurl, ngon ngu en/vi)
├── archetypes/           # Mau khoi tao trang moi
├── content/              # Noi dung cac bai viet (Markdown)
│   ├── _index.md         # Trang chu tieng Anh
│   ├── _index.vi.md      # Trang chu tieng Viet
│   ├── 1-Worklog/        # Muc nhat ky theo tuan
│   ├── 2-Proposal/       # Muc de xuat du an
│   ├── 3-BlogsPosted/    # Muc cac bai blog
│   ├── 4-Events/         # Muc su kien tham gia
│   ├── 5-Workshop/       # Noi dung huong dan lab ky thuat
│   ├── 6-Evaluation/     # Tu danh gia ban than
│   └── 7-Feedback/       # Phan hoi chuong trinh
├── layouts/              # Giao dien tuy bien
├── static/               # Chua hinh anh, CSS, JavaScript, file download
└── themes/
    └── hugo-theme-learn/ # Giao dien hoc tap chuan AWS
```

## 3. Cach bien dich va Host tren GitHub Pages
1. Cai dat Hugo (ban extended) tren may tinh:
   ```bash
   brew install hugo
   ```
2. Chay thu nghiem cuc bo (Local Development Server):
   ```bash
   hugo server -D
   ```
   Truy cap tai `http://localhost:1313/`.
3. Bien dich ra file tinh:
   ```bash
   hugo
   ```
   Ket qua xuat ra thu muc `public/`.
4. Deploy len GitHub Pages:
   - Tao repo GitHub rieng cho workshop.
   - Su dung GitHub Actions de tu dong build Hugo hoac push truc tiep thu muc `public/` len nhanh `gh-pages`.
   - Domain truy cap mac dinh co dang: `https://<ten-user>.github.io/<ten-repo>/`.

## 4. Quy uoc file Markdown da ngon ngu
- Moi muc hoac trang viet can co 2 file de ho tro song ngu:
  - `_index.md` hoac `ten-trang.md`: Noi dung tieng Anh.
  - `_index.vi.md` hoac `ten-trang.vi.md`: Noi dung tieng Viet.
- Header cua moi file Markdown (Frontmatter):
  ```yaml
  ---
  title: "Tieu de bai viet"
  date: 2026-09-18
  weight: 1
  chapter: false
  pre: "<b>1. </b>"
  ---
  ```
