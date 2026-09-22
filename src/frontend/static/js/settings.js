/**
 * Logic JavaScript quan ly trang Cai Dat Ca Nhan Hoa (Settings Page)
 */
window.initSettingsPage = () => {
  const prefForm = document.getElementById("preferencesForm");
  const pwdForm = document.getElementById("passwordForm");

  // 1. Luu Tuy Chon Ca Nhan
  if (prefForm && !prefForm.dataset.initialized) {
    prefForm.dataset.initialized = "true";
    prefForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = document.getElementById("btnSavePreferences");
      btn.disabled = true;
      btn.textContent = "Đang lưu...";

      const payload = {
        theme: document.getElementById("settingTheme").value,
        language: document.getElementById("settingLanguage").value,
        default_model: document.getElementById("settingDefaultModel").value,
        default_target_lang: document.getElementById("settingTargetLang").value,
        fast_path_default: document.getElementById("settingFastPath").checked
      };

      try {
        const resp = await fetch("/api/settings", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        const res = await resp.json();

        if (resp.ok) {
          showToast(res.message || "Đã lưu cài đặt thành công", "success");
          // Dong bo ngay lap tuc theme voi giao dien
          document.documentElement.setAttribute("data-theme", payload.theme);
          localStorage.setItem("app-theme", payload.theme);
          const themeBtn = document.getElementById("themeToggleBtn");
          if (themeBtn && window.AppIcons) {
            const isDark = payload.theme === "dark";
            themeBtn.innerHTML = `${isDark ? AppIcons.get("sun", 16) : AppIcons.get("moon", 16)} <span>${isDark ? "Sáng" : "Tối"}</span>`;
          }
        } else {
          showToast(res.error || "Không thể lưu cài đặt", "error");
        }
      } catch (err) {
        showToast("Lỗi kết nối máy chủ: " + err.message, "error");
      } finally {
        btn.disabled = false;
        btn.textContent = "Lưu Tùy Chọn Cài Đặt";
      }
    });
  }

  // 2. Doi Mat Khau
  if (pwdForm && !pwdForm.dataset.initialized) {
    pwdForm.dataset.initialized = "true";
    pwdForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const oldPwd = document.getElementById("oldPassword").value;
      const newPwd = document.getElementById("newPassword").value;
      const confirmPwd = document.getElementById("confirmPassword").value;

      if (newPwd !== confirmPwd) {
        showToast("Mật khẩu mới và xác nhận mật khẩu không khớp", "error");
        return;
      }

      const btn = document.getElementById("btnChangePassword");
      btn.disabled = true;
      btn.textContent = "Đang xử lý...";

      try {
        const resp = await fetch("/api/settings/password", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            old_password: oldPwd,
            new_password: newPwd,
            confirm_password: confirmPwd
          })
        });
        const res = await resp.json();

        if (resp.ok) {
          showToast(res.message || "Đổi mật khẩu thành công", "success");
          pwdForm.reset();
        } else {
          showToast(res.error || "Đổi mật khẩu thất bại", "error");
        }
      } catch (err) {
        showToast("Lỗi kết nối máy chủ: " + err.message, "error");
      } finally {
        btn.disabled = false;
        btn.textContent = "Cập Nhật Mật Khẩu";
      }
    });
  }
  if (window.AppIcons) window.AppIcons.initAutoIcons();
};

document.addEventListener("DOMContentLoaded", () => {
  window.initSettingsPage();
});
