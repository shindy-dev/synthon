import cv2
import numpy as np


class IconMaker:
    def __init__(self, tmp, color_code="#000000", mag=1, alpha_ch=True):
        self.tmp_ico = tmp.astype(int)
        self.tmp_w, self.tmp_h = self.tmp_ico.shape[:2][::-1]
        self.B, self.G, self.R = ColorCode(color_code).BGR_norm

        self.mag = int(mag) if mag > 0 else 1
        self.alpha_ch = alpha_ch

        # output size
        self.output_shape = (self.tmp_h * self.mag, self.tmp_w * self.mag)
        self.img_ini = np.zeros(self.output_shape, dtype=int)
        self.create_ico()

    def _plot_to_img(self, tmp):
        img = self.img_ini.copy()
        for i in range(self.tmp_h):
            for j in range(self.tmp_w):
                img[
                    i * self.mag : i * self.mag + self.mag,
                    j * self.mag : j * self.mag + self.mag,
                ] = tmp[i, j]
        return img

    def _make_mask(self, img):
        ret_img = self.img_ini.copy()
        ret_img[np.where(img != 0)[:2]] = 255
        return ret_img

    def create_ico(self):
        self.img_ico = self._plot_to_img(self.tmp_ico)

        self.img_ico = cv2.merge(
            (self.img_ico * self.B, self.img_ico * self.G, self.img_ico * self.R)
        ).astype(int)

        if not self.alpha_ch:
            return self.img_ico

        img_msk = self._make_mask(self.img_ico)
        bgra = list(cv2.split(self.img_ico)) + [img_msk]  # 一回バラして
        self.img_ico = cv2.merge(bgra)  # くっつける

        return self.img_ico

    def save_ico(self, path):
        cv2.imwrite(path, self.img_ico)


class ColorCode:
    def __init__(self, color_code):
        R, G, B = self._parse(color_code.upper())

        self.RGB = (R, G, B)
        self.BGR = (B, G, R)
        self.RGB_norm = (float(c) / 255 for c in self.RGB)
        self.BGR_norm = (float(c) / 255 for c in self.BGR)

    def _parse(self, cc):
        self._check(cc)
        return int(cc[1:3], 16), int(cc[3:5], 16), int(cc[5:7], 16)

    def _check(self, cc):
        ex = "ex. #FF0ABD"
        if len(cc) == 7 and cc.startswith("#"):
            for c in cc[1:]:
                if not "0" <= c <= "F":
                    raise ValueError("{} is not hex in {}. {}".format(c, cc, ex))
            return None
        elif len(cc) < 7:
            raise ValueError("{} is short. {}".format(cc, ex))
        elif len(cc) > 7:
            raise ValueError("{} is long. {}".format(cc, ex))
        else:
            raise ValueError("wrong code {}. {}".format(cc, ex))


""" main example
if __name__ == '__main__':
    tmp_ico = np.array([
        [0, 0, 1, 1, 1, 0, 0],
        [0, 1, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0, 0],
    ]) * 255

    im = IconMaker(tmp=tmp_ico, color_code='#58FAF4', mag=100, alpha_ch=False)
    im.save_ico('my_icon.png')
"""
