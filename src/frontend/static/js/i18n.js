/**
 * Tu dien da ngon ngu Song ngu Tieng Viet (VI) va Tieng Anh (EN)
 * He thong Serverless Hybrid Document OCR & Parsing Platform
 */

const I18N_DICT = {
  vi: {
    // Header & Navigation
    nav_studio: "Studio Bóc Tách",
    nav_library: "Kho Tài Liệu",
    nav_admin: "Quản Trị Hệ Thống",
    nav_logout: "Đăng Xuất",
    role_admin: "Quản Trị Viên",
    role_user: "Người Dùng",
    
    // Auth Page
    tab_login: "Đăng Nhập",
    tab_register: "Đăng Ký",
    auth_title: "Cổng Đăng Nhập Doanh Nghiệp",
    auth_desc: "Nền tảng OCR & Bóc tách tài liệu hybrid bảo toàn 100% cấu trúc",
    lbl_username: "Tên đăng nhập",
    lbl_password: "Mật khẩu",
    lbl_email: "Địa chỉ email",
    btn_login: "Đăng Nhập Hệ Thống",
    btn_register: "Tạo Tài Khoản Mới",
    
    // Studio Page
    studio_title: "Studio Bóc Tách Tài Liệu",
    studio_subtitle: "Bóc tách văn bản số, bảng biểu phân cấp và công thức toán từ PDF/Ảnh",
    dropzone_title: "Kéo thả tệp PDF hoặc Ảnh tại đây",
    dropzone_desc: "Hỗ trợ tệp PDF, PNG, JPG (Dung lượng tối đa 50MB)",
    lbl_model_select: "Bộ chọn Mô hình OCR / AI",
    opt_model_auto: "Tự động (Fast-Path Native + Tour Xoay Key Siêu Tốc)",
    opt_model_gemini_lite: "Google Gemini Flash Lite (Siêu Tốc - Đề Xuất)",
    opt_model_gemini_flash: "Google Gemini 3.6 Flash Vision (Khóa chính thức)",
    opt_model_kaggle: "Kaggle TPU/GPU (Qwen2.5-VL)",
    opt_model_aws_bedrock: "AWS Native Model (Amazon Bedrock / Nova - Pay-as-you-go)",
    opt_model_groq: "Groq LLaMA 3.2 Vision",
    opt_model_mock: "Mô phỏng Cục bộ (Local Mock)",
    lbl_language: "Ngôn ngữ tài liệu",
    opt_lang_vi: "Tiếng Việt (Có dấu chuẩn)",
    opt_lang_en: "Tiếng Anh (English)",
    opt_lang_multi: "Đa ngôn ngữ kết hợp",
    lbl_fast_path: "Kích hoạt Tầng 1 (Fast-Path Vector bóc tách siêu tốc)",
    btn_process: "Bắt Đầu Bóc Tách Tài Liệu",
    pane_original: "Bản Quét Gốc (Trang",
    pane_markdown: "Bản Xem Trước A4 & Bố Cục Markdown",
    btn_download_docx: "Tải Về Word (.docx)",
    btn_download_md: "Tải Về Markdown (.md)",
    btn_copy: "Sao Chép Toàn Bộ Văn Bản",
    
    // Library Page
    lib_title: "Kho Lưu Trữ Tài Liệu Cá Nhân",
    lib_subtitle: "Toàn bộ tài liệu được bảo mật và cô lập tuyệt đối theo tài khoản của bạn",
    search_placeholder: "Tìm kiếm tài liệu theo tên...",
    th_filename: "Tên Tài Liệu",
    th_pages: "Số Trang (Số/Scan)",
    th_model: "Mô Hình",
    th_time: "Thời Gian Xử Lý",
    th_date: "Ngày Lưu",
    th_actions: "Thao Tác",
    btn_view: "Xem Bản A4",
    btn_delete: "Xóa",
    empty_lib: "Chưa có tài liệu nào trong kho lưu trữ của bạn. Hãy tải tài liệu mới từ Studio.",
    confirm_delete: "Bạn có chắc chắn muốn xóa tài liệu này khỏi kho lưu trữ?",
    
    // Admin Page
    admin_title: "Bảng Điều Khiển Quản Trị Hệ Thống",
    admin_subtitle: "Giám sát tài nguyên, điều phối xoay tour API Key và quản lý tài khoản",
    kpi_users: "Tổng Số Người Dùng",
    kpi_docs: "Tài Liệu Toàn Hệ Thống",
    kpi_keys: "API Key Đang Hoạt Động",
    kpi_usage: "Tổng Lượt Gọi Key Tour",
    sec_key_tour: "Quản Lý Tour Xoay API Key (Round-Robin Key Tour)",
    btn_add_key: "Thêm API Key Vào Tour",
    th_provider: "Nhà Cung Cấp",
    th_alias: "Tên Gợi Nhớ (Alias)",
    th_key_val: "Khóa API (Masked)",
    th_target_model: "Mô Hình Đích",
    th_priority: "Độ Ưu Tiên",
    th_usage_count: "Lượt Đã Dùng",
    th_status: "Trạng Thái",
    status_active: "Hoạt Động",
    status_paused: "Tạm Dừng",
    btn_toggle: "Đổi Trạng Thái",
    sec_users: "Danh Sách Tài Khoản Người Dùng",
    th_user_id: "ID",
    th_username: "Tên Đăng Nhập",
    th_email: "Email",
    th_role: "Vai Trò",
    th_created_at: "Ngày Tạo",
    
    // Modal Add Key
    modal_add_key_title: "Thêm Khóa API Mới Vào Tour Xoay",
    lbl_provider: "Nhà cung cấp (Provider)",
    lbl_key_alias: "Tên gợi nhớ (Alias)",
    lbl_key_value: "Giá trị API Key / Endpoint URL",
    lbl_target_model: "Tên mô hình (Model Name)",
    lbl_base_url: "Base URL (Tùy chọn cho Groq/OpenAI)",
    lbl_priority: "Độ ưu tiên (1 = Cao nhất)",
    btn_save: "Lưu Khóa API",
    btn_cancel: "Hủy",
    
    // Common
    loading: "Đang xử lý...",
    success: "Thao tác thành công",
    error: "Đã xảy ra lỗi"
  },
  en: {
    // Header & Navigation
    nav_studio: "OCR Studio",
    nav_library: "Document Library",
    nav_admin: "System Admin",
    nav_logout: "Log Out",
    role_admin: "Administrator",
    role_user: "Standard User",
    
    // Auth Page
    tab_login: "Sign In",
    tab_register: "Register",
    auth_title: "Enterprise Sign In",
    auth_desc: "Serverless Hybrid Document OCR & Parsing Platform preserving 100% layout",
    lbl_username: "Username",
    lbl_password: "Password",
    lbl_email: "Email Address",
    btn_login: "Sign In to Platform",
    btn_register: "Create New Account",
    
    // Studio Page
    studio_title: "Document OCR Studio",
    studio_subtitle: "Extract digital text, nested tables, and formulas from PDF/Images",
    dropzone_title: "Drag and drop PDF or Image here",
    dropzone_desc: "Supports PDF, PNG, JPG (Maximum size 50MB)",
    lbl_model_select: "OCR / AI Model Selection",
    opt_model_auto: "Automatic (Fast-Path Native + High-Speed Key Tour)",
    opt_model_gemini_lite: "Google Gemini Flash Lite (Ultra Fast - Recommended)",
    opt_model_gemini_flash: "Google Gemini 3.6 Flash Vision (Official Key)",
    opt_model_kaggle: "Kaggle TPU/GPU (Qwen2.5-VL)",
    opt_model_aws_bedrock: "AWS Native Model (Amazon Bedrock / Nova - Pay-as-you-go)",
    opt_model_groq: "Groq LLaMA 3.2 Vision",
    opt_model_mock: "Local Mock Simulation",
    lbl_language: "Document Language",
    opt_lang_vi: "Vietnamese (Standard)",
    opt_lang_en: "English",
    opt_lang_multi: "Multilingual",
    lbl_fast_path: "Enable Layer 1 (Fast-Path Native Vector Extraction)",
    btn_process: "Start Document Parsing",
    pane_original: "Original Scanned Page (Page",
    pane_markdown: "A4 Layout Preview & Structured Markdown",
    btn_download_docx: "Export Word (.docx)",
    btn_download_md: "Export Markdown (.md)",
    btn_copy: "Copy Full Text",
    
    // Library Page
    lib_title: "Personal Document Library",
    lib_subtitle: "All parsed documents are securely isolated under your account",
    search_placeholder: "Search documents by filename...",
    th_filename: "Document Name",
    th_pages: "Pages (Digital/Scan)",
    th_model: "Model Used",
    th_time: "Process Time",
    th_date: "Date Added",
    th_actions: "Actions",
    btn_view: "View A4 Sheet",
    btn_delete: "Delete",
    empty_lib: "No documents in your personal library yet. Upload a new document in Studio.",
    confirm_delete: "Are you sure you want to delete this document from your library?",
    
    // Admin Page
    admin_title: "System Administration Dashboard",
    admin_subtitle: "Monitor resources, orchestrate Key Tour rotations, and manage accounts",
    kpi_users: "Total Registered Users",
    kpi_docs: "Total Documents Processed",
    kpi_keys: "Active API Keys",
    kpi_usage: "Total Tour Call Count",
    sec_key_tour: "API Key Tour Management (Round-Robin Tour)",
    btn_add_key: "Add Key to Tour",
    th_provider: "Provider",
    th_alias: "Alias",
    th_key_val: "API Key (Masked)",
    th_target_model: "Target Model",
    th_priority: "Priority",
    th_usage_count: "Usage Count",
    th_status: "Status",
    status_active: "Active",
    status_paused: "Paused",
    btn_toggle: "Toggle Status",
    sec_users: "Registered User Accounts",
    th_user_id: "ID",
    th_username: "Username",
    th_email: "Email",
    th_role: "Role",
    th_created_at: "Created At",
    
    // Modal Add Key
    modal_add_key_title: "Add New API Key into Rotation Tour",
    lbl_provider: "Provider",
    lbl_key_alias: "Alias Name",
    lbl_key_value: "API Key / Endpoint URL",
    lbl_target_model: "Target Model Name",
    lbl_base_url: "Base URL (Optional for Groq/OpenAI)",
    lbl_priority: "Priority (1 = Highest)",
    btn_save: "Save API Key",
    btn_cancel: "Cancel",
    
    // Common
    loading: "Processing...",
    success: "Operation successful",
    error: "An error occurred"
  }
};

let currentLang = localStorage.getItem("ocr_platform_lang") || "vi";

function setLanguage(lang) {
  if (lang !== "vi" && lang !== "en") return;
  currentLang = lang;
  localStorage.setItem("ocr_platform_lang", lang);
  updatePageLanguage();
}

function t(key) {
  const dict = I18N_DICT[currentLang] || I18N_DICT["vi"];
  return dict[key] || key;
}

function updatePageLanguage() {
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (key && I18N_DICT[currentLang][key]) {
      el.textContent = I18N_DICT[currentLang][key];
    }
  });

  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (key && I18N_DICT[currentLang][key]) {
      el.setAttribute("placeholder", I18N_DICT[currentLang][key]);
    }
  });

  const langBtn = document.getElementById("langSwitcherBtn");
  if (langBtn) {
    langBtn.textContent = currentLang.toUpperCase();
  }
}

document.addEventListener("DOMContentLoaded", () => {
  updatePageLanguage();
  const langBtn = document.getElementById("langSwitcherBtn");
  if (langBtn) {
    langBtn.addEventListener("click", () => {
      setLanguage(currentLang === "vi" ? "en" : "vi");
    });
  }
});
