from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class AnalysisSession(db.Model):
    """Model to store analysis sessions and results"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    session_id = db.Column(db.String(64), unique=True, nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    he_image_path = db.Column(db.String(500), nullable=False)
    ihc_image_path = db.Column(db.String(500))
    
    # Prediction results
    her2_prediction = db.Column(db.String(20))  # positive, negative, equivocal
    confidence_score = db.Column(db.Float)
    cancer_grade = db.Column(db.String(10))
    biomarker_percentage = db.Column(db.Float)
    staining_intensity = db.Column(db.String(20))  # weak, moderate, strong
    
    # Analysis metadata
    processing_status = db.Column(db.String(20), default='uploaded')  # uploaded, processing, completed, failed
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<AnalysisSession {self.session_id}>'

class ReportData(db.Model):
    """Model to store generated report data"""
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(64), db.ForeignKey('analysis_session.session_id'), nullable=False)
    report_type = db.Column(db.String(50), nullable=False)  # diagnostic, research
    
    # Report content
    summary = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    technical_notes = db.Column(db.Text)
    
    # Quantitative analysis
    positive_cell_count = db.Column(db.Integer)
    total_cell_count = db.Column(db.Integer)
    stained_area_percentage = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    session = db.relationship('AnalysisSession', backref=db.backref('reports', lazy=True))
    
    def __repr__(self):
        return f'<ReportData {self.session_id}>'

class User(UserMixin, db.Model):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    institution = db.Column(db.String(100))
    role = db.Column(db.String(50), default='researcher')
    active_status = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    sessions = db.relationship('AnalysisSession', backref='user', lazy=True)
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f'<User {self.username}>'
