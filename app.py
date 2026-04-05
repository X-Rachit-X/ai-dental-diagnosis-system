from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from werkzeug.utils import secure_filename
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import warnings
warnings.filterwarnings('ignore')

# Use double underscores for __name__
app = Flask(__name__) 

# Load model - Use .keras format for better compatibility
try:
    model = load_model('teeth_model.keras', compile=False)
    logger.info("✓ Model loaded successfully!")
except Exception as e:
    logger.error(f"✗ Failed to load model: {e}")
    raise

class_names = ['Calculus', 'Mouth Ulcer', 'Tooth Discoloration', 'Caries', 'Hypodontia']

# Define the path for uploads - separate from static assets
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'classes': class_names
    }), 200

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'file' not in request.files:
            logger.warning("No file in request")
            return render_template('index.html', error='No file uploaded'), 400
            
        file = request.files['file']

        if file.filename == '':
            logger.warning("Empty filename")
            return render_template('index.html', error='No file selected'), 400

        if file:
            filename = secure_filename(file.filename)
            
            # Validate file extension
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
            if not '.' in filename or filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                logger.warning(f"Invalid file type: {filename}")
                return render_template('index.html', error='Invalid file type. Please upload an image.'), 400
            
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Save the file
            file.save(filepath)
            logger.info(f"File saved: {filename}")

            # Load the saved image and resize it to 128x128
            img = image.load_img(filepath, target_size=(128, 128))
            
            x = image.img_to_array(img)
            
            # Add normalization (dividing by 255)
            x = x / 255.0 
            
            # Add a batch dimension
            x = np.expand_dims(x, axis=0)
            
            # Make the prediction with verbose=0 to suppress output
            preds = model.predict(x, verbose=0)
            
            # Get the class name
            pred_class = class_names[np.argmax(preds)]
            
            # Get confidence score
            confidence = float(np.max(preds) * 100)
            
            logger.info(f"Prediction: {pred_class} ({confidence:.1f}%)")

            # Pass the prediction back to the template
            # Note: Image is deleted after prediction, so no image display needed
            result = render_template('index.html', 
                                    prediction=pred_class, 
                                    confidence=f"{confidence:.1f}")
            
            # Clean up: Delete the uploaded file after prediction to prevent overflow
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    logger.info(f"File deleted: {filename}")
            except Exception as e:
                logger.error(f"Error deleting file: {e}")
            
            return result
        
        return render_template('index.html', error='An error occurred during prediction'), 500
        
    except Exception as e:
        logger.error(f"Prediction error: {e}", exc_info=True)
        return render_template('index.html', error='An error occurred during prediction'), 500

# Use double underscores for __name__ and '__main__'
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)