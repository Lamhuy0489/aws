/**
 * API Client Helper & Toast Notifications
 * Serverless Hybrid Document OCR Platform
 */

function showToast(message, type = "info") {
  let container = document.getElementById("toastContainer");
  if (!container) {
    container = document.createElement("div");
    container.id = "toastContainer";
    container.className = "toast-container";
    document.body.appendChild(container);
  }

  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  
  const textSpan = document.createElement("span");
  textSpan.textContent = message;
  toast.appendChild(textSpan);

  const closeBtn = document.createElement("button");
  closeBtn.textContent = "[X]";
  closeBtn.style.background = "transparent";
  closeBtn.style.border = "none";
  closeBtn.style.color = "white";
  closeBtn.style.cursor = "pointer";
  closeBtn.style.fontWeight = "bold";
  closeBtn.onclick = () => toast.remove();
  toast.appendChild(closeBtn);

  container.appendChild(toast);

  setTimeout(() => {
    if (toast.parentNode) {
      toast.remove();
    }
  }, 4000);
}

async function apiFetch(url, options = {}) {
  try {
    const response = await fetch(url, options);
    
    // Xu ly tu dong neu session het han hoac gap 401
    if (response.status === 401 && !url.includes("/api/auth/login")) {
      window.location.href = `/login?next=${encodeURIComponent(window.location.pathname)}`;
      return null;
    }

    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      const errorMsg = data.error || `HTTP Error ${response.status}`;
      throw new Error(errorMsg);
    }
    return data;
  } catch (err) {
    showToast(err.message, "error");
    throw err;
  }
}
