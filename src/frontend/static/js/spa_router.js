/**
 * Seamless Client-Side Navigation Router (Zero-Flicker SPA Tab Swapper)
 * Loại bỏ hoàn toàn hiện tượng nhấp nháy / trắng trang khi chuyển tab giữa Studio, Kho tài liệu, Cài đặt, Quản trị.
 */

(function () {
  const pageCache = {};
  const loadedScripts = new Set();

  // Danh sách script tương ứng với từng tuyến đường
  const ROUTE_SCRIPTS = {
    "/studio": "/static/js/studio.js?v=20260922_02",
    "/library": "/static/js/library.js?v=20260922_02",
    "/settings": "/static/js/settings.js?v=20260922_03",
    "/admin": "/static/js/admin.js?v=20260922_03"
  };

  const ROUTE_INIT_FN = {
    "/studio": () => window.initStudioPage && window.initStudioPage(),
    "/library": () => window.initLibraryPage && window.initLibraryPage(),
    "/settings": () => window.initSettingsPage && window.initSettingsPage(),
    "/admin": () => window.initAdminPage && window.initAdminPage()
  };

  document.addEventListener("DOMContentLoaded", () => {
    // Lưu trang hiện tại vào cache
    const currentPath = window.location.pathname;
    const currentMain = document.querySelector("main.main-content");
    if (currentMain) {
      pageCache[currentPath] = {
        html: currentMain.innerHTML,
        title: document.title
      };
    }

    // Ghi nhận các script đã có trong trang
    document.querySelectorAll("script[src]").forEach(s => {
      loadedScripts.add(s.getAttribute("src"));
    });

    // Bắt sự kiện click trên toàn bộ navbar links
    document.addEventListener("click", (e) => {
      const link = e.target.closest("a.nav-link") || e.target.closest("a[data-spa]");
      if (!link) return;

      const href = link.getAttribute("href");
      if (!href || href.startsWith("http") || href.startsWith("#") || href.startsWith("/logout") || href.startsWith("/login")) {
        return;
      }

      // Chỉ xử lý các route nội bộ chính
      if (ROUTE_SCRIPTS[href]) {
        e.preventDefault();
        navigateTo(href);
      }
    });

    // Xử lý nút Back / Forward trên trình duyệt
    window.addEventListener("popstate", (e) => {
      const path = window.location.pathname;
      if (ROUTE_SCRIPTS[path]) {
        navigateTo(path, false);
      }
    });
  });

  async function navigateTo(targetPath, updateHistory = true) {
    if (window.location.pathname === targetPath && updateHistory) {
      return;
    }

    const mainEl = document.querySelector("main.main-content");
    if (!mainEl) return;

    // 1. Cập nhật trạng thái active trên navbar tức thì (0ms)
    document.querySelectorAll(".nav-menu .nav-link").forEach(item => {
      const itemHref = item.getAttribute("href");
      if (itemHref === targetPath) {
        item.classList.add("active");
      } else {
        item.classList.remove("active");
      }
    });

    // 2. Cập nhật URL trình duyệt
    if (updateHistory) {
      window.history.pushState({ path: targetPath }, "", targetPath);
    }

    // 3. Lấy nội dung trang mới (Ưu tiên từ Cache để chuyển đổi tức thì 0ms)
    try {
      let pageData = pageCache[targetPath];

      if (!pageData) {
        // Hiệu ứng chuyển cảnh nhẹ nhàng
        mainEl.style.transition = "opacity 0.1s ease";
        mainEl.style.opacity = "0.6";

        const resp = await fetch(targetPath, {
          headers: { "X-Requested-With": "SPA-Fetch" }
        });
        if (!resp.ok) {
          window.location.href = targetPath;
          return;
        }

        const htmlText = await resp.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(htmlText, "text/html");
        const newMain = doc.querySelector("main.main-content");

        if (!newMain) {
          window.location.href = targetPath;
          return;
        }

        pageData = {
          html: newMain.innerHTML,
          title: doc.querySelector("title") ? doc.querySelector("title").textContent : document.title
        };
        pageCache[targetPath] = pageData;
      }

      // 4. Thay thế nội dung cực êm không reload trang
      mainEl.innerHTML = pageData.html;
      if (pageData.title) {
        document.title = pageData.title;
      }
      mainEl.style.opacity = "1";

      // Cuộn nhẹ về đầu trang
      window.scrollTo({ top: 0, behavior: "instant" });

      // 5. Nạp kịch bản JS của trang đích nếu chưa nạp
      const scriptUrl = ROUTE_SCRIPTS[targetPath];
      if (scriptUrl && !loadedScripts.has(scriptUrl)) {
        await loadScript(scriptUrl);
      }

      // 6. Tái khởi tạo các icon 2D Vector
      if (window.AppIcons && window.AppIcons.initAutoIcons) {
        window.AppIcons.initAutoIcons();
      }

      // 7. Gọi hàm khởi tạo của view tương ứng
      const initFn = ROUTE_INIT_FN[targetPath];
      if (initFn) {
        initFn();
      }
    } catch (err) {
      console.error("Lỗi điều hướng SPA:", err);
      window.location.href = targetPath;
    }
  }

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src = src;
      script.onload = () => {
        loadedScripts.add(src);
        resolve();
      };
      script.onerror = reject;
      document.body.appendChild(script);
    });
  }

  // Xuất hàm điều hướng toàn cục để gọi từ các trang khác (ví dụ: mở trong Studio)
  window.spaNavigate = navigateTo;
})();
