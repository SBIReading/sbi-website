// --- KONFIG ---
const PAGE_SIZE = 6; // ile projektów na jedną stronę

// --- ELEMENTY Z HTML ---
const gridEl = document.getElementById("grid");
const paginationEl = document.getElementById("pagination");
const categorySelect = document.getElementById("categoryFilter");
const searchInput = document.getElementById("searchInput");

// --- STAN DANYCH ---
let allProjects = [];        // wszystko z projects.json
let filteredProjects = [];   // po filtrach / wyszukiwaniu
let currentPage = 1;

// --- 1. POBIERZ DANE Z JSON ---
async function loadProjects() {
  try {
    const res = await fetch("assets/projects/projects.json");
    const data = await res.json();

    // spodziewamy się tablicy obiektów w stylu:
    // { "id":"G34", "title":"G34", "category":"Garden", "coverImage":"assets/projects/G34/xxx.jpg", "images":[ ... ] }

    allProjects = data;
    filteredProjects = [...allProjects];

    renderPage();
  } catch (err) {
    console.error("Błąd ładowania projects.json:", err);
    gridEl.innerHTML = `<p style="color:#fff;">Couldn't load projects.</p>`;
  }
}

// --- 2. FILTROWANIE / WYSZUKIWANIE ---
function applyFilters() {
  const selectedCat = categorySelect.value;      // np. "Garden", "Patio", "All categories"
  const query = searchInput.value.toLowerCase(); // tekst z wyszukiwarki

  filteredProjects = allProjects.filter(project => {
    const matchesCategory =
      selectedCat === "All categories" ||
      selectedCat === "All categories " || // just in case whitespace
      project.category === selectedCat ||
      project.category === selectedCat.replace("Interior Renovations","Interior")
                                       .replace("Structural Works","Structural");

    const matchesSearch =
      project.id.toLowerCase().includes(query) ||
      (project.title && project.title.toLowerCase().includes(query)) ||
      (project.category && project.category.toLowerCase().includes(query));

    return matchesCategory && matchesSearch;
  });

  // po zmianie filtrów zaczynamy od strony 1
  currentPage = 1;
  renderPage();
}

// --- 3. RYSOWANIE KAFELKÓW NA OBECNEJ STRONIE ---
function renderGrid() {
  // oblicz zakres elementów dla tej strony
  const startIndex = (currentPage - 1) * PAGE_SIZE;
  const endIndex = startIndex + PAGE_SIZE;
  const pageItems = filteredProjects.slice(startIndex, endIndex);

  // budujemy HTML kafelków
  const cardsHtml = pageItems.map(project => {
    const title = project.id || project.title || "Project";
    const cat = project.category || "";
    const imgSrc = project.coverImage || (project.images && project.images[0]) || "";

    return `
      <div class="project-card">
        <div class="image-wrap">
          <img src="${imgSrc}" alt="${title}" />
        </div>
        <div class="card-bottom">
          <div class="p-title">${title}</div>
          <div class="p-cat">${cat}</div>
        </div>
      </div>
    `;
  }).join("");

  // wstaw do siatki
  gridEl.innerHTML = cardsHtml || `<p style="color:#fff;">No projects found.</p>`;
}

// --- 4. PAGINACJA (PRZYCISKI 1,2,3...) ---
function renderPagination() {
  const totalPages = Math.ceil(filteredProjects.length / PAGE_SIZE);

  // jeżeli tylko jedna strona -> brak przycisków
  if (totalPages <= 1) {
    paginationEl.innerHTML = "";
    return;
  }

  let buttonsHtml = "";

  for (let p = 1; p <= totalPages; p++) {
    const activeClass = p === currentPage ? "active" : "";
    buttonsHtml += `
      <button class="${activeClass}" data-page="${p}">
        ${p}
      </button>
    `;
  }

  paginationEl.innerHTML = buttonsHtml;

  // podpinamy kliknięcia
  [...paginationEl.querySelectorAll("button")].forEach(btn => {
    btn.addEventListener("click", () => {
      const pageNum = parseInt(btn.getAttribute("data-page"), 10);
      currentPage = pageNum;
      renderPage(); // przerysuj grid i paginację
    });
  });
}

// --- 5. RENDER CAŁEJ STRONY (GRID + PAGINACJA) ---
function renderPage() {
  renderGrid();
  renderPagination();
}

// --- 6. LISTENERY DO FILTRÓW / SEARCH ---
categorySelect.addEventListener("change", applyFilters);
searchInput.addEventListener("input", applyFilters);

// --- START ---
loadProjects();
// ----- CONTACT FORM -> open email client -----
(function () {
  const btn = document.getElementById("sendBtn");
  if (!btn) return;

  btn.addEventListener("click", () => {
    const name = document.querySelector('input[name="name"]')?.value.trim() || "";
    const email = document.querySelector('input[name="email"]')?.value.trim() || "";
    const message = document.querySelector('textarea[name="message"]')?.value.trim() || "";

    // budujemy temat i treść wiadomości
    const subject = encodeURIComponent(
      `New enquiry from ${name || "website visitor"}`
    );

    const body = encodeURIComponent(
      `Name: ${name}\nEmail: ${email}\n\nMessage:\n${message}`
    );

    // otwieramy domyślny mail klienta
    window.location.href =
  `mailto:info@smartbuildersinnovation.co.uk?subject=${subject}&body=${body}`;
  });
})();(function () {
  // Tekst startowy do WhatsApp (edytujesz go tutaj, nie w HTML)
  const msg =
    "Hi, I'd like a quote.\n" +
    "Name: [your name]\n" +
    "Service: [painting/fencing/landscaping]\n" +
    "Postcode: [RGxx].\n" +
    "Seen on smartbuildersinnovation.co.uk";

  const encoded = encodeURIComponent(msg);

  // Ustaw prefill dla wszystkich linków WhatsApp z klasą .wa
  document.querySelectorAll('a.wa').forEach(a => {
    a.href = `https://wa.me/447737883907?text=${encoded}`;
  });
})();
