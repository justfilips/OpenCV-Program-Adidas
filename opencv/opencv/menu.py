import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import numpy as np
import cv2
import imutils
import math
from databasefiles import dbhandling


print("Main program start")

# check if user has logged in
try:
    with open("databasefiles/user.txt", "r") as user_f:
        user = user_f.read()
        if user == "":
            print("Terminated; no user found")
            exit()
except:
    print("Terminated; unable to read user.txt")
    exit()
else:
    with open("databasefiles/user.txt", "w") as user_f:
        user_f.close()

    print("Logged in as", user)

eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_mouth.xml")
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt.xml")

app = tk.Tk()

# Load your background image (PIL)
bg_image = Image.open(
    "assets/background.jpg"
)  # Change to your background image path (from PIL to Tkinter)
bg_photo = ImageTk.PhotoImage(bg_image)

#Creates a label for the image
bg_label = tk.Label(app, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

resize_delay = 100 
resize_timer = None

# Function for resizing the background
def resize_background():
    global bg_photo
    app_width = app.winfo_width()
    app_height = app.winfo_height()
    resized_bg = bg_image.resize((app_width, app_height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(resized_bg)
    bg_label.config(image=bg_photo)

#Prevents lagging when resizing the window
def delayed_resize_background(event):
    global resize_timer
    if resize_timer:
        app.after_cancel(resize_timer)
    resize_timer = app.after(resize_delay, resize_background)


app.bind("<Configure>", delayed_resize_background) #Whenever window is resized, it calls in the function
resize_background()  # Initially set the background image


app.minsize(600, 800)

app.title("Abibas")

app.geometry("800x850")

app.configure(bg="#f5f5f5")
button_font = ("Helvetica", 20, "bold")

# Load the "Abibas.png" image
abibas_image = Image.open(
    "assets/Abibas.png"
) 

desired_width = 200
desired_height = 100

# Calculate new dimensions while preserving the aspect ratio
width, height = abibas_image.size #Original size
aspect_ratio = width / height #Aspect ratio calculation
if width > height:
    new_width = desired_width
    new_height = int(desired_width / aspect_ratio)
else:
    new_height = desired_height
    new_width = int(desired_height * aspect_ratio)

# Resize the image to the calculated dimensions
abibas_image = abibas_image.resize((new_width, new_height), Image.LANCZOS)

# Convert the resized image to a PhotoImage (Tkinter format)
abibas_photo = ImageTk.PhotoImage(abibas_image)

# Create a label to display the resized Abibas image
abibas_label = tk.Label(app, image=abibas_photo, bg="#A0FF91")
abibas_label.grid(row=0, column=0, columnspan=3, pady=(20, 10), sticky="n")


subtitle_label = tk.Label(
    app,
    text="Try on Accessories!",
    font=("Circular Std Book", 30),
    bg="#CCFFCC",
    fg="#333",
)
subtitle_label.grid(row=1, column=0, columnspan=3, sticky="n")

# Prevent the labels from disappearing when minimizing
app.grid_rowconfigure(0, weight=0) #wont expand or resize
app.grid_rowconfigure(1, weight=0) #wont expand or resize
app.grid_columnconfigure(0, weight=1) #will expand or resize
app.grid_columnconfigure(1, weight=1) #will expand or resize
app.grid_columnconfigure(2, weight=1) #will expand or resize


frame = None
gray = None
faces = None


def chooseFile():
    global frame, gray, faces, original_frame, file_path
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")]
    )
    if file_path:
        frame = cv2.imread(file_path, 1) #Reads in color mode
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA) #Converts to Blue Green Red Alpha format
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Converts image to grayscale
        faces = face_cascade.detectMultiScale(gray, 1.3, 10)
        original_frame = frame.copy()
        display_image(file_path)


def display_image(file_path):
    max_width = 400
    max_height = 400

    image = Image.open(file_path)

    # Calculate the aspect ratio to maintain proportions
    width, height = image.size
    new_width = width
    new_height = height

    if width > max_width or height > max_height:
        #The image is larger than the maximum size so we need to resize it proportionally
        ratio = min(max_width / width, max_height / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        image = image.resize((new_width, new_height), Image.LANCZOS)

    # Rounded corners
    mask = Image.new("L", (new_width, new_height), 0)
    draw = ImageDraw.Draw(mask)
    rounded_radius = 65
    draw.ellipse(
        (
            -rounded_radius,
            -rounded_radius,
            new_width + rounded_radius,
            new_height + rounded_radius,
        ),
        fill=255,
    )
    image.putalpha(mask)

    photo = ImageTk.PhotoImage(image)

    image_label.config(image=photo)
    image_label.image = photo

    put_mustache1_button.grid(row=6, column=0, padx=10, sticky="nsew")
    put_mustache2_button.grid(row=6, column=1, padx=10, sticky="nsew")
    put_mustache3_button.grid(row=6, column=2, padx=10, sticky="nsew")
    put_mustache4_button.grid(row=6, column=3, padx=10, sticky="nsew")

    app.update_idletasks()# Update the window

    # Create a label for the main image display
    image_label.grid(
        row=4, column=0, columnspan=3, pady=10, sticky="nsew"
    ) 

    #Hide buttons for now
    put_glasses1_button.grid_forget()
    put_glasses2_button.grid_forget()
    put_glasses3_button.grid_forget()
    put_glasses4_button.grid_forget()
    put_glasses5_button.grid_forget()


def apply_glasses(glasses_path):
    global frame, gray, faces
    if frame is not None:
        for x, y, w, h in faces: #Get coordinates of bounding boxes
            roi_gray = gray[y : y + h, x : x + w]#Region of interest in gray
            roi_color = frame[y : y + h, x : x + w]# Region of interest in color
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 10) # (where, scaleFactor, minNighbors)
            for x, y, w, h in eyes:
                glasses = cv2.imread(glasses_path, cv2.IMREAD_UNCHANGED) #Loading image with alpha channel
                eye1 = (eyes[0][0], eyes[0][1]) #Coordinate of top left first eye
                eye2 = (eyes[1][0] + eyes[1][3], eyes[1][1])# Coordinate of top right second eye
                eyesWidth = math.dist(eye1, eye2)
                eyesHeight = (int(eyes[0][1]) + int(eyes[1][1])) / 2 #Average height of two detected eyes
                eyesMidPointX = int(eyesWidth) / 2
                glassesHeight = float((eyes[0][3]+eyes[1][3])/2)
                glasses = cv2.resize(
                    glasses, (int(eyesWidth) + 10, int(glassesHeight) + 5)
                )
                gh, gw, gc= glasses.shape
                PlacementX = int(eyesMidPointX) - (gh // 2) #Since the glasses will be displayed with top left coordinates, I will make it so its somewhere around the left eye
                #Making transparent parts of the image show up as transparent
                for i in range(0, gh):
                    for j in range(0, gw): #Iterates over every pixel of glasses
                        if glasses[i, j][3] != 0: #If the pixel is not transparent then add it to the image (a value of 0 in the alpha channel would mean its transparent)
                            roi_color[int(eyesHeight) + i, int(PlacementX) + j] = glasses[i, j] #Apply every pixel of glasses image to the roi

            # Convert from BGR to RGB so PIL can use it
            modified_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

            # Create an image object from the modified image
            modified_image_pil = Image.fromarray(modified_image)

            max_width = 400
            max_height = 400

            # Initialize new_width and new_height
            new_width = modified_image_pil.width
            new_height = modified_image_pil.height

            # Calculate the aspect ratio to maintain proportions
            if new_width > max_width or new_height > max_height:
                ratio = min(max_width / new_width, max_height / new_height)
                new_width = int(new_width * ratio)
                new_height = int(new_height * ratio)
                modified_image_pil = modified_image_pil.resize(
                    (new_width, new_height), Image.LANCZOS
                )

            # Create a mask for the slightly rounded corners
            mask = Image.new("L", modified_image_pil.size, 0)
            draw = ImageDraw.Draw(mask)
            rounded_radius = 65
            draw.ellipse(
                (
                    -rounded_radius,
                    -rounded_radius,
                    new_width + rounded_radius,
                    new_height + rounded_radius,
                ),
                fill=255,
            )
            modified_image_pil.putalpha(mask)

            modified_image_pil.thumbnail((800, 800))
            modified_photo = ImageTk.PhotoImage(modified_image_pil)# Converts to a Tkinter photo

            #Display the image
            image_label.config(image=modified_photo)
            image_label.image = modified_photo

            # Hide glasses buttons
            put_glasses1_button.grid_forget()
            put_glasses2_button.grid_forget()
            put_glasses3_button.grid_forget()
            put_glasses4_button.grid_forget()
            put_glasses5_button.grid_forget()





def apply_accessories(accesories_path):
    global frame, gray, faces
    if frame is not None:
        for x, y, w, h in faces:
            roi_gray = gray[y : y + h, x : x + h]
            roi_color = frame[y : y + h, x : x + h]
            mouth = smile_cascade.detectMultiScale(roi_gray, 1.3, 30)
            for mx, my, mw, mh in mouth:
                accesories_img = cv2.imread(accesories_path, cv2.IMREAD_UNCHANGED)
                accessoriesHeight = mh / 2
                accessories_resized = cv2.resize(accesories_img, (mw, int(accessoriesHeight)))
                h, w, c = accessories_resized.shape
                accessoriesX = mouth[0][0]
                accessoriesY = int(mouth[0][1]) - int(w / 9) #Make the mustache above lips
                for i in range(0, h):
                    for j in range(0, w):
                        if accessories_resized[i, j][3] != 0:
                            roi_color[
                                int(accessoriesY) + i, int(accessoriesX) + j
                            ] = accessories_resized[i, j]

            modified_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            modified_image_pil = Image.fromarray(modified_image)

            max_width = 400
            max_height = 400

            new_width = modified_image_pil.width
            new_height = modified_image_pil.height

            if new_width > max_width or new_height > max_height:
                ratio = min(max_width / new_width, max_height / new_height)
                new_width = int(new_width * ratio)
                new_height = int(new_height * ratio)
                modified_image_pil = modified_image_pil.resize(
                    (new_width, new_height), Image.LANCZOS
                )

            #Create a mask for the slightly rounded corners
            mask = Image.new("L", modified_image_pil.size, 0)
            draw = ImageDraw.Draw(mask)
            rounded_radius = 65 
            draw.ellipse(
                (
                    -rounded_radius,
                    -rounded_radius,
                    new_width + rounded_radius,
                    new_height + rounded_radius,
                ),
                fill=255,
            )
            modified_image_pil.putalpha(mask)

            modified_image_pil.thumbnail((800, 800))
            modified_photo = ImageTk.PhotoImage(modified_image_pil)

            image_label.config(image=modified_photo)
            image_label.image = modified_photo

            # Hide mustache buttons
            put_mustache1_button.grid_forget()
            put_mustache2_button.grid_forget()
            put_mustache3_button.grid_forget()
            put_mustache4_button.grid_forget()

            # Show glasses buttons
            put_glasses1_button.grid(row=6, column=0, padx=10)
            put_glasses2_button.grid(row=6, column=1, padx=10)
            put_glasses3_button.grid(row=6, column=2, padx=10)
            put_glasses4_button.grid(row=6, column=3, padx=10)
            put_glasses5_button.grid(row=6, column=4, padx=10)


def reset_frame():
    global frame, gray, faces, file_path
    if original_frame is not None:
        frame = original_frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 10)
        display_image(file_path)


button_width = int(
    app.winfo_screenwidth() * 0.05
)
button_height = int(
    app.winfo_screenwidth() * 0.03
)


#create a frame for the upload and reset buttons
upload_reset_frame = tk.Frame(app, bg="#121212")
upload_reset_frame.grid(row=5, column=0, columnspan=3, pady=(0, 10), sticky="n")

upload_button = tk.Button(
    upload_reset_frame,
    text="Upload Image",
    font=button_font,
    compound=tk.CENTER,
    bg="#007bff",
    fg="#121212",
    width=10,
    height=2,
    command=chooseFile,
    borderwidth=5,
    relief="ridge",
    padx=20,
    pady=10,
)
upload_button.grid(row=0, column=0, padx=(10, 5))

reset_button = tk.Button(
    upload_reset_frame,
    text="Reset",
    font=button_font,
    bg="#dc3545",
    compound=tk.CENTER,
    fg="#121212",
    width=10,
    height=2,
    command=reset_frame,
    borderwidth=5,
    relief="ridge",
    padx=20,
    pady=10,
)
reset_button.grid(row=0, column=1, padx=(5, 10))


# Create a frame for the accessories buttons
button_frame = tk.Frame(app, bg="#121212", width=button_width, height=button_height)
button_frame.grid(row=3, column=0, columnspan=3, pady=5)


mustache_image1 = Image.open("assets/mustachep.jpg")
mustache_image1 = mustache_image1.resize((button_width, button_height), Image.LANCZOS)
mustache_photo1 = ImageTk.PhotoImage(mustache_image1)

put_mustache1_button = tk.Button(
    button_frame,
    image=mustache_photo1,
    compound=tk.CENTER,
    bg="#121212",
    fg="#121212",
    width=button_width,
    height=button_height,
    command=lambda: apply_accessories("assets/mustache.png"),
    relief="ridge",
    borderwidth=5,
)

mustache_image2 = Image.open("assets/mustachep2.jpg")
mustache_image2 = mustache_image2.resize((button_width, button_height), Image.LANCZOS)
mustache_photo2 = ImageTk.PhotoImage(mustache_image2)

put_mustache2_button = tk.Button(
    button_frame,
    image=mustache_photo2,
    compound=tk.CENTER,
    bg="#121212",
    fg="#fff",
    width=button_width,
    height=button_height,
    command=lambda: apply_accessories("assets/mustache2.png"),
    relief="ridge",
    borderwidth=5,
)

mustache_image3 = Image.open("assets/piercing.jpg")
mustache_image3 = mustache_image3.resize((button_width, button_height), Image.LANCZOS)
mustache_photo3 = ImageTk.PhotoImage(mustache_image3)

put_mustache3_button = tk.Button(
    button_frame,
    image=mustache_photo3,
    compound=tk.CENTER,
    bg="#121212",
    fg="#fff",
    width=button_width,
    height=button_height,
    command=lambda: apply_accessories("assets/piercing.png"),
    relief="ridge",
    borderwidth=5,
)

mustache_image4 = Image.open("assets/piercing1.jpg")
mustache_image4 = mustache_image4.resize((button_width, button_height), Image.LANCZOS)
mustache_photo4 = ImageTk.PhotoImage(mustache_image4)

put_mustache4_button = tk.Button(
    button_frame,
    image=mustache_photo4,
    compound=tk.CENTER,
    bg="#121212",
    fg="#fff",
    width=button_width,
    height=button_height,
    command=lambda: apply_accessories("assets/piercing1.png"),
    relief="ridge",
    borderwidth=5,
)

glasses_image1 = Image.open("assets/glassesp1.jpg")
glasses_image1 = glasses_image1.resize((button_width, button_height), Image.LANCZOS)
glasses_photo1 = ImageTk.PhotoImage(glasses_image1)

put_glasses1_button = tk.Button(
    button_frame,
    image=glasses_photo1,
    compound=tk.CENTER,
    bg="#121212",
    fg="#fff",
    width=button_width,
    height=button_height,
    command=lambda: apply_glasses("assets/glasses1.png"),
    relief="ridge",
    borderwidth=5,
)

glasses_image2 = Image.open("assets/glassesp2.jpg")
glasses_image2 = glasses_image2.resize((button_width, button_height), Image.LANCZOS)
glasses_photo2 = ImageTk.PhotoImage(glasses_image2)

put_glasses2_button = tk.Button(
    button_frame,
    image=glasses_photo2,
    compound=tk.CENTER,
    bg="#121212",
    fg="#fff",
    width=button_width,
    height=button_height,
    command=lambda: apply_glasses("assets/glasses2.png"),
    relief="ridge",
    borderwidth=5,
)

glasses_image3 = Image.open("assets/glassesp3.jpg")
glasses_image3 = glasses_image3.resize((button_width, button_height), Image.LANCZOS)
glasses_photo3 = ImageTk.PhotoImage(glasses_image3)

put_glasses3_button = tk.Button(
    button_frame,
    image=glasses_photo3,
    compound=tk.CENTER,
    bg="#121212",
    fg="#fff",
    width=button_width,
    height=button_height,
    command=lambda: apply_glasses("assets/glasses3.png"),
    relief="ridge",
    borderwidth=5,
)

glasses_image4 = Image.open("assets/glassesp4.jpg")
glasses_image4 = glasses_image4.resize((button_width, button_height), Image.LANCZOS)
glasses_photo4 = ImageTk.PhotoImage(glasses_image4)

put_glasses4_button = tk.Button(
    button_frame,
    image=glasses_photo4,
    compound=tk.CENTER,
    bg="#121212",
    fg="#fff",
    width=button_width,
    height=button_height,
    command=lambda: apply_glasses("assets/glasses4.png"),
    relief="ridge",
    borderwidth=5,
)

glasses_image5 = Image.open("assets/glassesp5.jpg")
glasses_image5 = glasses_image5.resize((button_width, button_height), Image.LANCZOS)
glasses_photo5 = ImageTk.PhotoImage(glasses_image5)

put_glasses5_button = tk.Button(
    button_frame,
    image=glasses_photo5,
    compound=tk.CENTER,
    bg="#121212",
    fg="#fff",
    width=button_width,
    height=button_height,
    command=lambda: apply_glasses("assets/glasses5.png"),
    relief="ridge",
    borderwidth=5,
)

# label for the main image display
image_label = tk.Label(app)
image_label.configure(bg="#121212")

app.mainloop()
