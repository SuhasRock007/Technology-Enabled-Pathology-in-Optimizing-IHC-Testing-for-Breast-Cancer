# Overview

This is a medical imaging analysis system that provides virtual immunohistochemical (IHC) analysis from H&E (Hematoxylin and Eosin) stained tissue slides. The system uses a two-phase machine learning pipeline: first converting H&E images to virtual IHC images using a Pix2Pix GAN model, then analyzing the converted images for cancer classification and biomarker prediction. The application generates comprehensive diagnostic reports with quantitative analysis results.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Web Framework
- **Flask Application**: Built with Flask using SQLAlchemy ORM for database operations
- **Template Engine**: Jinja2 templates with Bootstrap 5 dark theme for responsive UI
- **Session Management**: Uses environment-based secret keys for session security

## Database Design
- **SQLAlchemy Models**: Two main entities - AnalysisSession for tracking image processing workflows, and ReportData for storing generated diagnostic reports
- **Database Support**: Configured for both SQLite (development) and PostgreSQL (production via DATABASE_URL environment variable)
- **Connection Pooling**: Implements connection pooling with ping checks for database reliability

## Machine Learning Pipeline
- **Two-Phase Processing**: 
  1. H&E to IHC conversion using Pix2Pix GAN architecture
  2. Cancer classification and biomarker analysis on converted images
- **Image Processing**: OpenCV and PIL for image preprocessing, normalization, and resizing
- **Model Architecture**: Placeholder implementation designed for TensorFlow/PyTorch model integration

## File Management
- **Upload System**: Secure file handling with configurable size limits (16MB default)
- **Directory Structure**: Separate folders for uploaded originals and generated outputs
- **File Validation**: Supports TIFF, PNG, and JPEG formats with secure filename handling

## Report Generation
- **PDF Reports**: ReportLab-based PDF generation with structured diagnostic information
- **Content Types**: Supports both diagnostic and research report formats
- **Quantitative Analysis**: Includes cell counting, staining intensity, and area percentage calculations

## Frontend Architecture
- **Responsive Design**: Bootstrap-based UI with dark theme support
- **Interactive Features**: File drag-and-drop, image preview, progress indicators
- **Chart Visualization**: Chart.js integration for displaying analysis results
- **Print Support**: Browser-based printing with optimized layouts

## Error Handling and Logging
- **Comprehensive Logging**: Debug-level logging throughout the application pipeline
- **Error Tracking**: Database storage of error messages and processing status
- **Status Management**: Multi-state workflow tracking (uploaded, processing, completed, failed)

# External Dependencies

## Core Web Technologies
- **Flask**: Web framework with SQLAlchemy ORM extension
- **Werkzeug**: WSGI utilities and security middleware
- **Bootstrap 5**: Frontend CSS framework with dark theme

## Machine Learning Stack
- **OpenCV**: Image processing and computer vision operations
- **PIL/Pillow**: Python imaging library for basic image operations
- **NumPy**: Numerical computing for array operations

## Report Generation
- **ReportLab**: PDF generation library for diagnostic reports
- **Chart.js**: Client-side charting for result visualization

## Development Tools
- **Feather Icons**: Icon library for UI components
- **JavaScript**: Client-side functionality for file handling and UI interactions

## Database Support
- **SQLite**: Default development database
- **PostgreSQL**: Production database (via DATABASE_URL configuration)

## File System Dependencies
- **Local Storage**: File upload and generated content storage
- **Secure Filename Handling**: Werkzeug utilities for file security