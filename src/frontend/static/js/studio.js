/**
 * Logic OCR Studio Bóc Tách Tài Liệu Enterprise
 * Tích hợp: Thanh tiến trình 5 bước, Xuất PDF/Word, Toàn màn hình, Dịch thuật AI & 2D Vector Icons
 */

let currentProcessedResult = null;
let currentPageIndex = 0;
let currentActiveDocTab = "original"; // "original" hoac "translated"
let currentViewMode = "preview"; // "preview" hoac "editor"
let pipelineInterval = null;

window.initStudioPage = () => {
  const dropZone = document.getElementById("dropZone") || document.getElementById("studioDropzone");
  const fileInput = document.getElementById("fileInput") || document.getElementById("studioFileInput");
  const selectedFileInfo = document.getElementById("selectedFileInfo") || document.getElementById("fileInfoBox");
  const selectedFileName = document.getElementById("selectedFileName") || document.getElementById("fileNameDisplay");
  const processBtn = document.getElementById("processBtn");
  const emptyGuide = document.getElementById("emptyStudioGuide");
  const resultViewer = document.getElementById("resultViewer");

  // Khoi tao cac 2D Vector Icons chuan ky thuat
  initStudioIcons();

  let selectedFile = null;

  if (dropZone && fileInput) {
    // Click vao dropzone de mo file dialog
    dropZone.addEventListener("click", () => {
      fileInput.click();
    });

    // Tranh noi bot su kien click tu fileInput nguoc len dropZone
    fileInput.addEventListener("click", (e) => {
      e.stopPropagation();
    });

    // Keo tha tap tin (Drag & Drop)
    dropZone.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZone.classList.add("dragover");
    });

    dropZone.addEventListener("dragleave", () => {
      dropZone.classList.remove("dragover");
    });

    dropZone.addEventListener("drop", (e) => {
      e.preventDefault();
      dropZone.classList.remove("dragover");
      if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        try {
          fileInput.files = e.dataTransfer.files;
        } catch (err) {
          // Trinh duyet khong cho phep gan FileList
        }
        handleFileSelected(e.dataTransfer.files[0]);
      }
    });

    fileInput.addEventListener("change", (e) => {
      if (e.target.files && e.target.files.length > 0) {
        handleFileSelected(e.target.files[0]);
      }
    });
  }

  function handleFileSelected(file) {
    if (!file && fileInput && fileInput.files && fileInput.files.length > 0) {
      file = fileInput.files[0];
    }
    if (!file) return;

    selectedFile = file;
    if (selectedFileName) {
      selectedFileName.textContent = `${file.name} (${formatBytes(file.size)})`;
    }
    if (selectedFileInfo) {
      selectedFileInfo.style.display = "block";
    }
    if (processBtn) {
      processBtn.disabled = false;
    }
    showToast("Đã chọn tệp: " + file.name, "success");
  }

  const STUDIO_STORAGE_KEY = "hybrid_ocr_active_studio_doc";

  function saveDocState(docData) {
    if (!docData) return;
    try {
      const safeDoc = {
        document_id: docData.document_id,
        filename: docData.filename,
        total_pages: docData.total_pages,
        digital_pages_count: docData.digital_pages_count !== undefined ? docData.digital_pages_count : docData.digital_pages,
        scanned_pages_count: docData.scanned_pages_count !== undefined ? docData.scanned_pages_count : docData.scanned_pages,
        full_markdown: docData.full_markdown,
        translated_markdown: docData.translated_markdown || null,
        processing_time_seconds: docData.processing_time_seconds !== undefined ? docData.processing_time_seconds : docData.processing_time,
        model_used: docData.model_used,
        page_images: (docData.page_images && docData.page_images.length > 0 && docData.page_images[0] && docData.page_images[0].length < 400000)
          ? [docData.page_images[0]]
          : []
      };
      sessionStorage.setItem(STUDIO_STORAGE_KEY, JSON.stringify(safeDoc));
    } catch (e) {
      console.warn("Dung lượng bộ nhớ vượt mức, lưu cấu trúc tối giản:", e);
      try {
        const minimalDoc = {
          document_id: docData.document_id,
          filename: docData.filename,
          total_pages: docData.total_pages,
          digital_pages_count: docData.digital_pages_count,
          scanned_pages_count: docData.scanned_pages_count,
          full_markdown: docData.full_markdown,
          translated_markdown: docData.translated_markdown || null,
          processing_time_seconds: docData.processing_time_seconds,
          model_used: docData.model_used,
          page_images: []
        };
        sessionStorage.setItem(STUDIO_STORAGE_KEY, JSON.stringify(minimalDoc));
      } catch (err2) {
        console.error("Không thể lưu cache vào storage:", err2);
      }
    }
  }

  let lastStudioSyncTime = 0;

  // Tự động khôi phục tài liệu khi chuyển tab hoặc tải lại trang
  restoreActiveStudioDoc();

  async function restoreActiveStudioDoc(force = false) {
    const now = Date.now();
    // Nếu trong bộ nhớ RAM đã có tài liệu và vừa đồng bộ cách đây chưa đầy 30 giây:
    if (!force && currentProcessedResult && currentProcessedResult.full_markdown && (now - lastStudioSyncTime < 30000)) {
      if (emptyGuide) emptyGuide.style.display = "none";
      if (resultViewer) resultViewer.style.display = "grid";
      if (selectedFileInfo) selectedFileInfo.style.display = "block";
      return;
    }

    // 1. Phục hồi tức thì từ sessionStorage nếu có
    try {
      const savedDocStr = sessionStorage.getItem(STUDIO_STORAGE_KEY);
      if (savedDocStr) {
        const savedDoc = JSON.parse(savedDocStr);
        if (savedDoc && (savedDoc.full_markdown || savedDoc.filename)) {
          currentProcessedResult = savedDoc;
          currentPageIndex = 0;
          currentActiveDocTab = savedDoc.translated_markdown ? "translated" : "original";
          if (emptyGuide) emptyGuide.style.display = "none";
          renderResult(savedDoc, false);
          if (savedDoc.translated_markdown) {
            switchDocTab("translated");
          }
          if (selectedFileName && savedDoc.filename) {
            selectedFileName.textContent = `${savedDoc.filename} (Đang mở trong Studio)`;
          }
          if (selectedFileInfo) {
            selectedFileInfo.style.display = "block";
          }
          if (window.AppIcons) window.AppIcons.initAutoIcons();
        }
      }
    } catch (e) {
      console.warn("Không thể đọc từ sessionStorage:", e);
    }

    // 2. Đồng bộ từ backend CSDL SQLite âm thầm, chỉ re-render khi có thay đổi thực sự
    try {
      const resp = await fetch("/api/studio/active-document");
      if (resp.ok) {
        const data = await resp.json();
        if (data && data.document) {
          const doc = data.document;
          // Nếu dữ liệu giống hệt với dữ liệu đã hiển thị từ cache, KHÔNG re-render DOM để tránh chớp nháy
          if (currentProcessedResult && currentProcessedResult.document_id === doc.id && currentProcessedResult.full_markdown === doc.full_markdown) {
            if (doc.translated_markdown && !currentProcessedResult.translated_markdown) {
              currentProcessedResult.translated_markdown = doc.translated_markdown;
              saveDocState(currentProcessedResult);
            }
            return;
          }

          currentProcessedResult = {
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
          currentPageIndex = 0;
          currentActiveDocTab = doc.translated_markdown ? "translated" : "original";
          if (emptyGuide) emptyGuide.style.display = "none";
          renderResult(currentProcessedResult, false);
          if (doc.translated_markdown) {
            switchDocTab("translated");
          }
          if (selectedFileName && doc.filename) {
            selectedFileName.textContent = `${doc.filename} (Đang mở trong Studio)`;
          }
          if (selectedFileInfo) {
            selectedFileInfo.style.display = "block";
          }
          if (window.AppIcons) window.AppIcons.initAutoIcons();
          saveDocState(currentProcessedResult);
        }
      }
      lastStudioSyncTime = Date.now();
    } catch (apiErr) {
      console.warn("Không thể lấy active-document từ server:", apiErr);
    }
  }

  window.clearSelectedFile = async () => {
    selectedFile = null;
    currentProcessedResult = null;
    try {
      sessionStorage.removeItem(STUDIO_STORAGE_KEY);
    } catch (e) {}
    try {
      await fetch("/api/studio/active-document", { method: "DELETE" });
    } catch (e) {}
    if (fileInput) fileInput.value = "";
    if (selectedFileInfo) selectedFileInfo.style.display = "none";
    if (processBtn) processBtn.disabled = true;
    if (resultViewer) resultViewer.style.display = "none";
    if (emptyGuide) emptyGuide.style.display = "block";
    const pipelineCard = document.getElementById("pipelineProgressCard");
    if (pipelineCard) pipelineCard.style.display = "none";
    window.switchViewMode("preview");
    showToast("Đã đóng tài liệu và làm mới vùng làm việc", "info");
  };

  // Xu ly boc tach tai lieu
  if (processBtn) {
    processBtn.addEventListener("click", async () => {
      try {
        const file = selectedFile || (fileInput && fileInput.files && fileInput.files[0]);
        if (!file) {
          showToast("Vui lòng chọn một tệp tài liệu trước", "error");
          return;
        }

        const modelEl = document.getElementById("modelChoice") || document.getElementById("modelSelect");
        const modelChoice = modelEl ? modelEl.value : "auto";

        const langEl = document.getElementById("docLanguage") || document.getElementById("langSelect");
        const language = langEl ? langEl.value : "vi";

        const fastPathEl = document.getElementById("fastPathToggle");
        const fastPath = fastPathEl ? fastPathEl.checked : true;

        const formData = new FormData();
        formData.append("file", file);
        formData.append("model_choice", modelChoice);
        formData.append("language", language);
        formData.append("fast_path", fastPath ? "true" : "false");

        processBtn.disabled = true;
        const btnText = document.getElementById("processBtnText");
        if (btnText) {
          btnText.textContent = "Đang xử lý tài liệu...";
        } else {
          processBtn.textContent = "Đang xử lý tài liệu...";
        }

        if (emptyGuide) emptyGuide.style.display = "none";

        // Kich hoat thanh tien trinh 5 buoc ngay lap tuc
        startPipelineProgress();

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
          throw new Error(data.error || "Lỗi bóc tách tài liệu");
        }

        currentProcessedResult = data;
        currentPageIndex = 0;
        currentActiveDocTab = "original";

        // Luu vao storage an toan de bao toan trang thai khi chuyen tab hoac tai lai trang
        saveDocState(data);

        // Hoan thanh tien trinh 100%
        finishPipelineProgress();

        renderResult(data, true);
        if (window.AppIcons) window.AppIcons.initAutoIcons();
        showToast("Bóc tách tài liệu thành công", "success");
      } catch (err) {
        showPipelineError(err.message);
        showToast("Lỗi xử lý: " + err.message, "error");
        if (emptyGuide && (!currentProcessedResult)) emptyGuide.style.display = "block";
      } finally {
        processBtn.disabled = false;
        const btnText = document.getElementById("processBtnText");
        if (btnText) {
          btnText.textContent = "Bắt Đầu Bóc Tách Tài Liệu";
        } else {
          processBtn.textContent = "Bắt Đầu Bóc Tách Tài Liệu";
        }
      }
    });
  }

  let cachedOriginalHtml = null;
  let cachedTranslatedHtml = null;

  function renderResult(data, shouldScroll = false) {
    if (!resultViewer) return;
    resultViewer.style.display = "grid";

    cachedOriginalHtml = null;
    cachedTranslatedHtml = null;

    // Cap nhat thong ke
    const digitalCount = data.digital_pages_count !== undefined ? data.digital_pages_count : (data.digital_pages || 0);
    const scannedCount = data.scanned_pages_count !== undefined ? data.scanned_pages_count : (data.scanned_pages || 0);
    document.getElementById("statPages").textContent = `${data.total_pages || 1} (Số: ${digitalCount}, Quét: ${scannedCount})`;

    const timeVal = data.processing_time_seconds !== undefined ? data.processing_time_seconds : (data.processing_time || 0);
    document.getElementById("statTime").textContent = `${Number(timeVal).toFixed(2)}s`;

    const modelChoiceEl = document.getElementById("modelChoice");
    const modelText = data.model_used || (modelChoiceEl && modelChoiceEl.options[modelChoiceEl.selectedIndex] ? modelChoiceEl.options[modelChoiceEl.selectedIndex].text : "Fast-Path Native");
    document.getElementById("statModel").textContent = modelText;

    const tabOrig = document.getElementById("tabOriginal");
    const tabTrans = document.getElementById("tabTranslated");
    if (currentActiveDocTab === "translated" && data.translated_markdown) {
      tabTrans.classList.add("active");
      tabOrig.classList.remove("active");
    } else {
      tabOrig.classList.add("active");
      tabTrans.classList.remove("active");
    }

    // Hien thi anh scan goc va Markdown A4
    renderPageImage();
    if (currentActiveDocTab === "translated" && data.translated_markdown) {
      renderDocSheetContent(data.translated_markdown);
    } else {
      renderDocSheetContent(data.full_markdown);
    }

    // Dong bo noi dung vao trinh chinh sua Markdown neu dang o che do Editor
    if (currentViewMode === "editor") {
      const editorInput = document.getElementById("markdownEditorInput");
      if (editorInput) {
        editorInput.value = (currentActiveDocTab === "translated" && data.translated_markdown)
          ? data.translated_markdown
          : (data.full_markdown || "");
      }
    }

    if (window.AppIcons) window.AppIcons.initAutoIcons();
    if (shouldScroll) {
      resultViewer.scrollIntoView({ behavior: "smooth" });
    }
  }

  function renderDocSheetContent(markdownText) {
    const docSheet = document.getElementById("docSheetContent");
    if (!docSheet) return;
    if (window.marked && window.marked.parse) {
      docSheet.innerHTML = window.marked.parse(markdownText);
    } else {
      docSheet.innerHTML = `<pre style="white-space: pre-wrap; font-family: monospace;">${escapeHtml(markdownText)}</pre>`;
    }
  }

  function renderPageImage() {
    const imgContainer = document.getElementById("pageImageContainer");
    const pageIndicator = document.getElementById("pageIndicator");
    const prevBtn = document.getElementById("prevPageBtn");
    const nextBtn = document.getElementById("nextPageBtn");

    if (!currentProcessedResult || !currentProcessedResult.page_images || !currentProcessedResult.page_images.length) {
      imgContainer.innerHTML = `<div style="padding: 40px; text-align: center; color: var(--color-muted-foreground);">Không có hình ảnh trang xem trước</div>`;
      pageIndicator.textContent = "0 / 0";
      return;
    }

    const total = currentProcessedResult.page_images.length;
    pageIndicator.textContent = `${currentPageIndex + 1} / ${total}`;
    prevBtn.disabled = currentPageIndex === 0;
    nextBtn.disabled = currentPageIndex >= total - 1;

    const base64Img = currentProcessedResult.page_images[currentPageIndex];
    const imgSrc = base64Img.startsWith("data:") ? base64Img : `data:image/png;base64,${base64Img}`;
    imgContainer.innerHTML = `<img id="currentScanImg" src="${imgSrc}" alt="Trang ${currentPageIndex + 1}" style="width: 100%; max-width: 600px; height: auto; border: 1px solid var(--color-border); box-shadow: var(--shadow-sm); border-radius: 4px;" />`;
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

  // Chuyen doi Tab Ban Goc / Ban Dich Song Ngu
  window.switchDocTab = (tabName) => {
    if (!currentProcessedResult) return;
    currentActiveDocTab = tabName;

    const tabOrig = document.getElementById("tabOriginal");
    const tabTrans = document.getElementById("tabTranslated");
    const docSheet = document.getElementById("docSheetContent");

    if (tabName === "original") {
      tabOrig.classList.add("active");
      tabTrans.classList.remove("active");
      if (!cachedOriginalHtml && currentProcessedResult.full_markdown) {
        cachedOriginalHtml = (window.marked && window.marked.parse)
          ? window.marked.parse(currentProcessedResult.full_markdown)
          : `<pre style="white-space: pre-wrap; font-family: monospace;">${escapeHtml(currentProcessedResult.full_markdown)}</pre>`;
      }
      if (docSheet) docSheet.innerHTML = cachedOriginalHtml || "";
    } else {
      tabTrans.classList.add("active");
      tabOrig.classList.remove("active");
      if (currentProcessedResult.translated_markdown) {
        if (!cachedTranslatedHtml) {
          cachedTranslatedHtml = (window.marked && window.marked.parse)
            ? window.marked.parse(currentProcessedResult.translated_markdown)
            : `<pre style="white-space: pre-wrap; font-family: monospace;">${escapeHtml(currentProcessedResult.translated_markdown)}</pre>`;
        }
        if (docSheet) docSheet.innerHTML = cachedTranslatedHtml;
      } else {
        if (docSheet) {
          docSheet.innerHTML = `
            <div style="text-align: center; padding: 60px 20px; color: var(--color-muted-foreground);">
              <p style="font-size: 14px; margin-bottom: 12px;">Tài liệu này chưa có bản dịch.</p>
              <p style="font-size: 13px;">Vui lòng chọn ngôn ngữ đích bên trên và bấm <strong>Dịch Thuật</strong> để kích hoạt Gemini AI.</p>
            </div>
          `;
        }
      }
    }

    // Dong bo noi dung neu dang o che do Editor
    if (currentViewMode === "editor") {
      const editorInput = document.getElementById("markdownEditorInput");
      if (editorInput) {
        editorInput.value = (tabName === "translated" && currentProcessedResult.translated_markdown)
          ? currentProcessedResult.translated_markdown
          : (currentProcessedResult.full_markdown || "");
      }
    }
  };

  // Chuyen doi che do Xem Truoc (Preview) va Chinh Sua Markdown (Editor)
  window.switchViewMode = (mode) => {
    currentViewMode = mode;
    const tabPrev = document.getElementById("tabModePreview");
    const tabEdit = document.getElementById("tabModeEditor");
    const docSheet = document.getElementById("docSheetContent");
    const editorContainer = document.getElementById("markdownEditorContainer");
    const editorInput = document.getElementById("markdownEditorInput");

    if (mode === "editor") {
      if (tabEdit) tabEdit.classList.add("active");
      if (tabPrev) tabPrev.classList.remove("active");
      if (docSheet) docSheet.style.display = "none";
      if (editorContainer) editorContainer.style.display = "flex";

      if (editorInput && currentProcessedResult) {
        const currentMd = (currentActiveDocTab === "translated" && currentProcessedResult.translated_markdown)
          ? currentProcessedResult.translated_markdown
          : (currentProcessedResult.full_markdown || "");
        editorInput.value = currentMd;
      }
    } else {
      if (tabPrev) tabPrev.classList.add("active");
      if (tabEdit) tabEdit.classList.remove("active");
      if (editorContainer) editorContainer.style.display = "none";
      if (docSheet) docSheet.style.display = "block";

      if (currentProcessedResult) {
        const currentMd = (currentActiveDocTab === "translated" && currentProcessedResult.translated_markdown)
          ? currentProcessedResult.translated_markdown
          : (currentProcessedResult.full_markdown || "");
        renderDocSheetContent(currentMd);
      }
    }
    if (window.AppIcons) window.AppIcons.initAutoIcons();
  };

  // Luu noi dung Markdown da chinh sua
  window.saveMarkdownContent = async () => {
    if (!currentProcessedResult) {
      showToast("Không tìm thấy dữ liệu tài liệu để lưu", "error");
      return;
    }

    const editorInput = document.getElementById("markdownEditorInput");
    if (!editorInput) return;
    const updatedText = editorInput.value;

    const saveBtn = document.getElementById("btnSaveMarkdown");
    if (saveBtn) {
      saveBtn.disabled = true;
      saveBtn.innerHTML = `<span>Đang lưu...</span>`;
    }

    try {
      const docId = currentProcessedResult.document_id;
      const resp = await fetch(`/api/studio/document/${encodeURIComponent(docId)}/markdown`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          markdown: updatedText,
          tab_type: currentActiveDocTab
        })
      });

      const resData = await resp.json();
      if (!resp.ok) {
        throw new Error(resData.error || "Không thể lưu nội dung Markdown");
      }

      if (currentActiveDocTab === "translated") {
        currentProcessedResult.translated_markdown = updatedText;
        cachedTranslatedHtml = null;
      } else {
        currentProcessedResult.full_markdown = updatedText;
        cachedOriginalHtml = null;
      }

      saveDocState(currentProcessedResult);
      renderDocSheetContent(updatedText);

      showToast("Đã lưu nội dung Markdown thành công", "success");
    } catch (err) {
      showToast("Lỗi lưu Markdown: " + err.message, "error");
    } finally {
      if (saveBtn) {
        saveBtn.disabled = false;
        saveBtn.innerHTML = `<span data-icon="check" data-icon-size="14"></span> <span>Lưu Thay Đổi</span>`;
        if (window.AppIcons) window.AppIcons.initAutoIcons();
      }
    }
  };

  // Dich thuat AI song ngu
  window.translateDocument = async () => {
    if (!currentProcessedResult || !currentProcessedResult.full_markdown) {
      showToast("Vui lòng bóc tách tài liệu trước khi dịch", "error");
      return;
    }

    const targetLang = document.getElementById("translateTargetLang").value;
    const btn = document.getElementById("btnTranslate");
    btn.disabled = true;
    btn.innerHTML = `<span data-icon="refresh" data-icon-size="14"></span> <span>Đang dịch thuật...</span>`;
    if (window.AppIcons) window.AppIcons.initAutoIcons();
    showToast("Hệ thống đang tiến hành dịch thuật tài liệu...", "info");

    try {
      const modelSelect = document.getElementById("selectModel");
      const currentModel = modelSelect ? modelSelect.value : "";

      const resp = await fetch("/api/translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          markdown: currentProcessedResult.full_markdown,
          target_lang: targetLang,
          model: currentModel
        })
      });

      const data = await resp.json();
      if (!resp.ok) throw new Error(data.error || "Lỗi dịch thuật");

      currentProcessedResult.translated_markdown = data.translated_markdown;
      saveDocState(currentProcessedResult);

      showToast("Dịch thuật tài liệu hoàn tất thành công", "success");
      switchDocTab("translated");
    } catch (err) {
      showToast("Lỗi dịch thuật: " + err.message, "error");
    } finally {
      btn.disabled = false;
      btn.innerHTML = `<span data-icon="translate" data-icon-size="14"></span> <span>Dịch Thuật</span>`;
      if (window.AppIcons) window.AppIcons.initAutoIcons();
    }
  };

  // Xuat PDF chuan A4
  window.downloadPdf = async () => {
    if (!currentProcessedResult) return;
    try {
      showToast("Đang kết xuất tệp PDF in ấn...", "info");
      const activeMd = (currentActiveDocTab === "translated" && currentProcessedResult.translated_markdown)
        ? currentProcessedResult.translated_markdown
        : currentProcessedResult.full_markdown;

      const resp = await fetch("/api/download/pdf", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          document_id: currentProcessedResult.document_id,
          filename: currentProcessedResult.filename,
          total_pages: currentProcessedResult.total_pages,
          digital_pages_count: currentProcessedResult.digital_pages_count,
          scanned_pages_count: currentProcessedResult.scanned_pages_count,
          full_markdown: activeMd
        })
      });

      if (!resp.ok) {
        const err = await resp.json();
        throw new Error(err.error || "Lỗi tạo tệp PDF");
      }

      const blob = await resp.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      const suffix = currentActiveDocTab === "translated" ? "_dich" : "";
      a.download = `${currentProcessedResult.filename}${suffix}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
      showToast("Tải tệp PDF thành công", "success");
    } catch (err) {
      showToast("Lỗi tải tệp PDF: " + err.message, "error");
    }
  };

  // Xuat Word (.docx)
  window.downloadDocx = async () => {
    if (!currentProcessedResult) return;
    try {
      showToast("Đang tạo tệp Word (.docx) chuẩn thể thức...", "info");
      const activeMd = (currentActiveDocTab === "translated" && currentProcessedResult.translated_markdown)
        ? currentProcessedResult.translated_markdown
        : currentProcessedResult.full_markdown;

      const resp = await fetch("/api/download/docx", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          document_id: currentProcessedResult.document_id,
          filename: currentProcessedResult.filename,
          total_pages: currentProcessedResult.total_pages,
          digital_pages_count: currentProcessedResult.digital_pages_count,
          scanned_pages_count: currentProcessedResult.scanned_pages_count,
          full_markdown: activeMd
        })
      });

      if (!resp.ok) {
        const err = await resp.json();
        throw new Error(err.error || "Lỗi tạo tệp Word");
      }

      const blob = await resp.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      const suffix = currentActiveDocTab === "translated" ? "_dich" : "";
      a.download = `${currentProcessedResult.filename}${suffix}.docx`;
      a.click();
      URL.revokeObjectURL(url);
      showToast("Tải tệp Word thành công", "success");
    } catch (err) {
      showToast("Lỗi tải tệp Word: " + err.message, "error");
    }
  };

  // Xuat Markdown
  window.downloadMarkdown = () => {
    if (!currentProcessedResult) return;
    const activeMd = (currentActiveDocTab === "translated" && currentProcessedResult.translated_markdown)
      ? currentProcessedResult.translated_markdown
      : currentProcessedResult.full_markdown;

    const blob = new Blob([activeMd], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    const suffix = currentActiveDocTab === "translated" ? "_dich" : "";
    a.download = `${currentProcessedResult.filename}${suffix}.md`;
    a.click();
    URL.revokeObjectURL(url);
    showToast("Đã tải tệp Markdown", "success");
  };

  // Sao chep van ban
  window.copyText = () => {
    if (!currentProcessedResult) return;
    const activeMd = (currentActiveDocTab === "translated" && currentProcessedResult.translated_markdown)
      ? currentProcessedResult.translated_markdown
      : currentProcessedResult.full_markdown;

    navigator.clipboard.writeText(activeMd).then(() => {
      showToast("Đã sao chép nội dung vào khay nhớ tạm", "success");
    }).catch((err) => {
      showToast("Không thể sao chép: " + err.message, "error");
    });
  };

  // Toan Man Hinh (Fullscreen Viewer Modal)
  window.expandImage = () => {
    if (!currentProcessedResult || !currentProcessedResult.page_images.length) return;
    const modal = document.getElementById("fullscreenModal");
    const body = document.getElementById("fullscreenBody");
    const title = document.getElementById("fullscreenTitle");

    const base64Img = currentProcessedResult.page_images[currentPageIndex];
    const imgSrc = base64Img.startsWith("data:") ? base64Img : `data:image/png;base64,${base64Img}`;
    title.textContent = `Bản Quét Gốc - Trang ${currentPageIndex + 1} / ${currentProcessedResult.page_images.length}`;
    body.innerHTML = `<img src="${imgSrc}" alt="Scan Trang ${currentPageIndex + 1}" style="max-width: 100%; height: auto; border: 1px solid var(--color-border); box-shadow: var(--shadow-lg);" />`;
    modal.style.display = "flex";
  };

  window.expandDocument = () => {
    if (!currentProcessedResult) return;
    const modal = document.getElementById("fullscreenModal");
    const body = document.getElementById("fullscreenBody");
    const title = document.getElementById("fullscreenTitle");

    const tabLabel = currentActiveDocTab === "translated" ? "Bản Dịch AI" : "Bản Gốc";
    title.textContent = `Bản Xem Trước A4 (${tabLabel}) - ${currentProcessedResult.filename}`;
    const activeMd = (currentActiveDocTab === "translated" && currentProcessedResult.translated_markdown)
      ? currentProcessedResult.translated_markdown
      : currentProcessedResult.full_markdown;

    const rendered = window.marked && window.marked.parse ? window.marked.parse(activeMd) : activeMd;
    body.innerHTML = `<div class="doc-sheet" style="max-width: 900px; width: 100%;">${rendered}</div>`;
    modal.style.display = "flex";
  };

  window.closeFullscreen = () => {
    const modal = document.getElementById("fullscreenModal");
    if (modal) modal.style.display = "none";
  };

  // Bat phim ESC de dong modal toan man hinh
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeFullscreen();
    }
  });

  // Quan ly Thanh Tien Trinh Da Tang (5 Buoc)
  function startPipelineProgress() {
    const card = document.getElementById("pipelineProgressCard");
    const status = document.getElementById("pipelineStatusText");
    const bar = document.getElementById("pipelineProgressBar");

    if (!card) return;
    card.style.display = "block";

    if (status) {
      status.style.color = "";
      status.textContent = "Đang khởi tạo...";
    }
    if (bar) {
      bar.style.backgroundColor = "";
      bar.style.width = "0%";
    }

    for (let i = 1; i <= 5; i++) {
      const el = document.getElementById(`step${i}`);
      if (el) {
        el.classList.remove("active", "completed", "error");
      }
    }

    setStep(1, "Đang tải lên và phân tích cấu trúc tài liệu...", 20);

    let progress = 20;
    clearInterval(pipelineInterval);
    pipelineInterval = setInterval(() => {
      progress += 4;
      if (progress > 85) {
        progress = 85;
        clearInterval(pipelineInterval);
      }
      if (bar) bar.style.width = `${progress}%`;

      if (progress >= 35 && progress < 55) {
        setStep(2, "Đang phân loại trang văn bản số vs ảnh quét...", progress);
      } else if (progress >= 55 && progress < 75) {
        setStep(3, "Đang trích xuất cấu trúc bảng & văn bản Fast-Path...", progress);
      } else if (progress >= 75) {
        setStep(4, "Kích hoạt mô hình Vision OCR xử lý trang scan...", progress);
      }
    }, 450);
  }

  function setStep(stepNum, text, percent) {
    const status = document.getElementById("pipelineStatusText");
    const bar = document.getElementById("pipelineProgressBar");
    if (status) status.textContent = text;
    if (bar) bar.style.width = `${percent}%`;

    for (let i = 1; i < stepNum; i++) {
      const prev = document.getElementById(`step${i}`);
      if (prev) {
        prev.classList.remove("active");
        prev.classList.add("completed");
      }
    }
    const curr = document.getElementById(`step${stepNum}`);
    if (curr) curr.classList.add("active");
  }

  function showPipelineError(errorMsg) {
    clearInterval(pipelineInterval);
    const card = document.getElementById("pipelineProgressCard");
    const status = document.getElementById("pipelineStatusText");
    const bar = document.getElementById("pipelineProgressBar");

    if (card) card.style.display = "block";
    if (status) {
      status.style.color = "var(--color-danger, #DC2626)";
      status.textContent = `Tạm dừng do lỗi: ${errorMsg}`;
    }
    if (bar) {
      bar.style.backgroundColor = "var(--color-danger, #DC2626)";
    }

    const activeStep = document.querySelector(".pipeline-step.active") || document.getElementById("step4");
    if (activeStep) {
      activeStep.classList.remove("active");
      activeStep.classList.add("error");
    }
  }

  function finishPipelineProgress() {
    clearInterval(pipelineInterval);
    setStep(5, "Hoàn thành bóc tách tài liệu!", 100);
    for (let i = 1; i <= 5; i++) {
      const el = document.getElementById(`step${i}`);
      if (el) {
        el.classList.remove("active");
        el.classList.add("completed");
      }
    }
    setTimeout(() => {
      const card = document.getElementById("pipelineProgressCard");
      if (card) card.style.display = "none";
    }, 2500);
  }

  function stopPipelineProgress() {
    clearInterval(pipelineInterval);
    const card = document.getElementById("pipelineProgressCard");
    if (card) card.style.display = "none";
  }

  function formatBytes(bytes, decimals = 1) {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
  }

  function escapeHtml(str) {
    return str.replace(/[&<>'"]/g, 
      tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
    );
  }

  function initStudioIcons() {
    if (window.AppIcons && window.AppIcons.initAutoIcons) {
      window.AppIcons.initAutoIcons();
    }
  }
};

document.addEventListener("DOMContentLoaded", () => {
  window.initStudioPage();
});
