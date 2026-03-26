# 🍳 Voice-to-Recipe Generator

An AI-powered application that converts voice notes about ingredients into sustainable recipes with carbon footprint analysis and nutritional information.

## ✨ Features

- **🎤 Voice Input**: Record your ingredients using your microphone
- **🤖 AI Processing**: Advanced speech-to-text and ingredient extraction
- **🍽️ Recipe Generation**: Intelligent recipe creation based on available ingredients
- **🌱 Sustainability Scoring**: Carbon footprint analysis and environmental impact
- **📊 Nutrition Analysis**: Detailed nutritional breakdown (calories, protein, carbs, fat)
- **🎨 Beautiful UI**: Modern, responsive interface with smooth animations
- **📱 Mobile Friendly**: Works perfectly on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- Microphone access for voice recording

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the FastAPI server:**
   ```bash
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the React development server:**
   ```bash
   npm start
   ```
   
   The app will open at `http://localhost:3000`

## 🎯 How to Use

1. **Open the application** in your web browser
2. **Click "Start Recording"** and speak your ingredients (e.g., "I have chicken, tomatoes, rice, and garlic")
3. **Click "Stop Recording"** when finished
4. **Click "Generate Recipe"** to process your voice and create a recipe
5. **View your recipe** with sustainability metrics and cooking instructions

## 🛠️ Technical Architecture

### Backend (Python/FastAPI)
- **Speech-to-Text**: OpenAI Whisper model for accurate transcription
- **Ingredient Extraction**: Advanced keyword matching and fuzzy search
- **Recipe Generation**: Intelligent recipe templates based on ingredient types
- **Sustainability Analysis**: Carbon footprint calculation using comprehensive databases
- **Nutrition Analysis**: Detailed nutritional information per ingredient

### Frontend (React)
- **Voice Recording**: Browser MediaRecorder API
- **Real-time UI**: Dynamic updates with loading states and error handling
- **Responsive Design**: Mobile-first approach with beautiful animations
- **Accessibility**: Keyboard navigation and screen reader support

### Data Sources
- **Carbon Database**: CO₂ emissions data for 70+ ingredients
- **Nutrition Database**: Comprehensive nutritional information
- **Ingredient Mapping**: 150+ ingredient variations and synonyms

## 📊 Supported Ingredients

The application recognizes a wide variety of ingredients including:

- **Proteins**: Chicken, beef, pork, fish, eggs, tofu, beans, lentils
- **Vegetables**: Tomatoes, onions, garlic, carrots, broccoli, spinach, peppers
- **Grains**: Rice, pasta, bread, quinoa, oats
- **Dairy**: Milk, cheese, yogurt, butter
- **Fruits**: Apples, bananas, oranges, berries, avocados
- **Spices**: Curry, paprika, cumin, cinnamon, ginger, herbs
- **Oils**: Olive oil, coconut oil, vegetable oil

## 🌱 Sustainability Features

- **Carbon Footprint Analysis**: Real-time CO₂ emissions calculation
- **Sustainability Rating**: Easy-to-understand environmental impact scores
- **Carbon Savings**: Comparison with average recipe emissions
- **Eco-friendly Suggestions**: Recommendations for sustainable cooking

## 🔧 Configuration

### Backend Configuration
- Modify `main.py` to adjust API settings
- Update database files (`carbon_db.json`, `nutrition_db.json`, `ingredient_map.json`)
- Configure CORS origins for different environments

### Frontend Configuration
- Update API endpoint in `frontend/src/App.js` if needed
- Modify styling in `frontend/src/App.css`
- Configure build settings in `frontend/package.json`

## 🐛 Troubleshooting

### Common Issues

1. **Microphone not working**: Check browser permissions and try refreshing
2. **API connection failed**: Ensure backend is running on port 8000
3. **No ingredients detected**: Try speaking more clearly and using common ingredient names
4. **Slow processing**: This is normal for the first request as models load

### Error Messages

- **"No speech detected"**: Speak louder or check microphone
- **"No ingredients found"**: Try using more specific ingredient names
- **"Request timed out"**: Check your internet connection and try again

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI Whisper for speech recognition
- FastAPI for the backend framework
- React for the frontend framework
- Poore & Nemecek for carbon footprint data
- USDA for nutritional information

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Recipe difficulty adjustment
- [ ] Ingredient substitution suggestions
- [ ] Cooking time optimization
- [ ] Dietary restriction filtering
- [ ] Recipe sharing and saving
- [ ] Voice command shortcuts
- [ ] Integration with smart kitchen devices

---

**Built with ❤️ for sustainable cooking | Powered by AI**