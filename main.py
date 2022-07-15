# Importing all necessary libraries from multiprocessing.connection import Listener
import cv2
import os
from pynput.keyboard import Key, Listener
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd


wait_key = 10
current_frame_array = []
is_beginning = True
frame_range = [0, 0]
video_string = ""
data_string = ""
destination_string = ""
img_array = []
is_paused = False
current_frame = 0
end_program = False
one_pressed = False
num = 0
jump = False
jump_end = False


def run_main():
    global jump
    global num
    if destination_label["text"] != "mp4 file" and video_label["text"] != "select destination":
        global current_frame
        root.destroy()
        # Collect events until released
        with Listener(on_press=on_press, on_release=on_release) as listener:
            video_window = tk.Tk("Express Video Chopper")
            vid = cv2.VideoCapture(video_string)
            if not vid.isOpened():
                print("error...")

            while vid.isOpened():
                if jump:
                    vid.set(1, num)
                    jump = False
                elif jump_end:
                    break
                    # vid.set(1, vid.get(cv2.CAP_PROP_FRAME_COUNT) + 1)
                ute, pic_fra = vid.read()
                num = num + 1
                if ute and not end_program:
                    cv2.imshow("Express Video Chopper", pic_fra)
                    current_frame = int(vid.get(cv2.CAP_PROP_POS_FRAMES))
                    if cv2.waitKey(wait_key) & 0xFF == ord('u'):
                        break
                else:
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    break

            vid.release()

            # run the application
            listener.join()

            cv2.destroyAllWindows()


def check_frame(frame):
    for x in current_frame_array:
        if x[0] <= frame <= x[1]:
            return True
    return False


def get_next_frame(frame):
    for x in current_frame_array:
        if frame < x[0] and frame < x[1]:
            return x[0]
    return frame


def on_press(key):
    global wait_key
    global is_paused
    global is_beginning
    global frame_range
    global current_frame
    global end_program
    global one_pressed
    global jump
    global num
    if key == Key.space and not is_paused:
        if is_beginning:
            frame_range[0] = current_frame
            print("Recording from " + str(frame_range[0]))
            is_beginning = False
        else:
            frame_range[1] = current_frame
            current_frame_array.append(frame_range)
            print("Stopped Recording at " + str(frame_range[1]))
            frame_range = [0, 0]
            is_beginning = True
    if format(key) == '\'s\'' and not is_paused:
        save_video()
    if format(key) == '\'r\'' and not is_paused:
        current_frame_array.pop()
        print("Deleted last frames...")
    if key == Key.ctrl_l or key == Key.ctrl_r and not is_paused:
        wait_key = 1
    if format(key) == '\'p\'':
        if is_paused and one_pressed:
            wait_key = 10
            is_paused = False
            print("Video resume...")
        elif not is_paused:
            wait_key = 0
            is_paused = True
            print("Video paused...")
    if format(key) == '\'q\'' and not is_paused:
        print("Exiting program...press q again")
        end_program = True
    if format(key) == '\'1\'':
        one_pressed = True
    if key == Key.left and not is_paused:
        jump = True
        num = num - 30


def on_release(key):
    global jump
    global num
    global one_pressed
    global wait_key
    if key == Key.right and not is_paused:
        wait_key = 10
    if format(key) == '\'1\'':
        one_pressed = False
    if key == Key.right and not is_paused:
        jump = True
        num = num + 324000


def save_video():
    global end_program
    global is_paused
    is_paused = True
    print("Video paused...")
    print("Saving video...")
    # Read the video from specified path
    cam = cv2.VideoCapture(video_string)

    # frame
    currentframe = 0
    width = 1920
    height = 1080

    mp4string = "new_video.mp4"
    path_count = 1

    while os.path.exists(destination_string + "/" + mp4string):
        mp4string = "new_video(" + str(path_count) + ").mp4"
        path_count += 1

    # choose codec according to format needed
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(destination_string + "/" + mp4string, fourcc, 30, (width, height))
    cam.set(1, current_frame_array[0][0])
    while True:
        # reading from frame
        ret, frame = cam.read()
        if ret:
            # writing the extracted images
            if check_frame(currentframe):
                video.write(frame)
            else:
                cam.set(1, get_next_frame(currentframe))
                currentframe = int(cam.get(cv2.CAP_PROP_POS_FRAMES))

            # increasing counter so that it will
            # show how many frames are created
            currentframe += 1
            if currentframe > current_frame_array[len(current_frame_array) - 1][1]:
                break
        else:
            break

    cam.release()
    video.release()
    print("Video saved")
    end_program = True


def select_media_file():
    global video_string
    global codec_num
    media_filetypes = (
        ('MP4', '*.mp4'),
        ('MOV', '*.mov'),
        ('All files', '*.*')
    )

    video_string = fd.askopenfilename(
        title='Import Video',
        initialdir='/',
        filetypes=media_filetypes)
    if video_string != "":
        video_label["text"] = video_string


def choose_directory():
    global destination_string
    destination_string = fd.askdirectory(
        title='Select Destination')
    if destination_string != "":
        destination_label["text"] = destination_string


# create the root window
root = tk.Tk()
root.title('Express Video Trimmer Setup')
root.resizable(False, False)
root.geometry('1000x300')

# video file label
video_label = ttk.Label(
    root,
    text="mp4 file")
video_label.pack()

# import video button
import_video_button = ttk.Button(
    root,
    text='Import Video',
    command=select_media_file
)
import_video_button.pack(expand=True)

# space label
space_label = ttk.Label(
    root,
    text="")
space_label.pack()

# select destination label
destination_label = ttk.Label(
    root,
    text="select destination")
destination_label.pack()

# choose directory button
choose_directory_button = ttk.Button(
    root,
    text='Choose Directory',
    command=choose_directory
)
choose_directory_button.pack(expand=True)

# space label
space_label = ttk.Label(
    root,
    text="")
space_label.pack()

# go button
go_button = ttk.Button(
    root,
    text='Go',
    command=run_main
)
go_button.pack(expand=True)

# run the application
root.mainloop()

# Release all space and windows once done
cv2.destroyAllWindows()
