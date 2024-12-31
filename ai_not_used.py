import tensorflow
import numpy as np

model = tensorflow.saved_model.load('segment')
classes = ["empty",  "pill", ]

def segment(img):
    img = img.resize((256, 256))
    inp_numpy = np.array(img)[None]
    inp = tensorflow.constant(inp_numpy, dtype='float32')

    segmentation_output = model(inp)[0].numpy().argmax(-1)
    return segmentation_output
