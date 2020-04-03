# ai-project-character-recognition
An AI based program which can recognize handwritten english alphabets and digits(0-9) using Deep Learning.

### For Windows:
Make sure you have python3(along with pip) and ghostscript installed.  If not, you can install them using "python.exe", and for ghostscript using "ghostscript64.exe" for x64 based systems and using "ghostscript32.exe" for x32 based systems.<br>
To install emnist dataset, execute the file named as "emnist-0.0-py3-none-any.whl"<br>
To install other requirements:<br>
```pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-0.12.0-py3-none-any.whl```<br>
```python3 -m pip install -r requirements.txt```<br>
<br>
<br>
### For Linux:
Install python3 and pip3 using following commands:<br>
```apt-get install python3
apt-get install python3-pip
```
To install tkinter module, enter the following command:<br>
```apt-get install python3-tk```<br>
To install emnist module, enter the following commands:<br>
```
tar -xvzf emnist-0.0.tar.gz
cd emnist-0.0
python3 setup.py
```
To install the other requirements, enter the following command:<br>
```pip3 install -r requirements.txt```<br>
<br><br>
### After installation:
To train the model:<br>
```python3 train.py```<br>
To predict the handwritten inputs:<br>
```python3 main.py```<br>
