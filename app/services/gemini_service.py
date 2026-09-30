import json
import logging
from io import BytesIO
from typing import Optional, Dict, Any, List
from PIL import Image
from google import genai
from google.genai import types
from app.config import get_settings
from app.models.schemas import RecommendationResponse

settings = get_settings()
log = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key) if settings.gemini_api_key else None

    def generate(
        self,
        planner: str,
        payload: Dict[str, Any],
        catalog: List[Dict[str, Any]],
        image_bytes: Optional[bytes] = None
    ) -> Optional[Dict[str, Any]]:
        if not self.client or not settings.gemini_api_key:
            return None

        # Build tailored domain prompt
        domain_instructions = {
            "home": (
                "You are an expert AI interior designer and smart home budgeting consultant. "
                "Analyze the user's budget, requested rooms, and specified item quantities (e.g., lights, ceiling fans, dining tables). "
                "Recommend cost-effective, high-quality options from platforms like IKEA, Amazon, and Flipkart. "
                "Balance functionality, style, and price to create a harmonious space without overspending. "
                "Provide a realistic proportional budget allocation across Furniture, Lighting, Utility/Appliances, and Buffer."
            ),
            "party": (
                "You are a premier AI event planner and party budgeting strategist. "
                "Analyze the user's total budget, guest count, event type, venue, city, and preferences. "
                "Proportionally allocate the budget across Catering, Decoration, Venue/Accommodation, Entertainment, and Contingency Buffer. "
                "Source and curate options from platforms like Swiggy, Zomato, OYO, Amazon, and Blinkit. "
                "Highlight cost-per-guest efficiency and actionable event-hosting tips."
            ),
            "jewelry": (
                "You are a luxury jewelry stylist and gemology consultant. "
                "Analyze the user's budget, occasion, style preference, and metal tone. "
                "If an outfit image or description is provided, carefully examine the color harmony, aesthetic, and silhouette. "
                "Curate matching jewelry options (necklace, earrings, bangles, rings) from platforms like Amazon, Flipkart, Tanishq, CaratLane, and GIVA. "
                "Ensure the selected pieces elevate the outfit within the user's defined budget."
            )
        }

        system_instruction = domain_instructions.get(planner, "You are PocketSmart AI, a budget-aware recommendation assistant.")
        
        prompt = f"""
{system_instruction}

PLANNER CATEGORY: {planner}
USER REQUEST:
{json.dumps(payload, indent=2, ensure_ascii=False)}

CANDIDATE PRODUCT CATALOG (Use items and links from here or close equivalents):
{json.dumps(catalog, indent=2, ensure_ascii=False)}

TASK:
1. Generate a personalized summary of the plan.
2. Provide proportional budget allocations (categories, rupee amounts, and percentages that sum up to 100%).
3. Curate recommended items strictly adhering to or within the user's budget. Explain why each item is chosen and how it fits the requested style, quantities, or occasion.
4. Give 3-4 insightful budgeting or styling tips.
5. In the disclaimer, clearly note that prices, availability, and marketplace entries are estimates for planning and should be verified before purchase.

Return JSON strictly matching the response schema.
"""
        # List of candidate models to try in case of transient spikes
        candidate_models = [settings.gemini_model]
        for m in ["gemini-3.5-flash-lite", "gemini-2.5-flash-lite", "gemini-flash-latest"]:
            if m not in candidate_models:
                candidate_models.append(m)

        for model_name in candidate_models:
            try:
                contents = [prompt]
                if image_bytes:
                    try:
                        pil_img = Image.open(BytesIO(image_bytes))
                        contents.append(pil_img)
                        contents.append("Outfit Image provided by the user. Coordinate jewelry colors, metals, and formality with this visual.")
                    except Exception as img_err:
                        log.warning("Could not parse image for Gemini: %s", img_err)

                r = self.client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=RecommendationResponse,
                        temperature=0.3,
                        max_output_tokens=4096
                    )
                )

                if r and r.text:
                    data = RecommendationResponse.model_validate_json(r.text).model_dump()
                    data["source_mode"] = "gemini"
                    return data
            except Exception as e:
                log.warning("Gemini model %s encountered error: %s. Trying fallback model if available.", model_name, e)
                continue

        return None

gemini_service = GeminiService()
