/**
 * Logic Kho Luu Tru Tai Lieu Ca Nhan (Library)
 * Phan dinh ranh gioi tai khoan chat che: Chi hien thi va thao tac tren tai lieu cua user hien tai.
 */

let userDocuments = [];
let currentViewingDoc = null;

document.addEventListener("DOMContentLoaded", () => {
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
});

async function loadDocuments() {
  const tableBody = document.getElementById("libraryTableBody");
  const emptyState = document.getElementById("libraryEmptyState");
  if (!tableBody) return;

  try {
    const data = await apiFetch("/api/documents");
    userDocuments = data.documents || [];
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
    countBadge.textContent = `${docs.length} tai lieu`;
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
          (So: ${doc.digital_pages}, Scan: ${doc.scanned_pages})
        </span>
      </td>
      <td>
        <span class="badge badge-muted">${escapeHtml(doc.model_used || "Fast-Path")}</span>
      </td>
      <td>${doc.processing_time ? doc.processing_time.toFixed(2) + "s" : "0.00s"}</td>
      <td style="font-size: 12px; color: var(--color-muted-foreground);">${doc.created_at || ""}</td>
      <td>
        <div style="display: flex; gap: 6px;">
          <button class="btn btn-outline btn-sm" onclick="viewDocModal('${doc.id}')">Xem Ban A4</button>
          <button class="btn btn-danger btn-sm" onclick="confirmDeleteDoc('${doc.id}', '${escapeHtml(doc.filename)}')">Xoa</button>
        </div>
      </td>
    `;
    tableBody.appendChild(tr);
  });
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
  } catch (err) {
    showToast("Khong the tai chi tiet tai lieu: " + err.message, "error");
  }
}

window.closeDocModal = () => {
  document.getElementById("docPreviewModal").style.display = "none";
  currentViewingDoc = null;
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
};

window.downloadModalDocx = async () => {
  if (!currentViewingDoc) return;
  try {
    showToast("Dang tao tep Word (.docx)...", "info");
    const resp = await fetch("/api/download/docx", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(currentViewingDoc)
    });
    if (!resp.ok) throw new Error("Loi khi tao tep Word");
    const blob = await resp.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${currentViewingDoc.filename}.docx`;
    a.click();
    URL.revokeObjectURL(url);
    showToast("Da tai xuong tep Word thanh cong", "success");
  } catch (err) {
    showToast(err.message, "error");
  }
};

async function confirmDeleteDoc(docId, filename) {
  if (!confirm(`Ban co chac chan muon xoa tai lieu "${filename}" khoi kho luu tru?`)) {
    return;
  }

  try {
    await apiFetch(`/api/documents/${docId}`, { method: "DELETE" });
    showToast("Da xoa tai lieu thanh cong", "success");
    loadDocuments();
  } catch (err) {
    showToast("Loi khi xoa tai lieu: " + err.message, "error");
  }
}

function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/[&<>'"]/g, 
    tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
  );
}
