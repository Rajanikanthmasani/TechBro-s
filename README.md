# Modern Mestri - AI-Powered Construction Planning System

## Overview
Modern Mestri is an intelligent web-based platform that acts as a virtual construction project manager, providing AI-driven planning, estimation, scheduling, and decision support for residential construction projects.

## Features
- 🏗️ **Intelligent Cost Estimation** - Automated material and labor cost calculations
- 📊 **Resource Planning** - Workforce allocation and productivity analysis
- 📅 **Smart Scheduling** - Week-by-week construction timeline generation
- 🤖 **AI Reasoning** - Feasibility validation and optimization suggestions
- 💬 **Chat Agent** - Conversational AI assistant for planning queries
- 📐 **Blueprint Visualization** - Simplified floor plan generation
- ⚠️ **Risk Analysis** - Identify potential delays and budget overruns

## Technology Stack
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **Backend**: Python, Flask
- **AI**: IBM Granite 3.3 2B (via Ollama)
- **Data Format**: JSON

## Quick Start

### Prerequisites
- Python 3.8+
- Ollama installed with IBM Granite 3.3 model
- Modern web browser

### Installation

1. **Install Ollama and Pull Granite Model**
```bash
# Install Ollama from https://ollama.ai
# Pull IBM Granite 3.3 model
ollama pull granite3.1-dense:2b
```

2. **Install Python Dependencies**
```bash
pip install flask flask-cors requests
```

3. **Run the Application**
```bash
python backend/app.py
```

4. **Open in Browser**
Navigate to `http://localhost:5000`

## Project Structure
```
Modern_Mestri/
├── backend/
│   ├── app.py                 # Flask application
│   ├── estimation.py          # Cost & material calculations
│   ├── scheduling.py          # Timeline generation
│   ├── resources.py           # Labor planning
│   ├── ai_agent.py           # AI integration
│   └── blueprints.py         # Floor plan generation
├── frontend/
│   ├── index.html            # Main application
│   ├── css/
│   │   └── styles.css        # Premium styling
│   └── js/
│       ├── app.js            # Main application logic
│       ├── charts.js         # Visualization
│       └── chat.js           # AI chat interface
└── README.md

```

## Usage

1. **Enter Project Details**
   - Built-up area (sq ft)
   - Number of floors
   - Budget constraints
   - Timeline requirements

2. **Get AI-Powered Plan**
   - Detailed cost breakdown
   - Material requirements
   - Labor allocation
   - Week-by-week schedule
   - Floor plan visualization

3. **Chat with AI Agent**
   - Ask questions about estimates
   - Request optimizations
   - Explore alternatives

## License
MIT License

## Contributors
Built with ❤️ using Generative AI
