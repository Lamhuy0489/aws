/**
 * Logic Kho Lưu Trữ Tài Liệu Cá Nhân (Library)
 * Phân định ranh giới tài khoản chặt chẽ: Chỉ hiển thị và thao tác trên tài liệu của người dùng hiện tại.
 * Hỗ trợ: Xem trước A4, Tải Word/Markdown, và Mở làm việc trực tiếp trong OCR Studio.
 */

let userDocuments = [];
let currentViewingDoc = null;

window.initLibraryPage = () => {
  loadDocuments();

  const searchInput = document.getElementById("librarySearchInput");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      const q = e.target.value.toLowerCase().trim();
      renderDocumentTable(userDocuments.filter(d => 
        d.filename.toLowerCase().includes(q) || (d.model_used && d.model_used.toLowerCase().includes(q))
      ));
    });
  }
  if (window.AppIcons) window.AppIcons.initAutoIcons();
};

document.addEventListener("DOMContentLoaded", () => {
  window.initLibraryPage();
});

let lastLibraryLoadTime = 0;

async function loadDocuments(force = false) {
  const tableBody = document.getElementById("libraryTableBody");
  const emptyState = document.getElementById("libraryEmptyState");
  if (!tableBody) return;

  const now = Date.now();
  // Nếu đã có dữ liệu và vừa tải cách đây chưa đầy 30 giây thì dùng ngay dữ liệu cache không gọi lại backend
  if (!force && userDocuments && userDocuments.length > 0 && (now - lastLibraryLoadTime < 30000)) {
    renderDocumentTable(userDocuments);
    return;
  }

  try {
    const data = await apiFetch("/api/documents");
    userDocuments = data.documents || [];
    lastLibraryLoadTime = Date.now();
    renderDocumentTable(userDocuments);
  } catch (err) {
    // Da hien thi toast qua apiFetch
  }
}

function renderDocumentTable(docs) {
  const tableBody = document.getElementById("libraryTableBody");
  const emptyState = document.getElementById("libraryEmptyState");
  const countBadge = document.getElementById("docCountBadge");

  if (countBadge) {
    countBadge.textContent = `${docs.length} tài liệu`;
  }

  tableBody.innerHTML = "";

  if (!docs.length) {
    if (emptyState) emptyState.style.display = "block";
    return;
  }

  if (emptyState) emptyState.style.display = "none";

  docs.forEach(doc => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>
        <strong style="color: var(--color-foreground);">${escapeHtml(doc.filename)}</strong>
        <div style="font-size: 12px; color: var(--color-muted-foreground);">${(doc.file_size / 1024).toFixed(1)} KB</div>
      </td>
      <td>
        <span class="badge badge-muted">${doc.total_pages} trang</span>
        <span style="font-size: 11px; color: var(--color-muted-foreground); display: block; margin-top: 2px;">
          (Số: ${doc.digital_pages}, Quét: ${doc.scanned_pages})
        </span>
      </td>
      <td>
        <span class="badge badge-muted">${escapeHtml(doc.model_used || "Fast-Path Native")}</span>
      </td>
      <td>${doc.processing_time ? Number(doc.processing_time).toFixed(2) + "s" : "0.00s"}</td>
      <td style="font-size: 12px; color: var(--color-muted-foreground);">${doc.created_at || ""}</td>
      <td>
        <div style="display: flex; gap: 6px; flex-wrap: wrap;">
          <button class="btn btn-primary btn-sm" onclick="openDocInStudio('${doc.id}')" title="Mở tiếp tục làm việc trong OCR Studio" style="display: inline-flex; align-items: center; gap: 4px;">
            <span data-icon="externalLink" data-icon-size="13"></span>
            <span>Mở Trong Studio</span>
          </button>
          <button class="btn btn-outline btn-sm" onclick="viewDocModal('${doc.id}')" title="Xem trước bản dàn trang A4" style="display: inline-flex; align-items: center; gap: 4px;">
            <span data-icon="eye" data-icon-size="13"></span>
            <span>Xem Bản A4</span>
          </button>
          <button class="btn btn-danger btn-sm" onclick="confirmDeleteDoc('${doc.id}', '${escapeHtml(doc.filename)}')" title="Xóa tài liệu khỏi kho" style="display: inline-flex; align-items: center; gap: 4px;">
            <span data-icon="trash" data-icon-size="13"></span>
            <span>Xóa</span>
          </button>
        </div>
      </td>
    `;
    tableBody.appendChild(tr);
  });

  if (window.AppIcons && window.AppIcons.initAutoIcons) {
    window.AppIcons.initAutoIcons();
  }
}

async function viewDocModal(docId) {
  try {
    const data = await apiFetch(`/api/documents/${docId}`);
    const doc = data.document;
    currentViewingDoc = doc;

    document.getElementById("modalDocTitle").textContent = doc.filename;
    const sheet = document.getElementById("modalDocSheet");
    if (window.marked && window.marked.parse) {
      sheet.innerHTML = window.marked.parse(doc.full_markdown || "");
    } else {
      sheet.innerHTML = `<pre style="white-space: pre-wrap;">${escapeHtml(doc.full_markdown || "")}</pre>`;
    }

    document.getElementById("docPreviewModal").style.display = "flex";
    if (window.AppIcons && window.AppIcons.initAutoIcons) {
      window.AppIcons.initAutoIcons();
    }
  } catch (err) {
    showToast("Không thể tải chi tiết tài liệu: " + err.message, "error");
  }
}

window.closeDocModal = () => {
  document.getElementById("docPreviewModal").style.display = "none";
  currentViewingDoc = null;
};

// Mo tai lieu tu kho truc tiep vao giao dien Studio de xem kep va xuat file
window.openDocInStudio = async (docId) => {
  try {
    const data = await apiFetch(`/api/documents/${docId}`);
    if (data && data.document) {
      const doc = data.document;
      const studioDoc = {
        document_id: doc.id,
        filename: doc.filename,
        total_pages: doc.total_pages,
        digital_pages_count: doc.digital_pages,
        scanned_pages_count: doc.scanned_pages,
        full_markdown: doc.full_markdown,
        translated_markdown: doc.translated_markdown || null,
        processing_time_seconds: doc.processing_time || 0,
        model_used: doc.model_used || "Fast-Path Native",
        page_images: []
      };
      try {
        sessionStorage.setItem("hybrid_ocr_active_studio_doc", JSON.stringify(studioDoc));
      } catch (e) {}

      try {
        await fetch("/api/studio/active-document", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ document_id: doc.id })
        });
      } catch (e) {}

      if (window.spaNavigate) {
        window.spaNavigate("/studio");
      } else {
        window.location.href = "/studio";
      }
    }
  } catch (err) {
    showToast("Không thể mở tài liệu trong Studio: " + err.message, "error");
  }
};

window.openCurrentDocInStudio = async () => {
  if (!currentViewingDoc) return;
  const studioDoc = {
    document_id: currentViewingDoc.id,
    filename: currentViewingDoc.filename,
    total_pages: currentViewingDoc.total_pages,
    digital_pages_count: currentViewingDoc.digital_pages,
    scanned_pages_count: currentViewingDoc.scanned_pages,
    full_markdown: currentViewingDoc.full_markdown,
    translated_markdown: currentViewingDoc.translated_markdown || null,
    processing_time_seconds: currentViewingDoc.processing_time || 0,
    model_used: currentViewingDoc.model_used || "Fast-Path Native",
    page_images: []
  };
  try {
    sessionStorage.setItem("hybrid_ocr_active_studio_doc", JSON.stringify(studioDoc));
  } catch (e) {}

  try {
    await fetch("/api/studio/active-document", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ document_id: currentViewingDoc.id })
    });
  } catch (e) {}

  if (window.spaNavigate) {
    window.spaNavigate("/studio");
  } else {
    window.location.href = "/studio";
  }
};

window.downloadModalMarkdown = () => {
  if (!currentViewingDoc) return;
  const blob = new Blob([currentViewingDoc.full_markdown], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${currentViewingDoc.filename}.md`;
  a.click();
  URL.revokeObjectURL(url);
  showToast("Đã tải xuống mã nguồn Markdown", "success");
};

window.downloadModalDocx = async () => {
  if (!currentViewingDoc) return;
  try {
    showToast("Đang kết xuất tệp Word (.docx)...", "info");
    const resp = await fetch("/api/download/docx", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(currentViewingDoc)
    });
    if (!resp.ok) throw new Error("Lỗi khi kết xuất tệp Word");
    const blob = await resp.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${currentViewingDoc.filename}.docx`;
    a.click();
    URL.revokeObjectURL(url);
    showToast("Đã tải xuống tệp Word thành công", "success");
  } catch (err) {
    showToast("Lỗi tải tệp: " + err.message, "error");
  }
};

async function confirmDeleteDoc(docId, filename) {
  if (!confirm(`Bạn có chắc chắn muốn xóa tài liệu "${filename}" khỏi kho lưu trữ? Thao tác này không thể hoàn tác.`)) {
    return;
  }

  try {
    await apiFetch(`/api/documents/${docId}`, { method: "DELETE" });
    showToast("Đã xóa tài liệu thành công", "success");
    loadDocuments();
  } catch (err) {
    showToast("Lỗi khi xóa tài liệu: " + err.message, "error");
  }
}

function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/[&<>'"]/g, 
    tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
  );
}
