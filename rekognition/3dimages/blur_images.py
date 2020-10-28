import cv2
import numpy as np
import json
import xmltodict
from os import listdir
from os.path import isfile, join


def gaussian_blur(file_name, coordinates):
    # Read in image
    image = cv2.imread("./set2/"+file_name+".jpg")

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

    cv2.imwrite('./set2_blurred/', final_image)


def xml_to_json(file_name):
    with open("./3dimages/set2_annotations/"+file_name) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())

    xml_file.close()

    json_data = json.dumps(data_dict)

    with open("./3dimages/set2_annotations_json/"+file_name.split(".")[0]+".json", "w") as json_file:
        json_file.write(json_data)

    json_file.close()


def blur_region(id):
    with open("./3dimages/set2_annotations_json/"+id+".json", "r") as json_file:
        json_data = json.load(json_file)

    points = []

    for object in json_data['annotation']['object']:

        print(object['polygon']['pt'])

    gaussian_blur(id, points)


if __name__ == "__main__":

    with open("./3dimages/set2_annotations_json/0.json", "r") as json_file:
        json_data = json.load(json_file)

    segments = []
    for object in json_data['annotation']['object']:

        polygons = []
        for point in object['polygon']['pt']:
            polygons.append([point['x'], point['y']])

        segments.append(polygons)

    print(segments)

    gaussian_blur("0", segments)

    '''
    annotation_path = "./3dimages/set2_annotations"
    files = [f for f in listdir(annotation_path) if isfile(join(annotation_path, f))]

    for file in files:
        xml_to_json(file)
    
    #xml_to_json("0_blur_test")

    with open("./0_blur_test.json", "r") as json_file:
        json_data = json.load(json_file)

    #print(json_data['annotation']['object']['polygon']['pt'][0])

    points = []

    for point in json_data['annotation']['object']['polygon']['pt']:
        points.append([point['x'], point['y']])

    gaussian_blur("0_blur_test", points)

    #gaussian_blur()
    '''

