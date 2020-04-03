from tkinter import *
from PIL import Image, ImageFilter
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

def png_to_nparray(path):
    im = Image.open(path).convert("L")
    width = float(im.size[0])
    height = float(im.size[1])
    output = Image.new("L", (28,28), (255))
    if width>height:
        nheight = int(round((20.0/width*height), 0))
        if nheight==0:
            nheight=1
        img = im.resize((20,nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wtop = int(round(((28-nheight)/2), 0))
        output.paste(img, (4, wtop))
    else:
        nwidth = int(round((20.0/height*width), 0))
        if nwidth==0:
            nwidth=1
        img = im.resize((nwidth,20), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wleft = int(round(((28-nwidth)/2), 0))
        output.paste(img, (wleft,4))
    output1 = list(output.getdata())
    linear_array = [(255-x)*1.0/255.0 for x in output1]
    arr = np.array(linear_array)
    arr = np.reshape(arr, (28,28))
    return arr

class Paint(object):

    def __init__(self):
        self.root = Tk()
        self.root.title("Character Recognition")
        self.root.geometry("485x499")
        self.root.resizable(0,0)
        self.root.configure(background="#d9d9d9")

        self.pen_button = Button(self.root, text='pen', command=self.use_pen)
        self.pen_button.place(relx=0.233, rely=0.066, height=33, width=106)
        self.pen_button.configure(pady="0")

        self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser)
        self.eraser_button.place(relx=0.567, rely=0.066, height=33, width=106)
        self.eraser_button.configure(pady="0")

        self.canv = Canvas(self.root, bg='white')
        self.canv.place(relx=0.247, rely=0.214, relheight=0.501, relwidth=0.515)
        self.canv.configure(background="#ffffff")
        self.canv.configure(borderwidth="2")
        self.canv.configure(cursor="dot")
        self.canv.configure(relief="ridge")

        self.reset_button = Button(self.root, text='Reset', command=self.resetall)
        self.reset_button.place(relx=0.247, rely=0.782, height=33, width=106)
        self.reset_button.configure(pady="0")

        self.predict_button = Button(self.root, text='Predict', command=self.predict)
        self.predict_button.place(relx=0.577, rely=0.782, height=33, width=106)
        self.predict_button.configure(pady='0')

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.color = 'black'
        self.line_width = 10.0
        self.eraser_on = False
        self.active_button = self.pen_button
        self.canv.bind('<B1-Motion>', self.draw)
        self.canv.bind('<ButtonRelease-1>', self.release_button)

    def use_pen(self):
        self.activate_button(self.pen_button)

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def draw(self, event):
        draw_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.canv.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=draw_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def release_button(self, event):
        self.old_x, self.old_y = None, None

    def resetall(self):
        self.old_x, self.old_y = None, None
        self.canv.delete("all")

    def predict(self):
        self.canv.postscript(file="temp.eps")
        img = Image.open("temp.eps")
        img.save("temp.png")
        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = tf.keras.models.model_from_json(loaded_model_json)
        loaded_model.load_weights("model.h5")
        arr = png_to_nparray("temp.png")
        print("Shape of array is:", arr.shape)
        probability_model = tf.keras.Sequential([tf.keras.layers.Reshape((28,28)), 
                                                loaded_model, 
                                                tf.keras.layers.Softmax()])
        predictions = probability_model.predict(np.array([arr]))
        chars = "0123456789abcdefghijklmnopqrstuvwxyz"
        labelindex = np.argmax(predictions[0])
        chars_array=[i for i in chars]
        plt.bar(chars_arry,predictions[0])
        plt.show()

if __name__ == '__main__':
    Paint()
