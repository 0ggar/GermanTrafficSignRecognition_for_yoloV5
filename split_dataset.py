import shutil
import os 
from sklearn.model_selection import train_test_split

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

# before splitting the dataset, you need to regroup every images and annotations into a distinct common folder
def prepare_architecture_for_splitting():
    annotations_folder = 'annotations_/'
    images_folder = 'images_/'
    ann_test_folder_content = [os.path.join('annotations_test', x) for x in os.listdir('annotations_test') if x[-3:] == "txt"]
    ann_train_folder_content = [os.path.join('annotations_train', x) for x in os.listdir('annotations_train') if x[-3:] == "txt"]

    if not os.path.exists(annotations_folder):
        os.mkdir(annotations_folder)
    
    if not os.path.exists(images_folder):
        os.mkdir(images_folder)
    
    print("Created images_ and annotations_ folder")

    copy_files_to_folder(ann_test_folder_content, annotations_folder)
    copy_files_to_folder(ann_train_folder_content, annotations_folder) 
    print("Copying files successfull ! ")

    ann_folder_content = [os.path.join('annotations_', x) for x in os.listdir('annotations_') if x[-3:] == "txt"]

    for count, filename in enumerate(ann_folder_content):
        dst = f"Annotation_{str(count)}.txt"
        dst = f"{annotations_folder}/{dst}"
        os.rename(filename, dst)
    
    print("Renaiming annotations file successful !")



# Function to split the dataset into train / valid / test folders
def split_dataset():
    # Read images and annotations
    images = [os.path.join('images', x) for x in os.listdir('images')]
    annotations = [os.path.join('annotations', x) for x in os.listdir('annotations') if x[-3:] == "txt"]

    images.sort()
    annotations.sort()

    # Split the dataset into train-valid-test splits 
    train_images, val_images, train_annotations, val_annotations = train_test_split(images, annotations, test_size = 0.2, random_state = 1)
    val_images, test_images, val_annotations, test_annotations = train_test_split(val_images, val_annotations, test_size = 0.5, random_state = 1)

    # create new folders to split the dataset accordingly
    i_train = 'images/train'
    i_val = 'images/val'
    i_test = 'images/test'
    a_train = 'annotations/train'
    a_val = 'annotations/val'
    a_test = 'annotations/test'
    os.mkdir(i_train)
    os.mkdir(i_val)
    os.mkdir(i_test)
    os.mkdir(a_train)
    os.mkdir(a_val)
    os.mkdir(a_test)

    # move files accordingly to the split they belong
    move_files_to_folder(train_images, i_train)
    move_files_to_folder(val_images, i_val)
    move_files_to_folder(test_images, i_test)
    move_files_to_folder(train_annotations, a_train)
    move_files_to_folder(val_annotations, a_val)
    move_files_to_folder(test_annotations, a_test)

    print("Done splitting the dataset !")


if __name__ == '__main__':
    prepare_architecture_for_splitting()
    # split_dataset()