import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import LassoSelector
from PIL import Image, ImageDraw
from tkinter import Tk, filedialog


def openFile():
    file_path = filedialog.askopenfilename(
        title="Select Image File For Pixel Counting",
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif"),
            ("All Files", "*.*")
        ]
    )
    return file_path


window = Tk()
img_path = openFile()

img = Image.open(img_path).convert("RGB")
img_array = np.array(img)

# Setup figure
fig, ax = plt.subplots(figsize=(12, 8))
ax.imshow(img_array)
ax.set_title("Draw lasso to select area")

# Display text object to update pixel count
pixel_count_text = ax.text(0.01, -0.05, '', transform=ax.transAxes, fontsize=12, color='red')

# We store the current polygon artist here to remove it before drawing new one
current_polygon = []

# Function to process lasso selection
def onselect(verts):
    global current_polygon

    # Clear previous polygon if exists
    if current_polygon:
        for poly in current_polygon:
            poly.remove()
        current_polygon.clear()

    # Create mask from lasso vertices
    mask_img = Image.new('L', (img_array.shape[1], img_array.shape[0]), 0)
    ImageDraw.Draw(mask_img).polygon(verts, outline=1, fill=1)
    mask = np.array(mask_img).astype(bool)

    # Count white pixels inside mask
    white_pixels = np.all(img_array >= 250, axis=2)
    selected_white_pixels = np.logical_and(white_pixels, mask)
    count = np.sum(selected_white_pixels)

    # Update displayed pixel count
    ax.set_title(f"White pixels in selection: {count}")

    # Overlay the lasso polygon
    verts_np = np.array(verts)
    poly, = ax.plot(verts_np[:, 0], verts_np[:, 1], color='cyan', linewidth=1.5)
    current_polygon.append(poly)

    plt.draw()

# Initialize lasso selector
lasso = LassoSelector(ax, onselect)
plt.show()
