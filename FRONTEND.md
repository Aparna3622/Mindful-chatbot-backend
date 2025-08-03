# Frontend Development Guide

This guide covers the frontend architecture, features, and customization options for the STAN Chatbot.

## Overview

The frontend is a modern, responsive web application built with vanilla HTML, CSS, and JavaScript. It features a beautiful glassmorphism design with dark/light theme support and smooth animations.

## Architecture

```
Frontend Structure
├── HTML (Structure)
│   ├── Chat Container
│   ├── Header Section
│   ├── Messages Area
│   └── Input Section
├── CSS (Styling)
│   ├── Base Styles
│   ├── Component Styles
│   ├── Animations
│   └── Responsive Design
└── JavaScript (Functionality)
    ├── ChatBot Class
    ├── Theme Management
    ├── API Communication
    └── UI Interactions
```

## Features

### 🎨 Visual Design

#### Glassmorphism Effects
- Semi-transparent containers with backdrop blur
- Layered depth with shadows and borders
- Modern, premium appearance

#### Theme System
- **Light Theme**: Bright gradients with blue/purple accents
- **Dark Theme**: Deep space colors with purple highlights
- **Persistence**: Theme choice saved in localStorage
- **System Detection**: Respects OS preference

#### Animations
- **Background**: Shifting gradient animations
- **Messages**: Slide-in animations for new messages
- **Buttons**: Hover and click feedback
- **Typing Indicator**: Bouncing dots animation

### 🖱️ User Interface

#### Chat Header
```html
<div class="chat-header">
    <button class="theme-toggle" onclick="toggleTheme()">
        <i class="fas fa-moon" id="themeIcon"></i>
    </button>
    <div class="avatar">
        <i class="fas fa-robot"></i>
    </div>
    <h1>STAN</h1>
    <p>Your Intelligent AI Assistant</p>
    <div class="connection-status">
        <div class="status-indicator"></div>
        <span>Connected</span>
    </div>
</div>
```

#### Message Display
- **User Messages**: Right-aligned with gradient background
- **Bot Messages**: Left-aligned with light background
- **Avatars**: Icons for user and bot identification
- **Metadata**: Timestamp and sentiment indicators

#### Input Section
- **Text Input**: Rounded input with focus effects
- **Send Button**: Circular button with hover animations
- **Typing Indicator**: Shows when bot is responding

### 📱 Responsive Design

#### Breakpoints
```css
/* Desktop: Default styles */
@media (max-width: 768px) {
    /* Tablet and Mobile adjustments */
}
```

#### Mobile Optimizations
- Compact header with smaller avatars
- Adjusted padding and spacing
- Touch-friendly button sizes
- Optimized message bubble sizes

## Component Architecture

### ChatBot Class

The main JavaScript class that handles all chat functionality:

```javascript
class ChatBot {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.initializeEventListeners();
        this.checkConnection();
    }
    
    // Session management
    generateSessionId() { /* ... */ }
    
    // API communication
    async checkConnection() { /* ... */ }
    async sendMessage() { /* ... */ }
    
    // UI management
    addMessage(content, sender, metadata) { /* ... */ }
    showTypingIndicator() { /* ... */ }
    updateConnectionStatus(status, text) { /* ... */ }
}
```

### Theme Management

Theme switching functionality:

```javascript
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
}

function toggleTheme() {
    const isDark = document.body.classList.contains('dark-theme');
    setTheme(isDark ? 'light' : 'dark');
}

function setTheme(theme) {
    const body = document.body;
    const themeIcon = document.getElementById('themeIcon');
    
    if (theme === 'dark') {
        body.classList.add('dark-theme');
        themeIcon.className = 'fas fa-sun';
    } else {
        body.classList.remove('dark-theme');
        themeIcon.className = 'fas fa-moon';
    }
    
    localStorage.setItem('theme', theme);
}
```

## Styling System

### CSS Custom Properties (Variables)

```css
:root {
    /* Light theme colors */
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    --text-primary: #333;
    --bg-container: rgba(255, 255, 255, 0.95);
}

body.dark-theme {
    /* Dark theme colors */
    --primary-gradient: linear-gradient(135deg, #4c4c6d 0%, #3e3e5e 100%);
    --background-gradient: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 50%, #3e3e5e 100%);
    --text-primary: #e8e8e8;
    --bg-container: rgba(30, 30, 46, 0.95);
}
```

### Component Styles

#### Glassmorphism Container
```css
.chat-container {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    box-shadow: 0 32px 64px rgba(0, 0, 0, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.2);
}
```

#### Message Bubbles
```css
.message-content {
    padding: 16px 20px;
    border-radius: 20px;
    word-wrap: break-word;
    font-size: 15px;
    line-height: 1.5;
}

.message.user .message-content {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-bottom-right-radius: 6px;
}

.message.bot .message-content {
    background: white;
    border: 1px solid rgba(0, 0, 0, 0.08);
    color: #333;
    border-bottom-left-radius: 6px;
}
```

### Animation System

#### Keyframe Animations
```css
@keyframes backgroundShift {
    0%, 100% { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); 
    }
    50% { 
        background: linear-gradient(135deg, #f093fb 0%, #667eea 50%, #764ba2 100%); 
    }
}

@keyframes messageSlide {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes typingBounce {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-10px); }
}
```

## API Integration

### Backend Communication

The frontend communicates with the backend through RESTful API calls:

```javascript
// Health check
const response = await fetch(`${API_BASE_URL}/health`);

// Send message
const response = await fetch(`${API_BASE_URL}/chat`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        message: message,
        session_id: this.sessionId
    })
});
```

### Error Handling

```javascript
try {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    // Handle successful response
} catch (error) {
    console.error('Error:', error);
    this.addErrorMessage('Sorry, I encountered an error. Please try again.');
}
```

## Customization Guide

### Changing Colors

1. **Update CSS Variables**
   ```css
   :root {
       --primary-color: #your-color;
       --accent-color: #your-accent;
   }
   ```

2. **Modify Gradients**
   ```css
   .chat-header {
       background: linear-gradient(135deg, #your-start 0%, #your-end 100%);
   }
   ```

### Adding New Themes

1. **Create Theme Class**
   ```css
   body.custom-theme {
       --primary-gradient: /* your gradient */;
       --background-gradient: /* your background */;
   }
   ```

2. **Update Theme Toggle**
   ```javascript
   function setTheme(theme) {
       // Add your theme logic
       if (theme === 'custom') {
           body.classList.add('custom-theme');
       }
   }
   ```

### Adding New Message Types

1. **Update Message Rendering**
   ```javascript
   addMessage(content, sender, metadata = {}) {
       // Add support for new message types
       if (metadata.type === 'image') {
           // Handle image messages
       }
   }
   ```

2. **Add Corresponding Styles**
   ```css
   .message.image .message-content {
       /* Image message styles */
   }
   ```

## Performance Optimization

### Image Optimization
- Use modern image formats (WebP, AVIF)
- Implement lazy loading for images
- Optimize icon usage with Font Awesome

### CSS Optimization
- Minimize CSS file size
- Use CSS containment for better performance
- Optimize animations for 60fps

### JavaScript Optimization
- Debounce user input
- Minimize DOM manipulations
- Use efficient event handling

## Accessibility Features

### Keyboard Navigation
- Tab order for interactive elements
- Enter key support for sending messages
- Escape key for closing modals

### Screen Reader Support
- Semantic HTML structure
- ARIA labels for interactive elements
- Role attributes for custom components

### Visual Accessibility
- High contrast mode support
- Scalable text and UI elements
- Focus indicators for keyboard navigation

## Browser Compatibility

### Supported Browsers
- Chrome 70+
- Firefox 65+
- Safari 12+
- Edge 79+

### Feature Detection
```javascript
// Check for backdrop-filter support
if (CSS.supports('backdrop-filter', 'blur(10px)')) {
    // Use backdrop-filter
} else {
    // Fallback styles
}
```

## Testing

### Manual Testing Checklist
- [ ] Theme toggle functionality
- [ ] Message sending and receiving
- [ ] Responsive design on different screen sizes
- [ ] Keyboard navigation
- [ ] Error handling scenarios

### Automated Testing (Future Enhancement)
- Unit tests for JavaScript functions
- Integration tests for API communication
- End-to-end tests for user workflows

## Deployment

### Build Process
No build process required - static files can be deployed directly.

### Environment Configuration
Update the API URL for different environments:

```javascript
// Development
const API_BASE_URL = 'http://localhost:5000';

// Production
const API_BASE_URL = 'https://your-backend-url.onrender.com';
```

### Performance Monitoring
- Use browser dev tools for performance analysis
- Monitor Core Web Vitals
- Track user engagement metrics

## Future Enhancements

### Planned Features
- Voice input/output
- File upload support
- Emoji picker
- Message search
- Chat history export

### Technical Improvements
- Progressive Web App (PWA) features
- Offline support
- Service worker implementation
- Virtual scrolling for large conversations

## Contributing

When contributing to the frontend:

1. Follow the existing code style
2. Test on multiple browsers and devices
3. Ensure accessibility standards are met
4. Update documentation for new features
5. Add appropriate comments for complex logic

## Resources

### Documentation
- [MDN Web Docs](https://developer.mozilla.org/)
- [CSS-Tricks](https://css-tricks.com/)
- [Font Awesome Icons](https://fontawesome.com/icons)

### Tools
- Browser Developer Tools
- [Can I Use](https://caniuse.com/) for browser compatibility
- [Lighthouse](https://developers.google.com/web/tools/lighthouse) for performance auditing
