// PocketSmart AI — Global Application Script

// API Wrapper
async function api(url, opt = {}) {
  const defaultHeaders = opt.body instanceof FormData ? {} : { 'Content-Type': 'application/json' };
  const r = await fetch(url, {
    credentials: 'include',
    ...opt,
    headers: { ...defaultHeaders, ...(opt.headers || {}) }
  });
  
  let d = {};
  try {
    d = await r.json();
  } catch (err) {
    // Non-JSON response
  }
  
  if (!r.ok) {
    throw new Error(d.detail || (typeof d === 'string' ? d : 'Request failed'));
  }
  return d;
}

// Toast Notification System
function showToast(message, type = 'success') {
  const container = document.getElementById('toastContainer');
  if (!container) return;
  
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <span>${type === 'success' ? '✓' : '⚠️'}</span>
    <span>${message}</span>
  `;
  container.appendChild(toast);
  
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// Mobile Menu Toggle
document.getElementById('mobileToggle')?.addEventListener('click', () => {
  document.getElementById('navMenu')?.classList.toggle('open');
});

// Check AI Service Health on load
async function checkAiHealth() {
  try {
    const health = await api('/api/health');
    const pill = document.getElementById('aiStatusPill');
    const label = document.getElementById('statusLabel');
    if (pill && label) {
      if (health.gemini_configured) {
        label.textContent = 'Gemini 3.5 Active';
        pill.title = `Powered by ${health.model}`;
      } else {
        label.textContent = 'Smart Fallback';
        pill.title = 'Running on deterministic fallback engine';
      }
    }
  } catch (e) {
    console.warn('Health check issue:', e);
  }
}

// Sync User Session
async function syncSession() {
  try {
    const info = await api('/api/session-info');
    if (info.authenticated) {
      document.getElementById('loginBtn')?.classList.add('hidden');
      document.getElementById('registerBtn')?.classList.add('hidden');
      const badge = document.getElementById('userBadge');
      if (badge) {
        badge.classList.remove('hidden');
        const email = info.email || 'user';
        const name = email.split('@')[0];
        document.getElementById('userNameLabel').textContent = name;
        document.getElementById('userInitial').textContent = name[0].toUpperCase();
      }
    }
  } catch {
    // Unauthenticated guest user
  }
}

// Logout handler
document.getElementById('logoutBtn')?.addEventListener('click', async () => {
  try {
    await api('/api/auth/logout', { method: 'POST' });
    showToast('Logged out successfully');
    setTimeout(() => { location.href = '/login'; }, 400);
  } catch (err) {
    showToast(err.message, 'error');
  }
});

// Quick Demo Login
async function quickDemoLogin() {
  const demoEmail = 'demo@pocketsmart.ai';
  const demoPass = 'password123';
  const submitBtn = document.getElementById('authSubmitBtn');
  if (submitBtn) submitBtn.disabled = true;
  
  try {
    // Try registering first, ignore if exists
    try {
      await api('/api/auth/register', {
        method: 'POST',
        body: JSON.stringify({ name: 'Demo Planner', email: demoEmail, password: demoPass })
      });
    } catch {
      // User might already exist
    }

    // Login
    await api('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email: demoEmail, password: demoPass })
    });
    
    showToast('Logged into demo account!');
    setTimeout(() => { location.href = '/dashboard'; }, 400);
  } catch (err) {
    showToast(err.message, 'error');
    if (submitBtn) submitBtn.disabled = false;
  }
}

// Auth Form Handler
if (window.AUTH_MODE) {
  document.getElementById('authForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = document.getElementById('authSubmitBtn');
    const msg = document.getElementById('message');
    msg.textContent = '';
    
    const formData = new FormData(e.target);
    const payload = Object.fromEntries(formData);
    
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> Processing...';
    
    try {
      const endpoint = window.AUTH_MODE === 'register' ? '/api/auth/register' : '/api/auth/login';
      await api(endpoint, {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      
      // If registered, also login
      if (window.AUTH_MODE === 'register') {
        await api('/api/auth/login', {
          method: 'POST',
          body: JSON.stringify({ email: payload.email, password: payload.password })
        });
      }
      
      showToast('Welcome to PocketSmart AI!');
      setTimeout(() => { location.href = '/dashboard'; }, 400);
    } catch (err) {
      msg.textContent = err.message;
      msg.style.color = '#f87171';
      btn.disabled = false;
      btn.textContent = window.AUTH_MODE === 'register' ? 'Create Free Account' : 'Sign In to Dashboard';
    }
  });
}

// Interactive Chip Selection helper
document.addEventListener('click', (e) => {
  const chip = e.target.closest('.chip-option');
  if (!chip) return;
  
  const radio = chip.querySelector('input[type="radio"]');
  const checkbox = chip.querySelector('input[type="checkbox"]');
  
  if (radio) {
    const groupName = radio.name;
    document.querySelectorAll(`input[name="${groupName}"]`).forEach(r => {
      r.closest('.chip-option')?.classList.remove('selected');
    });
    radio.checked = true;
    chip.classList.add('selected');
  } else if (checkbox) {
    checkbox.checked = !checkbox.checked;
    chip.classList.toggle('selected', checkbox.checked);
  }
});

// Run initial checks
document.addEventListener('DOMContentLoaded', () => {
  checkAiHealth();
  syncSession();
});
