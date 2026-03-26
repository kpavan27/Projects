#!/usr/bin/env python3
"""
Demo script for Voice-to-Recipe application
This script demonstrates the core functionality without requiring audio input
"""

import json
from main import extract_ingredients_advanced, generate_recipe_advanced, CARBON_DB, NUTRITION_DB

def demo_ingredient_extraction():
    """Demonstrate ingredient extraction with various text inputs"""
    print("🎤 DEMO: Ingredient Extraction")
    print("=" * 40)
    
    demo_texts = [
        "I have chicken breast, tomatoes, and rice for dinner",
        "I need beef, onions, garlic, and pasta to make spaghetti",
        "I want to cook salmon with broccoli and quinoa",
        "I have eggs, milk, and bread for breakfast",
        "I need chicken, curry powder, and rice for curry",
        "I have tofu, spinach, and brown rice for a healthy meal"
    ]
    
    for i, text in enumerate(demo_texts, 1):
        print(f"\n{i}. Text: '{text}'")
        ingredients = extract_ingredients_advanced(text)
        print(f"   Extracted ingredients: {ingredients}")
        
        # Show carbon footprint for detected ingredients
        if ingredients:
            total_carbon = 0
            for ing in ingredients:
                if ing in CARBON_DB:
                    carbon = CARBON_DB[ing]['co2_kg_per_kg'] / 10  # Assume 100g serving
                    total_carbon += carbon
                    print(f"   - {ing}: {carbon:.3f} kg CO₂")
            print(f"   Total carbon footprint: {total_carbon:.3f} kg CO₂")

def demo_recipe_generation():
    """Demonstrate recipe generation with different ingredient combinations"""
    print("\n\n🍽️ DEMO: Recipe Generation")
    print("=" * 40)
    
    demo_ingredients = [
        ["chicken", "tomato", "rice", "garlic"],
        ["beef", "onion", "pasta", "basil"],
        ["salmon", "broccoli", "quinoa", "lemon"],
        ["egg", "milk", "bread", "butter"],
        ["tofu", "spinach", "rice", "ginger"],
        ["chicken", "curry powder", "rice", "onion"]
    ]
    
    for i, ingredients in enumerate(demo_ingredients, 1):
        print(f"\n{i}. Ingredients: {ingredients}")
        recipe = generate_recipe_advanced(ingredients)
        
        print(f"   Recipe: {recipe['title']}")
        print(f"   Cooking time: {recipe['cooking_time']}")
        print(f"   Servings: {recipe['servings']}")
        print(f"   Difficulty: {recipe['difficulty']}")
        print("   Instructions:")
        for j, instruction in enumerate(recipe['instructions'], 1):
            print(f"     {j}. {instruction}")

def demo_sustainability_analysis():
    """Demonstrate sustainability analysis"""
    print("\n\n🌱 DEMO: Sustainability Analysis")
    print("=" * 40)
    
    sample_ingredients = ["chicken", "tomato", "rice", "garlic"]
    
    print(f"Analyzing ingredients: {sample_ingredients}")
    
    total_calories = 0
    total_carbon = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    
    print("\nNutritional Analysis:")
    print("-" * 25)
    
    for ing in sample_ingredients:
        if ing in NUTRITION_DB:
            nutrition = NUTRITION_DB[ing]
            calories = nutrition.get('calories_per_100g', 0)
            protein = nutrition.get('protein', 0)
            carbs = nutrition.get('carbs', 0)
            fat = nutrition.get('fat', 0)
            
            total_calories += calories
            total_protein += protein
            total_carbs += carbs
            total_fat += fat
            
            print(f"{ing.title():12} | Calories: {calories:3.0f} | Protein: {protein:2.0f}g | Carbs: {carbs:2.0f}g | Fat: {fat:2.0f}g")
    
    print("-" * 25)
    print(f"{'TOTAL':12} | Calories: {total_calories:3.0f} | Protein: {total_protein:2.0f}g | Carbs: {total_carbs:2.0f}g | Fat: {total_fat:2.0f}g")
    
    print("\nCarbon Footprint Analysis:")
    print("-" * 30)
    
    for ing in sample_ingredients:
        if ing in CARBON_DB:
            carbon = CARBON_DB[ing]['co2_kg_per_kg'] / 10  # Assume 100g serving
            total_carbon += carbon
            print(f"{ing.title():12} | {carbon:.3f} kg CO₂")
    
    print("-" * 30)
    print(f"{'TOTAL':12} | {total_carbon:.3f} kg CO₂")
    
    # Calculate sustainability rating
    if total_carbon < 1.0:
        rating = "Excellent"
    elif total_carbon < 2.0:
        rating = "Good"
    elif total_carbon < 3.0:
        rating = "Fair"
    else:
        rating = "Needs Improvement"
    
    print(f"\nSustainability Rating: {rating}")

def main():
    """Run the complete demo"""
    print("🍳 Voice-to-Recipe Application Demo")
    print("===================================")
    print("This demo shows the core functionality without requiring audio input.")
    print("In the real application, you would record your voice and the system")
    print("would process it to extract ingredients and generate recipes.\n")
    
    try:
        demo_ingredient_extraction()
        demo_recipe_generation()
        demo_sustainability_analysis()
        
        print("\n\n🎉 Demo completed successfully!")
        print("The application is ready to use with voice input.")
        print("\nTo start the full application:")
        print("1. Run: python main.py (for backend)")
        print("2. Run: cd frontend && npm start (for frontend)")
        print("3. Or run: ./start_app.sh (for both)")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("Make sure all dependencies are installed and databases are loaded.")

if __name__ == "__main__":
    main()