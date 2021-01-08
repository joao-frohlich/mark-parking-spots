import cv2 as cv
import numpy as np

def processMask(raw_mask):
    x = 0
    status = raw_mask['status_id']-1
    id = raw_mask['id']
    raw_mask = raw_mask['contour']
    mask = []
    for i in range(0,len(raw_mask)):
        if i&1:
            mask.append([x,raw_mask[i]])
        else:
            x = raw_mask[i]
    x = int(mask[0][0])
    y = int(mask[0][1])
    mask = np.array(mask, np.int32)
    mask = mask.reshape(-1,1,2)
    return mask, status, id, x, y

def drawMask(img, raw_mask):
    mask,status,id,x,y = processMask(raw_mask)
    font = cv.FONT_HERSHEY_SIMPLEX
    cv.polylines(img, [mask], True, ((status//2)*255, (not (status&1))*255, (status&1)*255))
    cv.putText(img, str(id), (x,y), font, 1,(255,0,255),1,cv.LINE_AA)
    return img

def openImage(image_path):
    return cv.imread(image_path, -1)


def drawMasks(image_path, tmp_img_path, raw_masks):
    img = openImage(image_path)
    centers = []
    for raw_mask in raw_masks:
        img = drawMask(img, raw_mask)
        centers.append([raw_mask['id'], int(raw_mask['rotatedRect'][0]), int(raw_mask['rotatedRect'][1]), raw_mask['status_id']])
    cv.imwrite(tmp_img_path, img)
    return centers