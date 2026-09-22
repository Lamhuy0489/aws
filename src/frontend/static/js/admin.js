/**
 * Logic Bang Dieu Khien Quan Tri Vien (Admin Panel)
 * Quan ly KPIs, Dieu phoi tour xoay API Key va danh sach nguoi dung toan he thong
 */

window.initAdminPage = () => {
  loadAdminStats();
  loadAdminKeys();
  loadAdminUsers();

  const addKeyForm = document.getElementById("formAddKey");
  if (addKeyForm && !addKeyForm.dataset.initialized) {
    addKeyForm.dataset.initialized = "true";
    addKeyForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const provider = document.getElementById("newKeyProvider").value;
      const key_alias = document.getElementById("newKeyAlias").value.trim();
      const key_value = document.getElementById("newKeyValue").value.trim();
      const model_name = document.getElementById("newKeyModel").value.trim();
      const base_url = document.getElementById("newKeyBaseUrl").value.trim();
      const priority = parseInt(document.getElementById("newKeyPriority").value, 10) || 1;

      if (!key_alias || !key_value) {
        showToast("Vui long nhap ten goi nho va khoa API", "error");
        return;
      }

      try {
        await apiFetch("/api/admin/keys", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ provider, key_alias, key_value, model_name, base_url, priority })
        });
        showToast("Da them khoa API moi vao tour xoay thanh cong", "success");
        closeAddKeyModal();
        addKeyForm.reset();
        loadAdminKeys();
        loadAdminStats();
      } catch (err) {
        // apiFetch da hien thi toast
      }
    });
  }
  if (window.AppIcons) window.AppIcons.initAutoIcons();
};

async function loadAdminStats() {
  try {
    const data = await apiFetch("/api/admin/stats");
    const stats = data.stats;
    if (!stats) return;

    document.getElementById("kpiTotalUsers").textContent = stats.total_users || 0;
    document.getElementById("kpiTotalDocs").textContent = stats.total_documents || 0;
    document.getElementById("kpiActiveKeys").textContent = `${stats.active_keys || 0} / ${stats.total_keys || 0}`;
    document.getElementById("kpiKeyUsage").textContent = stats.total_key_usage || 0;

    // Render recent activity logs
    const actBody = document.getElementById("recentActivityTableBody");
    if (actBody && stats.recent_activity) {
      actBody.innerHTML = "";
      stats.recent_activity.forEach(item => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td><strong>${escapeHtml(item.filename)}</strong></td>
          <td><span class="badge badge-muted">${item.username || "Hệ thống"}</span></td>
          <td>${item.total_pages} trang</td>
          <td><span class="badge badge-muted">${escapeHtml(item.model_used)}</span></td>
          <td>${item.processing_time ? item.processing_time.toFixed(2) + "s" : "0.00s"}</td>
          <td style="font-size: 12px; color: var(--color-muted-foreground);">${item.created_at}</td>
        `;
        actBody.appendChild(tr);
      });
    }
  } catch (err) {
    console.error("Loi load stats:", err);
  }
}

async function loadAdminKeys() {
  const tableBody = document.getElementById("adminKeysTableBody");
  if (!tableBody) return;

  try {
    const data = await apiFetch("/api/admin/keys");
    const keys = data.keys || [];
    tableBody.innerHTML = "";

    keys.forEach(k => {
      const tr = document.createElement("tr");
      const isActive = k.is_active === 1;
      const statusBadge = isActive 
        ? `<span class="badge badge-success"><span class="status-dot active"></span>Hoat dong</span>`
        : `<span class="badge badge-muted"><span class="status-dot inactive"></span>Tam dung</span>`;

      tr.innerHTML = `
        <td><strong style="text-transform: uppercase;">${escapeHtml(k.provider)}</strong></td>
        <td>${escapeHtml(k.key_alias)}</td>
        <td><code>${escapeHtml(k.key_masked)}</code></td>
        <td><span class="badge badge-muted">${escapeHtml(k.model_name)}</span></td>
        <td>${k.priority}</td>
        <td><strong style="color: var(--color-accent);">${k.usage_count}</strong></td>
        <td>${statusBadge}</td>
        <td>
          <div style="display: flex; gap: 6px;">
            <button class="btn btn-outline btn-sm btn-toggle">
              ${isActive ? "Tạm dừng" : "Kích hoạt"}
            </button>
            <button class="btn btn-danger btn-sm btn-delete">
              Xóa
            </button>
          </div>
        </td>
      `;

      const btnToggle = tr.querySelector(".btn-toggle");
      if (btnToggle) {
        btnToggle.addEventListener("click", () => toggleKeyStatus(k.id));
      }
      const btnDelete = tr.querySelector(".btn-delete");
      if (btnDelete) {
        btnDelete.addEventListener("click", () => deleteKey(k.id, k.key_alias));
      }

      tableBody.appendChild(tr);
    });
  } catch (err) {
    console.error("Lỗi tải danh sách keys:", err);
  }
}

async function toggleKeyStatus(keyId) {
  try {
    const resp = await apiFetch(`/api/admin/keys/${keyId}/toggle`, { method: "POST" });
    showToast(resp.message, "success");
    loadAdminKeys();
    loadAdminStats();
  } catch (err) {
    showToast("Không thể đổi trạng thái key: " + err.message, "error");
  }
}

async function deleteKey(keyId, alias) {
  if (!confirm(`Bạn có chắc chắn muốn xóa khóa "${alias}" khỏi tour xoay?`)) {
    return;
  }

  try {
    await apiFetch(`/api/admin/keys/${keyId}`, { method: "DELETE" });
    showToast("Đã xóa khóa API khỏi tour xoay", "success");
    loadAdminKeys();
    loadAdminStats();
  } catch (err) {
    showToast("Lỗi khi xóa key: " + err.message, "error");
  }
}

async function loadAdminUsers() {
  const tableBody = document.getElementById("adminUsersTableBody");
  if (!tableBody) return;

  try {
    const data = await apiFetch("/api/admin/users");
    const users = data.users || [];
    tableBody.innerHTML = "";

    users.forEach(u => {
      const tr = document.createElement("tr");
      const roleBadge = u.role === "admin" 
        ? `<span class="badge" style="background-color: var(--color-destructive); color: white;">ADMIN</span>`
        : `<span class="badge badge-muted">USER</span>`;

      tr.innerHTML = `
        <td><code>${escapeHtml(u.id)}</code></td>
        <td><strong>${escapeHtml(u.username)}</strong></td>
        <td>${escapeHtml(u.email || "-")}</td>
        <td>${roleBadge}</td>
        <td style="font-size: 12px; color: var(--color-muted-foreground);">${u.created_at || "-"}</td>
      `;
      tableBody.appendChild(tr);
    });
  } catch (err) {
    console.error("Loi load users:", err);
  }
}

window.openAddKeyModal = () => {
  document.getElementById("addKeyModal").style.display = "flex";
};

window.closeAddKeyModal = () => {
  document.getElementById("addKeyModal").style.display = "none";
};

function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/[&<>'"]/g, 
    tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
  );
}

window.loadAdminStats = loadAdminStats;
window.loadAdminKeys = loadAdminKeys;
window.loadAdminUsers = loadAdminUsers;
window.toggleKeyStatus = toggleKeyStatus;
window.deleteKey = deleteKey;

document.addEventListener("DOMContentLoaded", () => {
  window.initAdminPage();
});
