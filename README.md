# 🦷 SmileCare Dental - AI Tooth Disease Detection

An AI-powered web application that uses deep learning to detect dental diseases from uploaded images. Built with Flask and TensorFlow, this application can identify 5 common dental conditions with high accuracy.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Features

- **AI-Powered Detection**: Uses a trained CNN model to identify dental conditions
- **5 Disease Classifications**:
  - 🦴 Calculus (Tartar buildup)
  - 🔴 Mouth Ulcer
  - 🟡 Tooth Discoloration
  - 🕳️ Caries (Cavities)
  - 🦷 Hypodontia (Missing teeth)
- **User-Friendly Interface**: Modern, responsive web UI with dark theme
- **Instant Results**: Upload an image and get immediate predictions
- **Automatic Cleanup**: Uploaded images are automatically deleted to save storage

## 🚀 Live Demo

[**Try the Live App**](#) *(Add your deployment URL here after deploying)*

## 📋 Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- 10MB+ free disk space for the model

## 🛠️ Installation

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/tooth-disease-detection.git
   cd tooth-disease-detection
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://127.0.0.1:5000`

## 📁 Project Structure

```
tooth-disease-detection/
│
├── app.py                  # Main Flask application
├── teeth_model.h5          # Pre-trained TensorFlow model
├── requirements.txt        # Python dependencies
├── Procfile               # Deployment configuration
├── runtime.txt            # Python version specification
├── .gitignore             # Git ignore rules
│
├── templates/
│   └── index.html         # Frontend interface
│
├── static/                # Static assets (CSS, demo images)
│   └── [sample images]
│
└── uploads/               # Temporary folder for uploads (auto-cleaned)
    └── .gitkeep
```

## 🎨 How It Works

1. **Upload Image**: User uploads a dental image through the web interface
2. **Preprocessing**: Image is resized to 128x128 pixels and normalized
3. **Prediction**: TensorFlow model analyzes the image
4. **Results**: Predicted condition is displayed to the user
5. **Cleanup**: Uploaded image is automatically deleted

## 🌐 Deployment

### Deploy to Render (Free)

1. **Push code to GitHub** (see instructions below)

2. **Create Render account**
   - Go to [render.com](https://render.com)
   - Sign up with your GitHub account

3. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Use these settings:
     - **Name**: `smilecare-dental` (or your choice)
     - **Environment**: `Python`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
     - **Instance Type**: `Free`

4. **Deploy**
   - Click "Create Web Service"
   - Wait 3-5 minutes for deployment
   - Your app will be live at `https://your-app-name.onrender.com`

### Alternative Platforms

- **Railway**: [railway.app](https://railway.app) - Easy deployment, free tier
- **Heroku**: [heroku.com](https://heroku.com) - Classic platform (paid)
- **PythonAnywhere**: [pythonanywhere.com](https://pythonanywhere.com) - Good for beginners

## 📤 Pushing to GitHub

```bash
# Initialize Git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: SmileCare Dental AI app"

# Create repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## 🧪 Testing

Upload a sample dental image to test the application:
1. Navigate to the home page
2. Click "Choose File" or drag and drop an image
3. Click "Analyze Image"
4. View the predicted condition

## 🔧 Configuration

- **Max Upload Size**: 16MB (configurable in `app.py`)
- **Image Input Size**: 128x128 pixels (automatic resize)
- **Supported Formats**: JPG, JPEG, PNG

## 📊 Model Information

- **Architecture**: Convolutional Neural Network (CNN)
- **Input Size**: 128x128x3 (RGB)
- **Output Classes**: 5 dental conditions
- **Framework**: TensorFlow/Keras
- **Model File**: `teeth_model.h5` (~10MB)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

**This application is for educational purposes only.** It should not be used as a substitute for professional dental diagnosis. Always consult with a qualified dentist for proper medical advice.

## 👨‍💻 Author

**Your Name**
- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- Project Link: [https://github.com/YOUR_USERNAME/tooth-disease-detection](https://github.com/YOUR_USERNAME/tooth-disease-detection)

## 🙏 Acknowledgments

- SEM 5 Artificial Intelligence Course Project
- TensorFlow & Keras teams
- Flask framework developers

---

Made with ❤️ for better dental health awareness
