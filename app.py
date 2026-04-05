from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from werkzeug.utils import secure_filename

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import warnings
warnings.filterwarnings('ignore')

# Use double underscores for __name__
app = Flask(__name__) 

# Load model - Use .keras format for better compatibility
model = load_model('teeth_model.keras', compile=False)
print("Model loaded successfully!")

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

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return 'No file uploaded'
        
    file = request.files['file']

    if file.filename == '':
        return 'No file selected'

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the file to the 'static' folder
        file.save(filepath)

        # *** THIS IS THE FIX ***
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

        # Pass the prediction and image path back to the template
        result = render_template('index.html', prediction=pred_class, img_path=filepath)
        
        # Clean up: Delete the uploaded file after prediction to prevent overflow
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"Error deleting file: {e}")
        
        return result

    return 'An error occurred during prediction'

# Use double underscores for __name__ and '__main__'
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)