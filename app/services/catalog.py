from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass(frozen=True)
class Item:
    name: str
    category: str
    platform: str
    price: float
    url: str
    tags: tuple[str, ...]
    rating: float = 4.6
    badge: str = ""

CATALOG: list[Item] = [
    # ------------------ HOME INTERIOR & APPLIANCES ------------------
    # Lighting & Electricals
    Item("LÄTTBAKAD Modern LED Ceiling Light", "lighting", "IKEA", 1899, "https://www.ikea.com/in/en/", ("modern", "lighting", "living room", "lights", "ceiling"), 4.7, "IKEA Favorite"),
    Item("IKEA NYMÅNE 4-Spot Ceiling Spotlight Bar", "lighting", "IKEA", 2490, "https://www.ikea.com/in/en/", ("spotlight", "lighting", "kitchen", "modern", "lights"), 4.8, "Top Rated"),
    Item("Philips Wiz Wi-Fi Smart Tunable LED Downlight (Pack of 4)", "lighting", "Amazon", 2199, "https://www.amazon.in/", ("smart", "lighting", "bedroom", "living room", "lights", "iot"), 4.6, "Smart Choice"),
    Item("Wipro Garnet 20W LED Batten Surface Fixture", "lighting", "Flipkart", 499, "https://www.flipkart.com/", ("utility", "lighting", "kitchen", "bathroom", "lights", "budget"), 4.4, "Value Pick"),
    Item("HEKTAR Dark Grey Industrial Pendant Lamp", "lighting", "IKEA", 3990, "https://www.ikea.com/in/en/", ("chandelier", "pendant", "lighting", "dining", "modern"), 4.9, "Designer Choice"),
    Item("Warm White Smart Ambient LED Strip Light (5m)", "lighting", "Amazon", 899, "https://www.amazon.in/", ("lighting", "smart", "cove", "modern", "bedroom", "lights"), 4.5, "Bestseller"),
    Item("Crompton Solarium 15W Magnetic Track Spotlight", "lighting", "Amazon", 1650, "https://www.amazon.in/", ("lighting", "spotlight", "gallery", "living room", "lights"), 4.6),
    Item("Boho Bamboo Weave Hanging Chandelier Shade", "lighting", "Flipkart", 1299, "https://www.flipkart.com/", ("lighting", "boho", "living room", "balcony", "lights"), 4.5),

    # Ceiling Fans
    Item("Atomberg Renesa 1200mm BLDC Smart Fan with Remote", "fan", "Amazon", 3699, "https://www.amazon.in/", ("fan", "bldc", "smart", "bedroom", "living room", "energy saving"), 4.8, "5-Star Energy"),
    Item("Havells Ambrose 1200mm Decorative High-Speed Fan", "fan", "Flipkart", 2499, "https://www.flipkart.com/", ("fan", "decorative", "bedroom", "budget", "fans"), 4.5, "Popular"),
    Item("Orient Electric Aeroquiet Silent BLDC Ceiling Fan", "fan", "Amazon", 4299, "https://www.amazon.in/", ("fan", "silent", "luxury", "living room", "bldc"), 4.7, "Silent Tech"),
    Item("Crompton Hill Briz 1200mm Heavy-Duty Fan", "fan", "Amazon", 1599, "https://www.amazon.in/", ("fan", "budget", "utility", "kitchen", "fans"), 4.4, "Budget King"),

    # Dining & Living Furniture
    Item("IKEA MELLTORP / TEODORES 4-Seater Dining Set", "dining", "IKEA", 11990, "https://www.ikea.com/in/en/", ("dining", "dining table", "modern", "minimal", "kitchen"), 4.8, "Best Value"),
    Item("Solid Sheesham Wood 6-Seater Royal Dining Table & Chairs", "dining", "Amazon", 24999, "https://www.amazon.in/", ("dining", "dining table", "wood", "luxury", "traditional"), 4.7, "Solid Wood"),
    Item("Compact 2-Seater Foldable Dining & Breakfast Bar", "dining", "Flipkart", 4899, "https://www.flipkart.com/", ("dining", "dining table", "compact", "small space", "kitchen"), 4.3),
    Item("Wakefit Napper 3-Seater Comfort Fabric Sofa (Slate Grey)", "furniture", "Amazon", 14499, "https://www.amazon.in/", ("sofa", "furniture", "living room", "modern", "comfort"), 4.7, "Top Comfort"),
    Item("IKEA KALLAX Modular 4-Cube Shelving & Room Divider", "furniture", "IKEA", 4990, "https://www.ikea.com/in/en/", ("storage", "furniture", "living room", "bedroom", "shelving"), 4.8, "Versatile"),
    Item("IKEA LACK Minimalist Coffee Table (Black-Brown)", "furniture", "IKEA", 1499, "https://www.ikea.com/in/en/", ("table", "furniture", "living room", "minimal"), 4.6, "Budget Pick"),
    Item("Solimo Engineered Wood 2-Door Wardrobe with Full Mirror", "furniture", "Amazon", 8999, "https://www.amazon.in/", ("wardrobe", "storage", "furniture", "bedroom"), 4.5),
    Item("Solid Wood Bedside Nightstand Table with Dual Drawers", "furniture", "Flipkart", 2499, "https://www.flipkart.com/", ("bedside", "storage", "bedroom", "furniture"), 4.6),
    Item("Ergonomic High-Back Mesh Home Office Study Chair", "furniture", "Amazon", 5499, "https://www.amazon.in/", ("chair", "home office", "furniture", "ergonomic"), 4.7),

    # Decor & Soft Furnishings
    Item("Minimal Scandinavian Geometric Framed Canvas Wall Art (Set of 3)", "decor", "Amazon", 1299, "https://www.amazon.in/", ("decor", "wall art", "minimal", "living room", "scandinavian"), 4.7, "Trending"),
    Item("IKEA TIPHEDE Recycled Cotton Flatwoven Rug (120x180 cm)", "decor", "IKEA", 1290, "https://www.ikea.com/in/en/", ("rug", "decor", "living room", "bedroom", "sustainable"), 4.8, "Eco Choice"),
    Item("Blackout Thermal Insulated Eyelet Curtains (Set of 2)", "decor", "Amazon", 999, "https://www.amazon.in/", ("curtains", "decor", "bedroom", "living room"), 4.6),
    Item("Bohemian Macrame Woven Wall Hanging Tapestry", "decor", "Amazon", 799, "https://www.amazon.in/", ("decor", "boho", "living room", "balcony"), 4.5),
    Item("Full-Length Arched Aluminum Floor Standing Mirror (65x24 in)", "decor", "Flipkart", 3499, "https://www.flipkart.com/", ("mirror", "decor", "bedroom", "living room", "luxury"), 4.8),
    Item("Nordic Ceramic Indoor Planters with Matte Metal Stands (Trio)", "decor", "Amazon", 1199, "https://www.amazon.in/", ("planters", "decor", "balcony", "living room", "greenery"), 4.6),

    # ------------------ PARTY & EVENT PLANNING ------------------
    # Catering & Refreshments
    Item("Swiggy Gourmet Party Appetizer Box (Spring Rolls, Kebabs, Dimsums - 10 Pax)", "catering", "Swiggy", 1899, "https://www.swiggy.com/", ("catering", "food", "party", "snacks", "appetizers", "birthday"), 4.8, "Crowd Pleaser"),
    Item("Zomato Grand Biryani Celebration Feast with Kebabs & Desserts (15-20 Pax)", "catering", "Zomato", 4499, "https://www.zomato.com/", ("catering", "food", "party", "buffet", "wedding", "feast"), 4.9, "Best Value Feast"),
    Item("Swiggy Artisan Bakery Mini Dessert Box (Brownies, Cheesecakes - 16 Pcs)", "catering", "Swiggy", 1099, "https://www.swiggy.com/", ("catering", "dessert", "party", "birthday", "cocktail"), 4.7),
    Item("Zomato Royal Mughlai & North Indian Live Buffet Spread (25 Pax)", "catering", "Zomato", 8999, "https://www.zomato.com/", ("catering", "buffet", "wedding", "corporate", "food"), 4.8, "Deluxe Buffet"),
    Item("Haldiram's Deluxe Street Chaat & Crispy Savory Platter", "catering", "Swiggy", 1299, "https://www.swiggy.com/", ("catering", "food", "vegetarian", "snacks", "house party"), 4.6),
    Item("Blinkit Instant Party Mixers, Soda, Juices & Ice Bucket Kit (30 Pax)", "catering", "Blinkit", 1599, "https://www.blinkit.com/", ("catering", "beverages", "drinks", "party", "instant"), 4.8, "10-Min Delivery"),
    Item("Gourmet Wood-Fired Pizza & Pasta Party Combo (8-10 Pax)", "Zomato", "Zomato", 2999, "https://www.zomato.com/", ("catering", "food", "house party", "kids", "birthday"), 4.6),

    # Party Decoration
    Item("Rose Gold & Metallic Confetti Balloon Arch Garland DIY Kit (120 Pcs)", "decoration", "Amazon", 899, "https://www.amazon.in/", ("decoration", "balloon", "birthday", "anniversary", "party"), 4.7, "DIY Favorite"),
    Item("Warm White 300-LED Fairy Curtain Lights Backdrop (3x3 m)", "decoration", "Amazon", 699, "https://www.amazon.in/", ("decoration", "lights", "wedding", "backdrop", "party"), 4.8, "Top Aesthetic"),
    Item("Customizable LED Neon Signboard ('Happy Birthday' / 'Celebration')", "decoration", "Flipkart", 1899, "https://www.flipkart.com/", ("decoration", "neon", "party", "trendy", "corporate"), 4.9, "Glow Effect"),
    Item("Floral Marigold & Jasmine Festive Backdrop Strings (Pack of 12)", "decoration", "Amazon", 649, "https://www.amazon.in/", ("decoration", "floral", "wedding", "festive", "traditional"), 4.6),
    Item("Photo Booth Frame & 30-Piece Quirky Party Props Kit", "decoration", "Flipkart", 599, "https://www.flipkart.com/", ("decoration", "photobooth", "party", "games", "props"), 4.5),
    Item("Table Runner, Centerpiece Candle Lanterns & Confetti Set", "decoration", "Amazon", 1199, "https://www.amazon.in/", ("decoration", "table", "dinner", "anniversary", "elegant"), 4.7),

    # Venue & Stays
    Item("OYO Townhouse Banquet Hall & Rooftop Lounge (30-50 Guest Booking)", "accommodation", "OYO", 8500, "https://www.oyorooms.com/", ("venue", "accommodation", "hall", "party", "oyo", "corporate"), 4.7, "Prime Venue"),
    Item("OYO Flagship 3-Room Deluxe Block for Outstation Guests", "accommodation", "OYO", 4800, "https://www.oyorooms.com/", ("stay", "accommodation", "rooms", "wedding", "guests"), 4.5, "Stay Saver"),
    Item("Boutique Lawn & Covered Pavilion Party Space (Evening Slot)", "accommodation", "OYO", 16000, "https://www.oyorooms.com/", ("venue", "lawn", "wedding", "grand", "outdoor"), 4.8, "Spacious"),
    Item("Private Poolside Farmhouse Villa Day Pass (Up to 25 Guests)", "accommodation", "OYO", 12500, "https://www.oyorooms.com/", ("venue", "villa", "pool", "bachelor", "house party"), 4.9, "Exclusive"),

    # Entertainment & Sound
    Item("Party Rocker 100W Wireless Bluetooth Speaker with Dual Mic", "entertainment", "Amazon", 4499, "https://www.amazon.in/", ("entertainment", "sound", "karaoke", "music", "party"), 4.7, "Banging Bass"),
    Item("Strobe Stage RGB DJ Disco Party Light with Remote Control", "entertainment", "Flipkart", 1499, "https://www.flipkart.com/", ("entertainment", "lighting", "dj", "party", "dance"), 4.6),
    Item("Deluxe Icebreaker Board Games & Party Trivia Box", "entertainment", "Amazon", 799, "https://www.amazon.in/", ("entertainment", "games", "house party", "fun"), 4.5),

    # ------------------ JEWELRY RECOMMENDATIONS ------------------
    # Necklaces & Sets
    Item("Royal Kundan & Pearl Choker Necklace Set with Matching Chandbalis", "necklace", "Amazon", 2899, "https://www.amazon.in/", ("necklace", "kundan", "wedding", "festive", "traditional", "gold"), 4.8, "Bridal Classic"),
    Item("South Indian Matte Temple Coin Necklace with Divine Motif", "necklace", "Flipkart", 1999, "https://www.flipkart.com/", ("necklace", "temple", "traditional", "festive", "gold"), 4.7, "Temple Heritage"),
    Item("CaratLane 18K Yellow Gold Delicate Clover Diamond Pendant Chain", "necklace", "Amazon", 18500, "https://www.amazon.in/", ("necklace", "diamond", "gold", "minimal", "cocktail", "luxury"), 4.9, "Fine Gold"),
    Item("Zirconia Crystal Teardrop Solitaire Statement Collar Choker", "necklace", "Amazon", 1499, "https://www.amazon.in/", ("necklace", "diamond", "crystal", "cocktail", "western", "silver"), 4.6, "Sparkle Chic"),
    Item("Oxidized German Silver Bohemian Choker with Vintage Coins", "necklace", "Flipkart", 799, "https://www.flipkart.com/", ("necklace", "silver", "boho", "oxidized", "daily", "festive"), 4.5, "Boho Vibe"),
    Item("Tanishq Mia 14K Rose Gold Floral Elegance Dainty Necklace", "necklace", "Amazon", 14200, "https://www.amazon.in/", ("necklace", "rose gold", "office", "minimal", "modern"), 4.9, "Tanishq Certified"),
    Item("Emerald Green Jadau Polki Bridal Heritage Necklace Set", "necklace", "Flipkart", 4499, "https://www.flipkart.com/", ("necklace", "polki", "emerald", "wedding", "green", "royal"), 4.8, "Showstopper"),

    # Earrings
    Item("Oversized Kundan Chandbali Dangler Earrings with Cluster Pearls", "earrings", "Amazon", 1199, "https://www.amazon.in/", ("earrings", "kundan", "wedding", "festive", "statement"), 4.7, "Top Dangler"),
    Item("GIVA 925 Sterling Silver Classic Solitaire Stud Earrings", "earrings", "Amazon", 1599, "https://www.amazon.in/", ("earrings", "silver", "solitaire", "minimal", "office", "daily"), 4.9, "Pure 925"),
    Item("Traditional Enamelled Meenakari Peacock Jhumkas", "earrings", "Flipkart", 749, "https://www.flipkart.com/", ("earrings", "jhumka", "meenakari", "festive", "traditional"), 4.6),
    Item("Rose Gold American Diamond Chandelier Cocktail Earrings", "earrings", "Amazon", 1350, "https://www.amazon.in/", ("earrings", "rose gold", "diamond", "cocktail", "party"), 4.8),
    Item("Tribal Oxidized Silver Jhumkas with Mirror Accents", "earrings", "Flipkart", 499, "https://www.flipkart.com/", ("earrings", "oxidized", "silver", "boho", "budget"), 4.5, "Budget Style"),
    Item("Freshwater Cultured Pearl Drop Huggie Hoops", "earrings", "Flipkart", 899, "https://www.flipkart.com/", ("earrings", "pearl", "minimal", "office", "elegant"), 4.7),

    # Bangles & Bracelets
    Item("Kundan Enamelled Royal Openable Kada Bangles (Set of 2)", "bracelet", "Amazon", 1699, "https://www.amazon.in/", ("bracelet", "bangles", "kundan", "wedding", "gold"), 4.7, "Royal Touch"),
    Item("GIVA 925 Sterling Silver Adjustable Tennis Bracelet with Sparkling Zircons", "bracelet", "Amazon", 2499, "https://www.amazon.in/", ("bracelet", "silver", "tennis", "diamond", "cocktail"), 4.9, "Timeless"),
    Item("Traditional Gold-Plated Intricate Filigree Broad Bangles (Set of 4)", "bracelet", "Flipkart", 1299, "https://www.flipkart.com/", ("bracelet", "bangles", "gold", "traditional", "festive"), 4.5),
    Item("Bohemian Silver Stackable Carved Bangle Set (Pack of 6)", "bracelet", "Flipkart", 649, "https://www.flipkart.com/", ("bracelet", "bangles", "oxidized", "silver", "boho"), 4.6),
    Item("Rose Gold Charm Bangle Cuff with Micro-Pave Crystals", "bracelet", "Amazon", 999, "https://www.amazon.in/", ("bracelet", "rose gold", "cuff", "modern", "party"), 4.6),

    # Rings & Accessories
    Item("Adjustable Polki Emerald Centerpiece Statement Cocktail Ring", "rings", "Amazon", 749, "https://www.amazon.in/", ("rings", "polki", "cocktail", "wedding", "emerald"), 4.7),
    Item("GIVA 925 Silver Princess Crown Solitaire Ring", "rings", "Flipkart", 1199, "https://www.flipkart.com/", ("rings", "silver", "crown", "solitaire", "gift"), 4.8),
    Item("Kundan & Pearl Matha Patti / Maang Tikka Traditional Set", "accessories", "Amazon", 899, "https://www.amazon.in/", ("maangtikka", "accessories", "kundan", "wedding", "traditional"), 4.7)
]

def search_catalog(domain: str, budget: float, tags: List[str], limit: int = 8) -> List[Dict[str, Any]]:
    """
    Search catalog with domain restrictions and intelligent multi-attribute scoring:
    - Tag keyword matching
    - Price budget appropriateness
    - Platform diversity
    """
    domain_map = {
        "home": {"lighting", "fan", "dining", "decor", "furniture"},
        "party": {"catering", "decoration", "accommodation", "entertainment"},
        "jewelry": {"necklace", "earrings", "bracelet", "rings", "accessories"}
    }
    allowed = domain_map.get(domain, set())
    
    # Process requested tags
    clean_tags = [str(t).lower().strip() for t in tags if t]
    
    scored: List[tuple[float, Item]] = []
    
    for item in CATALOG:
        if item.category not in allowed:
            continue
            
        score = 0.0
        item_tag_set = {t.lower() for t in item.tags}
        
        # Keyword relevance
        for ct in clean_tags:
            if ct in item_tag_set:
                score += 3.0
            elif any(ct in t or t in ct for t in item_tag_set):
                score += 1.5
            if ct in item.name.lower():
                score += 2.5
                
        # Price suitability: reward items within budget
        if item.price <= budget:
            score += 2.0
            # Higher score for items that represent meaningful value
            ratio = item.price / max(budget, 1.0)
            if 0.05 <= ratio <= 0.70:
                score += 1.5
        else:
            # Over budget penalty
            score -= 3.0
            
        # Rating boost
        score += (item.rating - 4.0) * 2.0
        
        scored.append((score, item))
        
    # Sort descending by score
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Ensure variety of platforms and categories
    selected: List[Item] = []
    seen_categories: set[str] = set()
    
    for _, item in scored:
        if len(selected) >= limit:
            break
        # Give preference to category diversity in first pass
        if item.category not in seen_categories or len(selected) >= 4:
            selected.append(item)
            seen_categories.add(item.category)
            
    # If still need items to reach limit, backfill
    if len(selected) < limit:
        for _, item in scored:
            if item not in selected:
                selected.append(item)
                if len(selected) >= limit:
                    break

    return [
        {
            "name": i.name,
            "category": i.category,
            "platform": i.platform,
            "estimated_price": i.price,
            "currency": "INR",
            "url": i.url,
            "tags": list(i.tags),
            "rating": i.rating,
            "badge": i.badge
        }
        for i in selected
    ]
