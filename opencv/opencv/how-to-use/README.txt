-------INSTALLATION-------------
pip install opencv-python
pip install imutils
pip install pillow

files from haarcascades folder must be downloaded and placed in C:\Users\user\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\cv2\data

in databasefiles/dbhandling.py change the named file directories according to your pc name, for an example:
conn = db.connect(r"C:\Users\micro\Desktop\opencv\opencv\databasefiles\accounts.db") TO conn = db.connect(r"C:\Users\YOUR_USER\Desktop\opencv\opencv\databasefiles\accounts.db")

Works best if-
Frontal angled face.
Users face is nearly covering the whole picture.
Users face is close to the camera with good quality.
The picture is more likely to comply with the functions if the flashlight function had been enabled.
Users head is not tilted to right or left or down or up.

1. Users registration
When the app has been launched, it will promt the user to begin the registration process. The user has to provide their name, surname, username, e-mail and password to finish
registration. If the user already has an account, then the sign in process can be skipped. The user has to click on the log in button and input their username and password.
2. Upload image
To upload an image, the user must click on the blue upload image button and select the desired image.
3. Usage
Once the image has been selected and displayed on the application, the user is free to click on the accessories that apply on the picture
4. Reset button
If the user wants to try out a different set of accessories, then the reset button can be used to clear out all of the equiped accessories.
