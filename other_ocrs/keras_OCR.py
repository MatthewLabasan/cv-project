import keras_ocr
from matplotlib import pyplot as plt
import numpy as np

# keras-ocr will auto download pretained model
pipeline = keras_ocr.pipeline.Pipeline()

images = [keras_ocr.tools.read('test_images/GUI.png')]

# print shape
print(np.shape(images))

prediction_groups = pipeline.recognize(images)

fig, axs = plt.subplots(nrows=len(images), figsize=(20, 20))
for ax, image, predictions in zip(axs, images, prediction_groups):
    keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)