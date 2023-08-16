import os
import cv2
import numpy as np

points = []

def blacken_inside(img, points):
    mask = np.ones_like(img) * 255
    points = np.array(points)
    cv2.fillPoly(mask, [points], (0,0,0))
    blackened_img = cv2.bitwise_and(img, mask)
    return blackened_img

points = []

def click_event(event, x, y, flags, params):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        if len(points) == 4:
            center = [sum([point[j] for point in points])/4 for j in range(2)]
            points.sort(key=lambda point: np.arctan2(point[1] - center[1], point[0] - center[0]))
            cv2.imshow('image', img)



folder_path = "your images folder"
new_path = folder_path + "/edited_images"
os.makedirs(new_path,exist_ok = True)


for filename in os.listdir(folder_path):
    img_path = os.path.join(folder_path, filename)
    img = cv2.imread(img_path)
    if img is None:
        print(f"Error reading file {filename}. Skipping.")
        continue
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 800, 600)
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', click_event)
    
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or len(points) == 4:
            break
    if key == ord('q'):
        break
    modified_img = blacken_inside(img, points)
    new_filename = filename
    new_img_path = os.path.join(folder_path,new_path,new_filename)
    print(new_img_path)
    cv2.imwrite(new_img_path, modified_img)
    points = []
    cv2.destroyAllWindows()
