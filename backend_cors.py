# Add CORS support to your backend for separate deployment
from flask_cors import CORS

# Add this to your app_lightweight.py
app = Flask(__name__)

# Enable CORS for frontend domain
CORS(app, origins=[
    "https://your-frontend.vercel.app",
    "https://your-frontend.netlify.app", 
    "http://localhost:3000",  # For local development
    "http://127.0.0.1:3000"   # Alternative local
])

# Or allow all origins during development (not recommended for production)
# CORS(app, origins="*")
