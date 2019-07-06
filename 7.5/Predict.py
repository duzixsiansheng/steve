from keras.models import load_model
import matplotlib.image as processimage
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

class Prediction(object):

    def __init__(self,ModelFile, PredictFile, testType, Width=100, Height=100):
        self.modelfile = ModelFile
        self.predict_file = PredictFile
        self.Width = Width
        self.Height = Height
        self.testType = testType

    def Predict(self):
        #
        model = load_model(self.modelfile)
        #处理照片并覆盖
        img_open = Image.open(self.predict_file)
        conv_RGB = img_open.convert('RGB')
        img = conv_RGB.resize((self.Width, self.Height), Image.BILINEAR) #last one fang ju chi
        img.save(self.predict_file)

        #处理shape
        image = processimage.imread(self.predict_file)
        img_to_array = np.array(image)/255.0 #转成float
        img_to_array = img_to_array.reshape(1, 100, 100, 3) #

        #预测
        prediction = model.predict(img_to_array)
        Final_Prediction = [result.argmax() for result in prediction][0]
        print(prediction)
        count = 0
        for i in prediction[0]:
            percent = '%.2f%%' % (i*100)
            print(self.testType[count], 'percent', percent)
            count += 1


testType = ["cats", "dogs"]
Pred = Prediction(PredictFile = 'predict/cat.6889.jpg', ModelFile='AI.h5',Width=100, Height=100, testType = testType)
Pred.Predict()