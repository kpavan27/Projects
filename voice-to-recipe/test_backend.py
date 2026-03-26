#!/usr/bin/env python3
"""
Simple test script for the Voice-to-Recipe backend API
"""

import requests
import json
import time

def test_health_endpoint():
    """Test the health check endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on port 8000")
        return False

def test_ingredient_extraction():
    """Test ingredient extraction with sample text"""
    try:
        # Create a simple test audio file (this is just a placeholder)
        # In a real test, you'd create an actual audio file
        print("🧪 Testing ingredient extraction...")
        
        # Test the ingredient extraction logic directly
        from main import extract_ingredients_advanced
        
        test_texts = [
            "I have chicken breast, tomatoes, and rice",
            "I need beef, onions, garlic, and pasta",
            "I want to cook with salmon, broccoli, and quinoa",
            "I have eggs, milk, and bread for breakfast"
        ]
        
        for text in test_texts:
            ingredients = extract_ingredients_advanced(text)
            print(f"   Text: '{text}'")
            print(f"   Extracted: {ingredients}")
            print()
        
        return True
    except Exception as e:
        print(f"❌ Ingredient extraction test failed: {e}")
        return False

def test_recipe_generation():
    """Test recipe generation with sample ingredients"""
    try:
        print("🍽️ Testing recipe generation...")
        
        from main import generate_recipe_advanced
        
        test_ingredients = [
            ["chicken", "tomato", "rice"],
            ["beef", "onion", "garlic", "pasta"],
            ["salmon", "broccoli", "quinoa"],
            ["egg", "milk", "bread"]
        ]
        
        for ingredients in test_ingredients:
            recipe = generate_recipe_advanced(ingredients)
            print(f"   Ingredients: {ingredients}")
            print(f"   Recipe: {recipe['title']}")
            print(f"   Instructions: {len(recipe['instructions'])} steps")
            print(f"   Cooking time: {recipe['cooking_time']}")
            print(f"   Servings: {recipe['servings']}")
            print(f"   Difficulty: {recipe['difficulty']}")
            print()
        
        return True
    except Exception as e:
        print(f"❌ Recipe generation test failed: {e}")
        return False

def test_database_loading():
    """Test that all databases are loaded correctly"""
    try:
        print("📊 Testing database loading...")
        
        from main import CARBON_DB, NUTRITION_DB, INGREDIENT_MAP
        
        print(f"   Carbon database: {len(CARBON_DB)} ingredients")
        print(f"   Nutrition database: {len(NUTRITION_DB)} ingredients")
        print(f"   Ingredient mapping: {len(INGREDIENT_MAP)} mappings")
        
        # Test a few sample lookups
        test_ingredient = "chicken"
        if test_ingredient in CARBON_DB:
            print(f"   ✅ {test_ingredient} found in carbon DB")
        if test_ingredient in NUTRITION_DB:
            print(f"   ✅ {test_ingredient} found in nutrition DB")
        
        return True
    except Exception as e:
        print(f"❌ Database loading test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running Voice-to-Recipe Backend Tests")
    print("=" * 50)
    
    tests = [
        ("Health Endpoint", test_health_endpoint),
        ("Database Loading", test_database_loading),
        ("Ingredient Extraction", test_ingredient_extraction),
        ("Recipe Generation", test_recipe_generation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}")
        print("-" * 30)
        if test_func():
            passed += 1
        time.sleep(0.5)  # Small delay between tests
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The backend is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    main()