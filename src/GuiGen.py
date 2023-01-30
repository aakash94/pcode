import os
import numpy as np
import glob
from pathlib import Path
import cv2
import matplotlib.pyplot as plt
import string
from sklearn.model_selection import train_test_split


class GuiGen():

    def __init__(self, path_root):
        self.path_root = path_root
        self.path_images = os.path.join(self.path_root, "IMAGES", "")
        self.path_guis = os.path.join(self.path_root, "TEXT_LABELS", "")

    def pyplot_image(self, image:np.ndarray):
        plt_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.imshow(plt_image)
        plt.show()

    def generate_code(self, img: np.ndarray) -> str:
        raise NotImplemented

    def get_file_names(self):
        files = glob.glob(pathname=self.path_images)
        file_names = []
        for file in files:
            file = Path(file).stem
            file_names.append(file)

    def get_images(self, extension="png") -> list:
        full_path = self.path_images + "*." + extension
        files = glob.glob(pathname=full_path)
        images = []
        for file in files:
            image = cv2.imread(file)
            images.append(image)
        return images

    def get_guis(self, extension="gui") -> list:
        full_path = self.path_guis + "*." + extension
        files = glob.glob(pathname=full_path)
        guis = []
        for file in files:
            with open(file, 'r') as f:
                text = f.read()
                guis.append(text)
        return guis

    def get_complete_dataset(self) -> list:
        images = self.get_images()
        guis = self.get_guis()
        return list(zip(images, guis))

    def get_test_train_dataset(self, test_size=0.33, random_state=42):
        x = self.get_images()
        y = self.get_guis()
        dataset = self.get_complete_dataset()
        dataset_train, dataset_test = train_test_split(dataset, test_size=test_size, random_state=random_state)
        return dataset_train, dataset_test

    def compare_gui_code(self, code_1: str, code_2: str) -> bool:
        # this removes all spaces,
        # and converts every character to lowercase before comparing.
        # print(code_1)
        # print(code_2)
        c1 = code_1.translate({ord(c): None for c in string.whitespace})
        c2 = code_2.translate({ord(c): None for c in string.whitespace})
        return c1.casefold() == c2.casefold()


def main():
    print("Get Gui")
    path_root = os.path.join("..", "Assignment_Data", "D2", "")
    gg = GuiGen(path_root=path_root)
    d_train, d_test = gg.get_test_train_dataset()
    print(len(d_train))
    print(len(d_test))
    print(d_test[0])


if __name__ == "__main__":
    main()
