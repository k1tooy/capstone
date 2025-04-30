import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
import pathlib

loaded_model = load_model(os.path.join("models", "balut_classifier.h5"))
batch_size = 32
img_height = 180
img_width = 180
class_names = ["balut", "bugok", "penoy"]

# Define the test images directory
test_dir = pathlib.Path("tests")

# Loop through all images in the test directory
for image_path in test_dir.glob("*.jpg"):  # Adjust for different formats if needed
    img = tf.keras.utils.load_img(image_path, target_size=(img_height, img_width))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    # Make prediction
    predictions = loaded_model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    # Print results
    print(
        "Image: {}\nPredicted: {} with {:.2f}% confidence\n".format(
            image_path.name, class_names[np.argmax(score)], 100 * np.max(score)
        )
    )
