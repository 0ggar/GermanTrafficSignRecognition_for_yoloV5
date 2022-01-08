import os 
import random
import xml.etree.ElementTree as ET
from tqdm import tqdm
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt


# Function to get the data from XML Annotation
def extract_info_from_xml(xml_file):
    root = ET.parse(xml_file).getroot()
    
    # Initialise the info dict 
    info_dict = {}
    info_dict['bboxes'] = []

    # Parse the XML Tree
    for elem in root:
        # Get the file name 
        if elem.tag == "filename":
            info_dict['filename'] = elem.text
            
        # Get the image size
        elif elem.tag == "size":
            image_size = []
            for subelem in elem:
                image_size.append(int(subelem.text))
            
            info_dict['image_size'] = tuple(image_size)
        
        # Get details of the bounding box 
        elif elem.tag == "object":
            bbox = {}
            for subelem in elem:
                if subelem.tag == "name":
                    bbox["class"] = subelem.text
                    
                elif subelem.tag == "bndbox":
                    for subsubelem in subelem:
                        bbox[subsubelem.tag] = int(subsubelem.text)            
            info_dict['bboxes'].append(bbox)
    
    return info_dict






# Dictionary that maps class names to IDs
class_name_to_id_mapping = {'Speed limit (20km/h)' : 0,
                            'Speed limit (30km/h)' : 1, 
                            'Speed limit (50km/h)' : 2, 
                            'Speed limit (60km/h)' : 3, 
                            'Speed limit (70km/h)' : 4, 
                            'Speed limit (80km/h)' : 5, 
                            'End of speed limit (80km/h)' : 6, 
                            'Speed limit (100km/h)' : 7, 
                            'Speed limit (120km/h)' : 8, 
                            'No passing' : 9, 
                            'No passing veh over 3.5 tons' : 10, 
                            'Right-of-way at intersection' : 11, 
                            'Priority road' : 12, 
                            'Yield' : 13, 
                            'Stop' : 14, 
                            'No vehicles' : 15, 
                            'Veh > 3.5 tons prohibited' : 16, 
                            'No entry' : 17, 
                            'General caution' : 18, 
                            'Dangerous curve left' : 19, 
                            'Dangerous curve right' : 20, 
                            'Double curve' : 21, 
                            'Bumpy road' : 22, 
                            'Slippery road' : 23, 
                            'Road narrows on the right' : 24, 
                            'Road work' : 25, 
                            'Traffic signals' : 26, 
                            'Pedestrians' : 27, 
                            'Children crossing' : 28, 
                            'Bicycles crossing' : 29, 
                            'Beware of ice/snow' : 30,
                            'Wild animals crossing' : 31, 
                            'End speed + passing limits' : 32, 
                            'Turn right ahead' : 33, 
                            'Turn left ahead' : 34, 
                            'Ahead only' : 35, 
                            'Go straight or right' : 36, 
                            'Go straight or left' : 37, 
                            'Keep right' : 38, 
                            'Keep left' : 39, 
                            'Roundabout mandatory' : 40, 
                            'End of no passing' : 41, 
                            'End no passing veh > 3.5 tons' : 42
                            }
                           



# Name of the file which we have to save 
dest_ann_folder = "annotations_train"

# Convert the info dict to the required yolo format and write it to disk
def convert_to_yolov5(info_dict):
    print_buffer = []
    
    # For each bounding box
    for b in info_dict["bboxes"]:
        try:
            class_id = (b["class"])
        except KeyError:
            print("Invalid Class. Check Meta.csv to find out why.")
        
        # Transform the bbox co-ordinates as per the format required by YOLO v5
        b_center_x = (b["xmin"] + b["xmax"]) / 2 
        b_center_y = (b["ymin"] + b["ymax"]) / 2
        b_width    = (b["xmax"] - b["xmin"])
        b_height   = (b["ymax"] - b["ymin"])
        
        # Normalise the co-ordinates by the dimensions of the image
        image_w, image_h, image_c = info_dict["image_size"]  
        b_center_x /= image_w 
        b_center_y /= image_h 
        b_width    /= image_w 
        b_height   /= image_h 
        
        #Write the bbox details to the file 
        print_buffer.append("{} {:.3f} {:.3f} {:.3f} {:.3f}".format(class_id, b_center_x, b_center_y, b_width, b_height))
        
    if not os.path.exists(dest_ann_folder):
        os.mkdir(dest_ann_folder)
    save_file_name = os.path.join(dest_ann_folder, info_dict["filename"].replace("png", "txt"))
    
    # Save the annotation to disk
    print("\n".join(print_buffer), file= open(save_file_name, "w"))


def annote():
    # Get the annotations
    annotations = [os.path.join('train_xmls', x) for x in os.listdir('train_xmls') if x[-3:] == "xml"]
    annotations.sort()

    # Convert and save the annotations
    for ann in tqdm(annotations):
        info_dict = extract_info_from_xml(ann)
        convert_to_yolov5(info_dict)
    annotations = [os.path.join(dest_ann_folder, x) for x in os.listdir(dest_ann_folder) if x[-3:] == "txt"]

    return annotations



class_id_to_name_mapping = dict(zip(class_name_to_id_mapping.values(), class_name_to_id_mapping.keys()))


def plot_bounding_box(image, annotation_list):
    annotations = np.array(annotation_list)
    w, h = image.size
    
    plotted_image = ImageDraw.Draw(image)

    transformed_annotations = np.copy(annotations)
    transformed_annotations[:,[1,3]] = annotations[:,[1,3]] * w
    transformed_annotations[:,[2,4]] = annotations[:,[2,4]] * h 
    
    transformed_annotations[:,1] = transformed_annotations[:,1] - (transformed_annotations[:,3] / 2)
    transformed_annotations[:,2] = transformed_annotations[:,2] - (transformed_annotations[:,4] / 2)
    transformed_annotations[:,3] = transformed_annotations[:,1] + transformed_annotations[:,3]
    transformed_annotations[:,4] = transformed_annotations[:,2] + transformed_annotations[:,4]
    
    for ann in transformed_annotations:
        obj_cls, x0, y0, x1, y1 = ann
        plotted_image.rectangle(((x0,y0), (x1,y1)))
        
        print("Class detected : ", class_id_to_name_mapping[(int(obj_cls))])

        plotted_image.text((x0, y0 - 10), class_id_to_name_mapping[(int(obj_cls))])
    
    plt.imshow(np.array(image))
    plt.show()


def plot_random_image_with_bbox(annotations):
     # Get any random annotation file 
    annotation_file = random.choice(annotations)
    
    with open(annotation_file, "r") as file:
        annotation_list = file.read().split("\n")[:-1]
        annotation_list = [x.split(" ") for x in annotation_list]
        annotation_list = [[float(y) for y in x ] for x in annotation_list]
    
    ann_list = annotation_file.rsplit('-', 1)
    filename = ann_list[1]
    foldername = ann_list[0].rsplit('/', 1)[1]

    #Get the corresponding image file
    image_file = ("Train/" + foldername + "/" + filename).replace("txt", "png")
    #image_file = annotation_file.replace("annotations", "images").replace("txt", "png")
    assert os.path.exists(image_file)

    print("Image : ", image_file)
    #Load the image
    image = Image.open(image_file)

    #Plot the Bounding Box
    plot_bounding_box(image, annotation_list)


if __name__ == '__main__':
    print("Transformation from XML file to YoloV5 compatible format for TRAIN data ...")

    # convert and change the annotations of every file, return a list of file with annotation in txt format
    annotations = annote()

    # Uncomment the following line to plot a randomize image with bbox in yolov5 format ! 
    # plot_random_image_with_bbox(annotations) 
    
    print("\tTransformation from XML file to YoloV5 compatible format for TRAIN data successfull ! \n")
