// Theme management
function getTheme() {
  return localStorage.getItem('theme') || 'dark';
}

function setTheme(theme) {
  localStorage.setItem('theme', theme);
  if (theme === 'light') {
    document.documentElement.removeAttribute('data-theme');
  } else {
    document.documentElement.setAttribute('data-theme', 'dark');
  }
  const btn = document.getElementById('theme-toggle-btn');
  if (btn) {
    btn.innerHTML = theme === 'dark'
      ? '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/></svg> ' + (window.__lang === 'fr' ? 'Mode clair' : 'Light mode')
      : '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/></svg> ' + (window.__lang === 'fr' ? 'Mode sombre' : 'Dark mode');
  }
}

function toggleTheme() {
  setTheme(getTheme() === 'dark' ? 'light' : 'dark');
}

// Language management
function setLanguage(lang) {
  fetch('/api/lang', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ lang })
  }).then(() => {
    window.location.reload();
  });
}

// Sidebar toggle
document.addEventListener('DOMContentLoaded', function() {
  // Apply saved theme
  setTheme(getTheme());

  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebar-overlay');
  const toggleBtn = document.getElementById('sidebar-toggle');

  if (toggleBtn) {
    toggleBtn.addEventListener('click', function() {
      const isHidden = sidebar.classList.contains('-translate-x-full');
      sidebar.classList.toggle('-translate-x-full');
      overlay.classList.toggle('hidden');
      document.body.classList.toggle('overflow-hidden');
    });
  }

  if (overlay) {
    overlay.addEventListener('click', function() {
      sidebar.classList.add('-translate-x-full');
      overlay.classList.add('hidden');
      document.body.classList.remove('overflow-hidden');
    });
  }

  // Highlight active nav link
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath) {
      link.classList.add('active');
    } else if (currentPath.startsWith('/projects') && href === '/projects') {
      link.classList.add('active');
    }
  });
});

// CV Modal
function openCvModal() {
  const modal = document.getElementById('cv-modal');
  const frame = document.getElementById('cv-frame');
  modal.classList.remove('hidden');
  document.body.style.overflow = 'hidden';
  if (frame) {
    frame.src = frame.src;
  }
}

function closeCvModal() {
  const modal = document.getElementById('cv-modal');
  modal.classList.add('hidden');
  document.body.style.overflow = '';
}
