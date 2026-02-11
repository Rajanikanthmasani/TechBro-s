# Modern Mestri - Setup Guide

## Prerequisites

Before running the application, ensure you have the following installed:

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - Verify: `python --version`

2. **Ollama**
   - Download from: https://ollama.ai
   - Install and run Ollama

3. **IBM Granite 3.3 Model**
   - After installing Ollama, pull the model:
   ```bash
   ollama pull granite3.1-dense:2b
   ```

## Installation Steps

### Step 1: Install Python Dependencies

Open a terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Flask-CORS (cross-origin support)
- Requests (HTTP library)

### Step 2: Verify Ollama is Running

Make sure Ollama is running in the background. You can verify by running:

```bash
ollama list
```

You should see `granite3.1-dense:2b` in the list.

### Step 3: Start the Backend Server

Navigate to the project directory and run:

```bash
python backend/app.py
```

The server will start on `http://localhost:5000`

You should see:
```
🏗️  Modern Mestri - AI Construction Planning System
============================================================
Starting server on http://localhost:5000
============================================================
```

### Step 4: Open the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## Troubleshooting

### Issue: "AI Offline" status

**Solution:**
1. Make sure Ollama is running
2. Verify the model is installed: `ollama list`
3. Test the model: `ollama run granite3.1-dense:2b "Hello"`
4. Check if Ollama is accessible at `http://localhost:11434`

### Issue: Backend server won't start

**Solution:**
1. Check if port 5000 is already in use
2. Verify Python dependencies are installed: `pip list`
3. Check for error messages in the terminal

### Issue: "Module not found" errors

**Solution:**
```bash
pip install --upgrade -r requirements.txt
```

### Issue: CORS errors in browser

**Solution:**
- Make sure you're accessing the app through `http://localhost:5000`
- Don't open `index.html` directly from the file system

## Alternative Model

If you prefer to use a different Granite model or if the 2B model is not available:

1. Check available models:
```bash
ollama list
```

2. Pull an alternative:
```bash
ollama pull granite3.1-dense:8b
```

3. Update `backend/ai_agent.py` line 11:
```python
def __init__(self, model='granite3.1-dense:8b', base_url='http://localhost:11434'):
```

## Running Without AI

The system will work even if Ollama is not available. It will use rule-based fallback logic for analysis and provide basic responses. However, for the best experience, we recommend running with AI enabled.

## Performance Tips

1. **First Request**: The first AI request may take longer as the model loads into memory
2. **Model Size**: The 2B model is faster but less detailed. The 8B model provides better responses but requires more RAM
3. **Concurrent Users**: For production use, consider using a production WSGI server like Gunicorn

## Next Steps

Once the application is running:

1. Enter your project details (area, floors, budget, timeline)
2. Select project complexity
3. Click "Generate AI Plan"
4. Review the comprehensive construction plan
5. Chat with the AI assistant for questions and optimizations

## Support

For issues or questions:
- Check the console for error messages
- Verify all prerequisites are installed
- Ensure Ollama is running and accessible
- Review the troubleshooting section above

Enjoy using Modern Mestri! 🏗️
