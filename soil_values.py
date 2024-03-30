import numpy as np
import h5py
from tensorflow.keras.preprocessing import image

# Load the pre-trained model using h5py
def load_model(model_path):
    with h5py.File(model_path, 'r') as f:
        model_weights = []
        for layer in f['model_weights'].values():
            model_weights.append(layer.value)
    return model_weights


# Define a function to preprocess the input image
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize the image
    return img_array


# Define a function to build the model
def build_model():
    # Define your model architecture here
    # Example:
    # model = ...  # Define your model using Keras Sequential or Functional API
    return model


# Define a function to make predictions
def predict_soil_type(model_weights, img_path):
    # Preprocess the input image
    img_array = preprocess_image(img_path)

    # Load the model architecture
    model = build_model()  # Define this function to build your model architecture

    # Set the model weights
    model.set_weights(model_weights)

    # Make predictions
    predictions = model.predict(img_array)

    # Decode the predictions
    soil_types = ['Clayey Soil', 'Black Soil', 'Sandy Soil', 'Red Soil', 'Laterite Soil']
    predicted_index = np.argmax(predictions)
    predicted_soil_type = soil_types[predicted_index]

    # Display the predicted soil type
    print("Predicted Soil Type:", predicted_soil_type)
    print("Confidence:", predictions[0][predicted_index])


# Get the input image path from the user
img_path = input("A:\ml_project\gettyimages-640955400-612x612.jpg ")

# Load the model weights
model_weights = load_model('SoilNet_93_86.h5')

# Make predictions
predict_soil_type(model_weights, img_path)
