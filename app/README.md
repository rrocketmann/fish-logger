# Fish Logger Web Application

## Overview
A community-powered web platform for uploading and labeling fish photos with a clean, flat design in light green and white colors.

## Features

### 🏠 Home Page
- Welcome screen with call-to-action buttons
- Overview of platform features
- Clean, flat design aesthetic

### 📸 Upload Section
- Upload fish photos
- Label with species name
- Add uploader name
- Optional location and notes
- Form validation

### 🌊 Community Gallery
- Grid layout of all uploaded fish photos
- Species name, uploader, location, date
- Like functionality (click hearts)
- Pagination for large collections
- Responsive design

### 📊 Statistics Page
- Total uploads counter
- Species count
- Species breakdown with photo counts
- Sorted by popularity

## Design System

### Colors
- **Background**: `#f5fff5` (very light green)
- **Primary Green**: `#a8d5a8` (light green)
- **Secondary Green**: `#c8e6c8` (lighter green)
- **Accent Green**: `#7cb87c` (medium green)
- **Text**: `#1a3a1a` (dark green)
- **White**: `#ffffff`

### Design Principles
- ✅ **Flat Design**: No rounded corners, no shadows, no gradients
- ✅ **Clean Borders**: 3px solid borders throughout
- ✅ **High Contrast**: Dark text on light backgrounds
- ✅ **Simple Transitions**: Basic hover effects only

## Tech Stack

- **Backend**: Flask 3.1.3
- **Database**: SQLite with Flask-SQLAlchemy
- **Frontend**: HTML5, CSS3 (no frameworks)
- **File Uploads**: Werkzeug secure filenames
- **Image Storage**: Local file system

## Database Schema

### FishUpload Model
```python
- id (Integer, Primary Key)
- filename (String, 200)
- species_label (String, 100)
- uploader_name (String, 100)
- location (String, 200, Optional)
- notes (Text, Optional)
- uploaded_at (DateTime)
- likes (Integer, default=0)
```

## Running the App

### Development Server
```bash
cd app
source ../venv/bin/activate
python app.py
```

The app will be available at: `http://localhost:5000`

### Production Deployment
For production, use a WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## File Structure
```
app/
├── app.py                   # Main Flask application
├── templates/               # HTML templates
│   ├── base.html           # Base template with styling
│   ├── index.html          # Home page
│   ├── upload.html         # Upload form
│   ├── community.html      # Gallery page
│   └── stats.html          # Statistics page
├── static/
│   └── uploads/            # Uploaded fish photos
└── instance/
    └── fish_community.db   # SQLite database
```

## Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page |
| `/upload` | GET/POST | Upload form and handler |
| `/community` | GET | Gallery with pagination |
| `/like/<id>` | POST | Like a fish photo (AJAX) |
| `/stats` | GET | Community statistics |

## Configuration

Edit `app.py` to customize:
```python
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
```

## Features Roadmap

Future enhancements:
- [ ] User accounts and authentication
- [ ] AI-powered species suggestions
- [ ] Search and filter functionality
- [ ] Export data as CSV
- [ ] Admin moderation panel
- [ ] Mobile app integration

## Security Notes

**Important for production:**
1. Change `SECRET_KEY` to a random string
2. Use environment variables for sensitive config
3. Add rate limiting for uploads
4. Implement CSRF protection
5. Add file size/type validation
6. Use HTTPS in production

## License
Same as main Fish Logger project
