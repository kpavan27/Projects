import React, { useState, useRef } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const [error, setError] = useState(null);
  const [recordingTime, setRecordingTime] = useState(0);
  const mediaRecorder = useRef(null);
  const audioChunks = useRef([]);
  const recordingInterval = useRef(null);

  const startRecording = async () => {
    try {
      setError(null);
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder.current = new MediaRecorder(stream);
      mediaRecorder.current.ondataavailable = (event) => {
        audioChunks.current.push(event.data);
      };
      mediaRecorder.current.onstop = () => {
        const blob = new Blob(audioChunks.current, { type: 'audio/webm' });
        setAudioBlob(blob);
        audioChunks.current = [];
        if (recordingInterval.current) {
          clearInterval(recordingInterval.current);
          setRecordingTime(0);
        }
      };
      mediaRecorder.current.start();
      setIsRecording(true);
      
      // Start recording timer
      recordingInterval.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
    } catch (err) {
      console.error("Error accessing microphone:", err);
      setError("Could not access microphone. Please check permissions and try again.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorder.current) {
      mediaRecorder.current.stop();
      setIsRecording(false);
    }
  };

  const resetRecording = () => {
    setAudioBlob(null);
    setResult(null);
    setError(null);
    setRecordingTime(0);
  };

  const handleSubmit = async () => {
    if (!audioBlob) {
      setError('Please record some audio first.');
      return;
    }
    setIsLoading(true);
    setError(null);
    const formData = new FormData();
    const audioFile = new File([audioBlob], "recording.webm", { type: 'audio/webm' });
    formData.append('file', audioFile);

    try {
      const response = await axios.post('http://127.0.0.1:8000/process-voice', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 30000, // 30 second timeout
      });
      setResult(response.data);
    } catch (error) {
      if (error.response?.data?.detail) {
        setError(error.response.data.detail);
      } else if (error.code === 'ECONNABORTED') {
        setError('Request timed out. Please try again.');
      } else {
        setError('An error occurred: ' + (error.message || 'Unknown error'));
      }
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getSustainabilityColor = (rating) => {
    switch (rating) {
      case 'Excellent': return '#4CAF50';
      case 'Good': return '#8BC34A';
      case 'Fair': return '#FF9800';
      case 'Needs Improvement': return '#F44336';
      default: return '#9E9E9E';
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🍳 Voice-to-Recipe Generator</h1>
        <p>Transform your ingredients into sustainable recipes with AI</p>
      </header>

      <main className="app-main">
        <div className="recording-section">
          <div className="recording-controls">
            {!isRecording ? (
              <button 
                className="record-button" 
                onClick={startRecording} 
                disabled={isLoading}
              >
                🎤 Start Recording
              </button>
            ) : (
              <button 
                className="stop-button" 
                onClick={stopRecording} 
                disabled={isLoading}
              >
                ⏹️ Stop Recording
              </button>
            )}
            
            {audioBlob && !isLoading && (
              <button className="submit-button" onClick={handleSubmit}>
                🍽️ Generate Recipe
              </button>
            )}
            
            {(audioBlob || result) && (
              <button className="reset-button" onClick={resetRecording}>
                🔄 New Recording
              </button>
            )}
          </div>

          {isRecording && (
            <div className="recording-status">
              <div className="recording-indicator"></div>
              <span>Recording... {formatTime(recordingTime)}</span>
            </div>
          )}

          {audioBlob && !isLoading && (
            <div className="audio-preview">
              <p>✅ Recording complete! Click "Generate Recipe" to process.</p>
              <audio src={URL.createObjectURL(audioBlob)} controls />
            </div>
          )}

          {isLoading && (
            <div className="loading">
              <div className="spinner"></div>
              <p>Processing your voice and generating recipe...</p>
            </div>
          )}

          {error && (
            <div className="error">
              <p>❌ {error}</p>
            </div>
          )}
        </div>

        {result && (
          <div className="recipe-result">
            <div className="recipe-header">
              <h2>🍽️ {result.recipe.title}</h2>
              <div className="recipe-meta">
                <span className="meta-item">⏱️ {result.recipe.cooking_time}</span>
                <span className="meta-item">👥 {result.recipe.servings} servings</span>
                <span className="meta-item">📊 {result.recipe.difficulty}</span>
              </div>
            </div>

            <div className="ingredients-section">
              <h3>🥘 Detected Ingredients</h3>
              <div className="ingredients-list">
                {result.extracted_ingredients.map((ingredient, index) => (
                  <span key={index} className="ingredient-tag">
                    {ingredient}
                  </span>
                ))}
              </div>
            </div>

            <div className="sustainability-section">
              <h3>🌱 Sustainability & Nutrition</h3>
              <div className="sustainability-grid">
                <div className="sustainability-card">
                  <h4>Carbon Footprint</h4>
                  <div className="metric-value">
                    {result.sustainability.total_carbon_kg_co2} kg CO₂
                  </div>
                  <div className="sustainability-rating" 
                       style={{color: getSustainabilityColor(result.sustainability.sustainability_rating)}}>
                    {result.sustainability.sustainability_rating}
                  </div>
                </div>
                
                <div className="sustainability-card">
                  <h4>Carbon Saved</h4>
                  <div className="metric-value">
                    {result.sustainability.carbon_saved_kg_co2} kg CO₂
                  </div>
                  <div className="metric-subtitle">vs average recipe</div>
                </div>
                
                <div className="sustainability-card">
                  <h4>Calories</h4>
                  <div className="metric-value">
                    {result.sustainability.nutrition.total_calories}
                  </div>
                  <div className="metric-subtitle">per serving</div>
                </div>
              </div>
              
              <div className="nutrition-details">
                <h4>📊 Nutrition Breakdown</h4>
                <div className="nutrition-grid">
                  <div className="nutrition-item">
                    <span className="nutrition-label">Protein:</span>
                    <span className="nutrition-value">{result.sustainability.nutrition.protein_g}g</span>
                  </div>
                  <div className="nutrition-item">
                    <span className="nutrition-label">Carbs:</span>
                    <span className="nutrition-value">{result.sustainability.nutrition.carbs_g}g</span>
                  </div>
                  <div className="nutrition-item">
                    <span className="nutrition-label">Fat:</span>
                    <span className="nutrition-value">{result.sustainability.nutrition.fat_g}g</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="instructions-section">
              <h3>👨‍🍳 Cooking Instructions</h3>
              <ol className="instructions-list">
                {result.recipe.instructions.map((step, i) => (
                  <li key={i} className="instruction-step">
                    {step}
                  </li>
                ))}
              </ol>
            </div>

            <div className="transcription-section">
              <h4>🎤 What you said:</h4>
              <p className="transcription-text">"{result.original_text}"</p>
            </div>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>Built with ❤️ for sustainable cooking | Powered by AI</p>
      </footer>
    </div>
  );
}

export default App;
