from rembg import remove
from PIL import Image
input_path = 'test.jpg'
input_img=Image.open(input_path)
output = remove(input_img)
output_path = 'output.png'
output.save("output.png")