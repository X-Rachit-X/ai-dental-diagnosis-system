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

# Define the path for uploads - must be in static folder so Flask can serve it
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    logger.info(f"Created upload folder: {UPLOAD_FOLDER}")

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

@app.route('/cleanup', methods=['POST'])
def cleanup_old_files():
    """
    Optional cleanup endpoint to remove old uploaded files
    Call this periodically or manually to prevent disk overflow
    """
    try:
        import time
        max_age = 3600  # 1 hour in seconds
        deleted_count = 0
        
        for filename in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                # Check if file is older than max_age
                file_age = time.time() - os.path.getmtime(filepath)
                if file_age > max_age:
                    os.remove(filepath)
                    deleted_count += 1
                    logger.info(f"Cleaned up old file: {filename}")
        
        return jsonify({
            'status': 'success',
            'deleted_files': deleted_count
        }), 200
    except Exception as e:
        logger.error(f"Cleanup error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

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

            # Create web-accessible path for the image
            # Path should be relative to static folder for Flask to serve it
            img_path = f"uploads/{filename}"  # Flask will prepend 'static/' automatically
            
            # Pass the prediction and image path back to the template
            result = render_template('index.html', 
                                    prediction=pred_class, 
                                    confidence=f"{confidence:.1f}",
                                    img_path=img_path)
            
            # DO NOT delete the file here - frontend needs to display it
            # Optional: Implement cleanup later (e.g., cron job to delete old files)
            
            return result
        
        return render_template('index.html', error='An error occurred during prediction'), 500
        
    except Exception as e:
        logger.error(f"Prediction error: {e}", exc_info=True)
        return render_template('index.html', error='An error occurred during prediction'), 500

# Use double underscores for __name__ and '__main__'
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)