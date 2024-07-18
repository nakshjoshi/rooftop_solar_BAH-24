import rasterio
import matplotlib.pyplot as plt
import numpy as np
import cv2

# Paths to your TIFF files
band2_path = 'datasets/data/BAND2.tif'
band3_path = 'datasets/data/BAND3.tif'
band4_path = 'datasets/data/BAND4.tif'

# Load the bands
with rasterio.open(band2_path) as src:
    band2 = src.read(1)
with rasterio.open(band3_path) as src:
    band3 = src.read(1)
with rasterio.open(band4_path) as src:
    band4 = src.read(1)

# Stack the bands to create a 3-channel image
combined_image = np.stack((band2, band3, band4), axis=-1)

# Resize and preprocess the image
def preprocess_image(image, target_size=(256, 256)):
    # Resize the image
    image_resized = cv2.resize(image, target_size)
    # Normalize the image
    image_normalized = cv2.normalize(image_resized, None, 0, 255, cv2.NORM_MINMAX)

    return image_normalized

# Preprocess the combined image
preprocessed_image = preprocess_image(combined_image)

# Plot the preprocessed image
plt.figure(figsize=(10, 10))
# Since it's a 3-channel image, we can use matplotlib's imshow directly
plt.imshow(preprocessed_image, cmap='gray')
plt.title('Preprocessed Resourcesat-2 LISS-4 Image')
plt.show()
