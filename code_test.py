import init
import cv2
import numpy as np
import support_lib as sl
import matplotlib.image as mpimg

init.Init()
def searh_image_for_rgb(image_fname, rgb):
    # img = mpimg.imread(image_fname)
    img = np.array(sl.screenshot())
    x, y = np.where(np.all(img == rgb, axis=2))

    for item in np.array([x, y]).transpose() :
        print(item)
        row, column = item
        cv2.circle(img, (column, row), 5, (0, 255, 0), -1)  # 점의 크기는 5, 색상은 (0, 255, 0)으로 설정
        break


    cv2.imshow('Image with Pixels', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


print(searh_image_for_rgb('1.bmp', [255, 136, 17]))