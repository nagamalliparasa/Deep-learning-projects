import cv2

def preprocess_image_fc(image_path, target_size=(224, 224)):
    try:
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Unable to load image at path: {image_path}")
            return None
        image = cv2.resize(image, target_size)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image / 255.0
        return image
    except Exception as e:
        print(f"Exception during preprocessing image {image_path}: {e}")
        return None
    
    
def read_image(image_path):
    # Read the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    return image
    
def equalization(image):
    equalized_img = cv2.equalizeHist(image)
    return equalized_img

def preprocessing_image(image_path):
    image=read_image(image_path)
    equalized_image=equalization(image)
    return image,equalized_image