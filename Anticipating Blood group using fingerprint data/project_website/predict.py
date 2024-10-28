from preprocessing import preprocess_image_fc, preprocessing_image
import numpy as np 
import cv2
def model_predict_fc(img_path, model):
    image = preprocess_image_fc(img_path)
    if image is None:
        return 'Wrong Input'
    image = np.expand_dims(image, axis=0)
    prediction = model.predict(image)
    pred=prediction[0][0]
    if pred >= 0.4:
        return 1
    else:
        return 0
    


lst=['A+', 'A-', 'AB+', 'AB-', 'B+', 'B-', 'O+', 'O-']
encoding={}

for idx,blood_type in enumerate(lst):
    encoding[idx]=blood_type


def predict_image(model, image_path):
    # Preprocess the image
    image,equalized_image = preprocessing_image(image_path)
    # img = cv2.imread(equalized_image, cv2.IMREAD_GRAYSCALE)
    if equalized_image is None:
        print(f"Failed to read {image_path}")
        return None
    img = cv2.resize(equalized_image, (32, 32))
    image_normalized = img / 255.0
        
    # Reshape the image to match the input shape of the model (1, 32, 32, 1)
    image_reshaped = np.reshape(image_normalized, (1, 32, 32, 1))
    
    
    # Make a prediction
    predictions = model.predict(image_reshaped)
    
    # Get the class label with the highest probability
    predicted_class = np.argmax(predictions, axis=1)[0]
    predicted_class=encoding[predicted_class]
    
    
    return predicted_class