import os
import cv2
import numpy as np
from GuiGen import GuiGen


class D1(GuiGen):
    def __init__(self):
        path_root = os.path.join("..", "Assignment_Data", "D1", "")
        super().__init__(path_root=path_root)

    def get_rects_row(self, img: np.ndarray) -> list:
        row_threshold = 5
        lower_bound = np.array([250, 250, 250])
        upper_bound = np.array([255, 255, 255])
        i2 = cv2.inRange(img, lowerb=lower_bound, upperb=upper_bound)
        i2 = cv2.bitwise_not(i2)
        contours, hierarchy = cv2.findContours(i2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rects = []
        for c in contours:
            x, y, width, height = cv2.boundingRect(c)
            if height > 30 and width > 30:
                rect = (x, y, width, height)
                rects.append(rect)
        rows = []
        row = []

        for r in rects:
            if 0 == len(row):
                row.append(r)
                continue
            last_x, last_y, last_w, last_h = row[-1]
            x, y, w, h = r
            if abs(last_y - y) < row_threshold:
                # same row
                row.append(r)

            else:
                # new row encounteres
                row.reverse()
                rows.append(row)
                row = []
                row.append(r)
        row.reverse()
        rows.append(row)
        rows.reverse()

        return rows

    def get_inrange_count(self, img: np.ndarray, colour: np.ndarray) -> int:
        tolerance = 2
        lowerb = colour - tolerance
        upperb = colour + tolerance
        i2 = cv2.inRange(img, lowerb=lowerb, upperb=upperb)
        # self.pyplot_image(i2)
        nz_count = cv2.countNonZero(i2)
        # print("NZ ",nz_count)
        return nz_count

    def get_btn_colour(self, img: np.ndarray, rect) -> str:
        x, y, w, h = rect
        image = img[y:y + h, x:x + w].copy()
        min_threshold = 100
        bgr_active = np.array([170, 178, 32])
        bgr_inactive = np.array([250, 206, 135])
        bgr_green = np.array([21, 179, 24])
        bgr_orange = np.array([51, 179, 245])
        bgr_red = np.array([51, 79, 245])

        if self.get_inrange_count(img=image, colour=bgr_active) > min_threshold:
            return "btn-active"
        elif self.get_inrange_count(img=image, colour=bgr_inactive) > min_threshold:
            return "btn-inactive"
        elif self.get_inrange_count(img=image, colour=bgr_green) > min_threshold:
            return "small-title, text, btn-green"
        elif self.get_inrange_count(img=image, colour=bgr_orange) > min_threshold:
            return "small-title, text, btn-orange"
        elif self.get_inrange_count(img=image, colour=bgr_red) > min_threshold:
            return "small-title, text, btn-red"
        return ""

    def generate_code(self, img: np.ndarray) -> str:
        rows = self.get_rects_row(img=img)
        # print(rows)
        code = ""
        for i, row in enumerate(rows):
            if i == 0:
                # Header row
                code = code + "header {\n"
                for rect in row:
                    colour = self.get_btn_colour(img=img, rect=rect)
                    code = code + colour + ", "
                code = code[:-2]
                code = code + "\n}"
            else:
                code = code + "\nrow {\n"
                box_count = len(row)
                button_text = ""
                if box_count == 1:
                    button_text = "\nsingle {\n"
                elif box_count == 2:
                    button_text = "\ndouble {\n"
                elif box_count == 3:
                    button_text = "\ntriple {\n"
                elif box_count == 4:
                    button_text = "\nquadruple {\n"

                for rect in row:
                    colour = self.get_btn_colour(img=img, rect=rect)
                    code = code + button_text + colour + "\n}"
                code = code + "\n}"

        # self.pyplot_image(img)
        return code

    def get_codes(self):
        dataset = self.get_complete_dataset()
        generated_codes = []
        for image, original_code in dataset:
            code = self.generate_code(img=image)
            if self.compare_gui_code(original_code, code):
                # print("Success")
                pass
            else:
                print("Fail")
            # self.pyplot_image(image)
            generated_codes.append(code)
            # break
        return generated_codes

    def get_code_from_image_path(self, image_path: str) -> str:
        image = cv2.imread(image_path)
        return self.generate_code(img=image)


def main():
    print("D1")
    d1 = D1()
    codes = d1.get_codes()

    # btn-active
    # btn-inactive
    # btn-green
    # btn-red
    # btn-orange


if __name__ == "__main__":
    main()
