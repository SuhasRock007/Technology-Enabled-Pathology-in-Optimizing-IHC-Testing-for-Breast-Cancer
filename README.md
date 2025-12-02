# 🧬 IHCGenie — Breast Cancer H&E to IHC Conversion & Severity Prediction  
### AI-powered Histopathology Image Processing System  
*(Learning/Academic Project)*

This project demonstrates an end-to-end workflow for **processing breast cancer histopathology images**, converting **H&E images into IHC-style images**, and performing **cancer severity prediction** using a deep-learning backend.

It is built using **Flask**, **Python**, and **Machine Learning**, with a simple web UI for uploading and analyzing images.

> ⚠️ Note: This is a learning project implemented using concepts and resources from online tutorials, research papers, and YouTube references.

---

## 📌 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Architecture](#project-architecture)
- [Folder Structure](#folder-structure)
- [Working Process](#working-process)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)
- [Credits / References](#credits--references)

---

## 🧩 Overview

Pathologists often rely on H&E-stained images for diagnosis, but **IHC (Immunohistochemistry)** provides more specific biomarker-level insight.  
Since IHC staining is expensive and time-consuming, this project attempts to:

### **Phase 1 — Convert H&E → IHC-like image**  
Using a deep learning image-translation model.

### **Phase 2 — Predict cancer severity**  
Using the generated image or extracted features.

---

## ⭐ Features

- 🔬 **Upload H&E image for analysis**  
- 🧪 **Generate IHC-style output**  
- 📊 **Predict severity / classification score**  
- 💾 **Save analysis sessions in database**  
- 🖼️ **Show before/after images**  
- 🌐 **User-friendly Flask web interface**

---

## 🛠 Tech Stack

| Component | Technology |
|----------|------------|
| Backend | Python, Flask |
| ML / DL | PyTorch / TensorFlow |
| Image Processing | OpenCV, Pillow |
| Frontend | HTML, CSS, Jinja Templates |
| Database | SQLite / MySQL |
| Deployment | Localhost (Flask) |

---

## 🏗 Project Architecture
User Upload → Preprocessing → H&E → IHC Generator Model → Severity Predictor → Report Output

---

## 📁 Folder Structure
```
IHCGenie/
│── app.py
│── routes.py
│── utils.py
│── models/
│── static/
│   ├── css/
│   ├── js/
│   └── images/
│── templates/
│   ├── upload.html
│   ├── results.html
│   └── home.html
│── database/
│   └── sessions.db
│── uploads/
│── outputs/
│── README.md
│── requirements.txt
└── .gitignore
```

---

## 🔄 Working Process

1. User uploads an H&E image  
2. Backend saves file into `/uploads/`  
3. ML model converts it → IHC-style image  
4. Severity prediction model evaluates the image  
5. Results saved in database + displayed on UI  

---

## 🧪 Installation

### 1️⃣ Clone this repository
```bash
git clone https://github.com/YOUR_USERNAME/IHCGenie.git
cd IHCGenie
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Add your ML models
Place your model files in:
```
models/
```
(They are ignored from Git for size reasons.)

---

## ▶️ Running the Application

### 4️⃣ Start the Flask server
```bash
python app.py
```

Then open:
```
http://127.0.0.1:5000
```

---

## 🚀 Future Enhancements

### 5️⃣ Planned Improvements
- Deploy on cloud (AWS / Render / Azure)  
- Add multi-class severity prediction  
- Improve IHC conversion quality  
- Add progress bar for processing  
- Support whole-slide images (WSI)

---

## 📚 Credits / References

### 6️⃣ Learning Sources
- Flask documentation  
- PyTorch / TensorFlow tutorials  
- YouTube tutorials  
- Research papers on H&E → IHC conversion  
- Roboflow datasets & examples  

---
