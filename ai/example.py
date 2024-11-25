
# TF for image segmentation model

import tensorflow
import numpy
from PIL import Image
import matplotlib.pyplot as plt

model = tensorflow.saved_model.load('./')
classes = [ "empty" ,  "Pill" , ]

img = Image.open("image.jpg").convert('RGB')
img = img.resize((256, 256))
inp_numpy = numpy.array(img)[None]


inp = tensorflow.constant(inp_numpy, dtype='float32')

segmentation_output = model(inp)[0].numpy().argmax(-1)

plt.imshow(segmentation_output)
plt.show()