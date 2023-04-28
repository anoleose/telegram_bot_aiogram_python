import os, sys
from PIL import Image
import numpy as np
import random 

#эта функция получает случайное изображение в определенном файле
def random_image():
	abs_path = os.path.abspath(__file__)
	base_dir = os.path.dirname(abs_path)
	list_img = os.listdir("img")
	random_img = random.choice(list_img)
	random_img  = os.path.join(base_dir, f'img/{random_img}')
	return random_img
if __name__ == '__main__':
	random_image()


