# Local XAMPP Setup Instructions

## Prerequisites
1. Install XAMPP with PHP and MySQL
2. Install Python 3.11+
3. Install pip (Python package manager)

## Python Dependencies
Install these packages using pip:

```bash
pip install Flask==3.0.0
pip install Flask-Login==0.6.3
pip install Flask-SQLAlchemy==3.1.1
pip install PyMySQL==1.1.0
pip install Werkzeug==3.0.1
pip install email-validator==2.1.0
pip install matplotlib==3.8.2
pip install numpy==1.24.3
pip install opencv-python==4.8.1.78
pip install pandas==2.1.4
pip install Pillow==10.1.0
pip install reportlab==4.0.7
pip install scikit-image==0.22.0
pip install seaborn==0.13.0
pip install tensorflow==2.15.0
pip install torch==2.1.2
pip install torchvision==0.16.2
```

## Database Setup
1. Start XAMPP and enable MySQL
2. Open phpMyAdmin (http://localhost/phpmyadmin)
3. Create a new database named: `virtual_ihc_db`
4. The application will automatically create the tables when first run

## Running the Application
```bash
python main.py
```

The application will be available at: http://localhost:5000

## Configuration
- Database: MySQL (localhost, root user, no password)
- Upload folder: uploads/
- Generated files folder: generated/
- Max file size: 16MB