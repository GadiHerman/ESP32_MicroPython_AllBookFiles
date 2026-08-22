import cv2
import numpy as np
from PIL import Image, ImageOps
#from keras.models import load_model
from tf_keras.models import load_model
import urllib.request

# Disable scientific notation for cleaner console output
np.set_printoptions(suppress=True)

# Load the trained Keras model and labels
model = load_model("keras_Model.h5", compile=False)
class_names = open("labels.txt", "r").readlines()

# Set ESP32 IP address on local network
# Replace this with the actual IP printed by ESP32 console
ESP32_IP = "http://10.0.0.27"

# Open default computer webcam
camera = cv2.VideoCapture(0)

# Create input array shape expected by model (1, 224, 224, 3)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

print("Starting real-time image recognition loop...")

while True:
    # Capture frame-by-frame from webcam
    success, frame = camera.read()
    if not success:
        print("Failed to capture image from camera")
        break

    # Convert OpenCV BGR frame to PIL RGB image
    cv2_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(cv2_rgb)

    # Resize and center crop image to 224x224
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # Convert image to numpy array and normalize pixel values
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array

    # Perform prediction
    prediction = model.predict(data, verbose=0)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    confidence_score = prediction[0][index]

    print("Detected Class:", class_name[2:], "| Confidence:", confidence_score)

    # If Target class (index 0) detected with high confidence (> 80%)
    if index == 0 and confidence_score > 0.8:
        print("Target object detected! Sending ON command to ESP32...")
        try:
            urllib.request.urlopen(ESP32_IP + "/led/on", timeout=1)
        except Exception as error:
            print("Failed to reach ESP32 API:", error)
    else:
        print("Target not detected. Sending OFF command to ESP32...")
        try:
            urllib.request.urlopen(ESP32_IP + "/led/off", timeout=1)
        except Exception as error:
            print("Failed to reach ESP32 API:", error)

    # Display video stream in window
    cv2.imshow("Webcam Recognition Stream", frame)

    # Press 'q' key to exit loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("User requested exit. Closing application...")
        break

# Release camera resource and close display windows
camera.release()
cv2.destroyAllWindows()
