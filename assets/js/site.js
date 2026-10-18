(() => {
  const header = document.getElementById("siteHeader");
  const nav = document.getElementById("primaryNav");
  const toggle = document.querySelector(".nav-toggle");

  if (header) {
    const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });

    nav.addEventListener("click", (event) => {
      if (event.target.closest("a")) {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && nav.classList.contains("is-open")) {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
  }

  const reveals = document.querySelectorAll(".reveal");
  if (reveals.length) {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      reveals.forEach((el) => el.classList.add("is-visible"));
    } else {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add("is-visible");
              observer.unobserve(entry.target);
            }
          });
        },
        { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
      );
      reveals.forEach((el) => observer.observe(el));
    }
  }

  const mainImage = document.getElementById("galleryImage");
  const thumbs = document.querySelectorAll(".gallery-thumbs .thumb");
  thumbs.forEach((thumb) => {
    thumb.addEventListener("click", () => {
      if (!mainImage) return;
      const src = thumb.dataset.src;
      const srcset = thumb.dataset.srcset;
      if (!src) return;
      mainImage.src = src;
      if (srcset) {
        mainImage.srcset = srcset;
      } else {
        mainImage.removeAttribute("srcset");
      }
      thumbs.forEach((t) => {
        t.classList.toggle("is-active", t === thumb);
        t.setAttribute("aria-pressed", String(t === thumb));
      });
    });
  });
})();
