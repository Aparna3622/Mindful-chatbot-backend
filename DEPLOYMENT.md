# Deployment Guide

This guide covers deploying the STAN Chatbot to production environments.

## Architecture Overview

```
┌─────────────────┐       ┌─────────────────┐
│   Frontend      │       │    Backend      │
│   (Vercel)      │ ←───→ │   (Render)      │
│                 │       │                 │
│ • Static Files  │       │ • Flask API     │
│ • HTML/CSS/JS   │       │ • Python App    │
│ • CDN Delivery  │       │ • Auto-scaling  │
└─────────────────┘       └─────────────────┘
```

## Frontend Deployment (Vercel)

### Prerequisites
- GitHub account
- Vercel account
- Repository with frontend code

### Step-by-Step Deployment

1. **Prepare Files**
   Ensure you have these files in your repository:
   ```
   stan_chatbot/
   ├── index.html          # Main frontend file
   ├── vercel.json         # Vercel configuration
   └── package.json        # Project metadata
   ```

2. **Vercel Configuration**
   The `vercel.json` file should contain:
   ```json
   {
     "version": 2,
     "name": "stan-chatbot-frontend",
     "builds": [
       {
         "src": "index.html",
         "use": "@vercel/static"
       }
     ],
     "rewrites": [
       {
         "source": "/(.*)",
         "destination": "/index.html"
       }
     ],
     "headers": [
       {
         "source": "/(.*)",
         "headers": [
           {
             "key": "X-Content-Type-Options",
             "value": "nosniff"
           },
           {
             "key": "X-Frame-Options",
             "value": "DENY"
           },
           {
             "key": "X-XSS-Protection",
             "value": "1; mode=block"
           }
         ]
       }
     ]
   }
   ```

3. **Deploy to Vercel**
   
   **Option A: Dashboard Deployment**
   - Visit [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Select the `stan_chatbot` directory as root
   - Configure settings:
     - Framework Preset: Other
     - Root Directory: `stan_chatbot` (if applicable)
     - Build Command: (leave empty)
     - Output Directory: (leave empty)
   - Click "Deploy"

   **Option B: CLI Deployment**
   ```bash
   # Install Vercel CLI
   npm i -g vercel
   
   # Navigate to project directory
   cd stan_chatbot
   
   # Login to Vercel
   vercel login
   
   # Deploy
   vercel --prod
   ```

4. **Configuration**
   - Custom domain (optional): Add in Vercel dashboard
   - Environment variables: Usually not needed for static frontend
   - Analytics: Enable in Vercel dashboard

### Frontend Environment Configuration

Update the API URL in `index.html`:
```javascript
// For production
const API_BASE_URL = 'https://your-backend-url.onrender.com';

// For development
const API_BASE_URL = 'http://localhost:5000';
```

## Backend Deployment (Render)

### Prerequisites
- GitHub account
- Render account
- Python application ready for deployment

### Step-by-Step Deployment

1. **Prepare Files**
   Ensure you have these files:
   ```
   stan_chatbot/
   ├── app_backend_only.py        # Main Flask application
   ├── requirements_backend.txt   # Python dependencies
   ├── runtime.txt               # Python version
   └── render.yaml               # Render configuration
   ```

2. **Dependencies File**
   `requirements_backend.txt`:
   ```
   flask==3.1.1
   flask-cors==4.0.0
   requests==2.32.4
   pymongo==4.6.1
   ```

3. **Runtime Specification**
   `runtime.txt`:
   ```
   python-3.11.0
   ```

4. **Render Configuration**
   `render.yaml`:
   ```yaml
   services:
     - type: web
       name: stan-chatbot-backend
       env: python
       plan: free
       buildCommand: pip install -r requirements_backend.txt
       startCommand: python app_backend_only.py
       envVars:
         - key: PYTHON_VERSION
           value: 3.11.0
         - key: PORT
           generateValue: true
   ```

5. **Deploy to Render**
   
   **Option A: Dashboard Deployment**
   - Visit [render.com](https://render.com)
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository
   - Configure settings:
     - Name: `stan-chatbot-backend`
     - Environment: Python
     - Region: Choose closest to your users
     - Branch: `main`
     - Root Directory: `stan_chatbot` (if applicable)
     - Build Command: `pip install -r requirements_backend.txt`
     - Start Command: `python app_backend_only.py`
   - Click "Create Web Service"

   **Option B: render.yaml Deployment**
   - Push `render.yaml` to your repository
   - Render will automatically detect and use the configuration

6. **Environment Variables**
   Render automatically provides:
   - `PORT`: The port your app should listen on
   - `PYTHON_VERSION`: Python version to use

### Backend Configuration

Ensure your Flask app is configured for production:

```python
if __name__ == '__main__':
    import os
    # Production settings
    port = int(os.environ.get('PORT', 5000))
    logger.info("🚀 Starting STAN Chatbot Backend...")
    app.run(debug=False, host='0.0.0.0', port=port)
```

## Environment-Specific Configurations

### Development Environment
```javascript
// Frontend
const API_BASE_URL = 'http://localhost:5000';

// Backend CORS
origins=[
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080"
]
```

### Production Environment
```javascript
// Frontend
const API_BASE_URL = 'https://mindful-chatbot-backend-2.onrender.com';

// Backend CORS
origins=[
    "https://mindful-chatbot.vercel.app",
    "https://*.vercel.app"
]
```

## Post-Deployment Steps

### 1. Verify Deployment
- **Frontend**: Visit your Vercel URL
- **Backend**: Test API endpoints
- **Integration**: Ensure frontend can communicate with backend

### 2. Configure Custom Domains (Optional)
- **Vercel**: Add custom domain in dashboard
- **Render**: Configure custom domain in service settings

### 3. Set Up Monitoring
- **Vercel Analytics**: Enable in dashboard
- **Render Metrics**: Monitor in service dashboard
- **Error Tracking**: Set up logging and error monitoring

### 4. Performance Optimization
- **Frontend**: Enable compression, optimize images
- **Backend**: Implement caching, optimize database queries

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure backend CORS configuration includes frontend domain
   - Check that preflight requests are handled

2. **Build Failures**
   - Verify all dependencies are in requirements files
   - Check Python version compatibility

3. **Environment Variables**
   - Ensure all required environment variables are set
   - Check variable names and values

4. **Port Configuration**
   - Backend must use `PORT` environment variable
   - Don't hardcode port numbers

### Debugging Commands

```bash
# Check backend health
curl https://your-backend-url.onrender.com/health

# Test CORS
curl -H "Origin: https://your-frontend-url.vercel.app" \
     https://your-backend-url.onrender.com/health

# View logs (Render)
# Available in Render dashboard under "Logs"

# View deployment status (Vercel)
vercel ls
```

## Scaling Considerations

### Frontend Scaling
- Vercel automatically handles CDN and global distribution
- No additional configuration needed for most use cases

### Backend Scaling
- **Free Tier**: Limited resources, suitable for development
- **Paid Tiers**: Better performance, custom domains, more resources
- **Database**: Consider upgrading from in-memory to persistent storage

### Performance Monitoring
- Monitor response times and error rates
- Set up alerts for service availability
- Track user engagement and usage patterns

## Security Best Practices

### Frontend Security
- Content Security Policy (CSP) headers
- HTTPS enforcement
- Input validation and sanitization

### Backend Security
- CORS configuration
- Input validation
- Rate limiting (future enhancement)
- Environment variable security

### General Security
- Keep dependencies updated
- Regular security audits
- Monitor for vulnerabilities

## Backup and Recovery

### Code Backup
- All code is backed up in GitHub repository
- Use version tags for releases

### Data Backup
- Current implementation uses in-memory storage
- For production, implement persistent storage with backups

### Disaster Recovery
- Frontend: Vercel has built-in redundancy
- Backend: Consider multi-region deployment for critical applications

## Cost Optimization

### Free Tier Limitations
- **Vercel**: 100GB bandwidth, custom domains on paid plans
- **Render**: 750 hours/month, goes to sleep after inactivity

### Optimization Strategies
- Use free tiers for development and small projects
- Upgrade to paid plans for production applications
- Monitor usage to avoid unexpected charges
