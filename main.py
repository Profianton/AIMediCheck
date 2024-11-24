from cam import capture
from glob import glob
while True:
    input("Ready")
    path=f"images/{len(glob('images/*'))}.png"
    capture().save(path)