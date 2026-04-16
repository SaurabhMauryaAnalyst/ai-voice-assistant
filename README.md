AI Voice Assistant

An AI Voice Assistant built using React, FastAPI, Whisper, and Ollama that allows users to interact with an AI system through voice commands.
The system converts speech into text, processes it using tools or a local LLM, and returns a spoken response.

The project runs entirely locally without external AI APIs, ensuring privacy and offline capability.

Features
Real-time voice interaction
Local speech-to-text using Whisper
Local LLM inference using Ollama (Phi-3 / Llama models)
Text-to-speech responses
Tool-based routing for:
Date and time
Weather information
Calculator operations
Wikipedia search
WebSocket-based low latency communication
Fully local AI pipeline
System Architecture
User Speech
     ↓
React Frontend
     ↓
WebSocket Connection
     ↓
FastAPI Backend
     ↓
FFmpeg Audio Processing
     ↓
Whisper (Speech → Text)
     ↓
Intent Router
  ├ Date/Time
  ├ Weather API
  ├ Calculator
  ├ Wikipedia
  └ LLM Fallback (Ollama)
     ↓
AI Response
     ↓
Text-to-Speech (TTS)
     ↓
Audio Response to Browser
Tech Stack
Frontend
React
WebSockets
MediaRecorder API
Backend
FastAPI
Python AsyncIO
WebSocket communication
AI / ML
Whisper (Speech-to-Text)
Ollama (Local LLM)
Phi-3 / Llama models
Utilities
FFmpeg (audio conversion)
pyttsx3 (text-to-speech)
Wikipedia API
Open Meteo Weather API
Project Structure
backend
│
├── app
│   ├── main.py          # FastAPI server & WebSocket handler
│   ├── transcribe.py    # Whisper STT
│   ├── llm.py           # Ollama integration
│   ├── tts.py           # Text-to-speech
│   ├── tools.py         # Weather, calculator, wiki
│   └── session.py       # Conversation history
│
frontend
│
├── src
│   ├── App.jsx
│   ├── VoiceAssistant.jsx
│   ├── useWebSocket.js
│   └── useVAD.js
Installation
1. Clone the repository
git clone https://github.com/yourusername/ai-voice-assistant.git
cd ai-voice-assistant
2. Install backend dependencies
cd backend
pip install -r requirements.txt

Example requirements:

fastapi
uvicorn
requests
wikipedia
pyttsx3
openai-whisper
3. Install system dependencies

Install FFmpeg

ffmpeg

Install Ollama

https://ollama.ai
4. Pull LLM model
ollama pull phi3

or

ollama pull llama3
Running the Application
Start Ollama
ollama serve
Start backend server
cd backend
uvicorn app.main:app --reload

Server will run on:

http://localhost:8000
Start frontend
cd frontend
npm install
npm run dev

Open:

http://localhost:5173
Example Commands

You can ask the assistant:

What date is today?
What time is it?
Temperature in Bangalore
Calculate 25 * 33
Who is Elon Musk?
Tell me a joke
DevOps / System Design Highlights
Designed an asynchronous FastAPI backend
Implemented WebSocket-based real-time communication
Built a tool routing architecture for deterministic responses
Integrated local LLM inference via Ollama
Modular architecture supporting containerization and Kubernetes deployment
Future Improvements
Real-time streaming voice interaction
Redis-based conversation memory
Docker containerization
Kubernetes deployment
Live sports score APIs
GPU acceleration for Whisper
