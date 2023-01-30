import string
import re
import os
import glob
from collections import Counter
from collections import defaultdict
from matplotlib import pyplot as plt

from D1 import D1
from D2 import D2
from D3 import D3


def get_tokens(txt: str) -> list:
    txt = txt.translate({ord(c): None for c in string.whitespace})
    tokens = re.split(r'[{,}]', txt)
    return tokens


def token_count(folder_name="D3"):
    path = os.path.join("..", "Assignment_Data", folder_name, "TEXT_LABELS", "")
    path = path + "*.gui"
    files = glob.glob(pathname=path)
    print(path)
    print(files)
    counts = Counter()

    for file in files:
        with open(file, 'r') as f:
            text = f.read()
            tokens = get_tokens(text)
            token_count = Counter(tokens)
            counts = counts + token_count

    # print(counts)
    del counts['']
    plt.bar(counts.keys(), counts.values())
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.25)
    plt.show()


def generate_gui():
    image_path = os.path.join("..", "Assignment_Data", "D1", "IMAGES", "1FE0BFB5-82F1-47CB-AECD-ABBC6B34CCC8.png")
    model = D1()
    gui_code = model.get_code_from_image_path(image_path=image_path)
    print(gui_code)


def main():
    print("Hello World")
    generate_gui()



if __name__ == "__main__":
    main()
