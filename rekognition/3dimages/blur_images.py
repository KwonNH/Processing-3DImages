import cv2
import numpy as np
import json
import xmltodict
from os import listdir
from os.path import isfile, join
from shapely.geometry import Polygon


def gaussian_blur(file_name, coordinates):
    # Read in image
    image = cv2.imread("./3dimages/set2/" + file_name + ".jpg")

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

    cv2.imwrite("./3dimages/set2/"+file_name+".jpg", final_image)


def xml_to_json(file_name):
    with open("./3dimages/set2_annotations/" + file_name) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())

    xml_file.close()

    json_data = json.dumps(data_dict)

    with open("./3dimages/set2_annotations_json/" + file_name.split(".")[0] + ".json", "w") as json_file:
        json_file.write(json_data)

    json_file.close()


def blur_region(id):
    with open("./3dimages/set2_annotations_json/" + id + ".json", "r") as json_file:
        json_data = json.load(json_file)

    points = []

    for object in json_data['annotation']['object']:
        print(object['polygon']['pt'])

    gaussian_blur(id, points)


def remove_overlapping_areas(polygons):

    for i in range(len(polygons)):
        for j in range(i+1, len(polygons)):
            p1 = Polygon(polygons[i])
            p2 = Polygon(polygons[j])

            if p1.intersects(p2):
                intersection = p1.intersection(p2)

                print(p1.difference(intersection))

                subtracted = str(p1.difference(intersection)).split("((")[1].split("))")[0].split(", ")
                '''
                coords = []
                print(subtracted)
                for coord in subtracted:
                    coords.append([coord.split(" ")[0], coord.split(" ")[1]])
                print(coords)

                polygons[i] = coords
                '''


if __name__ == "__main__":

    annotation_path = "./3dimages/set2_annotations_json"
    # image_path = "./3dimages/set2"
    files = [f for f in listdir(annotation_path) if isfile(join(annotation_path, f))]
    # images = [f for f in listdir(image_path) if isfile(join(image_path, f))]

    files.sort()

    '''

    for file in files:
        with open("./3dimages/set2_annotations_json/" + file, "r") as json_file:
            json_data = json.load(json_file)

        polygons = []
        for object in json_data['annotation']['object']:

            polygon = []

            try:
                for point in object['polygon']['pt']:
                    polygon.append([point['x'], point['y']])
                polygons.append(polygon)
            except TypeError:
                print(file)

            #gaussian_blur(file.split(".")[0], polygon)
    '''
    for file in files:
        with open("./3dimages/set2_annotations_json/"+file, "r") as json_file:
            json_data = json.load(json_file)

        polygons = []
        #print(str(json_data['annotation']['object']).count("polygon"))

        obj_count = str(json_data['annotation']['object']).count("polygon")

        if obj_count != 1:
            for i in range(obj_count):
                polygon = []
                obj = json_data['annotation']['object'][i]
                if obj['deleted'] == "0":
                    for point in obj['polygon']['pt']:
                        polygon.append([point['x'], point['y']])

                    gaussian_blur(file.split(".")[0], polygon)


        else:
            polygon = []
            obj = json_data['annotation']['object']
            if obj['deleted'] == "0":
                for point in obj['polygon']['pt']:
                    polygon.append([point['x'], point['y']])

                gaussian_blur(file.split(".")[0], polygon)

        print(polygons)

    '''

    for i in range(len(json_data['annotation']['object'])):

        print(json_data['annotation']['object']['polygon']['pt'][i])

        polygon = []

        try:
            for point in object['polygon']['pt']:
                polygon.append([point['x'], point['y']])
            polygons.append(polygon)
        except TypeError:
            pass
'''


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

