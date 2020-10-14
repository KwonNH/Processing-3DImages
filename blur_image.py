import cv2
import numpy as np
import json
import xmltodict


def gaussian_blur(file_name, coordinates):
    # Read in image
    image = cv2.imread("./"+file_name+".jpg")

    # Create ROI coordinates
    blurred_image = cv2.GaussianBlur(image, (43, 43), 30)

    roi_corners = np.array([coordinates], dtype=np.int32)

    mask = np.zeros(image.shape, dtype=np.uint8)
    channel_count = image.shape[2]
    ignore_mask_color = (255,) * channel_count
    cv2.fillPoly(mask, roi_corners, ignore_mask_color)

    mask_inverse = np.ones(mask.shape).astype(np.uint8) * 255 - mask

    final_image = cv2.bitwise_and(blurred_image, mask) + cv2.bitwise_and(image, mask_inverse)
    # cv2.imshow('blur', blur)
    # cv2.imshow('image', image)
    # cv2.waitKey()

    cv2.imwrite('image_masked.png', final_image)


def xml_to_json(file_name):
    with open("./"+file_name+".xml") as xml_file:
        data_dict = xmltodict.parse(xml_file.read())

    xml_file.close()

    json_data = json.dumps(data_dict)

    with open("./"+file_name+".json", "w") as json_file:
        json_file.write(json_data)

    json_file.close()


if __name__ == "__main__":
    #xml_to_json("0_blur_test")

    with open("./0_blur_test.json", "r") as json_file:
        json_data = json.load(json_file)

    #print(json_data['annotation']['object']['polygon']['pt'][0])

    points = []

    for point in json_data['annotation']['object']['polygon']['pt']:
        points.append([point['x'], point['y']])

    gaussian_blur("0_blur_test", points)

    #gaussian_blur()

