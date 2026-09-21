/**
 * Logic OCR Studio bóc tách tài liệu
 * Dual-Pane Viewer, Khung xem trước A4 (doc-sheet), Xuất Markdown và Word
 */

let currentProcessedResult = null;
let currentPageIndex = 0;

document.addEventListener("DOMContentLoaded", () => {
  const dropzone = document.getElementById("studioDropzone");
  const fileInput = document.getElementById("studioFileInput");
  const selectedFileInfo = document.getElementById("selectedFileInfo");
  const selectedFileName = document.getElementById("selectedFileName");
  const processBtn = document.getElementById("processBtn");
  const resultViewer = document.getElementById("resultViewer");

  if (!dropzone || !fileInput) return;

  // Click dropzone to open file dialog
  dropzone.addEventListener("click", () => fileInput.click());

  // Drag and drop events
  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("dragover");
  });

  dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("dragover");
  });

  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
    if (e.dataTransfer.files.length > 0) {
      fileInput.files = e.dataTransfer.files;
      handleFileSelected();
    }
  });

  fileInput.addEventListener("change", handleFileSelected);

  function handleFileSelected() {
    if (fileInput.files.length > 0) {
      const file = fileInput.files[0];
      selectedFileName.textContent = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
      selectedFileInfo.style.display = "block";
      processBtn.disabled = false;
    }
  }

  // Quick load sample documents
  window.loadSampleDoc = async (sampleType) => {
    try {
      showToast("Dang nap tai lieu mau: " + sampleType, "info");
      const url = sampleType === "invoice" 
        ? "/data/sample_documents/sample_invoice.pdf" 
        : "/data/sample_documents/sample_contract.pdf";
      
      const resp = await fetch(url);
      if (!resp.ok) throw new Error("Khong the tai tai lieu mau tu may chu");
      const blob = await resp.blob();
      const filename = sampleType === "invoice" ? "sample_invoice.pdf" : "sample_contract.pdf";
      const file = new File([blob], filename, { type: "application/pdf" });

      const dataTransfer = new DataTransfer();
      dataTransfer.items.add(file);
      fileInput.files = dataTransfer.files;
      handleFileSelected();
    } catch (err) {
      showToast(err.message, "error");
    }
  };

  // Process Document
  if (processBtn) {
    processBtn.addEventListener("click", async () => {
      if (!fileInput.files.length) {
        showToast("Vui long chon mot tep truoc", "error");
        return;
      }

      const file = fileInput.files[0];
      const modelChoice = document.getElementById("modelSelect").value;
      const language = document.getElementById("langSelect").value;
      const fastPath = document.getElementById("fastPathToggle").checked;

      const formData = new FormData();
      formData.append("file", file);
      formData.append("model_choice", modelChoice);
      formData.append("language", language);
      formData.append("fast_path", fastPath ? "true" : "false");

      processBtn.disabled = true;
      processBtn.textContent = t("loading");

      try {
        const response = await fetch("/api/process", {
          method: "POST",
          body: formData
        });

        if (response.status === 401) {
          window.location.href = `/login?next=${encodeURIComponent(window.location.pathname)}`;
          return;
        }

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.error || "Loi boc tach tai lieu");
        }

        currentProcessedResult = data;
        currentPageIndex = 0;
        renderResult(data);
        showToast(t("success"), "success");
      } catch (err) {
        showToast(err.message, "error");
      } finally {
        processBtn.disabled = false;
        processBtn.textContent = t("btn_process");
      }
    });
  }

  function renderResult(data) {
    if (!resultViewer) return;
    resultViewer.style.display = "grid";

    // Summary stats
    document.getElementById("statPages").textContent = `${data.total_pages} (So: ${data.digital_pages_count}, Scan: ${data.scanned_pages_count})`;
    document.getElementById("statTime").textContent = `${data.processing_time_seconds.toFixed(2)}s`;

    // Render Page Image
    renderPageImage();

    // Render A4 Sheet Markdown
    const docSheet = document.getElementById("docSheetContent");
    if (window.marked && window.marked.parse) {
      docSheet.innerHTML = window.marked.parse(data.full_markdown);
    } else {
      docSheet.innerHTML = `<pre style="white-space: pre-wrap; font-family: monospace;">${escapeHtml(data.full_markdown)}</pre>`;
    }

    resultViewer.scrollIntoView({ behavior: "smooth" });
  }

  function renderPageImage() {
    const imgContainer = document.getElementById("pageImageContainer");
    const pageIndicator = document.getElementById("pageIndicator");
    const prevBtn = document.getElementById("prevPageBtn");
    const nextBtn = document.getElementById("nextPageBtn");

    if (!currentProcessedResult || !currentProcessedResult.page_images || !currentProcessedResult.page_images.length) {
      imgContainer.innerHTML = `<div style="padding: 40px; text-align: center; color: var(--color-muted-foreground);">Khong co hinh anh trang xem truoc</div>`;
      pageIndicator.textContent = "0 / 0";
      return;
    }

    const total = currentProcessedResult.page_images.length;
    pageIndicator.textContent = `${currentPageIndex + 1} / ${total}`;
    prevBtn.disabled = currentPageIndex === 0;
    nextBtn.disabled = currentPageIndex >= total - 1;

    const base64Img = currentProcessedResult.page_images[currentPageIndex];
    imgContainer.innerHTML = `<img src="data:image/png;base64,${base64Img}" alt="Trang ${currentPageIndex + 1}" style="width: 100%; height: auto; border: 1px solid var(--color-border); box-shadow: var(--shadow-sm);" />`;
  }

  window.prevPage = () => {
    if (currentPageIndex > 0) {
      currentPageIndex--;
      renderPageImage();
    }
  };

  window.nextPage = () => {
    if (currentProcessedResult && currentPageIndex < currentProcessedResult.page_images.length - 1) {
      currentPageIndex++;
      renderPageImage();
    }
  };

  // Download Markdown
  window.downloadMarkdown = () => {
    if (!currentProcessedResult) return;
    const blob = new Blob([currentProcessedResult.full_markdown], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${currentProcessedResult.filename}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Download Word .docx
  window.downloadDocx = async () => {
    if (!currentProcessedResult) return;
    try {
      showToast("Dang tao tep Word (.docx)...", "info");
      const resp = await fetch("/api/download/docx", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(currentProcessedResult)
      });
      if (!resp.ok) throw new Error("Loi khi tao tep Word");
      const blob = await resp.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${currentProcessedResult.filename}.docx`;
      a.click();
      URL.revokeObjectURL(url);
      showToast("Da tai xuong tep Word thanh cong", "success");
    } catch (err) {
      showToast(err.message, "error");
    }
  };

  // Copy Full Text
  window.copyText = () => {
    if (!currentProcessedResult) return;
    navigator.clipboard.writeText(currentProcessedResult.full_markdown)
      .then(() => showToast("Da sao chep toan bo noi dung vao bo nho tam", "success"))
      .catch(() => showToast("Khong the sao chep van ban", "error"));
  };

  function escapeHtml(str) {
    return str.replace(/[&<>'"]/g, 
      tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
    );
  }
});
