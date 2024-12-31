import numpy as np

def bounding_box(img_nd):
    """Gibt eine Bounding Box zurück"""
    
    coords = np.argwhere(img_nd)
    y_min, x_min = coords.min(axis=0)
    y_max, x_max = coords.max(axis=0) + 1
    return (x_min, y_min, x_max, y_max)
