import uvicorn
import json
import re
import random
from typing import List, Dict, Any
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from faster_whisper import WhisperModel
import torch

# --- FASTAPI APP ---
app = FastAPI(
    title="Whisper-to-Recipe API",
    description="Converts voice notes about ingredients into recipes with sustainability scores.",
)

# Allow requests from the React frontend (default port 3000)
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Voice-to-Recipe API is running"}

# --- CONFIG & DATA LOADING ---
# Load data into memory for fast lookups
with open('carbon_db.json', 'r') as f:
    CARBON_DB = json.load(f)
with open('nutrition_db.json', 'r') as f:
    NUTRITION_DB = json.load(f) # Assume this has avg calories per 100g
with open('ingredient_map.json', 'r') as f:
    INGREDIENT_MAP = json.load(f)

# --- MODEL LOADING ---
# Load models on startup, not on every request
# Speech-to-Text
whisper_model = WhisperModel("small", device="cuda" if torch.cuda.is_available() else "cpu", compute_type="int8")

def extract_ingredients_advanced(text: str) -> List[str]:
    """Advanced ingredient extraction using keyword matching and fuzzy search."""
    text = text.lower()
    ingredients = set()
    
    # First, try exact matches in ingredient map
    for key, value in INGREDIENT_MAP.items():
        if key in text:
            ingredients.add(value)
    
    # Then try direct matches in carbon database
    for ingredient in CARBON_DB.keys():
        if ingredient in text:
            ingredients.add(ingredient)
    
    # Try partial matches for common ingredients
    words = re.findall(r'\b\w+\b', text)
    for word in words:
        if len(word) > 3:  # Skip very short words
            for ingredient in CARBON_DB.keys():
                if word in ingredient or ingredient in word:
                    ingredients.add(ingredient)
    
    return list(ingredients)

def generate_recipe_advanced(ingredients: List[str]) -> Dict[str, Any]:
    """Generate a more sophisticated recipe based on ingredients."""
    
    # Recipe templates based on ingredient types
    meat_ingredients = [ing for ing in ingredients if any(meat in ing for meat in ['chicken', 'beef', 'pork', 'lamb', 'fish', 'salmon', 'tuna'])]
    vegetable_ingredients = [ing for ing in ingredients if any(veg in ing for veg in ['tomato', 'onion', 'garlic', 'carrot', 'broccoli', 'spinach', 'lettuce', 'cucumber', 'pepper', 'mushroom', 'potato'])]
    grain_ingredients = [ing for ing in ingredients if any(grain in ing for grain in ['rice', 'pasta', 'bread', 'quinoa', 'oats'])]
    dairy_ingredients = [ing for ing in ingredients if any(dairy in ing for dairy in ['milk', 'cheese', 'yogurt', 'butter', 'eggs'])]
    spice_ingredients = [ing for ing in ingredients if any(spice in ing for spice in ['curry', 'paprika', 'cumin', 'cinnamon', 'ginger', 'turmeric', 'basil', 'oregano', 'thyme', 'rosemary', 'parsley', 'cilantro'])]
    
    # Determine recipe type
    if meat_ingredients and vegetable_ingredients:
        recipe_type = "stir_fry"
    elif meat_ingredients and grain_ingredients:
        recipe_type = "main_dish"
    elif vegetable_ingredients and grain_ingredients:
        recipe_type = "vegetarian"
    elif dairy_ingredients and grain_ingredients:
        recipe_type = "breakfast"
    else:
        recipe_type = "simple"
    
    # Generate recipe based on type
    if recipe_type == "stir_fry":
        title = f"Healthy {meat_ingredients[0].title()} Stir Fry"
        instructions = [
            f"1. Heat 2 tablespoons of oil in a large pan or wok over medium-high heat.",
            f"2. Add {meat_ingredients[0]} and cook for 4-5 minutes until golden brown.",
            f"3. Add {', '.join(vegetable_ingredients[:2])} and cook for 3-4 minutes until tender-crisp.",
            f"4. Season with {', '.join(spice_ingredients[:2]) if spice_ingredients else 'salt and pepper'}.",
            "5. Serve hot over rice or noodles."
        ]
    elif recipe_type == "main_dish":
        title = f"Savory {meat_ingredients[0].title()} with {grain_ingredients[0].title()}"
        instructions = [
            f"1. Season {meat_ingredients[0]} with {', '.join(spice_ingredients[:2]) if spice_ingredients else 'salt and pepper'}.",
            f"2. Cook {meat_ingredients[0]} in a pan over medium heat for 6-8 minutes per side.",
            f"3. Meanwhile, prepare {grain_ingredients[0]} according to package instructions.",
            f"4. Add {', '.join(vegetable_ingredients[:2]) if vegetable_ingredients else 'your favorite vegetables'} to the pan and cook until tender.",
            "5. Serve the meat over the grain with vegetables on the side."
        ]
    elif recipe_type == "vegetarian":
        title = f"Nutritious {vegetable_ingredients[0].title()} Bowl"
        instructions = [
            f"1. Cook {grain_ingredients[0]} according to package instructions.",
            f"2. Sauté {', '.join(vegetable_ingredients[:3])} in olive oil until tender.",
            f"3. Season with {', '.join(spice_ingredients[:2]) if spice_ingredients else 'salt, pepper, and herbs'}.",
            f"4. Add {', '.join(dairy_ingredients[:1]) if dairy_ingredients else 'your favorite protein source'} for extra nutrition.",
            "5. Serve in bowls and enjoy!"
        ]
    elif recipe_type == "breakfast":
        title = f"Energizing {dairy_ingredients[0].title()} Breakfast"
        instructions = [
            f"1. Heat a non-stick pan over medium heat.",
            f"2. Whisk together {dairy_ingredients[0]} and eggs in a bowl.",
            f"3. Add {grain_ingredients[0]} and mix well.",
            f"4. Cook the mixture in the pan for 3-4 minutes per side.",
            f"5. Serve with {', '.join(vegetable_ingredients[:1]) if vegetable_ingredients else 'fresh fruit'} on the side."
        ]
    else:
        title = f"Simple {ingredients[0].title()} Recipe"
        instructions = [
            f"1. Prepare {', '.join(ingredients[:3])} by washing and cutting as needed.",
            f"2. Heat oil in a pan and add the ingredients.",
            f"3. Season with {', '.join(spice_ingredients[:2]) if spice_ingredients else 'salt and pepper'}.",
            "4. Cook until everything is tender and well combined.",
            "5. Serve immediately and enjoy your sustainable meal!"
        ]
    
    return {
        "title": title,
        "instructions": instructions,
        "cooking_time": f"{random.randint(15, 45)} minutes",
        "servings": random.randint(2, 6),
        "difficulty": random.choice(["Easy", "Medium", "Intermediate"])
    }



@app.post("/process-voice")
async def process_voice(file: UploadFile = File(...)):
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="Please upload an audio file")
        
        # 1. Speech-to-Text
        segments, _ = whisper_model.transcribe(file.file, beam_size=5)
        full_text = "".join(segment.text for segment in segments).strip()
        
        if not full_text:
            raise HTTPException(status_code=400, detail="No speech detected in the audio file")

        # 2. Advanced Ingredient Extraction
        ingredients = extract_ingredients_advanced(full_text)
        if not ingredients:
            raise HTTPException(status_code=400, detail="No recognizable ingredients found in the audio. Please try mentioning specific ingredients like 'chicken', 'tomatoes', 'rice', etc.")

        # 3. Data Lookup & Scoring
        total_calories = 0
        total_carbon = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        avg_recipe_carbon = 5.0  # kg CO2/kg - example average

        for ing in ingredients:
            if ing in NUTRITION_DB:
                # Simplified: assume 100g serving for nutrition calculation
                nutrition = NUTRITION_DB[ing]
                total_calories += nutrition.get('calories_per_100g', 0)
                total_protein += nutrition.get('protein', 0)
                total_carbs += nutrition.get('carbs', 0)
                total_fat += nutrition.get('fat', 0)
            if ing in CARBON_DB:
                total_carbon += CARBON_DB[ing]['co2_kg_per_kg'] / 10  # Assume 100g serving

        # 4. Advanced Recipe Generation
        recipe = generate_recipe_advanced(ingredients)

        # 5. Calculate sustainability metrics
        carbon_score = round(total_carbon, 3)
        carbon_saved = max(0, round(avg_recipe_carbon - total_carbon, 3))
        
        # Calculate sustainability rating
        if carbon_score < 1.0:
            sustainability_rating = "Excellent"
        elif carbon_score < 2.0:
            sustainability_rating = "Good"
        elif carbon_score < 3.0:
            sustainability_rating = "Fair"
        else:
            sustainability_rating = "Needs Improvement"

        return {
            "original_text": full_text,
            "extracted_ingredients": ingredients,
            "recipe": recipe,
            "sustainability": {
                "total_carbon_kg_co2": carbon_score,
                "average_recipe_carbon_kg_co2": avg_recipe_carbon,
                "carbon_saved_kg_co2": carbon_saved,
                "sustainability_rating": sustainability_rating,
                "nutrition": {
                    "total_calories": round(total_calories, 1),
                    "protein_g": round(total_protein, 1),
                    "carbs_g": round(total_carbs, 1),
                    "fat_g": round(total_fat, 1)
                }
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)