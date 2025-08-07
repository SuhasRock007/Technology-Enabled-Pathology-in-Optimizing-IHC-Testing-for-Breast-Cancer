-- Virtual IHC Analysis System Database Schema
-- For XAMPP MySQL Setup
-- Run this script in phpMyAdmin or MySQL command line

-- Create database
CREATE DATABASE IF NOT EXISTS virtual_ihc_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE virtual_ihc_db;

-- Users table
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    institution VARCHAR(100),
    role VARCHAR(50) DEFAULT 'researcher',
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
);

-- Analysis sessions table
CREATE TABLE IF NOT EXISTS analysis_session (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    session_id VARCHAR(64) NOT NULL UNIQUE,
    original_filename VARCHAR(255) NOT NULL,
    he_image_path VARCHAR(500) NOT NULL,
    ihc_image_path VARCHAR(500),
    her2_prediction VARCHAR(20),
    confidence_score FLOAT,
    cancer_grade VARCHAR(10),
    biomarker_percentage FLOAT,
    staining_intensity VARCHAR(20),
    processing_status VARCHAR(20) DEFAULT 'uploaded',
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

-- Report data table
CREATE TABLE IF NOT EXISTS report_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(64) NOT NULL,
    report_type VARCHAR(50) NOT NULL,
    summary TEXT,
    recommendations TEXT,
    technical_notes TEXT,
    positive_cell_count INT,
    total_cell_count INT,
    stained_area_percentage FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES analysis_session(session_id) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX idx_user_username ON user(username);
CREATE INDEX idx_user_email ON user(email);
CREATE INDEX idx_session_user ON analysis_session(user_id);
CREATE INDEX idx_session_status ON analysis_session(processing_status);
CREATE INDEX idx_session_created ON analysis_session(created_at);
CREATE INDEX idx_report_session ON report_data(session_id);

-- Insert sample admin user (password: admin123)
-- Note: In production, use stronger passwords
INSERT INTO user (username, email, password_hash, first_name, last_name, role) 
VALUES (
    'admin', 
    'admin@virtualihc.demo', 
    'scrypt:32768:8:1$LGZEsQUYLQcH0MdO$1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef', 
    'Admin', 
    'User', 
    'administrator'
) ON DUPLICATE KEY UPDATE id=id;

-- Insert sample researcher user (password: demo123)
INSERT INTO user (username, email, password_hash, first_name, last_name, institution, role) 
VALUES (
    'demo_user', 
    'demo@virtualihc.demo', 
    'scrypt:32768:8:1$LGZEsQUYLQcH0MdO$abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890', 
    'Demo', 
    'Researcher', 
    'Medical University', 
    'researcher'
) ON DUPLICATE KEY UPDATE id=id;

-- Display setup completion message
SELECT 'Virtual IHC Database Setup Complete!' as Status;
SELECT 'Default login: admin / admin123 or demo_user / demo123' as Info;