// Smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function () {
  // Smooth scroll for nav links to sections with hashes
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href').slice(1);
      const target = document.getElementById(targetId);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // Active nav highlighting on scroll
  const navLinks = document.querySelectorAll('.nav-links a');
  const sections = Array.from(navLinks).map(a => {
    const href = a.getAttribute('href');
    if (href && href.startsWith('#')) {
      return document.getElementById(href.slice(1));
    } else if (href) {
      return document.querySelector(href === '/' ? 'body' : null);
    }
    return null;
  });

  window.addEventListener('scroll', () => {
    let scrollPos = window.scrollY + 120;
    navLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (!href || !href.startsWith('#')) return;
      const sec = document.getElementById(href.slice(1));
      if (!sec) return;
      if (scrollPos >= sec.offsetTop && scrollPos < sec.offsetTop + sec.offsetHeight) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
  });

  // Project modal
  const modal = document.getElementById('project-modal');
  const modalTitle = document.getElementById('modal-title');
  const modalDetails = document.getElementById('modal-details');
  const modalLinks = document.getElementById('modal-links');
  const modalClose = document.getElementById('modal-close');

  document.querySelectorAll('.project-more').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      modal.classList.remove('hidden');
      modal.setAttribute('aria-hidden', 'false');
      modalTitle.textContent = btn.dataset.title;
      modalDetails.textContent = btn.dataset.details;
      modalLinks.innerHTML = '';
      const url = btn.dataset.url;
      if (url) {
        modalLinks.innerHTML = `<p><a href="${url}" target="_blank" class="btn btn-primary">Visit project</a></p>`;
      }
      document.body.style.overflow = 'hidden';
    });
  });

  modalClose.addEventListener('click', () => {
    modal.classList.add('hidden');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  });
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.classList.add('hidden');
      modal.setAttribute('aria-hidden','true');
      document.body.style.overflow = '';
    }
  });
});

document.addEventListener('DOMContentLoaded', function () {
  // project modal
  const modal = document.getElementById('project-modal');
  const modalTitle = document.getElementById('modal-title');
  const modalDetails = document.getElementById('modal-details');
  const modalLinks = document.getElementById('modal-links');
  const modalImage = document.getElementById('modal-image');
  const modalClose = document.getElementById('modal-close');

  document.querySelectorAll('.project-more').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const title = btn.dataset.title || '';
      const details = btn.dataset.details || '';
      const url = btn.dataset.url || '';
      const id = btn.dataset.id || '';

      modalTitle.textContent = title;
      modalDetails.textContent = details;
      modalLinks.innerHTML = '';

      // find the project object image from DOM: try to find image inside same card
      const card = btn.closest('.project-card');
      const img = card ? card.querySelector('img') : null;
      if (img) {
        modalImage.innerHTML = `<img src="${img.src}" alt="${title}">`;
      } else {
        modalImage.innerHTML = '';
      }

      if (url) {
        modalLinks.innerHTML = `<p><a class="btn btn-link" href="${url}" target="_blank" rel="noopener">Open project</a></p>`;
      }
      modal.classList.remove('hidden');
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    });
  });

  modalClose.addEventListener('click', () => {
    modal.classList.add('hidden');
    modal.setAttribute('aria-hidden','true');
    document.body.style.overflow = '';
  });

  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.classList.add('hidden');
      modal.setAttribute('aria-hidden','true');
      document.body.style.overflow = '';
    }
  });
});

