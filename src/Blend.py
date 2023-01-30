import glob
import numpy as np
import cv2
import os


def get_images(folder_name="D3", extension="png"):
    path = os.path.join("..", "Assignment_Data", folder_name, "IMAGES", "")
    save_path = os.path.join("..", "Assignment_Data", folder_name, "avg.png")
    path = path + "*." + extension
    files = glob.glob(pathname=path)
    images = []
    for file in files:
        image = cv2.imread(file)
        images.append(image)

    # Calculate blended image
    dst = images[0]
    for i in range(len(images)):
        if i == 0:
            pass
        else:
            alpha = 1.0 / (i + 1)
            beta = 1.0 - alpha
            dst = cv2.addWeighted(images[i], alpha, dst, beta, 0.0)

    # Save blended image
    cv2.imshow(folder_name, dst)
    cv2.imwrite(save_path, dst)
    cv2.waitKey(0)


def main():
    print("Hello World")
    get_images()


if __name__ == "__main__":
    main()
