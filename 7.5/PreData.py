import os
import numpy as np
from PIL import Image


def FileReName(testType, FilePath):
    type_counter = 0
    for type in testType:
        file_counter = 0
        subfolder = os.listdir(FilePath + type)
        for subclass in subfolder:
            file_counter += 1
            os.rename(FilePath + type + '/' + subclass, FilePath + type + '/' + str(type_counter) + '_' + type + '_' + str(file_counter) +'.jpg')
        type_counter += 1

def FileReSize(Output_folder, testType, FilePath, Width = 100, Height = 100):
    for type in testType:
        for img in os.listdir(FilePath + type):
            img_open = Image.open(FilePath + type + '/' + img)

            #jpg cant be converted directly
            convert_RGB = img_open.convert('RGB')
            Resize_img = convert_RGB.resize((Width, Height), Image.BILINEAR)
            Resize_img.save(os.path.join(Output_folder, os.path.basename(img)))

def ReadImage_Array(filename, train_folder):
    img = Image.open(train_folder + filename)
    return np.array(img)

def DataSet(train_folder):
    Train_img = []
    Train_lable = []
    for file in os.listdir(train_folder):
        file_img_to_array = ReadImage_Array(filename = file, train_folder = train_folder)

        Train_img.append(file_img_to_array)

        Train_lable.append(int(file.split('_')[0]))

    Train_np_img = np.array(Train_img)
    Train_np_lable = np.array(Train_lable)

    print(Train_np_img.shape)
    print(Train_np_lable.shape)

if __name__ == "__main__":

    testType = ['cats', 'dogs']

    #FileReName(testType = testType, FilePath = 'raw_IMG/')

    #FileReSize(testType = testType, FilePath = 'raw_IMG/', Output_folder = 'train/')

    DataSet(train_folder = 'train/')
