from genericpath import isdir
import shutil
import os 
from sklearn.model_selection import train_test_split
import re



annotations_folder = 'annotations_/'
images_folder = 'images_/'



#Utility function to move images 
def move_files_to_folder(list_of_files, destination_folder):
    for f in list_of_files:
        try:
            shutil.move(f, destination_folder)
        except:
            print(f)
            assert False

#Utility function to copy images 
def copy_files_to_folder(list_of_files, destination_folder):
    for f in list_of_files:
        try:
            shutil.copy(f, destination_folder)
        except:
            print(f)
            assert False


# rename the images files properly
def rename_image(): 
    print("Renaming images in progress ...")
    
    img_folder_content = [os.path.join('images_', x) for x in os.listdir('images_') if x[-3:] == "png"]
    img_folder_content.sort()

    for count, filename in enumerate(img_folder_content):
        dst = f"Image_{str(count)}.png"
        dst = f"{images_folder}/{dst}"
        os.rename(filename, dst)
    
    print("\tRenaming images successfull !\n")


# rename the images annotations properly
def rename_annotations(): 
    print("Renaming annotations in progress ...")

    ann_folder_content = [os.path.join('annotations_', x) for x in os.listdir('annotations_') if x[-3:] == "txt"]
    ann_folder_content.sort()

    for count, filename in enumerate(ann_folder_content):
        dst = f"Image_{str(count)}.txt"
        dst = f"{annotations_folder}/{dst}"
        os.rename(filename, dst)
    
    print("\tRenaiming annotations successful ! \n")

# copy and rename function for annotations    
def copy_and_rename_annotation():
    ann_test_folder_content = [os.path.join('annotations_test', x) for x in os.listdir('annotations_test') if x[-3:] == "txt"]
    ann_train_folder_content = [os.path.join('annotations_train', x) for x in os.listdir('annotations_train') if x[-3:] == "txt"]

    print("Copying annotations from annotations_test/ .... ")
    copy_files_to_folder(ann_test_folder_content, annotations_folder)
    print("\tCopying annotations from annotations_test/ successfull ! \n")
   
    print("Copying annotations from annotations_train/ .... ")
    copy_files_to_folder(ann_train_folder_content, annotations_folder) 
    print("\tCopying annotations from annotations_train/ successfull ! \n")

    rename_annotations()


# copy and rename function for images    
def copy_and_rename_images():
    content = os.listdir('Train')

    # Make sure there is only appropriate folder here (no hidden file or config file or wtv)
    content = os.listdir('Train')
    for x in content:
        if not re.search("[0-9]", x):
            content.remove(x)

    # Sort the list of subfolder to maintain the structure when renaiming
    content.sort(key=int)

    img_train_content_folder = []
    for i in range(len(content)):
        path = os.path.join('Train/', str(i))
        leaf_folder_content = os.listdir(path)
        leaf_folder_content.sort()
        for x in leaf_folder_content:
            img_train_content_folder.append(os.path.join(path, x))
    
    img_train_content_folder.sort()

    img_test_content_folder = [os.path.join('Test', x) for x in os.listdir('Test') if x[-3:] == "png"]
    
    print("Copying images from Test/ .... ")
    copy_files_to_folder(img_test_content_folder, images_folder)
    print("\tCopying images from Test/ successfull ! \n")
   
    print("Copying images from Train/ .... ")
    copy_files_to_folder(img_train_content_folder, images_folder) 
    print("\tCopying images from Train/ successfull ! \n")
       
    rename_image()


    






# before splitting the dataset, you need to regroup every images and annotations into a distinct common folder
def prepare_architecture_for_splitting():
    if not os.path.exists(annotations_folder):
        os.mkdir(annotations_folder)
        print("Created annotations_ folder")
    if not os.path.exists(images_folder):
        os.mkdir(images_folder)
        print("Created images_ folder")

    print("\n")
    copy_and_rename_annotation()
    copy_and_rename_images()




# Function to split the dataset into train / valid / test folders
def split_dataset():
    # Read images and annotations
    images = [os.path.join('images_', x) for x in os.listdir('images_')]
    annotations = [os.path.join('annotations_', x) for x in os.listdir('annotations_') if x[-3:] == "txt"]

    images.sort()
    annotations.sort()

    # Split the dataset into train-valid-test splits 
    train_images, val_images, train_annotations, val_annotations = train_test_split(images, annotations, test_size = 0.2, random_state = 1)
    val_images, test_images, val_annotations, test_annotations = train_test_split(val_images, val_annotations, test_size = 0.5, random_state = 1)

    print("Creating folders ...")
    # create new folders to split the dataset accordingly
    i_train = 'images/train'
    i_val = 'images/val'
    i_test = 'images/test'
    a_train = 'labels/train'
    a_val = 'labels/val'
    a_test = 'labels/test'
    os.mkdir('images')
    os.mkdir('labels')
    os.mkdir(i_train)
    os.mkdir(i_val)
    os.mkdir(i_test)
    os.mkdir(a_train)
    os.mkdir(a_val)
    os.mkdir(a_test)
    print("\tCreating folders successfull ! \n")

    print("Moving images and annotations files to their appropriate folder ...")
    # move files accordingly to the split they belong
    move_files_to_folder(train_images, i_train)
    move_files_to_folder(val_images, i_val)
    move_files_to_folder(test_images, i_test)
    move_files_to_folder(train_annotations, a_train)
    move_files_to_folder(val_annotations, a_val)
    move_files_to_folder(test_annotations, a_test)

    if os.path.exists('images_'):
        os.rmdir('images_')
    if os.path.exists('annotations_'):
        os.rmdir('annotations_')
    if os.path.exists('annotations_test'):
        shutil.rmtree('annotations_test')
    if os.path.exists('annotations_train'):
        shutil.rmtree('annotations_train')
    if os.path.exists('test_xmls'):
        shutil.rmtree('test_xmls')
    if os.path.exists('train_xmls'):
        shutil.rmtree('train_xmls')

    print("\t Done splitting the dataset !!!! \n")


if __name__ == '__main__':
    prepare_architecture_for_splitting()
    split_dataset()
