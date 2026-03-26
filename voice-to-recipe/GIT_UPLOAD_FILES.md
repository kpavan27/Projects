# Voice-to-Recipe Project - Git Upload File List

This document lists all the necessary files and directories that should be included when uploading this voice-to-recipe project to Git.

## 📁 Project Structure Overview

```
voice-to-recipe/
├── Backend (FastAPI)
├── Frontend (React)
├── Data Files
├── Configuration Files
└── Documentation
```

## 🚀 **Backend Files (Python/FastAPI)**

### Core Application Files
- `main.py` - Main FastAPI application with voice processing endpoints
- `demo.py` - Demo/testing script
- `test_backend.py` - Backend testing script

### Configuration & Dependencies
- `requirements.txt` - Python dependencies
- `start_app.sh` - Application startup script

### Data Files
- `carbon_db.json` - Carbon footprint database for ingredients
- `nutrition_db.json` - Nutritional information database
- `ingredient_map.json` - Ingredient mapping for text processing

## 🎨 **Frontend Files (React)**

### Core React Files
- `frontend/package.json` - Node.js dependencies and scripts
- `frontend/package-lock.json` - Locked dependency versions

### Source Code
- `frontend/src/App.js` - Main React application component
- `frontend/src/App.css` - Main application styles
- `frontend/src/App.test.js` - App component tests
- `frontend/src/index.js` - React application entry point
- `frontend/src/index.css` - Global styles
- `frontend/src/logo.svg` - React logo
- `frontend/src/reportWebVitals.js` - Web vitals reporting
- `frontend/src/setupTests.js` - Test setup configuration

### Public Assets
- `frontend/public/index.html` - Main HTML template
- `frontend/public/favicon.ico` - Website favicon
- `frontend/public/logo192.png` - 192px logo
- `frontend/public/logo512.png` - 512px logo
- `frontend/public/manifest.json` - Web app manifest
- `frontend/public/robots.txt` - Search engine directives

## 📚 **Documentation Files**

- `README.md` - Project documentation and setup instructions
- `frontend/README.md` - Frontend-specific documentation

## 🚫 **Files to EXCLUDE (handled by .gitignore)**

### Python Cache & Build Files
- `__pycache__/` - Python bytecode cache
- `*.pyc` - Compiled Python files
- `*.pyo` - Optimized Python files
- `build/` - Build directories
- `dist/` - Distribution directories

### Node.js Dependencies
- `frontend/node_modules/` - Node.js dependencies (will be installed via npm)

### Environment & Config Files
- `.env` - Environment variables
- `.env.local` - Local environment variables
- `.env.production` - Production environment variables

### IDE & OS Files
- `.vscode/` - VS Code settings
- `.idea/` - IntelliJ/WebStorm settings
- `.DS_Store` - macOS system files
- `Thumbs.db` - Windows system files

### Logs & Temporary Files
- `*.log` - Log files
- `logs/` - Log directories
- `tmp/` - Temporary files
- `temp/` - Temporary files

### Model Files (if large)
- `*.bin` - Large binary model files
- `*.safetensors` - SafeTensors model files
- `models/` - Model directories

## 📋 **Git Upload Checklist**

### ✅ **Required Files to Include:**

#### Backend
- [ ] `main.py`
- [ ] `demo.py`
- [ ] `test_backend.py`
- [ ] `requirements.txt`
- [ ] `start_app.sh`

#### Data Files
- [ ] `carbon_db.json`
- [ ] `nutrition_db.json`
- [ ] `ingredient_map.json`

#### Frontend
- [ ] `frontend/package.json`
- [ ] `frontend/package-lock.json`
- [ ] `frontend/src/` (entire directory)
- [ ] `frontend/public/` (entire directory)

#### Documentation
- [ ] `README.md`
- [ ] `frontend/README.md`
- [ ] `.gitignore`

### ❌ **Files to Exclude:**
- [ ] `__pycache__/`
- [ ] `frontend/node_modules/`
- [ ] `.env*` files
- [ ] IDE configuration files
- [ ] OS system files
- [ ] Log files
- [ ] Large model files

## 🚀 **Quick Git Commands**

```bash
# Initialize git repository
git init

# Add all necessary files
git add .

# Check what will be committed
git status

# Commit changes
git commit -m "Initial commit: Voice-to-Recipe application"

# Add remote repository
git remote add origin <your-repository-url>

# Push to remote
git push -u origin main
```

## 📝 **Notes**

1. **Dependencies**: The `node_modules/` directory should NOT be uploaded as it can be recreated using `npm install`
2. **Environment Variables**: Any sensitive configuration should be in `.env` files which are excluded
3. **Model Files**: If you have large AI model files, consider using Git LFS or storing them separately
4. **Database Files**: The JSON data files are included as they contain the application's core data

## 🔧 **After Cloning the Repository**

### Backend Setup:
```bash
pip install -r requirements.txt
python main.py
```

### Frontend Setup:
```bash
cd frontend
npm install
npm start
```

This file list ensures that anyone can clone your repository and run the application with minimal setup.