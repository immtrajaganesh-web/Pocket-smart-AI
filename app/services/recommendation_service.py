from typing import Dict, Any, List, Optional
from app.services.catalog import search_catalog
from app.services.gemini_service import gemini_service

def fallback(planner: str, p: Dict[str, Any]) -> Dict[str, Any]:
    b = float(p.get("budget", 10000))
    currency = p.get("currency", "INR")
    
    # Context-aware tags
    if planner == "home":
        rooms = p.get("rooms", ["Living Room"])
        items_dict = p.get("items", {})
        priorities = p.get("priorities", [])
        style = p.get("style", "modern")
        item_keys = list(items_dict.keys())
        tags = rooms + [style] + priorities + item_keys
        
        alloc = [
            ("Furniture & Seating", 0.40),
            ("Lighting & Fixtures", 0.25),
            ("Appliances & Fans", 0.20),
            ("Decor & Soft Furnishings", 0.10),
            ("Contingency Buffer", 0.05)
        ]
        
        summary = (
            f"Curated Home Interior Plan for {', '.join(rooms)} designed in {style} aesthetic "
            f"with a structured ₹{b:,.0f} budget allocation."
        )
        tips = [
            "Opt for BLDC ceiling fans and LED fixtures to reduce monthly electricity bills by up to 50%.",
            "Prioritize multi-functional furniture like modular storage tables and expandable dining sets.",
            "Always inspect marketplace return policies and warranty coverage before finalizing purchases."
        ]

    elif planner == "party":
        guests = int(p.get("guests", 25))
        event_type = p.get("event_type", "Celebration Party")
        venue = p.get("venue", "Flexible")
        city = p.get("city", "")
        prefs = p.get("preferences", [])
        tags = [event_type, venue, city] + prefs
        
        # Per-guest budget
        per_guest = round(b / max(guests, 1), 2)
        
        if guests > 50:
            alloc = [
                ("Catering & Food Spread", 0.50),
                ("Venue & Space Setup", 0.20),
                ("Decoration & Lighting", 0.15),
                ("Entertainment & Music", 0.10),
                ("Emergency Buffer", 0.05)
            ]
        else:
            alloc = [
                ("Gourmet Food & Beverages", 0.45),
                ("Theme Decor & Lighting", 0.25),
                ("Music & Entertainment", 0.15),
                ("Venue / Logistics", 0.10),
                ("Buffer", 0.05)
            ]
            
        summary = (
            f"Optimized {event_type.title()} Plan for {guests} guests (Est. ₹{per_guest:,.0f}/guest) "
            f"balancing catering, decor, and entertainment within ₹{b:,.0f}."
        )
        tips = [
            f"Your estimated spend is ₹{per_guest:,.0f} per guest—consider combo banquet platters for better per-head economy.",
            "Use reusable warm fairy lights and balloon garlands for maximum visual impact at minimal cost.",
            "Pre-order beverages and party snacks via quick-commerce to take advantage of bundle discounts."
        ]

    else:  # jewelry
        occasion = p.get("occasion", "Special Occasion")
        style = p.get("style", "elegant")
        metal = p.get("metal", "any")
        outfit_desc = p.get("outfit_description", "")
        tags = [occasion, style, metal]
        if outfit_desc:
            tags.extend(outfit_desc.lower().split()[:5])
            
        alloc = [
            ("Statement Necklace / Choker", 0.45),
            ("Matching Earrings / Jhumkas", 0.25),
            ("Bangles / Kada / Bracelet", 0.15),
            ("Rings & Hair Accessories", 0.10),
            ("Contingency Buffer", 0.05)
        ]
        
        summary = (
            f"Handpicked {style.title()} Jewelry Ensemble for {occasion.title()} "
            f"in {metal.title()} tones within your ₹{b:,.0f} budget."
        )
        tips = [
            "Match your necklace neckline to your outfit collar: chokers for sweetheart necklines, long sets for high collars.",
            "Hallmarked 925 sterling silver and high-grade zircon offer diamond-like brilliance at a fraction of the cost.",
            "Store precious jewelry in airtight velvet-lined boxes to prevent oxidation and tarnishing."
        ]

    candidate_items = search_catalog(planner, b, tags, limit=8)
    items = []
    total_planned = 0.0
    
    for x in candidate_items:
        if x["estimated_price"] <= b:
            items.append({
                **x,
                "reason": f"Selected for {x['category'].title()} to balance price, durability, and style fit."
            })
            total_planned += x["estimated_price"]

    # If empty, take top 4 items regardless
    if not items:
        for x in candidate_items[:4]:
            items.append({
                **x,
                "reason": "Popular top-rated candidate within this style and category."
            })

    return {
        "planner": planner,
        "summary": summary,
        "budget": b,
        "currency": currency,
        "allocations": [
            {
                "category": cat,
                "amount": round(b * frac, 2),
                "percentage": round(frac * 100, 1)
            }
            for cat, frac in alloc
        ],
        "recommendations": items[:6],
        "tips": tips,
        "source_mode": "fallback",
        "disclaimer": "Marketplace entries are demo/mock data. Prices, ratings, and availability are estimates and must be verified before purchase."
    }

def generate(planner: str, p: Dict[str, Any], image_bytes: Optional[bytes] = None) -> Dict[str, Any]:
    b = float(p.get("budget", 10000))
    
    # Extract tags for candidate catalog filtering
    if planner == "home":
        tags = (
            p.get("rooms", []) + 
            [p.get("style", "modern")] + 
            p.get("priorities", []) + 
            list(p.get("items", {}).keys())
        )
    elif planner == "party":
        tags = (
            [p.get("event_type", "party"), p.get("venue", "")] + 
            p.get("preferences", []) + 
            [p.get("city", "")]
        )
    else:
        tags = (
            [p.get("occasion", ""), p.get("style", ""), p.get("metal", "")] + 
            (p.get("outfit_description", "").split()[:4] if p.get("outfit_description") else [])
        )
        
    catalog = search_catalog(planner, b, tags, limit=12)
    
    # Try live Gemini GenAI first
    ai_result = gemini_service.generate(planner, p, catalog, image_bytes)
    if ai_result:
        return ai_result
        
    # Fallback to local deterministic recommendation
    return fallback(planner, p)
