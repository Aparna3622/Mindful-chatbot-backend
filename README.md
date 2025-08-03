# STAN - AI Chatbot Assistant

A modern, full-stack AI chatbot application with beautiful UI and intelligent conversation capabilities.

## 🌟 Live Demo

- **Frontend**: [https://mindful-chatbot.vercel.app](https://mindful-chatbot.vercel.app)
- **Backend API**: [https://mindful-chatbot-backend-2.onrender.com](https://mindful-chatbot-backend-2.onrender.com)

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Deployment](#deployment)
- [API Documentation](#api-documentation)
- [Frontend Features](#frontend-features)
- [Backend Features](#backend-features)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### 🎨 Frontend Features
- **Modern UI Design**: Glassmorphism effects with smooth animations
- **Dark/Light Theme**: Toggle between themes with persistence
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Real-time Chat**: Instant message sending and receiving
- **Connection Status**: Live backend connectivity monitoring
- **Typing Indicators**: Professional chat experience
- **Sentiment Display**: Visual sentiment indicators on messages
- **Smooth Animations**: Enhanced user experience with CSS animations

### 🤖 Backend Features
- **AI-Powered Responses**: Intelligent conversation handling
- **Sentiment Analysis**: Automatic emotion detection in messages
- **Session Management**: Conversation context and history
- **RESTful API**: Clean, documented API endpoints
- **CORS Support**: Cross-origin requests for frontend integration
- **Health Monitoring**: System status and performance tracking
- **Error Handling**: Graceful error management and logging

## �️ Architecture

```
┌─────────────────┐       ┌─────────────────┐
│   Frontend      │       │    Backend      │
│   (Vercel)      │ ←───→ │   (Render)      │
│                 │       │                 │
│ • React-like JS │       │ • Flask API     │
│ • Modern CSS    │       │ • Sentiment AI  │
│ • Responsive    │       │ • Session Mgmt  │
└─────────────────┘       └─────────────────┘
```

### Deployment Strategy
- **Frontend**: Static hosting on Vercel
- **Backend**: Flask application on Render
- **Separation**: Independent deployment and scaling

## 🛠️ Technologies Used

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with animations
- **JavaScript (ES6+)**: Interactive functionality
- **Font Awesome**: Icon library
- **Google Fonts**: Typography (Inter font family)

### Backend
- **Python 3.11**: Programming language
- **Flask**: Web framework
- **Flask-CORS**: Cross-origin resource sharing
- **UUID**: Session ID generation
- **Logging**: Application monitoring

### Deployment & DevOps
- **Vercel**: Frontend hosting
- **Render**: Backend hosting
- **Git**: Version control
- **GitHub**: Repository hosting

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd C:\Stan_assign\stan_chatbot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

1. **Start the Flask server:**
   ```bash
   python app.py
   ```

2. **Open your web browser and visit:**
   ```
   http://localhost:5000
   ```

3. **Start chatting with STAN!**

### API Endpoints

- `GET /` - Main chat interface
- `POST /chat` - Send message to chatbot
- `GET /health` - Health check endpoint

### Example API Usage

```javascript
// Send a message to the chatbot
fetch('/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        message: 'Hello, how are you?',
        session_id: 'your-session-id'
    })
})
.then(response => response.json())
.then(data => {
    console.log('Bot response:', data.response);
});
```

## Configuration

You can configure the chatbot by setting environment variables:

- `MODEL_NAME` - Hugging Face model to use (default: microsoft/DialoGPT-medium)
- `TEMPERATURE` - Response generation temperature (default: 0.7)
- `MAX_CHAT_HISTORY` - Maximum chat history to maintain (default: 20)
- `PORT` - Server port (default: 5000)
- `FLASK_DEBUG` - Enable debug mode (default: False)

## Project Structure

```
stan_chatbot/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Chat interface template
└── README.md            # This file
```

## Model Information

The chatbot uses Microsoft's DialoGPT-medium model, which is:
- Pre-trained on 147M conversation-like exchanges
- Designed for multi-turn conversations
- Lightweight and suitable for real-time responses

## Fallback System

If the AI model fails to load or respond, the chatbot includes a rule-based fallback system that can handle:
- Greetings
- Basic questions
- Thank you messages
- Goodbyes
- General conversation

## Troubleshooting

### Model Loading Issues
If you encounter memory issues or slow loading times:
1. Try using a smaller model like `microsoft/DialoGPT-small`
2. Ensure you have sufficient RAM (recommended: 4GB+)
3. Check your internet connection for model downloading

### Common Error Solutions

**Error: "No module named 'transformers'"**
```bash
pip install transformers torch
```

**Error: "Port already in use"**
```bash
# Change the port in app.py or set PORT environment variable
export PORT=5001
python app.py
```

## Development

### Adding New Features

1. **Custom responses:** Modify the `_fallback_response` method in `app.py`
2. **UI changes:** Edit `templates/index.html`
3. **Model configuration:** Update `config.py`

### Testing

Test the health endpoint:
```bash
curl http://localhost:5000/health
```

Test the chat API:
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "test"}'
```

## Performance Tips

1. **Use GPU acceleration** if available (PyTorch will automatically detect CUDA)
2. **Adjust model size** based on your hardware capabilities
3. **Implement caching** for frequently asked questions
4. **Use a production WSGI server** like Gunicorn for deployment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the STAN Internship Challenge.

## Support

For issues and questions, please refer to the project documentation or contact the development team.

## Deployment

### Local Development Deployment

**Quick Start:**
```bash
# Run lightweight version (recommended for development)
python start_server.py

# Or run full version
python app.py
```

### Production Deployment Options

#### Option 1: Heroku Deployment

1. **Install Heroku CLI:**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Procfile:**
   ```bash
   echo "web: python app_lightweight.py" > Procfile
   ```

3. **Deploy to Heroku:**
   ```bash
   heroku create your-stan-chatbot
   git add .
   git commit -m "Deploy STAN chatbot"
   git push heroku main
   ```

#### Option 2: Railway Deployment

1. **Create railway.json:**
   ```json
   {
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "python app_lightweight.py",
       "healthcheckPath": "/health"
     }
   }
   ```

2. **Deploy:**
   - Visit https://railway.app
   - Connect your GitHub repository
   - Deploy automatically

#### Option 2.5: Vercel Deployment (Serverless)

**⚠️ Note:** Vercel is optimized for frontend/serverless functions, not long-running Flask apps.

1. **Create vercel.json:**
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "app_lightweight.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "app_lightweight.py"
       }
     ]
   }
   ```

2. **Modify app for serverless:**
   ```python
   # Create api/index.py for Vercel
   from app_lightweight import app
   
   # Export for Vercel
   def handler(request):
       return app(request.environ, start_response)
   ```

3. **Deploy:**
   ```bash
   npm i -g vercel
   vercel --prod
   ```

**Vercel Limitations:**
- ❌ 10-second function timeout
- ❌ No persistent storage
- ❌ Cold starts for inactive functions
- ❌ Limited for real-time chat applications

#### Option 3: Render Deployment

1. **Create render.yaml:**
   ```yaml
   services:
     - type: web
       name: stan-chatbot
       env: python
       buildCommand: pip install -r requirements_lightweight.txt
       startCommand: python app_lightweight.py
       envVars:
         - key: PORT
           value: 10000
   ```

2. **Deploy:**
   - Connect GitHub to Render
   - Auto-deploy on push

#### Option 4: DigitalOcean App Platform

1. **Create .do/app.yaml:**
   ```yaml
   name: stan-chatbot
   services:
     - name: web
       source_dir: /
       github:
         repo: your-username/your-repo
         branch: main
       run_command: python app_lightweight.py
       environment_slug: python
       instance_count: 1
       instance_size_slug: basic-xxs
       http_port: 5000
   ```

#### Option 5: AWS EC2 Deployment

1. **Launch EC2 instance** (Ubuntu 20.04)

2. **Install dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nginx
   pip3 install -r requirements_lightweight.txt
   ```

3. **Create systemd service:**
   ```bash
   sudo nano /etc/systemd/system/stan-chatbot.service
   ```
   ```ini
   [Unit]
   Description=STAN Chatbot
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/stan_chatbot
   ExecStart=/usr/bin/python3 app_lightweight.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

4. **Start service:**
   ```bash
   sudo systemctl enable stan-chatbot
   sudo systemctl start stan-chatbot
   ```

#### Option 6: Docker Deployment

1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app
   COPY requirements_lightweight.txt .
   RUN pip install -r requirements_lightweight.txt

   COPY . .
   EXPOSE 5000

   CMD ["python", "app_lightweight.py"]
   ```

2. **Build and run:**
   ```bash
   docker build -t stan-chatbot .
   docker run -p 5000:5000 stan-chatbot
   ```

3. **Docker Compose (with MongoDB):**
   ```yaml
   version: '3.8'
   services:
     chatbot:
       build: .
       ports:
         - "5000:5000"
       depends_on:
         - mongodb
       environment:
         - MONGODB_URI=mongodb://mongodb:27017/stan_chatbot

     mongodb:
       image: mongo:latest
       ports:
         - "27017:27017"
       volumes:
         - mongodb_data:/data/db

   volumes:
     mongodb_data:
   ```

### Environment Variables for Production

```bash
# Set these for production deployment
export FLASK_ENV=production
export FLASK_DEBUG=False
export PORT=5000
export MONGODB_URI=your_mongodb_connection_string
```

### Production Configuration Updates

For production, update your app to use environment variables:

```python
import os

# Production settings
if os.environ.get('FLASK_ENV') == 'production':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
else:
    app.run(debug=True, host='127.0.0.1', port=5000)
```

### SSL/HTTPS Setup

For production, enable HTTPS:

1. **Using Nginx reverse proxy:**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

2. **Get SSL certificate:**
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

### Performance Optimization for Production

1. **Use production WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn --bind 0.0.0.0:5000 app_lightweight:app
   ```

2. **Enable caching:**
   ```python
   from flask_caching import Cache
   cache = Cache(app, config={'CACHE_TYPE': 'simple'})
   ```

3. **Add rate limiting:**
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, key_func=lambda: request.remote_addr)
   ```

### Monitoring and Logging

```python
import logging
logging.basicConfig(level=logging.INFO)

# Add health check with detailed status
@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })
```

### Quick Deployment Checklist

- [ ] Choose deployment platform
- [ ] Update requirements file
- [ ] Set environment variables
- [ ] Configure production settings
- [ ] Set up SSL/HTTPS
- [ ] Enable monitoring
- [ ] Test health endpoints
- [ ] Set up CI/CD pipeline

### Recommended: Separate Frontend & Backend Deployment

**Best Practice:** Deploy frontend and backend separately for better scalability and performance.

#### Backend Deployment (API Server)

**Option A: Railway (Recommended for Backend)**
1. **Create backend repository** with only:
   - `app_lightweight.py`
   - `enhanced_features.py` 
   - `mongodb_config.py`
   - `requirements_lightweight.txt`

2. **Update app_lightweight.py for CORS:**
   ```python
   from flask_cors import CORS
   
   app = Flask(__name__)
   CORS(app, origins=["https://your-frontend-domain.vercel.app"])
   ```

3. **Deploy to Railway:**
   - Connect GitHub repo to Railway
   - Auto-deploy backend
   - Get API URL: `https://your-backend.railway.app`

**Option B: Heroku for Backend**
```bash
# Create Procfile
echo "web: gunicorn app_lightweight:app" > Procfile

# Deploy
heroku create your-stan-backend
git push heroku main
```

#### Frontend Deployment (Static Site)

**Option A: Vercel (Perfect for Frontend)**
1. **Create separate frontend repository** with only:
   - `templates/index.html` → `index.html`
   - Static assets (CSS, JS)

2. **Update JavaScript to use backend API:**
   ```javascript
   // Frontend Configuration
   const CONFIG = {
       API_BASE_URL: 'https://your-backend.railway.app',
       // For local development: 'http://localhost:5000'
   };
   
   // Updated fetch calls
   fetch(`${CONFIG.API_BASE_URL}/chat`, {
       method: 'POST',
       headers: {
           'Content-Type': 'application/json',
       },
       body: JSON.stringify({
           message: userMessage,
           session_id: sessionId
       })
   })
   ```

3. **Deploy to Vercel:**
   ```bash
   npm i -g vercel
   vercel --prod
   ```

**Option B: Netlify for Frontend**
1. **Drag and drop** your `index.html` to Netlify
2. **Or connect GitHub** for auto-deployment

**Option C: GitHub Pages for Frontend**
1. **Push frontend files** to GitHub
2. **Enable GitHub Pages** in repository settings

#### Complete Separation Architecture

**Backend (Railway/Heroku):**
- Handles `/chat`, `/health`, `/stats`, `/data` endpoints
- Returns JSON responses
- Manages MongoDB/in-memory storage
- CORS enabled for frontend domain

**Frontend (Vercel/Netlify):**
- Static HTML/CSS/JavaScript
- Makes API calls to backend
- Handles UI interactions
- Fast CDN delivery

#### Benefits of Separation:

✅ **Scalability:** Scale frontend and backend independently  
✅ **Performance:** Frontend on CDN, backend optimized for API  
✅ **Flexibility:** Different deployment strategies  
✅ **Security:** Better CORS control  
✅ **Development:** Teams can work independently  

#### Quick Setup Guide:

1. **Deploy Backend to Railway:** Get API URL
2. **Update Frontend:** Point to backend URL  
3. **Deploy Frontend to Vercel:** Static deployment
4. **Test:** Verify cross-origin communication works
5. **Monitor:** Check `/health` endpoint regularly

Your STAN chatbot will be production-ready with professional separation! 🚀
