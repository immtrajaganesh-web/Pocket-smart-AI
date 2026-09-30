# PocketSmart AI: Your Smart Budget & Cross-Platform Recommendation Assistant

PocketSmart AI is a GenAI-powered, cross-platform budget planning and recommendation system built with **FastAPI**, **Google Gemini 3.5**, and modern frontend design. It transforms budgeting across home interior design, party planning, and occasion jewelry into an intelligent, user-friendly experience.

---

## 🌟 The Three Core Scenarios

### Scenario 1: Home Interior Planning with Smart Budget Allocation
- **User Inputs**: Budget entry (in ₹ INR), room multi-selection (Living Room, Master Bedroom, Kitchen, Dining Area, Balcony, Home Office, Kids Room, Bathroom), and exact item quantities using interactive visual steppers (e.g. 4 ceiling lights, 2 BLDC fans, 1 dining set, 1 sofa, etc.).
- **AI Processing**: Gemini balances functionality, style (Scandinavian, Minimalist, Contemporary Indian, Industrial, Boho), and price across **IKEA**, **Amazon**, and **Flipkart**.
- **Output**: 100% balanced proportional allocation breakdown (Furniture, Lighting, Fans & Appliances, Decor, Contingency Buffer), item cards with direct links, and a live interactive shopping cart budget tracker.

### Scenario 2: AI-Based Party Budget Planning
- **User Inputs**: Total budget, guest count (with dynamic real-time **Cost Per Head** calculation), event occasion (Birthday, Wedding / Sangeet, Corporate Mixer, House Party, Anniversary, Festive Gala), venue details (Home, OYO Townhouse / Hall, Banquet Hall, Outdoor Lawn, Rooftop), city, and catering/dietary preferences.
- **AI Processing**: Proportionally allocates spend across gourmet catering, themed decor, music/entertainment, and venue/accommodation, sourcing options from **Swiggy**, **Zomato**, **OYO**, and **Amazon**.
- **Output**: Cost-per-head efficiency tiers, feast & party snack combos, balloon & fairy light backdrops, and event hosting tips.

### Scenario 3: Jewelry Recommendations for Occasions with Multimodal Outfit Analysis
- **User Inputs**: Target budget, occasion (Bridal, Sangeet, Cocktail Gala, Festive Puja, Everyday Chic, Workwear), style preference (Royal Kundan, Temple Jewelry, Minimalist Modern, American Diamond / CZ, Bohemian Silver), and metal tone (Yellow Gold, Rose Gold, Platinum / Silver, Antique).
- **Outfit Image Upload**: Users can drag & drop an outfit photo. The platform performs client-side Canvas color extraction (dominant 4-color palette swatches) and passes the visual to Gemini for color coordination, neckline fit, and aesthetic matching.
- **Output**: Coordinated jewelry ensembles (necklace sets, earrings, bangles, rings) from **Amazon**, **Flipkart**, **Tanishq**, **CaratLane**, and **GIVA**.

---

## 🚀 Key Architectural Highlights

1. **Dual AI & Fallback Resilience Engine**:
   - Primary: Live **Google Gemini 3.5** (`gemini-3.5-flash-lite` / `gemini-2.5-flash-lite` / `gemini-flash-latest`) using structured Pydantic JSON schemas and multimodal image analysis.
   - Secondary: Deterministic, local domain-aware fallback catalog engine that guarantees 100% uptime even if API keys or networks are offline.
2. **Cross-Platform Marketplace Adapter**:
   - Curated multi-platform catalog of 60+ realistic products and services across **IKEA, Amazon, Flipkart, Swiggy, Zomato, OYO, Blinkit, and Tanishq**.
3. **Interactive Budget Cart & Checklist**:
   - Check and uncheck recommendations to calculate live cart spend against your target budget in real time.
   - Copy clean shopping checklists to clipboard with a single click.
   - Print or save plans directly as PDF.
4. **Frictionless Usage & Authentication**:
   - Instant guest planner mode: generate plans immediately without forced signup.
   - Optional registration / login with JWT cookies, plus a **One-Click Instant Demo Login** for quick testing.
   - Saved plan dashboard with full detail modal inspector and history deletion.

---

## 🛠️ Quickstart

### Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- Windows / macOS / Linux

### Setup
```powershell
# 1. Activate virtual environment
.venv\Scripts\activate

# 2. Install dependencies (if not already installed)
pip install -r requirements.txt

# 3. Configure environment
copy .env.example .env
# Set GEMINI_API_KEY=your_key in .env

# 4. Start local development server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 🧪 Testing

Run all unit and end-to-end integration tests:
```powershell
.venv\Scripts\python -m pytest -v
```

All 5 test suites pass:
- `test_health`: API health status & Gemini configuration check.
- `test_home`: Home Interior plan generation & proportional allocations.
- `test_party`: Party planner with guest-scale budgeting.
- `test_jewelry`: Jewelry planner with occasion & style matching.
- `test_full_pipeline`: Complete E2E registration, JWT session, home generation, history persistence, detail retrieval, and all 7 frontend HTML routes.

---

## 📡 API Endpoints

- **Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Health**: `GET /api/health`
- **Auth**: `POST /api/auth/register`, `POST /api/auth/login`, `POST /api/auth/token`, `POST /api/auth/logout`
- **Session**: `GET /api/session-info`, `GET /api/session-data`
- **Planners**:
  - `POST /api/generate-home` (JSON: budget, rooms, items, style, priorities)
  - `POST /api/generate-party` (JSON: budget, guests, event_type, venue, city, preferences)
  - `POST /api/generate-jewelry` (Multipart Form: budget, occasion, style, metal, outfit_description, outfit_image)
- **Dashboard & History**:
  - `GET /api/history`
  - `GET /api/recommendations-details/{id}`
  - `POST /api/save-recommendation`
  - `DELETE /api/recommendations/{id}`
