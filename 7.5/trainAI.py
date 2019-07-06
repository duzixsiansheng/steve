import os
import numpy as np
from PIL import Image
from keras.models import Sequential
from keras.layers import Convolution2D, Flatten, Dropout, MaxPooling2D,Dense,Activation
from keras.optimizers import Adam
from keras.utils import np_utils

#Pre process images
class PreFile(object):
    def __init__(self,FilePath,testType):
        self.FilePath = FilePath
        # Main dog folder is shared path can be submit to param of this class
        self.testType = testType
        #the dogtype list is shared list between rename and resize fucntion

    def FileReName(self):
        type_counter = 0
        for type in self.testType:
            file_counter = 0
            subfolder = os.listdir(self.FilePath + type)
            for subclass in subfolder:
                file_counter += 1
                os.rename(self.FilePath + type + '/' + subclass,
                          self.FilePath + type + '/' + str(type_counter) + '_' + type + '_' + str(file_counter) + '.jpg')
            type_counter += 1

    def FileResize(self, Width, Height, Output_folder):
        for type in self.testType:
            files = os.listdir(self.FilePath+type)
            for i in files:
                img_open = Image.open(self.FilePath + type+'/' + i)
                conv_RGB = img_open.convert('RGB') #统一转换一下RGB格式 统一化
                new_img = conv_RGB.resize((Width,Height),Image.BILINEAR)
                new_img.save(os.path.join(Output_folder,os.path.basename(i)))


class Training(object):
    def __init__(self, batch_size, number_batch, catagories, train_folder):
        self.batch_size = batch_size
        self.number_batch = number_batch
        self.categories = catagories
        self.train_folder = train_folder

    def ReadImage_Array(self, filename):
        img = Image.open(self.train_folder + filename)
        return np.array(img)

    def train(self):
        Train_img = []
        Train_lable = []
        for file in os.listdir(self.train_folder):
            file_img_to_array = self.ReadImage_Array(filename = file)

            Train_img.append(file_img_to_array)
            Train_lable.append(int(file.split('_')[0]))

        Train_np_img = np.array(Train_img)
        Train_np_lable = np.array(Train_lable)

        Train_np_lable = np_utils.to_categorical(Train_np_lable, self.categories) #into binary
        Train_np_img = Train_np_img.astype('float32')
        Train_np_img /= 255.0

        model = Sequential()

        #input shape (100, 100, 3)
        model.add(Convolution2D(
            input_shape = (100, 100, 3),
            filters = 32,#next layer output (100, 100, 32)
            kernel_size = (5, 5),#每次扫多少像素
            padding = 'same', #外边距 (比如100/7除不尽，剩下的如何处理）
        ))

        model.add(Activation('relu'))

        model.add(MaxPooling2D(
            pool_size = (2,2), # Output next layer(50,50,32)
            strides = (2,2),
            padding = 'same'
        ))

        #2

        model.add(Convolution2D(
            filters=64,  # next layer output (50, 50, 64)
            kernel_size=(2, 2),  # 每次扫多少像素
            padding='same',  # 外边距 (比如100/7除不尽，剩下的如何处理）
        ))

        model.add(Activation('relu'))

        model.add(MaxPooling2D(
            pool_size=(2, 2),  # Output next layer(25,25,64)
            strides=(2, 2),
            padding='same'
        ))

        #Fully

        model.add(Flatten()) #降维
        model.add(Dense(1024))
        model.add(Activation('relu'))

        model.add(Dense(512))
        model.add(Activation('relu'))

        model.add(Dense(256))
        model.add(Activation('relu'))

        model.add(Dense(self.categories))
        model.add(Activation('softmax'))

        # Define Optimizer

        adam = Adam(lr = 0.0001)

        model.compile(optimizer=adam,
                      loss="categorical_crossentropy",
                      metrics=['accuracy']
                      )

        #network
        model.fit(
            x = Train_np_img,
            y = Train_np_lable,
            epochs = self.number_batch,
            batch_size = self.batch_size,
            verbose = 1
        )

        model.save('./AI.h5')

def Main():
    testType = ['cats', 'dogs']

    #File = PreFile(FilePath='raw_IMG/', testType=testType)
    #File.FileReName()
    #File.FileResize(Height=100,Width=100,Output_folder='train/')
    Train = Training(batch_size=256, number_batch = 30, catagories = 2, train_folder = 'train/')
    Train.train()

if __name__ == "__main__":
    Main()