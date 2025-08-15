import sys

sys.path.append("../../../")

import numpy as np

from synthon.graphics.generate_github_icon import IconMaker

if __name__ == "__main__":
    tmp_ico = (
        np.array(
            [
                [0, 0, 1, 1, 1, 0, 0],
                [0, 1, 0, 0, 0, 1, 0],
                [0, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 1, 0],
                [0, 1, 0, 0, 0, 1, 0],
                [0, 0, 1, 1, 1, 0, 0],
            ]
        )
        * 255
    )

    im = IconMaker(tmp=tmp_ico, color_code="#58FAF4", mag=100, alpha_ch=False)
    im.save_ico("my_icon.png")
