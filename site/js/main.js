/* =========================================================
   As You Like It Painting Company — site behavior
   All config values live here. Change them once, not in markup.
   ========================================================= */
const CONFIG = {
  // Estimate form endpoint. Formspree, Basin, Getform, etc. all accept a JSON POST.
  // Leave as "" to run the form in demo mode (validates + shows success, sends nothing).
  FORM_ENDPOINT: "",
  PHONE_DISPLAY: "(561) 502-7288",
  PHONE_TEL: "+15615027288",
  EMAIL: "tim@asyoulikeitpainting.com",
  FINANCING_URL: "https://www.acornfinance.com/apply?d=PERXM#/personal",
  GALLERY_URL: "https://timothystmary.smugmug.com/",
  REVIEWS_URL: "https://www.google.com/search?q=As+You+Like+It+Painting+Jupiter+FL",
};

document.documentElement.classList.remove("no-js");

/* ---------- Mobile nav ---------- */
(() => {
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.getElementById("site-nav");
  if (!toggle || !nav) return;
  const header = document.querySelector(".site-header");
  const setOpen = (open) => {
    if (open && header) {
      document.documentElement.style.setProperty("--nav-top", Math.max(0, header.getBoundingClientRect().bottom) + "px");
    }
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    nav.classList.toggle("is-open", open);
    document.body.classList.toggle("nav-open", open);
  };
  toggle.addEventListener("click", () => setOpen(toggle.getAttribute("aria-expanded") !== "true"));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && nav.classList.contains("is-open")) { setOpen(false); toggle.focus(); }
  });
  window.matchMedia("(min-width: 1021px)").addEventListener("change", (m) => { if (m.matches) setOpen(false); });
})();

/* ---------- Services dropdown ---------- */
(() => {
  document.querySelectorAll(".nav__trigger").forEach((btn) => {
    const menu = document.getElementById(btn.getAttribute("aria-controls"));
    if (!menu) return;
    const close = () => { btn.setAttribute("aria-expanded", "false"); menu.classList.remove("is-open"); };
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      const open = btn.getAttribute("aria-expanded") !== "true";
      btn.setAttribute("aria-expanded", String(open));
      menu.classList.toggle("is-open", open);
    });
    document.addEventListener("click", (e) => { if (!menu.contains(e.target)) close(); });
    menu.addEventListener("keydown", (e) => { if (e.key === "Escape") { close(); btn.focus(); } });
    btn.addEventListener("keydown", (e) => { if (e.key === "Escape") close(); });
  });
})();

/* ---------- Estimate form ---------- */
(() => {
  const form = document.getElementById("estimate-form");
  if (!form) return;
  const status = form.querySelector(".form-status");
  const submit = form.querySelector('button[type="submit"]');

  // Preselect a service from ?service= in the URL (set by service-page CTAs)
  const pre = new URLSearchParams(location.search).get("service");
  if (pre) {
    const box = form.querySelector(`input[name="services"][value="${CSS.escape(pre)}"]`);
    if (box) box.checked = true;
  }

  const rules = {
    name: (v) => v.trim().length >= 2 || "Please enter your name.",
    phone: (v) => v.replace(/\D/g, "").length >= 10 || "Enter a 10-digit phone number so we can call you back.",
    email: (v) => v === "" || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || "That email looks off. Check for a typo.",
    city: (v) => v.trim().length >= 2 || "Which city is the property in?",
  };

  const setError = (input, msg) => {
    const field = input.closest(".field");
    const err = field.querySelector(".field__error");
    if (msg) {
      field.setAttribute("data-invalid", "");
      input.setAttribute("aria-invalid", "true");
      err.textContent = msg;
    } else {
      field.removeAttribute("data-invalid");
      input.removeAttribute("aria-invalid");
      err.textContent = "";
    }
  };

  const validateField = (input) => {
    const rule = rules[input.name];
    if (!rule) return true;
    const res = rule(input.value);
    setError(input, res === true ? "" : res);
    return res === true;
  };

  Object.keys(rules).forEach((name) => {
    const input = form.elements[name];
    if (!input) return;
    input.addEventListener("blur", () => validateField(input));
    input.addEventListener("input", () => { if (input.hasAttribute("aria-invalid")) validateField(input); });
  });

  const show = (type, msg) => {
    status.className = `form-status is-visible form-status--${type}`;
    status.textContent = msg;
    status.focus();
  };

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (form.elements.company && form.elements.company.value) return; // honeypot
    let firstBad = null;
    Object.keys(rules).forEach((name) => {
      const input = form.elements[name];
      if (input && !validateField(input) && !firstBad) firstBad = input;
    });
    if (firstBad) { firstBad.focus(); return; }

    const data = Object.fromEntries(new FormData(form).entries());
    data.services = [...form.querySelectorAll('input[name="services"]:checked')].map((i) => i.value).join(", ") || "Not specified";
    delete data.company;

    submit.setAttribute("aria-busy", "true");
    try {
      if (CONFIG.FORM_ENDPOINT) {
        const res = await fetch(CONFIG.FORM_ENDPOINT, {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error(String(res.status));
      } else {
        await new Promise((r) => setTimeout(r, 700)); // demo mode
      }
      form.reset();
      show("ok", `Thanks, ${data.name.split(" ")[0]}. We got your request and will call you within one business day. Need us sooner? Call or text ${CONFIG.PHONE_DISPLAY}.`);
    } catch (err) {
      show("err", `Something went wrong sending the form. Please call or text ${CONFIG.PHONE_DISPLAY}, or email ${CONFIG.EMAIL}.`);
    } finally {
      submit.removeAttribute("aria-busy");
    }
  });
})();

/* ---------- Gallery filter ---------- */
(() => {
  const bar = document.querySelector(".filters");
  if (!bar) return;
  const tiles = document.querySelectorAll(".tile");
  const count = document.getElementById("gallery-count");
  bar.addEventListener("click", (e) => {
    const btn = e.target.closest("button");
    if (!btn) return;
    bar.querySelectorAll("button").forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
    const f = btn.dataset.filter;
    let shown = 0;
    tiles.forEach((t) => {
      const show = f === "all" || t.dataset.cat === f;
      t.hidden = !show;
      if (show) shown++;
    });
    if (count) count.textContent = `Showing ${shown} project${shown === 1 ? "" : "s"}`;
  });
})();

/* ---------- Reveal on scroll ---------- */
(() => {
  const els = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window) || matchMedia("(prefers-reduced-motion: reduce)").matches) {
    els.forEach((el) => el.classList.add("is-in"));
    return;
  }
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } });
  }, { rootMargin: "0px 0px -8% 0px" });
  els.forEach((el) => io.observe(el));
})();

/* ---------- Footer year ---------- */
document.querySelectorAll("[data-year]").forEach((el) => { el.textContent = new Date().getFullYear(); });
