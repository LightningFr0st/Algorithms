import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

import utils

images, labels = utils.load_dataset()

weights_input_to_hidden = np.random.uniform(-0.5, 0.5, (128, 784))
weights_hidden_to_output = np.random.uniform(-0.5, 0.5, (10, 128))
bias_input_to_hidden = np.zeros((128, 1)) #вектор смещений для скрытого слоя размером
bias_hidden_to_output = np.zeros((10, 1)) #вектор смещений для выходного слоя размером

epochs = 3
learning_rate = 0.01

for epoch in range(epochs):
    print(f"Iteration: {epoch}")

    for image, label in zip(images, labels):
        image = np.reshape(image, (-1, 1))
        label = np.reshape(label, (-1, 1))

        # Прямое распространение (до скрытого слоя)
        hidden_raw = bias_input_to_hidden + weights_input_to_hidden @ image
        hidden = 1 / (1 + np.exp(-hidden_raw)) # сигмоид

        # Прямое распространение (до выходного слоя)
        output_raw = bias_hidden_to_output + weights_hidden_to_output @ hidden
        output = 1 / (1 + np.exp(-output_raw))



        # Обратное распространение (выходной слой)
        delta_output = output - label
        weights_hidden_to_output += -learning_rate * delta_output @ np.transpose(hidden)
        bias_hidden_to_output += -learning_rate * delta_output

        # Обратное распространение (скрытый слой)
        delta_hidden = np.transpose(weights_hidden_to_output) @ delta_output * (hidden * (1 - hidden))
        weights_input_to_hidden += -learning_rate * delta_hidden @ np.transpose(image)
        bias_input_to_hidden += -learning_rate * delta_hidden


def load_and_predict():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
    if not file_path:
        return
    test_image = plt.imread(file_path, format="jpeg")

    gray = lambda rgb: np.dot(rgb[..., :3], [0.299, 0.587, 0.114])
    test_image = 1 - (gray(test_image).astype("float32") / 255)

    test_image = np.reshape(test_image, (test_image.shape[0] * test_image.shape[1]))
    image = np.reshape(test_image, (-1, 1))

    # Прямое распространение (до скрытого слоя)
    hidden_raw = bias_input_to_hidden + weights_input_to_hidden @ image
    hidden = 1 / (1 + np.exp(-hidden_raw))
    # Прямое распространение (до выходного слоя)
    output_raw = bias_hidden_to_output + weights_hidden_to_output @ hidden
    output = 1 / (1 + np.exp(-output_raw))

    pil_image = Image.fromarray((test_image.reshape(28, 28) * 255).astype(np.uint8))
    pil_image_resized = pil_image.resize((pil_image.width * 5, pil_image.height * 5), Image.NEAREST)
    photo_image = ImageTk.PhotoImage(image=pil_image_resized)

    image_label.config(image=photo_image)
    image_label.image = photo_image

    result_label.config(text=f"Letter: {output.argmax()}")


root = tk.Tk()
root.title("Perceptron")

button = tk.Button(root, text="Select", command=load_and_predict)
button.pack()

image_label = tk.Label(root)
image_label.pack()

result_label = tk.Label(root)
result_label.pack()

root.mainloop()
