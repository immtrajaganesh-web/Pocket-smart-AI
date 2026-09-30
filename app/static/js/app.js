// PocketSmart AI — Global Application Script

// API Wrapper
async function api(url, opt = {}) {
  const token = localStorage.getItem('ps_access_token');
  const authHeader = token ? { 'Authorization': `Bearer ${token}` } : {};
  const defaultHeaders = opt.body instanceof FormData ? {} : { 'Content-Type': 'application/json' };
  const r = await fetch(url, {
    credentials: 'include',
    ...opt,
    headers: { ...defaultHeaders, ...authHeader, ...(opt.headers || {}) }
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
    localStorage.removeItem('ps_access_token');
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
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner"></span> Logging in...';
  }
  
  try {
    // Try registering first, ignore if already exists
    try {
      await api('/api/auth/register', {
        method: 'POST',
        body: JSON.stringify({ name: 'Demo Planner', email: demoEmail, password: demoPass })
      });
    } catch {
      // User might already exist
    }

    // Login
    const loginRes = await api('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email: demoEmail, password: demoPass })
    });

    if (loginRes && loginRes.access_token) {
      localStorage.setItem('ps_access_token', loginRes.access_token);
    }
    
    showToast('Logged into demo account!');
    setTimeout(() => { location.href = '/dashboard'; }, 350);
  } catch (err) {
    showToast(err.message, 'error');
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Sign In to Dashboard';
    }
  }
}

// Global Auth Form Handler (handles both Submit event and onsubmit attribute)
async function handleAuthSubmit(e) {
  if (e && e.preventDefault) e.preventDefault();
  
  const form = document.getElementById('authForm');
  if (!form) return false;

  const btn = document.getElementById('authSubmitBtn');
  const msg = document.getElementById('message');
  if (msg) msg.textContent = '';

  const isRegister = (window.AUTH_MODE === 'register') || 
                     window.location.pathname.includes('/register') || 
                     document.getElementById('nameInput') !== null;

  const formData = new FormData(form);
  const payload = Object.fromEntries(formData.entries());

  const email = (payload.email || '').trim().toLowerCase();
  const password = payload.password || '';
  const name = (payload.name || '').trim();

  if (isRegister && name.length < 2) {
    if (msg) { msg.textContent = 'Please enter your full name (at least 2 characters).'; msg.style.color = '#f87171'; }
    return false;
  }
  if (!email || !email.includes('@')) {
    if (msg) { msg.textContent = 'Please enter a valid email address.'; msg.style.color = '#f87171'; }
    return false;
  }
  if (password.length < 8) {
    if (msg) { msg.textContent = 'Password must be at least 8 characters.'; msg.style.color = '#f87171'; }
    return false;
  }

  if (btn) {
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> Processing...';
  }

  try {
    if (isRegister) {
      await api('/api/auth/register', {
        method: 'POST',
        body: JSON.stringify({ name, email, password })
      });
    }

    const loginRes = await api('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });

    if (loginRes && loginRes.access_token) {
      localStorage.setItem('ps_access_token', loginRes.access_token);
    }

    showToast(isRegister ? 'Account created successfully! Welcome!' : 'Signed in successfully!');
    setTimeout(() => { location.href = '/dashboard'; }, 350);
  } catch (err) {
    if (msg) {
      msg.textContent = err.message || 'Authentication failed. Please check your credentials.';
      msg.style.color = '#f87171';
    } else {
      showToast(err.message, 'error');
    }
    if (btn) {
      btn.disabled = false;
      btn.textContent = isRegister ? 'Create Free Account' : 'Sign In to Dashboard';
    }
  }
  return false;
}
window.handleAuthSubmit = handleAuthSubmit;

function initAuthForm() {
  const form = document.getElementById('authForm');
  if (form && !form.dataset.bound) {
    form.dataset.bound = 'true';
    form.addEventListener('submit', handleAuthSubmit);
  }
}
window.initAuthForm = initAuthForm;

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
  initAuthForm();
  checkAiHealth();
  syncSession();
});

if (document.readyState === 'interactive' || document.readyState === 'complete') {
  initAuthForm();
}
