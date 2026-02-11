# Modern Mestri - Project Documentation

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Features](#features)
4. [Technology Stack](#technology-stack)
5. [Module Documentation](#module-documentation)
6. [API Documentation](#api-documentation)
7. [Deployment](#deployment)
8. [Future Enhancements](#future-enhancements)

## 🎯 Project Overview

Modern Mestri is an AI-powered construction planning system that transforms traditional construction planning into a smarter, faster, and more accessible experience. The platform acts as a virtual construction project manager, providing intelligent estimation, scheduling, and decision support.

### Key Objectives
- Reduce planning time from days to minutes
- Improve accuracy in cost and resource estimation
- Make professional-grade planning accessible to small contractors
- Provide AI-driven insights and optimizations
- Ensure data privacy through local AI deployment

## 🏗️ Architecture

### System Architecture
```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (HTML/CSS/JS)                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │  Input   │  │ Results  │  │   Chat   │              │
│  │  Form    │  │ Display  │  │Interface │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
                         │
                    REST API
                         │
┌─────────────────────────────────────────────────────────┐
│                  Backend (Python/Flask)                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │Estimation│  │Scheduling│  │Resources │              │
│  └──────────┘  └──────────┘  └──────────┘              │
│  ┌──────────┐  ┌──────────┐                            │
│  │Blueprint │  │ AI Agent │                            │
│  └──────────┘  └──────────┘                            │
└─────────────────────────────────────────────────────────┘
                         │
                    HTTP API
                         │
┌─────────────────────────────────────────────────────────┐
│              Ollama (IBM Granite 3.3 2B)                │
│                  Local AI Inference                      │
└─────────────────────────────────────────────────────────┘
```

### Data Flow
1. User inputs project parameters
2. Frontend sends request to Flask backend
3. Backend modules calculate estimates, schedules, resources
4. AI agent analyzes results and provides insights
5. Results returned to frontend
6. Charts and visualizations rendered
7. User can chat with AI for clarifications

## ✨ Features

### 1. Intelligent Cost Estimation
- Material quantity calculations
- Labor cost estimation
- Trade-wise breakdown (masonry, carpentry, electrical, plumbing)
- Contingency planning
- Cost per square foot analysis

### 2. Resource Planning
- Workforce allocation by phase
- Productivity-based calculations
- Peak workforce requirements
- Labor day estimations

### 3. Smart Scheduling
- Phase-wise timeline generation
- Week-by-week breakdown
- Milestone tracking
- Critical path identification
- Timeline feasibility analysis

### 4. Blueprint Visualization
- Automated floor plan generation
- Room layout calculations
- Dimension estimations
- Multi-floor support

### 5. AI Analysis
- Feasibility assessment
- Risk identification
- Budget status evaluation
- Timeline validation
- Optimization suggestions

### 6. Interactive Chat
- Conversational AI assistant
- Context-aware responses
- Question answering
- Alternative exploration

## 🛠️ Technology Stack

### Frontend
- **HTML5**: Semantic structure
- **CSS3**: Glassmorphism design, animations
- **JavaScript ES6+**: Modern async/await patterns
- **Chart.js**: Data visualization
- **Google Fonts**: Inter, Poppins

### Backend
- **Python 3.8+**: Core language
- **Flask**: Web framework
- **Flask-CORS**: Cross-origin support
- **Requests**: HTTP client

### AI/ML
- **Ollama**: Local LLM runtime
- **IBM Granite 3.3 2B**: Language model
- **Prompt Engineering**: Structured prompts for construction domain

### Development Tools
- **Git**: Version control
- **VS Code**: Development environment

## 📚 Module Documentation

### Backend Modules

#### 1. `app.py` - Main Application
**Purpose**: Flask application entry point and API endpoints

**Endpoints**:
- `GET /` - Serve frontend
- `GET /api/health` - Health check
- `POST /api/plan` - Generate construction plan
- `POST /api/chat` - Chat with AI
- `POST /api/optimize` - Get optimizations
- `POST /api/risks` - Analyze risks

#### 2. `estimation.py` - Cost Estimation
**Purpose**: Calculate material quantities and costs

**Key Functions**:
- `calculate_materials()` - Material quantity calculations
- `calculate_costs()` - Comprehensive cost breakdown

**Calculations**:
- Cement: 0.4 bags per sq ft (structure) + 0.3 bags per sq ft (foundation)
- Steel: 8 kg per sq ft (structure) + 12 kg per sq ft (foundation)
- Bricks: 50 per sq ft
- Labor: ₹350 per sq ft base rate

#### 3. `scheduling.py` - Timeline Generation
**Purpose**: Generate realistic construction schedules

**Key Functions**:
- `generate_schedule()` - Create phase-wise schedule
- `_calculate_base_duration()` - Estimate realistic duration
- `_generate_weekly_schedule()` - Week-by-week breakdown

**Phase Distribution**:
- Excavation/Foundation: 15%
- Structure/Masonry: 25%
- Roofing: 10%
- Plastering: 15%
- MEP: 12%
- Flooring: 10%
- Carpentry: 8%
- Finishing: 5%

#### 4. `resources.py` - Workforce Planning
**Purpose**: Calculate labor requirements

**Key Functions**:
- `plan_workforce()` - Calculate workforce needs
- `_calculate_phase_workforce()` - Phase-wise allocation

**Productivity Rates**:
- Excavation: 200 sq ft/day
- Masonry: 100 sq ft/day
- Plastering: 120 sq ft/day
- Painting: 200 sq ft/day

#### 5. `blueprints.py` - Floor Plan Generation
**Purpose**: Generate simplified floor plans

**Key Functions**:
- `generate_layout()` - Create floor layouts
- `_layout_ground_floor()` - Ground floor rooms
- `_layout_upper_floor()` - Upper floor rooms

**Room Distribution**:
- Living: 25-30% of area
- Kitchen: 12-15%
- Bedrooms: 20% each
- Bathrooms: 50 sq ft each

#### 6. `ai_agent.py` - AI Integration
**Purpose**: Interface with Ollama for AI reasoning

**Key Functions**:
- `analyze_plan()` - Comprehensive plan analysis
- `chat()` - Conversational interactions
- `suggest_optimizations()` - Optimization suggestions
- `identify_risks()` - Risk assessment

**AI Capabilities**:
- Feasibility scoring
- Budget assessment
- Timeline validation
- Risk calculation
- Natural language responses

### Frontend Modules

#### 1. `app.js` - Main Application Logic
**Purpose**: Core application functionality

**Key Functions**:
- `generatePlan()` - API integration
- `displayResults()` - Render results
- `navigateToSection()` - Navigation management

#### 2. `charts.js` - Data Visualization
**Purpose**: Chart.js integration

**Charts**:
- Cost breakdown (doughnut chart)
- Workforce distribution (horizontal bar chart)

#### 3. `chat.js` - Chat Interface
**Purpose**: AI chat functionality

**Key Functions**:
- `sendMessage()` - Send chat messages
- `addMessage()` - Display messages
- `getCurrentContext()` - Extract plan context

## 🔌 API Documentation

### POST /api/plan
Generate comprehensive construction plan

**Request Body**:
```json
{
  "area": 2000,
  "floors": 2,
  "budget": 5000000,
  "timeline": 180,
  "complexity": "medium"
}
```

**Response**:
```json
{
  "success": true,
  "project_summary": {...},
  "cost_estimate": {...},
  "material_estimate": {...},
  "labor_plan": {...},
  "schedule": {...},
  "blueprint": {...},
  "ai_analysis": {...}
}
```

### POST /api/chat
Chat with AI assistant

**Request Body**:
```json
{
  "message": "How can I reduce costs?",
  "context": {...}
}
```

**Response**:
```json
{
  "success": true,
  "response": "Here are some cost reduction strategies..."
}
```

## 🚀 Deployment

### Local Development
```bash
python backend/app.py
```

### Production Deployment

#### Option 1: Gunicorn (Linux/Mac)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

#### Option 2: Waitress (Windows)
```bash
pip install waitress
waitress-serve --port=5000 backend.app:app
```

#### Option 3: Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "backend/app.py"]
```

### Environment Variables
```bash
FLASK_ENV=production
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=granite3.1-dense:2b
```

## 🔮 Future Enhancements

### Phase 2 Features
1. **User Authentication**
   - Project saving and loading
   - User profiles
   - Project history

2. **Advanced Visualizations**
   - 3D floor plans
   - Gantt charts
   - Resource utilization graphs

3. **Export Capabilities**
   - PDF reports
   - Excel cost sheets
   - Project timelines

4. **Collaboration**
   - Multi-user access
   - Comments and annotations
   - Real-time updates

5. **Integration**
   - Material supplier APIs
   - Labor marketplace integration
   - Weather data for scheduling

6. **Mobile App**
   - React Native app
   - Offline support
   - Push notifications

### Technical Improvements
1. Database integration (PostgreSQL)
2. Caching layer (Redis)
3. API rate limiting
4. Comprehensive testing suite
5. CI/CD pipeline
6. Performance monitoring
7. Error tracking (Sentry)

## 📄 License
MIT License - Free to use and modify

## 👥 Contributors
Built with ❤️ using Generative AI

---

**Version**: 1.0.0  
**Last Updated**: February 2026
