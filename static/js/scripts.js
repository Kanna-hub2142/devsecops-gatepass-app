/* ============================================================
   AUTO-HIDE BOOTSTRAP ALERTS
   ============================================================ */

document.addEventListener("DOMContentLoaded", function () {
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 4000); // auto close after 4 seconds
    });
});


/* ============================================================
   CONFIRM DELETE (for hostel delete buttons)
   ============================================================ */

document.addEventListener("click", function (e) {
    if (e.target.classList.contains("confirm-delete")) {
        if (!confirm("Are you sure you want to delete this item?")) {
            e.preventDefault();
        }
    }
});


/* ============================================================
   SMOOTH SCROLL TO TOP (optional enhancement)
   ============================================================ */

const scrollBtn = document.createElement("button");
scrollBtn.innerText = "↑";
scrollBtn.id = "scrollTopBtn";
scrollBtn.style.position = "fixed";
scrollBtn.style.bottom = "20px";
scrollBtn.style.right = "20px";
scrollBtn.style.display = "none";
scrollBtn.style.zIndex = "999";
scrollBtn.style.borderRadius = "50%";
scrollBtn.style.padding = "8px 12px";
scrollBtn.style.background = "#0d6efd";
scrollBtn.style.color = "#fff";
scrollBtn.style.border = "none";
scrollBtn.style.cursor = "pointer";

document.body.appendChild(scrollBtn);

window.addEventListener("scroll", () => {
    if (window.scrollY > 300) {
        scrollBtn.style.display = "block";
    } else {
        scrollBtn.style.display = "none";
    }
});

scrollBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
});
