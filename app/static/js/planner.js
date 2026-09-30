// PocketSmart AI — Comprehensive Multi-Scenario Planner Engine

let currentPlanData = null;
let selectedCartItems = new Set();

// ----------------- SCENARIO 1: HOME PLANNER -----------------
const homeItemCounts = {
  lights: 4,
  ceiling_fans: 2,
  dining_tables: 1,
  sofas: 1,
  storage_units: 2,
  wall_decor: 2,
  curtains: 2,
  rugs: 1
};

function stepItem(itemKey, delta) {
  homeItemCounts[itemKey] = Math.max(0, (homeItemCounts[itemKey] || 0) + delta);
  const el = document.getElementById(`val-${itemKey}`);
  if (el) el.textContent = homeItemCounts[itemKey];
}

function applyHomePreset(preset) {
  const budgetInput = document.getElementById('budgetInput');
  const roomsChips = document.getElementById('roomsChips');
  
  if (preset === '1bhk') {
    budgetInput.value = 35000;
    homeItemCounts.lights = 4;
    homeItemCounts.ceiling_fans = 1;
    homeItemCounts.dining_tables = 0;
    homeItemCounts.sofas = 1;
    homeItemCounts.storage_units = 1;
    homeItemCounts.wall_decor = 1;
    homeItemCounts.curtains = 2;
    homeItemCounts.rugs = 1;
    setChipSelection(roomsChips, ['Living Room', 'Master Bedroom', 'Kitchen']);
  } else if (preset === '2bhk') {
    budgetInput.value = 85000;
    homeItemCounts.lights = 6;
    homeItemCounts.ceiling_fans = 2;
    homeItemCounts.dining_tables = 1;
    homeItemCounts.sofas = 1;
    homeItemCounts.storage_units = 2;
    homeItemCounts.wall_decor = 3;
    homeItemCounts.curtains = 4;
    homeItemCounts.rugs = 2;
    setChipSelection(roomsChips, ['Living Room', 'Master Bedroom', 'Kitchen', 'Dining Area', 'Balcony / Garden']);
  } else if (preset === '3bhk') {
    budgetInput.value = 250000;
    homeItemCounts.lights = 12;
    homeItemCounts.ceiling_fans = 4;
    homeItemCounts.dining_tables = 1;
    homeItemCounts.sofas = 2;
    homeItemCounts.storage_units = 4;
    homeItemCounts.wall_decor = 5;
    homeItemCounts.curtains = 6;
    homeItemCounts.rugs = 3;
    setChipSelection(roomsChips, ['Living Room', 'Master Bedroom', 'Kitchen', 'Dining Area', 'Home Office', 'Balcony / Garden', 'Bathroom']);
  } else if (preset === 'luxury') {
    budgetInput.value = 600000;
    homeItemCounts.lights = 16;
    homeItemCounts.ceiling_fans = 5;
    homeItemCounts.dining_tables = 2;
    homeItemCounts.sofas = 2;
    homeItemCounts.storage_units = 6;
    homeItemCounts.wall_decor = 8;
    homeItemCounts.curtains = 8;
    homeItemCounts.rugs = 4;
    setChipSelection(roomsChips, ['Living Room', 'Master Bedroom', 'Kitchen', 'Dining Area', 'Home Office', 'Kids Room', 'Balcony / Garden', 'Bathroom']);
  }

  // Update stepper displays
  Object.keys(homeItemCounts).forEach(k => {
    const el = document.getElementById(`val-${k}`);
    if (el) el.textContent = homeItemCounts[k];
  });
  showToast(`Applied ${preset.toUpperCase()} preset`);
}

function setChipSelection(container, values) {
  if (!container) return;
  const valSet = new Set(values);
  container.querySelectorAll('.chip-option').forEach(chip => {
    const input = chip.querySelector('input');
    if (input) {
      input.checked = valSet.has(input.value);
      chip.classList.toggle('selected', input.checked);
    }
  });
}

function initHomeForm() {
  const form = document.getElementById('homeForm');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = document.getElementById('homeSubmitBtn');
    const textSpan = document.getElementById('btnText');
    const resultBox = document.getElementById('result');
    
    // Collect form fields
    const formData = new FormData(form);
    const budget = parseFloat(formData.get('budget')) || 50000;
    const currency = formData.get('currency') || 'INR';
    
    // Collect checked rooms
    const rooms = Array.from(form.querySelectorAll('input[name="rooms"]:checked')).map(el => el.value);
    if (!rooms.length) {
      showToast('Please select at least one room type', 'error');
      return;
    }

    // Collect style & priorities
    const style = form.querySelector('input[name="style"]:checked')?.value || 'Scandinavian Modern';
    const priorities = Array.from(form.querySelectorAll('input[name="priorities"]:checked')).map(el => el.value);

    // Build payload
    const payload = {
      budget,
      currency,
      rooms,
      items: { ...homeItemCounts },
      style,
      priorities
    };

    btn.disabled = true;
    textSpan.innerHTML = '<span class="spinner"></span> Consulting Gemini AI Engine...';
    resultBox.innerHTML = `
      <div class="glass-card" style="text-align: center; padding: 3rem; margin-top: 2rem;">
        <div class="spinner" style="width: 32px; height: 32px; border-width: 3px;"></div>
        <h3 style="margin-top: 1.25rem; font-family: var(--font-display); color: #fff;">Balancing Style, Function & Budget...</h3>
        <p style="color: var(--ink-muted); font-size: 0.9rem; margin-top: 0.5rem;">Sourcing cost-effective options across IKEA, Amazon, and Flipkart candidate catalogs.</p>
      </div>
    `;

    try {
      const data = await api('/api/generate-home', {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      currentPlanData = data;
      renderPlanResult(data, 'home');
      resultBox.scrollIntoView({ behavior: 'smooth' });
      showToast('Home interior plan generated!');
    } catch (err) {
      resultBox.innerHTML = `<div class="glass-card" style="border-color: rgba(244, 63, 94, 0.4); color: #f87171; padding: 2rem; text-align: center;">Error generating plan: ${err.message}</div>`;
      showToast(err.message, 'error');
    } finally {
      btn.disabled = false;
      textSpan.textContent = '✨ Generate Home Budget Plan';
    }
  });
}

// ----------------- SCENARIO 2: PARTY PLANNER -----------------
function updateCostPerGuest() {
  const budget = parseFloat(document.getElementById('partyBudget')?.value) || 0;
  const guests = parseInt(document.getElementById('partyGuests')?.value) || 1;
  const cost = Math.round(budget / Math.max(1, guests));

  const valEl = document.getElementById('costPerGuestVal');
  const labelEl = document.getElementById('guestBudgetLabel');
  if (valEl) valEl.textContent = `₹${cost.toLocaleString('en-IN')}`;

  if (labelEl) {
    if (cost < 400) {
      labelEl.textContent = 'Pocket Saver Tier (Snacks & Platters)';
    } else if (cost < 1200) {
      labelEl.textContent = 'Comfortable Buffet & Theme Tier';
    } else if (cost < 2500) {
      labelEl.textContent = 'Deluxe Celebration & Live Setup';
    } else {
      labelEl.textContent = 'Grand Luxury Feast & Venue Tier';
    }
  }
}

function applyPartyPreset(preset) {
  const b = document.getElementById('partyBudget');
  const g = document.getElementById('partyGuests');
  const typeChips = document.getElementById('eventTypeChips');
  const venueChips = document.getElementById('venueChips');

  if (preset === 'house') {
    b.value = 12000;
    g.value = 15;
    selectRadioChip(typeChips, 'Casual House Party');
    selectRadioChip(venueChips, 'Home / Terrace');
  } else if (preset === 'birthday') {
    b.value = 30000;
    g.value = 35;
    selectRadioChip(typeChips, 'Birthday Party');
    selectRadioChip(venueChips, 'Home / Terrace');
  } else if (preset === 'corporate') {
    b.value = 75000;
    g.value = 60;
    selectRadioChip(typeChips, 'Corporate Team Mixer');
    selectRadioChip(venueChips, 'OYO Townhouse / Party Hall');
  } else if (preset === 'wedding') {
    b.value = 200000;
    g.value = 100;
    selectRadioChip(typeChips, 'Wedding / Sangeet');
    selectRadioChip(venueChips, 'Banquet Hall');
  }

  updateCostPerGuest();
  showToast(`Applied ${preset.toUpperCase()} party preset`);
}

function selectRadioChip(container, value) {
  if (!container) return;
  container.querySelectorAll('.chip-option').forEach(chip => {
    const radio = chip.querySelector('input[type="radio"]');
    if (radio) {
      const match = radio.value === value;
      radio.checked = match;
      chip.classList.toggle('selected', match);
    }
  });
}

function initPartyForm() {
  const form = document.getElementById('partyForm');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = document.getElementById('partySubmitBtn');
    const textSpan = document.getElementById('btnText');
    const resultBox = document.getElementById('result');

    const formData = new FormData(form);
    const budget = parseFloat(formData.get('budget')) || 25000;
    const guests = parseInt(formData.get('guests')) || 25;
    const event_type = form.querySelector('input[name="event_type"]:checked')?.value || 'Birthday Party';
    const venue = form.querySelector('input[name="venue"]:checked')?.value || 'Home / Terrace';
    const city = formData.get('city') || 'Bangalore';
    const preferences = Array.from(form.querySelectorAll('input[name="preferences"]:checked')).map(el => el.value);

    const payload = {
      budget,
      currency: 'INR',
      guests,
      event_type,
      venue,
      city,
      preferences
    };

    btn.disabled = true;
    textSpan.innerHTML = '<span class="spinner"></span> Analyzing Event Scale with Gemini...';
    resultBox.innerHTML = `
      <div class="glass-card" style="text-align: center; padding: 3rem; margin-top: 2rem;">
        <div class="spinner" style="width: 32px; height: 32px; border-width: 3px;"></div>
        <h3 style="margin-top: 1.25rem; font-family: var(--font-display); color: #fff;">Allocating Catering, Decor & Stays...</h3>
        <p style="color: var(--ink-muted); font-size: 0.9rem; margin-top: 0.5rem;">Sourcing vendors from Swiggy, Zomato, OYO, and Amazon for ${guests} guests.</p>
      </div>
    `;

    try {
      const data = await api('/api/generate-party', {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      currentPlanData = data;
      renderPlanResult(data, 'party');
      resultBox.scrollIntoView({ behavior: 'smooth' });
      showToast('Party budget plan generated!');
    } catch (err) {
      resultBox.innerHTML = `<div class="glass-card" style="border-color: rgba(244, 63, 94, 0.4); color: #f87171; padding: 2rem; text-align: center;">Error generating plan: ${err.message}</div>`;
      showToast(err.message, 'error');
    } finally {
      btn.disabled = false;
      textSpan.textContent = '✨ Generate Party Budget Plan';
    }
  });
}

// ----------------- SCENARIO 3: JEWELRY PLANNER -----------------
function applyJewelryPreset(preset) {
  const b = document.getElementById('jewelryBudget');
  const occChips = document.getElementById('occasionChips');
  const styleChips = document.getElementById('jewelryStyleChips');
  const metalChips = document.getElementById('metalChips');
  const desc = document.getElementById('outfitDescInput');

  if (preset === 'boho') {
    b.value = 5000;
    selectRadioChip(occChips, 'Festive / Diwali / Puja');
    selectRadioChip(styleChips, 'Bohemian Oxidized Silver');
    selectRadioChip(metalChips, 'Oxidized Antique');
    desc.value = 'Indigo blue cotton handblock kurti with mirror work jacket';
  } else if (preset === 'cocktail') {
    b.value = 15000;
    selectRadioChip(occChips, 'Cocktail & Black Tie Gala');
    selectRadioChip(styleChips, 'American Diamond Solitaires');
    selectRadioChip(metalChips, 'Platinum / 925 Silver');
    desc.value = 'Emerald green satin evening gown with off-shoulder neckline';
  } else if (preset === 'kundan') {
    b.value = 45000;
    selectRadioChip(occChips, 'Sangeet & Reception');
    selectRadioChip(styleChips, 'Royal Kundan & Polki');
    selectRadioChip(metalChips, 'Yellow Gold Tone');
    desc.value = 'Pastel peach lehenga with gold sequins and sweetheart neckline';
  } else if (preset === 'bridal') {
    b.value = 150000;
    selectRadioChip(occChips, 'Wedding / Bridal');
    selectRadioChip(styleChips, 'Royal Kundan & Polki');
    selectRadioChip(metalChips, 'Yellow Gold Tone');
    desc.value = 'Deep crimson raw silk bridal lehenga with heavy antique zardozi border';
  }
  showToast(`Applied ${preset.toUpperCase()} jewelry preset`);
}

// Image Selection & Canvas Color Extraction
function handleImageSelection(input) {
  const file = input.files?.[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (e) => {
    const previewBox = document.getElementById('imagePreviewBox');
    const previewImg = document.getElementById('previewImg');
    const nameEl = document.getElementById('previewFileName');
    
    previewImg.src = e.target.result;
    nameEl.textContent = `${file.name} (${(file.size / 1024).toFixed(0)} KB)`;
    previewBox.classList.remove('hidden');

    // Extract dominant colors via Canvas
    extractImagePalette(previewImg);
  };
  reader.readAsDataURL(file);
}

function clearOutfitImage() {
  const input = document.getElementById('outfitImageInput');
  if (input) input.value = '';
  document.getElementById('imagePreviewBox')?.classList.add('hidden');
  document.getElementById('previewImg').src = '';
  document.getElementById('paletteSwatches').innerHTML = '';
}

function extractImagePalette(imgElement) {
  imgElement.onload = () => {
    try {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      canvas.width = 40;
      canvas.height = 40;
      ctx.drawImage(imgElement, 0, 0, 40, 40);
      
      const imgData = ctx.getImageData(0, 0, 40, 40).data;
      const colorCounts = {};

      for (let i = 0; i < imgData.length; i += 16) {
        const r = imgData[i];
        const g = imgData[i + 1];
        const b = imgData[i + 2];
        const a = imgData[i + 3];
        if (a < 128) continue; // skip transparent

        // Quantize colors to reduce noise
        const qr = Math.round(r / 32) * 32;
        const qg = Math.round(g / 32) * 32;
        const qb = Math.round(b / 32) * 32;
        const hex = rgbToHex(qr, qg, qb);
        colorCounts[hex] = (colorCounts[hex] || 0) + 1;
      }

      // Sort by frequency
      const sorted = Object.entries(colorCounts).sort((a, b) => b[1] - a[1]).slice(0, 4);
      const swatchesBox = document.getElementById('paletteSwatches');
      if (swatchesBox) {
        swatchesBox.innerHTML = '';
        const detectedHexes = [];

        sorted.forEach(([hex]) => {
          detectedHexes.push(hex);
          const chip = document.createElement('span');
          chip.className = 'swatch-chip';
          chip.style.backgroundColor = hex;
          chip.title = `Color: ${hex}`;
          swatchesBox.appendChild(chip);
        });

        // Append detected colors to outfit description if not already present
        const descEl = document.getElementById('outfitDescInput');
        if (descEl && detectedHexes.length) {
          const colorNote = ` [Detected outfit palette: ${detectedHexes.join(', ')}]`;
          if (!descEl.value.includes('Detected outfit palette')) {
            descEl.value += colorNote;
          }
        }
      }
    } catch (err) {
      console.warn('Canvas palette extraction error:', err);
    }
  };
}

function rgbToHex(r, g, b) {
  return '#' + [r, g, b].map(x => Math.min(255, Math.max(0, x)).toString(16).padStart(2, '0')).join('');
}

function initJewelryForm() {
  const form = document.getElementById('jewelryForm');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = document.getElementById('jewelrySubmitBtn');
    const textSpan = document.getElementById('btnText');
    const resultBox = document.getElementById('result');

    const formData = new FormData(form);
    
    // Explicitly set radio chip values in FormData
    const occasion = form.querySelector('input[name="occasion"]:checked')?.value || 'Wedding / Bridal';
    const style = form.querySelector('input[name="style"]:checked')?.value || 'Royal Kundan & Polki';
    const metal = form.querySelector('input[name="metal"]:checked')?.value || 'Yellow Gold Tone';
    formData.set('occasion', occasion);
    formData.set('style', style);
    formData.set('metal', metal);

    btn.disabled = true;
    textSpan.innerHTML = '<span class="spinner"></span> Performing Multimodal Gemini Analysis...';
    resultBox.innerHTML = `
      <div class="glass-card" style="text-align: center; padding: 3rem; margin-top: 2rem;">
        <div class="spinner" style="width: 32px; height: 32px; border-width: 3px;"></div>
        <h3 style="margin-top: 1.25rem; font-family: var(--font-display); color: #fff;">Coordinating Jewelry Aesthetics & Color Harmony...</h3>
        <p style="color: var(--ink-muted); font-size: 0.9rem; margin-top: 0.5rem;">Matching necklaces, earrings, and bangles from Amazon, Flipkart, Tanishq, and CaratLane.</p>
      </div>
    `;

    try {
      const data = await api('/api/generate-jewelry', {
        method: 'POST',
        body: formData
      });
      currentPlanData = data;
      renderPlanResult(data, 'jewelry');
      resultBox.scrollIntoView({ behavior: 'smooth' });
      showToast('Jewelry recommendations generated!');
    } catch (err) {
      resultBox.innerHTML = `<div class="glass-card" style="border-color: rgba(244, 63, 94, 0.4); color: #f87171; padding: 2rem; text-align: center;">Error generating plan: ${err.message}</div>`;
      showToast(err.message, 'error');
    } finally {
      btn.disabled = false;
      textSpan.textContent = '✨ Generate Matched Jewelry Plan';
    }
  });
}

// ----------------- RESULTS RENDERER & INTERACTIVE CART TRACKER -----------------
function renderPlanResult(data, plannerType) {
  const container = document.getElementById('result');
  if (!container) return;

  selectedCartItems.clear();
  (data.recommendations || []).forEach((item, idx) => selectedCartItems.add(idx));

  const totalBudget = data.budget || 0;
  const isGemini = data.source_mode === 'gemini';

  // Build Allocations HTML
  const allocations = data.allocations || [];
  const barSegmentsHtml = allocations.map((a, i) => `
    <div class="bar-segment segment-${i % 6}" style="width: ${a.percentage}%" title="${a.category}: ₹${Number(a.amount).toLocaleString('en-IN')} (${a.percentage}%)"></div>
  `).join('');

  const allocCardsHtml = allocations.map((a, i) => `
    <div class="alloc-mini-card">
      <div class="alloc-category">${a.category}</div>
      <div class="alloc-amount">₹${Number(a.amount).toLocaleString('en-IN')}</div>
      <div class="alloc-pct">${a.percentage}% of total budget</div>
    </div>
  `).join('');

  // Build Recommendations HTML
  const items = data.recommendations || [];
  const recsHtml = items.map((x, idx) => {
    const platClass = (x.platform || 'Amazon').toLowerCase();
    return `
      <article class="product-card" data-platform="${platClass}" data-idx="${idx}">
        <div class="product-top">
          <div class="product-badges">
            <span class="platform-pill ${platClass}">${x.platform}</span>
            <span class="plat-tag" style="font-size: 0.7rem; padding: 0.15rem 0.5rem;">${x.category}</span>
            ${x.badge ? `<span style="font-size: 0.7rem; color: #38bdf8; font-weight: 700;">★ ${x.badge}</span>` : ''}
          </div>
          <span class="rating-badge">★ ${x.rating || 4.7}</span>
        </div>

        <h4 class="product-name">${x.name}</h4>
        <p class="product-reason">${x.reason}</p>

        <div class="product-bottom">
          <div class="product-price-box">
            <span class="price-label">Estimated Price</span>
            <span class="price-value">₹${Number(x.estimated_price).toLocaleString('en-IN')}</span>
          </div>

          <label class="cart-check-label">
            <input type="checkbox" checked onchange="toggleCartItem(${idx}, ${x.estimated_price}, this)">
            <span>Include</span>
          </label>
        </div>

        <div style="margin-top: 0.85rem;">
          <a class="btn btn-outline-sm" style="width: 100%;" target="_blank" rel="noopener noreferrer" href="${x.url}">
            <span>View on ${x.platform}</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
          </a>
        </div>
      </article>
    `;
  }).join('');

  // Tips HTML
  const tipsHtml = (data.tips || []).map(t => `<li>${t}</li>`).join('');

  container.innerHTML = `
    <div class="result-section">
      <!-- Result Banner Card -->
      <div class="result-header-card">
        <div class="result-badge-row">
          <span class="ai-engine-tag ${isGemini ? 'gemini' : 'fallback'}">
            ${isGemini ? '⚡ Gemini 3.5 AI Optimization' : '🛡️ Smart Fallback Engine'}
          </span>
          <span style="font-size: 0.82rem; color: var(--ink-muted); font-weight: 600;">
            Target Budget: ₹${Number(totalBudget).toLocaleString('en-IN')}
          </span>
        </div>
        <h2 class="result-title">${getPlannerTitle(plannerType)}</h2>
        <p class="result-summary">${data.summary}</p>
      </div>

      <!-- Proportional Budget Visualizer -->
      <div class="allocation-panel">
        <div class="allocation-panel-head">
          <h3 style="font-family: var(--font-display); font-size: 1.15rem; font-weight: 700; color: #fff;">
            Proportional Budget Allocation
          </h3>
          <span style="font-size: 0.82rem; color: var(--emerald); font-weight: 600;">100% Balanced</span>
        </div>
        
        <div class="allocation-bar-container">
          ${barSegmentsHtml}
        </div>

        <div class="allocation-cards-grid">
          ${allocCardsHtml}
        </div>
      </div>

      <!-- Live Cart Tracker Bar -->
      <div class="cart-tracker-bar" id="cartTrackerBar">
        <div class="cart-tracker-metrics">
          <div class="tracker-metric-col">
            <span class="tracker-label">Selected Items Total</span>
            <span class="tracker-val" id="selectedTotalDisplay">₹0</span>
          </div>
          <div class="tracker-metric-col">
            <span class="tracker-label">Allocated Budget</span>
            <span class="tracker-val">₹${Number(totalBudget).toLocaleString('en-IN')}</span>
          </div>
          <div class="tracker-metric-col">
            <span class="tracker-label">Remaining Balance</span>
            <span class="tracker-val remaining" id="remainingBalanceDisplay">₹0</span>
          </div>
        </div>

        <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
          <button type="button" class="btn btn-outline-sm" onclick="copyChecklistToClipboard()">
            📋 Copy Shopping List
          </button>
          <button type="button" class="btn btn-primary-sm" onclick="savePlanToUserDashboard('${plannerType}')" id="savePlanBtn">
            💾 Save to Dashboard
          </button>
        </div>
      </div>

      <!-- Recommendations Header & Filters -->
      <div class="recommendations-header-row">
        <h3 style="font-family: var(--font-display); font-size: 1.3rem; font-weight: 800; color: #fff;">
          Curated Product & Vendor Recommendations
        </h3>
        <div class="rec-filter-chips" id="platformFilterChips">
          <button type="button" class="rec-filter-btn active" onclick="filterRecommendations('all')">All Platforms</button>
          <button type="button" class="rec-filter-btn" onclick="filterRecommendations('ikea')">IKEA</button>
          <button type="button" class="rec-filter-btn" onclick="filterRecommendations('amazon')">Amazon</button>
          <button type="button" class="rec-filter-btn" onclick="filterRecommendations('flipkart')">Flipkart</button>
          <button type="button" class="rec-filter-btn" onclick="filterRecommendations('swiggy')">Swiggy</button>
          <button type="button" class="rec-filter-btn" onclick="filterRecommendations('zomato')">Zomato</button>
          <button type="button" class="rec-filter-btn" onclick="filterRecommendations('oyo')">OYO</button>
        </div>
      </div>

      <!-- Product Cards Grid -->
      <div class="products-grid" id="productsGrid">
        ${recsHtml}
      </div>

      <!-- Tips & Disclaimer Grid -->
      <div class="plan-extras-grid">
        <div class="tips-box">
          <h4>AI Budgeting & Strategy Insights</h4>
          <ul class="tips-list">
            ${tipsHtml}
          </ul>
        </div>

        <div class="disclaimer-card">
          <h4>Marketplace Adapter Notice</h4>
          <p>${data.disclaimer}</p>
          <p style="margin-top: 0.5rem; font-size: 0.78rem;">Cross-platform inventory is periodically refreshed. Check vendor pages for current live discounts, delivery timelines, and partner coupons.</p>
        </div>
      </div>

      <!-- Action Bar -->
      <div class="plan-actions-bar">
        <button type="button" class="btn btn-outline" onclick="window.print()">
          🖨️ Print / Save as PDF
        </button>
        <button type="button" class="btn btn-primary" onclick="copyChecklistToClipboard()">
          📋 Copy Checklist to Clipboard
        </button>
      </div>
    </div>
  `;

  recalculateCartTotal();
}

function getPlannerTitle(type) {
  if (type === 'home') return 'Home Interior Design & Budget Allocation';
  if (type === 'party') return 'Event Budget Allocation & Vendor Plan';
  return 'Jewelry & Outfit Styling Ensemble Plan';
}

function toggleCartItem(idx, price, checkbox) {
  if (checkbox.checked) {
    selectedCartItems.add(idx);
  } else {
    selectedCartItems.delete(idx);
  }
  recalculateCartTotal();
}

function recalculateCartTotal() {
  if (!currentPlanData) return;
  const items = currentPlanData.recommendations || [];
  let sum = 0;
  selectedCartItems.forEach(idx => {
    if (items[idx]) sum += items[idx].estimated_price;
  });

  const budget = currentPlanData.budget || 0;
  const remaining = budget - sum;

  const totalEl = document.getElementById('selectedTotalDisplay');
  const remEl = document.getElementById('remainingBalanceDisplay');

  if (totalEl) totalEl.textContent = `₹${sum.toLocaleString('en-IN')}`;
  if (remEl) {
    if (remaining >= 0) {
      remEl.className = 'tracker-val remaining';
      remEl.textContent = `+ ₹${remaining.toLocaleString('en-IN')}`;
    } else {
      remEl.className = 'tracker-val over';
      remEl.textContent = `- ₹${Math.abs(remaining).toLocaleString('en-IN')}`;
    }
  }
}

function filterRecommendations(platform) {
  document.querySelectorAll('.rec-filter-btn').forEach(btn => btn.classList.remove('active'));
  event.target.classList.add('active');

  const cards = document.querySelectorAll('.product-card');
  cards.forEach(card => {
    if (platform === 'all' || card.dataset.platform === platform) {
      card.style.display = 'flex';
    } else {
      card.style.display = 'none';
    }
  });
}

function copyChecklistToClipboard() {
  if (!currentPlanData) return;
  const items = currentPlanData.recommendations || [];
  let text = `PocketSmart AI — ${currentPlanData.summary}\n`;
  text += `Budget: ₹${currentPlanData.budget?.toLocaleString('en-IN')}\n\n`;
  text += `RECOMMENDED ITEMS:\n`;

  selectedCartItems.forEach(idx => {
    const x = items[idx];
    if (x) {
      text += `• [${x.platform}] ${x.name} — ₹${x.estimated_price?.toLocaleString('en-IN')} (${x.url})\n`;
    }
  });

  text += `\nTIPS:\n`;
  (currentPlanData.tips || []).forEach(t => { text += `- ${t}\n`; });

  navigator.clipboard.writeText(text).then(() => {
    showToast('Shopping list copied to clipboard!');
  }).catch(() => {
    showToast('Failed to copy list', 'error');
  });
}

async function savePlanToUserDashboard(planner) {
  if (!currentPlanData) return;
  const saveBtn = document.getElementById('savePlanBtn');
  if (saveBtn) saveBtn.disabled = true;

  try {
    // If it's already saved with an id
    if (currentPlanData.recommendation_id) {
      showToast('Plan is already saved in your dashboard!');
      return;
    }

    const payload = {
      planner,
      title: getPlannerTitle(planner),
      request_data: { budget: currentPlanData.budget },
      result_data: currentPlanData
    };

    await api('/api/save-recommendation', {
      method: 'POST',
      body: JSON.stringify(payload)
    });
    showToast('Plan saved to your dashboard successfully!');
  } catch (err) {
    if (err.message.includes('401') || err.message.includes('Authentication')) {
      showToast('Please sign in or use Demo Login to save plans to your dashboard', 'error');
      setTimeout(() => { location.href = '/login'; }, 1000);
    } else {
      showToast(err.message, 'error');
    }
  } finally {
    if (saveBtn) saveBtn.disabled = false;
  }
}

// ----------------- DASHBOARD FUNCTIONALITY -----------------
let dashboardHistoryItems = [];

async function loadDashboardHistory() {
  const container = document.getElementById('dashboardList');
  if (!container) return;

  try {
    const sessionData = await api('/api/session-data');
    const history = await api('/api/history');
    dashboardHistoryItems = history;

    // Update metrics
    document.getElementById('metricPlanCount').textContent = history.length;
    let totalCap = 0;
    history.forEach(h => { totalCap += (h.budget || 0); });
    document.getElementById('metricTotalBudget').textContent = `₹${totalCap.toLocaleString('en-IN')}`;

    if (!history.length) {
      container.innerHTML = `
        <div class="glass-card" style="text-align: center; padding: 3rem;">
          <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">📋</div>
          <h3 style="font-family: var(--font-display); font-size: 1.25rem; color: #fff;">No Plans Saved Yet</h3>
          <p style="color: var(--ink-muted); font-size: 0.9rem; margin: 0.5rem 0 1.5rem;">
            Create your first budget plan for Home Interior, a Party, or Jewelry styling.
          </p>
          <a href="/planner/home" class="btn btn-primary-sm">Start Planning Now →</a>
        </div>
      `;
      return;
    }

    renderDashboardCards(history);
  } catch (err) {
    container.innerHTML = `
      <div class="glass-card" style="text-align: center; padding: 2.5rem; border-color: rgba(244, 63, 94, 0.4);">
        <p style="color: #f87171; margin-bottom: 1rem;">Please sign in to view your dashboard history.</p>
        <a href="/login" class="btn btn-primary-sm">Sign In or One-Click Demo Access</a>
      </div>
    `;
  }
}

function renderDashboardCards(items) {
  const container = document.getElementById('dashboardList');
  if (!container) return;

  const iconMap = { home: '🏠', party: '🎉', jewelry: '💎' };

  container.innerHTML = items.map(item => `
    <article class="history-card" id="history-${item.id}">
      <div class="history-left">
        <div class="history-planner-icon">${iconMap[item.planner] || '📊'}</div>
        <div>
          <h4 class="history-title">${item.title}</h4>
          <p class="history-summary">${item.summary || 'Custom budget plan'}</p>
          <div class="history-meta">
            <span>Budget: ₹${Number(item.budget || 0).toLocaleString('en-IN')}</span> • 
            <span>${new Date(item.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}</span>
          </div>
        </div>
      </div>

      <div class="history-actions">
        <button type="button" class="btn btn-outline-sm" onclick="viewPlanDetails(${item.id})">
          View Plan
        </button>
        <button type="button" class="btn-logout" onclick="deletePlan(${item.id})" title="Delete plan">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
        </button>
      </div>
    </article>
  `).join('');
}

function filterDashboard(type) {
  document.querySelectorAll('#dashboardFilters .rec-filter-btn').forEach(btn => btn.classList.remove('active'));
  event.target.classList.add('active');

  if (type === 'all') {
    renderDashboardCards(dashboardHistoryItems);
  } else {
    renderDashboardCards(dashboardHistoryItems.filter(x => x.planner === type));
  }
}

async function viewPlanDetails(id) {
  try {
    const d = await api(`/api/recommendations-details/${id}`);
    const modal = document.getElementById('planModal');
    const badge = document.getElementById('modalPlannerBadge');
    const title = document.getElementById('modalPlanTitle');
    const body = document.getElementById('modalPlanBody');

    badge.textContent = d.planner.toUpperCase();
    badge.className = `platform-pill ${d.planner}`;
    title.textContent = d.title;

    const res = d.result || {};
    const allocs = res.allocations || [];
    const recs = res.recommendations || [];
    const tips = res.tips || [];

    body.innerHTML = `
      <p style="color: var(--ink-secondary); font-size: 0.95rem; margin-bottom: 1.5rem; line-height: 1.6;">
        ${res.summary || ''}
      </p>

      <h4 style="font-family: var(--font-display); font-size: 1rem; color: #fff; margin-bottom: 0.75rem;">
        Budget Allocations (Total: ₹${Number(res.budget || 0).toLocaleString('en-IN')})
      </h4>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 0.75rem; margin-bottom: 1.5rem;">
        ${allocs.map(a => `
          <div class="alloc-mini-card" style="padding: 0.75rem;">
            <div style="font-size: 0.72rem; color: var(--ink-muted);">${a.category}</div>
            <div style="font-size: 1.05rem; font-weight: 800; color: #fff;">₹${Number(a.amount).toLocaleString('en-IN')}</div>
            <div style="font-size: 0.7rem; color: var(--ink-faint);">${a.percentage}%</div>
          </div>
        `).join('')}
      </div>

      <h4 style="font-family: var(--font-display); font-size: 1rem; color: #fff; margin-bottom: 0.75rem;">
        Recommended Items (${recs.length})
      </h4>
      <div style="display: flex; flex-direction: column; gap: 0.75rem; margin-bottom: 1.5rem;">
        ${recs.map(x => `
          <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid var(--card-border); padding: 0.85rem; border-radius: var(--radius-sm); display: flex; justify-content: space-between; align-items: center;">
            <div>
              <div style="font-weight: 700; font-size: 0.9rem; color: #fff;">${x.name}</div>
              <div style="font-size: 0.75rem; color: var(--ink-muted);">${x.platform} • ${x.category}</div>
            </div>
            <div style="text-align: right;">
              <div style="font-weight: 800; color: #34d399;">₹${Number(x.estimated_price).toLocaleString('en-IN')}</div>
              <a href="${x.url}" target="_blank" rel="noopener" style="font-size: 0.72rem; color: var(--primary);">View ↗</a>
            </div>
          </div>
        `).join('')}
      </div>

      <h4 style="font-family: var(--font-display); font-size: 1rem; color: #fff; margin-bottom: 0.5rem;">Strategy Tips</h4>
      <ul class="tips-list">
        ${tips.map(t => `<li>${t}</li>`).join('')}
      </ul>
    `;

    modal.classList.add('open');
  } catch (err) {
    showToast(err.message, 'error');
  }
}

function closePlanModal() {
  document.getElementById('planModal')?.classList.remove('open');
}

async function deletePlan(id) {
  if (!confirm('Are you sure you want to delete this saved plan?')) return;
  try {
    await api(`/api/recommendations/${id}`, { method: 'DELETE' });
    showToast('Plan deleted');
    document.getElementById(`history-${id}`)?.remove();
    loadDashboardHistory();
  } catch (err) {
    showToast(err.message, 'error');
  }
}
