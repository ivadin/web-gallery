import numpy as np
from keras.models import model_from_json
from keras.preprocessing import image
from keras.optimizers import SGD


class DNN:

    def __init__(self):
        json_file = open("cifar10_model_v2.json", "r")
        loaded_model_json = json_file.read()
        json_file.close()
        self.loaded_model = model_from_json(loaded_model_json)
        self.loaded_model.load_weights("cifar10_model_v2.h5")
        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        self.loaded_model.compile(loss='categorical_crossentropy',
                             optimizer=sgd, metrics=['accuracy'])
        self.classes = ['самолет', 'автомобиль', 'птица', 'кот', 'олень',
                        'собака', 'лягушка', 'лошадь', 'корабль', 'грузовик']

    def detect(self, image_path):
        print("image_path")
        img = image.load_img(image_path, target_size=(32, 32))

        # Преобразуем изображением в массив numpy
        x = image.img_to_array(img)
        x /= 255
        x = np.expand_dims(x, axis=0)

        prediction = self.loaded_model.predict(x)

        return self.classes[np.argmax(prediction)]
        # print("Это", self.classes[np.argmax(prediction)])
