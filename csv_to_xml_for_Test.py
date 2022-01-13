from collections import defaultdict
import os
import csv
from tqdm import tqdm

from xml.etree.ElementTree import parse, Element, SubElement, ElementTree
import xml.etree.ElementTree as ET

save_root2 = "test_xmls"

print("\nConversion from CSV to XML for the Test.csv file ...")

if not os.path.exists(save_root2):
    os.mkdir(save_root2)

def filename_to_str(f):
     # Change the path to avoid using "/" in file name
    filename_list = list(f)
    filename_list[:5] = ''
    f = ''.join(filename_list)
    return f

def write_xml(folder, filename, bbox_list):
    root = Element('annotation')
    SubElement(root, 'folder').text = folder
    SubElement(root, 'filename').text = filename
    

    # Details from first entry
    e_width, e_height, e_xmin, e_ymin, e_xmax, e_ymax, e_class_id, e_filename = bbox_list[0]
    
    size = SubElement(root, 'size')
    SubElement(size, 'width').text = e_width
    SubElement(size, 'height').text = e_height
    SubElement(size, 'depth').text = '3'

    SubElement(root, 'segmented').text = '0'

    for entry in bbox_list:
        
        e_width, e_height, e_xmin, e_ymin, e_xmax, e_ymax, e_class_id, e_filename = entry
        
        obj = SubElement(root, 'object')
        SubElement(obj, 'name').text = e_class_id
        SubElement(obj, 'pose').text = 'Unspecified'
        SubElement(obj, 'truncated').text = '0'
        SubElement(obj, 'difficult').text = '0'

        bbox = SubElement(obj, 'bndbox')
        SubElement(bbox, 'xmin').text = e_xmin
        SubElement(bbox, 'ymin').text = e_ymin
        SubElement(bbox, 'xmax').text = e_xmax
        SubElement(bbox, 'ymax').text = e_ymax

    #indent(root)
    tree = ElementTree(root)
    
    xml_filename = os.path.join('.', folder, os.path.splitext('Test_' + filename)[0] + '.xml')
    tree.write(xml_filename)
    

entries_by_filename = defaultdict(list)

with open('Test.csv', 'r', encoding='utf-8') as f_input_csv:
    csv_input = csv.reader(f_input_csv)
    header = next(csv_input)

    for row in csv_input:
        width, height, xmin, ymin, xmax, ymax, class_name, filename = row

        filename = filename_to_str(filename)
        entries_by_filename[filename].append(row) #for whole csv to xml


for filename, entries in tqdm(entries_by_filename.items()):
    write_xml(save_root2, filename, entries)

print("\tConversion from CSV to XML for the Test.csv file successfull ! \n")