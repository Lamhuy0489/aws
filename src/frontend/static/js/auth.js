/**
 * Logic Dang nhap va Dang ky tai khoan
 * Ho tro tu dong chuyen huong theo vai tro nguoi dung (Admin -> /admin, User -> /studio)
 */

document.addEventListener("DOMContentLoaded", () => {
  const tabLogin = document.getElementById("tabLogin");
  const tabRegister = document.getElementById("tabRegister");
  const formLogin = document.getElementById("formLogin");
  const formRegister = document.getElementById("formRegister");
  const urlParams = new URLSearchParams(window.location.search);
  const nextParam = urlParams.get("next") || "";

  if (tabLogin && tabRegister) {
    tabLogin.addEventListener("click", () => {
      tabLogin.classList.add("active");
      tabRegister.classList.remove("active");
      formLogin.style.display = "block";
      formRegister.style.display = "none";
    });

    tabRegister.addEventListener("click", () => {
      tabRegister.classList.add("active");
      tabLogin.classList.remove("active");
      formRegister.style.display = "block";
      formLogin.style.display = "none";
    });
  }

  // Handle Login Submit
  if (formLogin) {
    formLogin.addEventListener("submit", async (e) => {
      e.preventDefault();
      const username = document.getElementById("loginUsername").value.trim();
      const password = document.getElementById("loginPassword").value.trim();
      const submitBtn = document.getElementById("loginSubmitBtn");

      if (!username || !password) {
        showToast("Vui long nhap day du ten dang nhap va mat khau", "error");
        return;
      }

      submitBtn.disabled = true;
      submitBtn.textContent = t("loading");

      try {
        const resp = await apiFetch("/api/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password, next: nextParam })
        });

        if (resp && resp.redirect_url) {
          showToast(t("success"), "success");
          setTimeout(() => {
            window.location.href = resp.redirect_url;
          }, 400);
        }
      } catch (err) {
        // apiFetch da hien thi toast loi
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = t("btn_login");
      }
    });
  }

  // Handle Register Submit
  if (formRegister) {
    formRegister.addEventListener("submit", async (e) => {
      e.preventDefault();
      const username = document.getElementById("regUsername").value.trim();
      const email = document.getElementById("regEmail").value.trim();
      const password = document.getElementById("regPassword").value.trim();
      const submitBtn = document.getElementById("regSubmitBtn");

      if (!username || !password) {
        showToast("Ten dang nhap va mat khau khong duoc de trong", "error");
        return;
      }

      submitBtn.disabled = true;
      submitBtn.textContent = t("loading");

      try {
        const resp = await apiFetch("/api/auth/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, email, password })
        });

        if (resp && resp.redirect_url) {
          showToast(t("success"), "success");
          setTimeout(() => {
            window.location.href = resp.redirect_url;
          }, 400);
        }
      } catch (err) {
        // apiFetch da hien thi toast loi
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = t("btn_register");
      }
    });
  }
});
