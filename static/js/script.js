document.addEventListener("DOMContentLoaded", () => {
    const root = document.documentElement;
    const menuButton = document.getElementById("menuButton");
    const sidebar = document.getElementById("sidebar");
    const sidebarBackdrop = document.getElementById("sidebarBackdrop");
    const themeToggle = document.getElementById("themeToggle");
    const dateElement = document.getElementById("currentDate");
    const searchInput = document.getElementById("busca");
    const deleteModal = document.getElementById("deleteModal");
    const deleteMessage = document.getElementById("deleteModalMessage");
    const confirmDeleteButton = document.getElementById("confirmDeleteButton");

    const savedTheme = localStorage.getItem("academia-theme");
    if (savedTheme === "dark" || savedTheme === "light") {
        root.dataset.theme = savedTheme;
    }

    themeToggle?.addEventListener("click", () => {
        const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
        root.dataset.theme = nextTheme;
        localStorage.setItem("academia-theme", nextTheme);
    });

    const closeSidebar = () => {
        sidebar?.classList.remove("is-open");
        sidebarBackdrop?.classList.remove("is-visible");
    };

    menuButton?.addEventListener("click", () => {
        sidebar?.classList.toggle("is-open");
        sidebarBackdrop?.classList.toggle("is-visible");
    });
    sidebarBackdrop?.addEventListener("click", closeSidebar);

    const pathname = window.location.pathname;
    document.querySelectorAll(".side-nav a").forEach((link) => {
        const route = link.dataset.route;
        const isHome = route === "/" && pathname === "/";
        const isSection = route !== "/" && pathname.startsWith(route.replace(/\/$/, ""));
        if (isHome || isSection) link.classList.add("active");
        link.addEventListener("click", closeSidebar);
    });

    if (dateElement) {
        const now = new Date();
        dateElement.textContent = now.toLocaleDateString("pt-BR", {
            weekday: "long",
            day: "2-digit",
            month: "long",
            year: "numeric",
        });
    }

    document.querySelectorAll('input[name="cpf"]').forEach((input) => {
        input.addEventListener("input", () => {
            let value = input.value.replace(/\D/g, "").slice(0, 11);
            value = value.replace(/(\d{3})(\d)/, "$1.$2");
            value = value.replace(/(\d{3})(\d)/, "$1.$2");
            value = value.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
            input.value = value;
        });
    });

    document.querySelectorAll('input[name="telefone"]').forEach((input) => {
        input.addEventListener("input", () => {
            let value = input.value.replace(/\D/g, "").slice(0, 11);
            value = value.replace(/(\d{2})(\d)/, "($1) $2");
            value = value.replace(/(\d{5})(\d)/, "$1-$2");
            input.value = value;
        });
    });

    searchInput?.addEventListener("input", () => {
        const term = searchInput.value.toLowerCase().trim();
        document.querySelectorAll("tbody tr").forEach((row) => {
            row.hidden = !row.innerText.toLowerCase().includes(term);
        });
    });

    document.querySelectorAll(".counter").forEach((counter) => {
        const target = Number(counter.dataset.target || 0);
        const duration = 650;
        const start = performance.now();
        const animate = (time) => {
            const progress = Math.min((time - start) / duration, 1);
            counter.textContent = Math.floor(target * (1 - Math.pow(1 - progress, 3)));
            if (progress < 1) requestAnimationFrame(animate);
        };
        requestAnimationFrame(animate);
    });

    const closeDeleteModal = () => {
        if (!deleteModal) return;
        deleteModal.classList.remove("is-open");
        deleteModal.setAttribute("aria-hidden", "true");
        document.body.style.overflow = "";
    };

    document.querySelectorAll(".js-delete").forEach((button) => {
        button.addEventListener("click", (event) => {
            event.preventDefault();
            const url = button.dataset.deleteUrl;
            const message = button.dataset.deleteMessage || "Essa ação não poderá ser desfeita.";
            if (deleteMessage) deleteMessage.textContent = message;
            if (confirmDeleteButton) confirmDeleteButton.href = url;
            deleteModal?.classList.add("is-open");
            deleteModal?.setAttribute("aria-hidden", "false");
            document.body.style.overflow = "hidden";
        });
    });

    document.querySelectorAll("[data-close-modal]").forEach((element) => {
        element.addEventListener("click", closeDeleteModal);
    });
    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") closeDeleteModal();
    });

    document.querySelectorAll(".toast").forEach((toast) => {
        const closeButton = toast.querySelector(".toast-close");
        const closeToast = () => {
            toast.style.transition = "opacity .25s ease, transform .25s ease";
            toast.style.opacity = "0";
            toast.style.transform = "translateX(18px)";
            setTimeout(() => toast.remove(), 260);
        };
        closeButton?.addEventListener("click", closeToast);
        setTimeout(closeToast, 4500);
    });
});
