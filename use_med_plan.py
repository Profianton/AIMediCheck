# %%
#from analyse import analyse
from PIL import Image
import json
from analyse import analyse
from PIL import Image

# %%
def read_user(name):
    with open(f"users/{name}.json",encoding="UTF-8")as f:
        return json.load(f)

# %%
user=read_user("user1")

# %%
img=Image.open(r"images\31.png")

# %%
pills_in_sample=analyse(img,user.keys())

# %%
out_img=Image.new("RGB",(img.width,int(img.height/8)))
out_img.paste(img.resize((int(img.width/8),int(img.height/8))),(0,0))
for i in range(sum(pills_in_sample.values())):
    out_img.paste(Image.open(f"{i}.png").resize((int(img.height/8),int(img.height/8))),(int(img.width/8)+int(img.height/8)*i,0))
out_img.save("img.png")
out_img

# %%
print("\n".join([f"{count} {pill_type}" for pill_type,count in pills_in_sample.items()]))

