# What is this ? and Why ?

This repo is about the work of Clément BOTTY and Nathan TERRADE on the [German traffic signs recognition dataset](https://www.kaggle.com/meowmeowmeowmeowmeow/gtsrb-german-traffic-sign).   
This comes from our TX project at UTC on autonomous driving. 

These scripts are designed to work with the dataset architecture. You can find the dataset on the internet and download it. 

Then, with these scripts, you will be able to work with the dataset and convert everything into a dataset that can be read and used by YoloV5.

# How it works

## First step 

Working fine Python 3.9.9, not tested with previous versions.  

Ugly files with redondant code but it works fine :)

- download sklearn lib

- use the scripts that convert CSV file into XML (`csv_to_xml_for_test.py` and `csv_to_xml_for_train.py`)  
Those will create 2 new folders : `test_xmls` and `train_xmls`

## Second step

Now you have successfully converted the data from the CSV files into specific XML file. 

Then, you need to convert those XML files into readable files for YoloV5. 

For that, you have 2 new scripts : `test_xmls_to_yolo_format.py` and  `train_xmls_to_yolo_format.py`

When you run those files, if everything worked correctly a random image with her annotation will be ploted. 

## Third step

All you have to do now, is split the dataset accordingly with the format that yolo want.   

- Create a folder named `images_` and copy all the images from the dataset (located in `Test` and in every `Train/x` folder) into that folder

Run the following script to do so `split_dataset.py`