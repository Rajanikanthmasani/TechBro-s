# 🚀 Quick Start Guide

## Fastest Way to Get Started

### Option 1: Using the Startup Script (Recommended for Windows)

1. **Double-click `start.bat`**
   - The script will check your setup and start the server automatically
   - Open your browser to `http://localhost:5000`

### Option 2: Manual Start

1. **Open Terminal/Command Prompt** in the project folder

2. **Install Dependencies** (first time only):
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Server**:
   ```bash
   python backend/app.py
   ```

4. **Open Browser**:
   - Navigate to `http://localhost:5000`

## First Time Setup

### Install Ollama (Optional but Recommended)

For full AI capabilities:

1. Download Ollama from https://ollama.ai
2. Install and run Ollama
3. Pull the AI model:
   ```bash
   ollama pull granite3.1-dense:2b
   ```

**Note**: The app works without Ollama, but AI features will be limited.

## Using the Application

### Step 1: Enter Project Details
- Built-up area (sq ft)
- Number of floors
- Budget (optional)
- Timeline (optional)
- Project complexity

### Step 2: Generate Plan
- Click "Generate AI Plan"
- Wait for AI analysis (5-10 seconds)

### Step 3: Review Results
- Cost breakdown with charts
- Material requirements
- Construction schedule
- Workforce planning
- Floor plan layout
- AI insights and recommendations

### Step 4: Chat with AI
- Ask questions about your plan
- Request optimizations
- Explore alternatives

## Example Projects to Try

### Small House
- Area: 1200 sq ft
- Floors: 1
- Complexity: Simple

### Medium Villa
- Area: 2500 sq ft
- Floors: 2
- Budget: 5000000
- Timeline: 180 days
- Complexity: Medium

### Large Complex Building
- Area: 4000 sq ft
- Floors: 3
- Budget: 12000000
- Timeline: 240 days
- Complexity: Complex

## Tips

✅ **Budget**: Leave blank to get cost estimation only  
✅ **Timeline**: Leave blank for recommended duration  
✅ **AI Chat**: Ask specific questions for better responses  
✅ **Optimization**: Use the chat to explore cost/time savings  

## Need Help?

- Check `SETUP.md` for detailed setup instructions
- Review `README.md` for project overview
- Check browser console for errors (F12)

---

**Ready to build? Let's go! 🏗️**
