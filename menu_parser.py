import re
from typing import List

import cv2 as cv
import numpy as np
import pytesseract
import util


class MenuParser:

    def __init__(self) -> None:
        c1_x_from, c1_x_to, c2_x_from, c2_x_to = 0.13, 0.43, 0.51, 0.80
        self._block_rois = [
            ((c1_x_from, 0.34), (c1_x_to, 0.44)),
            ((c2_x_from, 0.34), (c2_x_to, 0.44)),
            ((c1_x_from, 0.52), (c1_x_to, 0.65)),
            ((c2_x_from, 0.52), (c2_x_to, 0.65)),
            ((c1_x_from, 0.70), (c1_x_to, 0.80)),
            ((c2_x_from, 0.70), (c2_x_to, 0.80)),
        ]

    @staticmethod
    def _roi_img_relative(img, p1, p2):
        img_width = img.shape[1]
        img_height = img.shape[0]
        absolute_p1 = (int(p1[0] * img_width), int(p1[1] * img_height))
        absolute_p2 = (int(p2[0] * img_width), int(p2[1] * img_height))
        return img[absolute_p1[1]:absolute_p2[1], absolute_p1[0]:absolute_p2[0]]

    @staticmethod
    def _roi_img_absolute(img, p1, p2):
        return img[p1[1]:p2[1], p1[0]:p2[0]]

    @staticmethod
    def _threshold(img: np.ndarray):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        return cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]

    @staticmethod
    def _get_lines(im: np.ndarray):
        r2 = cv.morphologyEx(im, cv.MORPH_DILATE,
                             np.ones((10, 10), np.uint8))

        contours = cv.findContours(
            r2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]

        lines = []
        for cntr in contours:
            x, y, w, h = cv.boundingRect(cntr)
            lines.append(
                (MenuParser._roi_img_absolute(im, (x, y), (x + w, y + h)), y))

        return [x[0] for x in sorted(lines, key=lambda x: x[1])]

    def dish_names(self, img: np.ndarray) -> List[str]:
        th = MenuParser._threshold(img)
        block_images = [MenuParser._roi_img_relative(
            th, *r) for r in self._block_rois]

        dish_img_lines = []
        for block in block_images:
            lines = MenuParser._get_lines(block)
            dish_img_lines.extend(lines)

        all_lines = [MenuParser._ocr(x) for x in dish_img_lines]
        return [x for x in all_lines if len(x) > 2]

    @staticmethod
    def _ocr(image: np.ndarray):
        s = pytesseract.image_to_string(image, lang='rus', timeout=5, config='--psm 6 --oem 1')
        s = util.replace_all(s, '\'‘«»,‚”“°_.', ' ')
        table = str.maketrans('<{}©6',
                              'с()сб',
                              '')
        s = s.translate(table)
        s = s.strip().lower()
        s = re.sub(r'(\(.*)', '', s, flags=re.DOTALL)
        s = ' '.join(s.split())
        return s


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print('Usage: python3 menu_parser.py <image>')
        exit(1)

    mp = MenuParser()
    img = cv.imread(sys.argv[1])
    if img is None:
        print('File not found')
        sys.exit(1)
    dish_names = mp.dish_names(img)
    print(*dish_names, sep='\n')
