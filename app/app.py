"""
Fish Logger - Community Fish Identification App
Flask web application for uploading and labeling fish images
"""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fish-logger-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fish_community.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy(app)

# Database Models
class FishUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    species_label = db.Column(db.String(100), nullable=False)
    uploader_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))
    notes = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<FishUpload {self.species_label}>'

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def ensure_upload_dir():
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Routes
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/community')
def community():
    """Community gallery page"""
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    uploads = FishUpload.query.order_by(FishUpload.uploaded_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('community.html', uploads=uploads)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload page"""
    if request.method == 'POST':
        # Check if file was uploaded
        if 'fish_image' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['fish_image']
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # Secure the filename and add timestamp
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            
            # Save file
            ensure_upload_dir()
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Save to database
            new_upload = FishUpload(
                filename=filename,
                species_label=request.form.get('species_label', 'Unknown'),
                uploader_name=request.form.get('uploader_name', 'Anonymous'),
                location=request.form.get('location', ''),
                notes=request.form.get('notes', '')
            )
            
            db.session.add(new_upload)
            db.session.commit()
            
            flash('Fish photo uploaded successfully!', 'success')
            return redirect(url_for('community'))
        else:
            flash('Invalid file type. Please upload an image (PNG, JPG, JPEG, GIF)', 'error')
            return redirect(request.url)
    
    return render_template('upload.html')

@app.route('/like/<int:upload_id>', methods=['POST'])
def like_upload(upload_id):
    """Like a fish upload"""
    upload = FishUpload.query.get_or_404(upload_id)
    upload.likes += 1
    db.session.commit()
    return jsonify({'likes': upload.likes})

@app.route('/stats')
def stats():
    """Community statistics"""
    total_uploads = FishUpload.query.count()
    species_counts = db.session.query(
        FishUpload.species_label,
        db.func.count(FishUpload.id)
    ).group_by(FishUpload.species_label).all()
    
    return render_template('stats.html', 
                         total_uploads=total_uploads,
                         species_counts=species_counts)

# Initialize database
with app.app_context():
    db.create_all()
    ensure_upload_dir()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
