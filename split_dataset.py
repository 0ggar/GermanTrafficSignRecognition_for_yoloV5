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
    split_dataset()