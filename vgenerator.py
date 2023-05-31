import moviepy.editor as me
from moviepy.video.compositing.concatenate import concatenate_videoclips
import csv
import numpy as np
from moviepy.editor import clips_array
from moviepy.config import change_settings
from PIL import Image

def generate():

    change_settings(    {"IMAGEMAGICK_BINARY": r"C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"}) 
    
    images = []
    captions = []
    timestamps = []
    positionstexts = []
    image_clips = []
    voidclips = []
    positionsimages = [(0.1, 0.9), (0.5, 0.9), (0.9, 0.9),
                    (0.1, 0.5), (0.5, 0.5), (0.9, 0.5),
                    (0.1, 0.1), (0.5, 0.1), (0.9, 0.1)]
    positionsimagesstandard = [(0.5, 0.5), (0.1, 0.9),
                            (0.9, 0.9), (0.1, 0.1), (0.9, 0.1)]


    with open('config.txt') as f:
        lines = f.readlines()
        for index,line in enumerate(lines):
            lines[index]=line.replace("\n", "")
        print(lines)

    while True:
        try:
            x = "./input/"+lines[0]
            videopath = x
            video = me.VideoFileClip(videopath)
            break
        except OSError:
            print("File not found, edit config file")
            exit() 
    video = video.resize((1920, 1080))
    while True:
        try:
            pathTimest = "./spreadsheets/" + lines[1]
            with open(pathTimest, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                    timestamps.append(row)
            break
        except OSError:
            print("File not found, edit config file")
            exit()
    for timestamp in timestamps:
        timestamp[0] = timestamp[0].replace("\"", '')
        timestamp[0] = timestamp[0].replace("Untitled - ", '')
        timestamp[0]= timestamp[0].split('.', 1)[0]
        if lines[6]=="Default timestamp duration? yes":
            if len(timestamp)==2:
                timestamp[1]=int(lines[7])
            elif len(timestamp)==1:
                timestamp.append(int(lines[7]))
        elif lines[6]=="Default timestamp duration? no":
            timestamp[1] = timestamp[1].replace("\"", '')
            timestamp[1] = int(timestamp[1])
        else:
            print("Invalid input, edit config file")
            exit()
        h, m, s = timestamp[0].split(':')
        timestamp.append(int(h) * 3600 + int(m) * 60 + int(s))

    while True:
        try:
            pathCaptions = "./spreadsheets/" + lines[2]
            with open(pathCaptions, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for row in spamreader:
                    captions.append(row)
            if lines[3]=="generate file names automatically: yes":
                with open('./spreadsheets/'+lines[4], 'w+') as f:
            # create the csv writer
                # write a row to the csv file
                    for i in range(0,len(captions)):
                        filename=str(i)+".jpg"
                        f.write(filename)
                        f.write("\n")
                    for i in timestamps:
                        for j in range(0,9):
                            f.write("\n")
                while True:
                    try:
                        pathImages = "./spreadsheets/" + lines[4]
                        with open(pathImages, newline='') as csvfile:
                            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                            for row in spamreader:
                                images.append(row)
                        break
                    except OSError:
                        print("File not found, edit config file")
                        exit()
            elif lines[3]=="generate file names automatically: no":
                while True:
                    try:
                        pathImages = "./spreadsheets/" + lines[4]
                        with open(pathImages, newline='') as csvfile:
                            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                            for row in spamreader:
                                images.append(row)
                        break
                    except OSError:
                        print("File not found, edit config file")
                        exit()
            else:
                print("Invalid input, edit config file")
                exit()
            break
        except OSError:
            print("File not found, edit config file")
            exit()
    for image in images:
        if image!=[]:
            img = Image.open("./images/"+image[0])

        # Convert the image to RGB format
            img = img.convert("RGB")
            img.save("./images/"+image[0])

    i = 0
    if timestamps[0][2] != 0:
        voidclips.append(video.subclip(0, timestamps[0][2]))
    voidbegin = []
    for timestamp in timestamps:
        voidbegin.append(timestamp[2]+timestamp[1])
    for index, timestamp in enumerate(timestamps):
        if index == 0:
            continue
        voidclips.append("")
        voidclips.append(video.subclip(voidbegin[i], timestamp[2]))
        i = i+1
    i = 0
    voidclips.append("")
    if timestamps[len(timestamps)-1][2]+timestamps[len(timestamps)-1][1] < video.duration:
        voidclips.append(video.subclip(timestamps[len(
            timestamps)-1][2]+timestamps[len(timestamps)-1][1], video.duration))
    print("")

    while True:
        i=0
        for timestamp in timestamps:
            standardornot = ""
            while not ((standardornot == "Cross") or (standardornot == "3x3")):
                standardornot = lines[5]
                if not ((standardornot == "Cross") or (standardornot == "3x3")):
                    print("Invalid input, edit config file")
                    exit()

            if standardornot == "Cross":
                if images[i] == []:
                    image5 = me.ColorClip(color=[0, 0, 0], size=(
                        1, 1), duration=timestamp[1])
                    caption5 = me.TextClip(" ", fontsize=25, color="white", size=(
                        1, 1), bg_color="transparent").set_duration(timestamp[1])
                    i = i+1
                else:
                    image5 = me.ImageClip("./images/"+images[i][0])
                    if image5.size[1] <= image5.size[0]:
                        image5 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(width=450)
                        image5 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                            width=450).set_position((0.5*1920-225, 0.5*1080-image5.size[1]/2))
                    else:
                        image5 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(height=450)
                        image5 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                            height=450).set_position((0.5*1920-image5.size[0]/2, 0.5*1080-225))
                    if captions[i] == []:
                        caption5 = me.TextClip(" ", fontsize=25, color="white", size=(
                            1, 1), bg_color="transparent").set_duration(timestamp[1])
                    else:
                        fullcaption = ""
                        for c in captions[i]:
                            fullcaption = fullcaption+c
                            fullcaption = fullcaption+' '
                        caption5 = me.TextClip(fullcaption, font='Amiri-Bold', bg_color='black', fontsize=25, color='white', method='caption', size=(
                            image5.size[0], None)).set_duration(timestamp[1]).set_position((0.5*1920-image5.size[0]/2, 0.5*1080-image5.size[1]/2-45))
                        caption5 = me.TextClip(fullcaption, font='Amiri-Bold', bg_color='black', fontsize=25, color='white', method='caption', size=(
                            image5.size[0], None)).set_duration(timestamp[1]).set_position((0.5*1920-image5.size[0]/2, 0.5*1080-image5.size[1]/2-caption5.size[1]))
                    i = i+1

                if images[i] == []:
                    image1 = me.ColorClip(color=[0, 0, 0], size=(
                        1, 1), duration=timestamp[1])
                    caption1 = me.TextClip(" ", fontsize=25, color="white", size=(
                        1, 1), bg_color="transparent").set_duration(timestamp[1])
                    i = i+1
                else:
                    image1 = me.ImageClip("./images/"+images[i][0])
                    if image1.size[1] <= image1.size[0]:
                        image1 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(width=450)
                        image1 = me.ImageClip("./images/"+images[i][0]).set_duration(
                            timestamp[1]).resize(width=450).set_position((0.025*1920, 0.075*1080))
                    else:
                        image1 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(height=300)
                        image1 = me.ImageClip("./images/"+images[i][0]).set_duration(
                            timestamp[1]).resize(height=300).set_position((0.025*1920, 0.075*1080))
                    if captions[i] == []:
                        caption1 = me.TextClip(" ", fontsize=25, color="white", size=(
                            1, 1), bg_color="transparent").set_duration(timestamp[1])
                    else:
                        fullcaption = ""
                        for c in captions[i]:
                            fullcaption = fullcaption+c
                            fullcaption = fullcaption+' '
                        caption1 = me.TextClip(fullcaption, font='Amiri-Bold', fontsize=20, bg_color='black', color='white', method='caption',
                                            size=(image1.size[0], None)).set_duration(timestamp[1]).set_position((0.025*1920, 0.075*1080-45))
                        if image1.size[1] <= image1.size[0]:
                            image1 = me.ImageClip(
                                "./images/"+images[i][0]).set_duration(timestamp[1]).resize(width=450)
                            image1 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                                width=450).set_position((0.025*1920, 0.075*1080-45+caption1.size[1]))
                        else:
                            image1 = me.ImageClip(
                                "./images/"+images[i][0]).set_duration(timestamp[1]).resize(height=300)
                            image1 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                                height=300).set_position((0.025*1920, 0.075*1080-45+caption1.size[1]))
                    i = i+1

                if images[i] == []:
                    image3 = me.ColorClip(color=[0, 0, 0], size=(
                        1, 1), duration=timestamp[1])
                    caption3 = me.TextClip(" ", fontsize=25, color="white", size=(
                        1, 1), bg_color="transparent").set_duration(timestamp[1])
                    i = i+1
                else:
                    image3 = me.ImageClip("./images/"+images[i][0])
                    if image3.size[1] <= image3.size[0]:
                        image3 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(width=450)
                        image3 = me.ImageClip("./images/"+images[i][0]).set_duration(
                            timestamp[1]).resize(width=450).set_position((1920-450-0.025*1920, 0.075*1080))
                    else:
                        image3 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(height=300)
                        image3 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                            height=300).set_position((1920-image3.size[0]-0.025*1920, 0.075*1080))
                    if captions[i] == []:
                        caption3 = me.TextClip(" ", fontsize=25, color="white", size=(
                            1, 1), bg_color="transparent").set_duration(timestamp[1])
                    else:
                        fullcaption = ""
                        for c in captions[i]:
                            fullcaption = fullcaption+c
                            fullcaption = fullcaption+' '
                        caption3 = me.TextClip(fullcaption, font='Amiri-Bold', fontsize=20, bg_color='black', color='white', method='caption', size=(
                            image3.size[0], None)).set_duration(timestamp[1]).set_position((1920-image3.size[0]-0.025*1920, 0.075*1080-45))
                        if image3.size[1] <= image3.size[0]:
                            image3 = me.ImageClip(
                                "./images/"+images[i][0]).set_duration(timestamp[1]).resize(width=450)
                            image3 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                                width=450).set_position((1920-450-0.025*1920, 0.075*1080-45+caption3.size[1]))
                        else:
                            image3 = me.ImageClip(
                                "./images/"+images[i][0]).set_duration(timestamp[1]).resize(height=300)
                            image3 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                                height=300).set_position((1920-image3.size[0]-0.025*1920, 0.075*1080-45+caption3.size[1]))
                    i = i+1

                if images[i] == []:
                    image7 = me.ColorClip(color=[0, 0, 0], size=(
                        1, 1), duration=timestamp[1])
                    caption7 = me.TextClip(" ", fontsize=25, color="white", size=(
                        1, 1), bg_color="transparent").set_duration(timestamp[1])
                    i = i+1
                else:
                    image7 = me.ImageClip("./images/"+images[i][0])
                    if image7.size[1] <= image7.size[0]:
                        image7 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(width=450)
                        image7 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                            width=450).set_position((0.025*1920, 1080-0.025*1080-image7.size[1]))
                    else:
                        image7 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(height=300)
                        image7 = me.ImageClip("./images/"+images[i][0]).set_duration(
                            timestamp[1]).resize(height=300).set_position((0.025*1920, 1080-0.025*1080-300))
                    if captions[i] == []:
                        caption7 = me.TextClip(" ", fontsize=25, color="white", size=(
                            1, 1), bg_color="transparent").set_duration(timestamp[1])
                    else:
                        fullcaption = ""
                        for c in captions[i]:
                            fullcaption = fullcaption+c
                            fullcaption = fullcaption+' '
                        caption7 = me.TextClip(fullcaption, font='Amiri-Bold', bg_color='black', fontsize=20, color='white', method='caption', size=(
                            image7.size[0], None)).set_duration(timestamp[1]).set_position((0.025*1920, 1080-0.025*1080-image7.size[1]-45))
                        caption7 = me.TextClip(fullcaption, font='Amiri-Bold', bg_color='black', fontsize=20, color='white', method='caption', size=(
                            image7.size[0], None)).set_duration(timestamp[1]).set_position((0.025*1920, 1080-0.025*1080-image7.size[1]-caption7.size[1]))
                    i = i+1

                if images[i] == []:
                    image9 = me.ColorClip(color=[0, 0, 0], size=(
                        1, 1), duration=timestamp[1])
                    caption9 = me.TextClip(" ", fontsize=25, color="white", size=(
                        1, 1), bg_color="transparent").set_duration(timestamp[1])
                else:
                    image9 = me.ImageClip("./images/"+images[i][0])
                    if image9.size[1] <= image9.size[0]:
                        image9 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(width=450)
                        image9 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                            width=450).set_position((1920-450-0.025*1920, 1080-0.025*1080-image9.size[1]))
                    else:
                        image9 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(height=300)
                        image9 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                            height=300).set_position((1920-image9.size[0]-0.025*1920, 1080-0.025*1080-300))
                    if captions[i] == []:
                        caption9 = me.TextClip(" ", fontsize=25, color="white", size=(
                            1, 1), bg_color="transparent").set_duration(timestamp[1])
                    else:
                        fullcaption = ""
                        for c in captions[i]:
                            fullcaption = fullcaption+c
                            fullcaption = fullcaption+' '
                        caption9 = me.TextClip(fullcaption, font='Amiri-Bold', bg_color='black', fontsize=20, color='white', method='caption', size=(
                            image9.size[0], None)).set_duration(timestamp[1]).set_position((1920-image9.size[0]-0.025*1920, 1080-0.025*1080-image9.size[1]-45))
                        caption9 = me.TextClip(fullcaption, font='Amiri-Bold', bg_color='black', fontsize=20, color='white', method='caption', size=(
                            image9.size[0], None)).set_duration(timestamp[1]).set_position((1920-image9.size[0]-0.025*1920, 1080-0.025*1080-image9.size[1]-caption9.size[1]))

                clip = video.subclip(timestamp[2], timestamp[2]+timestamp[1])
                image_clips.append(me.CompositeVideoClip(
                    [clip, image5, image1, image3, image7, image9, caption5, caption1, caption3, caption7, caption9]))
                i = i+1

            elif standardornot == "3x3":

                if images[i] == []:
                    image1 = me.ColorClip(color=[0, 0, 0], size=(
                        1, 1), duration=timestamp[1])
                    caption1 = me.TextClip(" ", fontsize=25, color="white", size=(
                        1, 1), bg_color="transparent").set_duration(timestamp[1])
                    i = i+1
                else:
                    image1 = me.ImageClip("./images/"+images[i][0])
                    if image1.size[1] <= image1.size[0]:
                        image1 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(width=250)
                        image1 = me.ImageClip("./images/"+images[i][0]).set_duration(
                            timestamp[1]).resize(width=250).set_position((0.01*1920, 0.01*1080))
                    else:
                        image1 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(height=180)
                        image1 = me.ImageClip("./images/"+images[i][0]).set_duration(
                            timestamp[1]).resize(height=180).set_position((0.01*1920, 0.01*1080))
                    if captions[i] == []:
                        caption1 = me.TextClip(" ", fontsize=25, color="white", size=(
                            1, 1), bg_color="transparent").set_duration(timestamp[1])
                    else:
                        fullcaption = ""
                        for c in captions[i]:
                            fullcaption = fullcaption+c
                            fullcaption = fullcaption+' '
                        caption1 = me.TextClip(fullcaption, font='Amiri-Bold', fontsize=20, bg_color='black', color='white', method='caption',
                                            size=(250, None)).set_duration(timestamp[1]).set_position((0.01*1920, 0.01*1080))
                        if image1.size[1] <= image1.size[0]:
                            image1 = me.ImageClip(
                                "./images/"+images[i][0]).set_duration(timestamp[1]).resize(width=250)
                            image1 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                                width=250).set_position((0.01*1920, 0.01*1080+caption1.size[1]))
                        else:
                            image1 = me.ImageClip(
                                "./images/"+images[i][0]).set_duration(timestamp[1]).resize(height=180)
                            image1 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                                height=180).set_position((0.01*1920+125-image1.size[0]/2, 0.01*1080+caption1.size[1]))
                    i = i+1

                if images[i] == []:
                    image2 = me.ColorClip(color=[0, 0, 0], size=(
                        1, 1), duration=timestamp[1])
                    caption2 = me.TextClip(" ", fontsize=25, color="white", size=(
                        1, 1), bg_color="transparent").set_duration(timestamp[1])
                    i = i+1
                else:
                    image2 = me.ImageClip("./images/"+images[i][0])
                    if image2.size[1] <= image2.size[0]:
                        image2 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(width=250)
                        image2 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                            width=250).set_position((0.5*1920-125,  0.01*1080))
                    else:
                        image2 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(height=180)
                        image2 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                            height=180).set_position((0.5*1920-image2.size[0]/2,  0.01*1080))
                    if captions[i] == []:
                        caption2 = me.TextClip(" ", fontsize=25, color="white", size=(
                            1, 1), bg_color="transparent").set_duration(timestamp[1])
                    else:
                        fullcaption = ""
                        for c in captions[i]:
                            fullcaption = fullcaption+c
                            fullcaption = fullcaption+' '
                        caption2 = me.TextClip(fullcaption, font='Amiri-Bold', bg_color='black', fontsize=20, color='white', method='caption', size=(
                            250, None)).set_duration(timestamp[1]).set_position((0.5*1920-125,  0.01*1080))
                        caption2 = me.TextClip(fullcaption, font='Amiri-Bold', bg_color='black', fontsize=20, color='white', method='caption', size=(
                            250, None)).set_duration(timestamp[1]).set_position((0.5*1920-125,  0.01*1080))
                        if image2.size[1] <= image2.size[0]:
                            image2 = me.ImageClip(
                                "./images/"+images[i][0]).set_duration(timestamp[1]).resize(width=250)
                            image2 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                                width=250).set_position((0.5*1920-125,  0.01*1080+caption2.size[1]))
                        else:
                            image2 = me.ImageClip(
                                "./images/"+images[i][0]).set_duration(timestamp[1]).resize(height=180)
                            image2 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                                height=180).set_position((0.5*1920-image2.size[0]/2,  0.01*1080+caption2.size[1]))
                    i = i+1

                if images[i] == []:
                    image3 = me.ColorClip(color=[0, 0, 0], size=(
                        1, 1), duration=timestamp[1])
                    caption3 = me.TextClip(" ", fontsize=25, color="white", size=(
                        1, 1), bg_color="transparent").set_duration(timestamp[1])
                    i = i+1
                else:
                    image3 = me.ImageClip("./images/"+images[i][0])
                    if image3.size[1] <= image3.size[0]:
                        image3 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(width=250)
                        image3 = me.ImageClip("./images/"+images[i][0]).set_duration(
                            timestamp[1]).resize(width=250).set_position((1920-250-0.01*1920, 0.01*1080))
                    else:
                        image3 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(height=180)
                        image3 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                            height=180).set_position((1920-125-0.01*1920, 0.01*1080))
                    if captions[i] == []:
                        caption3 = me.TextClip(" ", fontsize=25, color="white", size=(
                            1, 1), bg_color="transparent").set_duration(timestamp[1])
                    else:
                        fullcaption = ""
                        for c in captions[i]:
                            fullcaption = fullcaption+c
                            fullcaption = fullcaption+' '
                        caption3 = me.TextClip(fullcaption, font='Amiri-Bold', fontsize=20, bg_color='black', color='white', method='caption', size=(
                            250, None)).set_duration(timestamp[1]).set_position((1920-250-0.01*1920, 0.01*1080))
                        if image3.size[1] <= image3.size[0]:
                            image3 = me.ImageClip(
                                "./images/"+images[i][0]).set_duration(timestamp[1]).resize(width=250)
                            image3 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                                width=250).set_position((1920-250-0.01*1920, 0.01*1080+caption3.size[1]))
                        else:
                            image3 = me.ImageClip(
                                "./images/"+images[i][0]).set_duration(timestamp[1]).resize(height=180)
                            image3 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                                height=180).set_position((1920-image3.size[0]/2-0.01*1920-125, 0.01*1080+caption3.size[1]))
                    i = i+1

                if images[i] == []:
                    image4 = me.ColorClip(color=[0, 0, 0], size=(
                        1, 1), duration=timestamp[1])
                    caption4 = me.TextClip(" ", fontsize=25, color="white", size=(
                        1, 1), bg_color="transparent").set_duration(timestamp[1])
                    i = i+1
                else:
                    image4 = me.ImageClip("./images/"+images[i][0])
                    if image4.size[1] <= image4.size[0]:
                        image4 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(width=250)
                        image4 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                            width=250).set_position((0.01*1920, 0.5*1080-image4.size[1]/2))
                    else:
                        image4 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(height=180)
                        image4 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                            height=180).set_position((0.01*1920+125-image4.size[0]/2, 0.5*1080-90))
                    if captions[i] == []:
                        caption4 = me.TextClip(" ", fontsize=25, color="white", size=(
                            1, 1), bg_color="transparent").set_duration(timestamp[1])
                    else:
                        fullcaption = ""
                        for c in captions[i]:
                            fullcaption = fullcaption+c
                            fullcaption = fullcaption+' '
                        caption4 = me.TextClip(fullcaption, font='Amiri-Bold', bg_color='black', fontsize=20, color='white', method='caption', size=(
                            250, None)).set_duration(timestamp[1]).set_position((0.01*1920, 0.5*1080-image4.size[1]/2-40))
                        caption4 = me.TextClip(fullcaption, font='Amiri-Bold', bg_color='black', fontsize=20, color='white', method='caption', size=(
                            250, None)).set_duration(timestamp[1]).set_position((0.01*1920, 0.5*1080-image4.size[1]/2-caption4.size[1]))
                    i = i+1

                if images[i] == []:
                    image5 = me.ColorClip(color=[0, 0, 0], size=(
                        1, 1), duration=timestamp[1])
                    caption5 = me.TextClip(" ", fontsize=25, color="white", size=(
                        1, 1), bg_color="transparent").set_duration(timestamp[1])
                    i = i+1
                else:
                    image5 = me.ImageClip("./images/"+images[i][0])
                    if image5.size[1] <= image5.size[0]:
                        image5 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(width=250)
                        image5 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                            width=250).set_position((0.5*1920-125, 0.5*1080-image5.size[1]/2))
                    else:
                        image5 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(height=180)
                        image5 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                            height=180).set_position((0.5*1920-image5.size[0]/2, 0.5*1080-90))
                    if captions[i] == []:
                        caption5 = me.TextClip(" ", fontsize=25, color="white", size=(
                            1, 1), bg_color="transparent").set_duration(timestamp[1])
                    else:
                        fullcaption = ""
                        for c in captions[i]:
                            fullcaption = fullcaption+c
                            fullcaption = fullcaption+' '
                        caption5 = me.TextClip(fullcaption, font='Amiri-Bold', bg_color='black', fontsize=20, color='white', method='caption', size=(
                            250, None)).set_duration(timestamp[1]).set_position((0.5*1920-125, 0.5*1080-image5.size[1]/2-40))
                        caption5 = me.TextClip(fullcaption, font='Amiri-Bold', bg_color='black', fontsize=20, color='white', method='caption', size=(
                            250, None)).set_duration(timestamp[1]).set_position((0.5*1920-125, 0.5*1080-image5.size[1]/2-caption5.size[1]))
                    i = i+1

                if images[i] == []:
                    image6 = me.ColorClip(color=[0, 0, 0], size=(
                        1, 1), duration=timestamp[1])
                    caption6 = me.TextClip(" ", fontsize=25, color="white", size=(
                        1, 1), bg_color="transparent").set_duration(timestamp[1])
                    i = i+1
                else:
                    image6 = me.ImageClip("./images/"+images[i][0])
                    if image6.size[1] <= image6.size[0]:
                        image6 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(width=250)
                        image6 = me.ImageClip("./images/"+images[i][0]).set_duration(
                            timestamp[1]).resize(width=250).set_position((1920-250-0.01*1920, 0.5*1080-image6.size[1]/2))
                    else:
                        image6 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(height=180)
                        image6 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                            height=180).set_position((1920-image6.size[0]/2-0.01*1920-125,  0.5*1080-90))
                    if captions[i] == []:
                        caption6 = me.TextClip(" ", fontsize=25, color="white", size=(
                            1, 1), bg_color="transparent").set_duration(timestamp[1])
                    else:
                        fullcaption = ""
                        for c in captions[i]:
                            fullcaption = fullcaption+c
                            fullcaption = fullcaption+' '
                        caption6 = me.TextClip(fullcaption, font='Amiri-Bold', fontsize=20, bg_color='black', color='white', method='caption', size=(
                            250, None)).set_duration(timestamp[1]).set_position((1920-0.01*1920-250, 0.5*1080-image6.size[1]/2-40))
                        caption6 = me.TextClip(fullcaption, font='Amiri-Bold', fontsize=20, bg_color='black', color='white', method='caption', size=(
                            250, None)).set_duration(timestamp[1]).set_position((1920-0.01*1920-250, 0.5*1080-image6.size[1]/2-caption6.size[1]))
                    i = i+1

                if images[i] == []:
                    image7 = me.ColorClip(color=[0, 0, 0], size=(
                        1, 1), duration=timestamp[1])
                    caption7 = me.TextClip(" ", fontsize=25, color="white", size=(
                        1, 1), bg_color="transparent").set_duration(timestamp[1])
                    i = i+1
                else:
                    image7 = me.ImageClip("./images/"+images[i][0])
                    if image7.size[1] <= image7.size[0]:
                        image7 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(width=250)
                        image7 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                            width=250).set_position((0.01*1920, 1080-0.09*1080-image7.size[1]))
                    else:
                        image7 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(height=180)
                        image7 = me.ImageClip("./images/"+images[i][0]).set_duration(
                            timestamp[1]).resize(height=180).set_position((0.01*1920+125-image7.size[0]/2, 1080-0.09*1080-180))
                    if captions[i] == []:
                        caption7 = me.TextClip(" ", fontsize=25, color="white", size=(
                            1, 1), bg_color="transparent").set_duration(timestamp[1])
                    else:
                        fullcaption = ""
                        for c in captions[i]:
                            fullcaption = fullcaption+c
                            fullcaption = fullcaption+' '
                        caption7 = me.TextClip(fullcaption, font='Amiri-Bold', bg_color='black', fontsize=20, color='white', method='caption', size=(
                            250, None)).set_duration(timestamp[1]).set_position((0.01*1920, 1080-0.09*1080-image7.size[1]-40))
                        caption7 = me.TextClip(fullcaption, font='Amiri-Bold', bg_color='black', fontsize=20, color='white', method='caption', size=(
                            250, None)).set_duration(timestamp[1]).set_position((0.01*1920, 1080-0.09*1080-image7.size[1]-caption7.size[1]))
                    i = i+1

                if images[i] == []:
                    image8 = me.ColorClip(color=[0, 0, 0], size=(
                        1, 1), duration=timestamp[1])
                    caption8 = me.TextClip(" ", fontsize=25, color="white", size=(
                        1, 1), bg_color="transparent").set_duration(timestamp[1])
                    i = i+1
                else:
                    image8 = me.ImageClip("./images/"+images[i][0])
                    if image8.size[1] <= image8.size[0]:
                        image8 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(width=250)
                        image8 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                            width=250).set_position((0.5*1920-image8.size[0]/2, 1080-0.09*1080-image8.size[1]))
                    else:
                        image8 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(height=180)
                        image8 = me.ImageClip("./images/"+images[i][0]).set_duration(
                            timestamp[1]).resize(height=180).set_position((0.5*1920-image8.size[0]/2, 1080-0.09*1080-180))
                    if captions[i] == []:
                        caption8 = me.TextClip(" ", fontsize=25, color="white", size=(
                            1, 1), bg_color="transparent").set_duration(timestamp[1])
                    else:
                        fullcaption = ""
                        for c in captions[i]:
                            fullcaption = fullcaption+c
                            fullcaption = fullcaption+' '
                        caption8 = me.TextClip(fullcaption, font='Amiri-Bold', bg_color='black', fontsize=20, color='white', method='caption', size=(
                            250, None)).set_duration(timestamp[1]).set_position((0.5*1920-125, 1080-0.09*1080-image8.size[1]-40))
                        caption8 = me.TextClip(fullcaption, font='Amiri-Bold', bg_color='black', fontsize=20, color='white', method='caption', size=(
                            250, None)).set_duration(timestamp[1]).set_position((0.5*1920-125, 1080-0.09*1080-image8.size[1]-caption8.size[1]))
                    i = i+1

                if images[i] == []:
                    image9 = me.ColorClip(color=[0, 0, 0], size=(
                        1, 1), duration=timestamp[1])
                    caption9 = me.TextClip(" ", fontsize=25, color="white", size=(
                        1, 1), bg_color="transparent").set_duration(timestamp[1])
                else:
                    image9 = me.ImageClip("./images/"+images[i][0])
                    if image9.size[1] <= image9.size[0]:
                        image9 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(width=250)
                        image9 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                            width=250).set_position((1920-250-0.01*1920, 1080-0.09*1080-image9.size[1]))
                    else:
                        image9 = me.ImageClip(
                            "./images/"+images[i][0]).set_duration(timestamp[1]).resize(height=180)
                        image9 = me.ImageClip("./images/"+images[i][0]).set_duration(timestamp[1]).resize(
                            height=180).set_position((1920-image9.size[0]/2-0.01*1920-125, 1080-0.09*1080-180))
                    if captions[i] == []:
                        caption9 = me.TextClip(" ", fontsize=25, color="white", size=(
                            1, 1), bg_color="transparent").set_duration(timestamp[1])
                    else:
                        fullcaption = ""
                        for c in captions[i]:
                            fullcaption = fullcaption+c
                            fullcaption = fullcaption+' '
                        caption9 = me.TextClip(fullcaption, font='Amiri-Bold', bg_color='black', fontsize=20, color='white', method='caption', size=(
                            250, None)).set_duration(timestamp[1]).set_position((1920-0.01*1920-250, 1080-0.09*1080-image9.size[1]-40))
                        caption9 = me.TextClip(fullcaption, font='Amiri-Bold', bg_color='black', fontsize=20, color='white', method='caption', size=(
                            250, None)).set_duration(timestamp[1]).set_position((1920-0.01*1920-250, 1080-0.09*1080-image9.size[1]-caption9.size[1]))

                clip = video.subclip(timestamp[2], timestamp[2]+timestamp[1])
                image_clips.append(me.CompositeVideoClip(
                    [clip, image1, image2, image3, image4, image5, image6, image7, image8, image9, caption1, caption2, caption3, caption4, caption5, caption6, caption7, caption8, caption9]))
                i = i+1

        j = 0
        for i in range(len(voidclips)):
            if voidclips[i] == '':
                voidclips[i] = image_clips[j]
                j = j+1

        final = ""
        final = concatenate_videoclips(voidclips)
        final.resize((1280, 720))
        for index, timestamp in enumerate(timestamps):
            final.save_frame("./frames/frame"+str(index)+".png", t=timestamp[2])
        x=""
        while not(x=="N" or x=="Y" or x=="n" or x=="y"):
            x=input("\n\nLook in the frame folder to see if you like the results, if yes type 'Y' and if not update the inputs and then type 'N': ")
        if x=="N" or x=="n":
            
            timestamps=[]
            images=[]
            captions=[]
            voidclips=[]
            image_clips=[]
            with open(pathTimest, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                    timestamps.append(row)

            with open(pathImages, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for row in spamreader:
                    images.append(row)
            for image in images:
                if image!=[]:
                    img = Image.open("./images/"+image[0])

                # Convert the image to RGB format
                    img = img.convert("RGB")
                    img.save("./images/"+image[0])
            with open(pathCaptions, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for row in spamreader:
                    captions.append(row)
            
            for timestamp in timestamps:
                timestamp[0] = timestamp[0].replace("\"", '')
                timestamp[0] = timestamp[0].replace("Untitled - ", '')
                timestamp[0]= timestamp[0].split('.', 1)[0]
                if lines[6]=="Default timestamp duration? yes":
                    if len(timestamp)==2:
                        timestamp[1]=int(lines[7])
                    elif len(timestamp)==1:
                        timestamp.append(int(lines[7]))
                elif lines[6]=="Default timestamp duration? no":
                    timestamp[1] = timestamp[1].replace("\"", '')
                    timestamp[1] = int(timestamp[1])
                else:
                    print("Invalid input, edit config file")
                    exit()
                h, m, s = timestamp[0].split(':')
                timestamp.append(int(h) * 3600 + int(m) * 60 + int(s))

            i = 0
            if timestamps[0][2] != 0:
                voidclips.append(video.subclip(0, timestamps[0][2]))
            voidbegin = []
            for timestamp in timestamps:
                voidbegin.append(timestamp[2]+timestamp[1])
            for index, timestamp in enumerate(timestamps):
                if index == 0:
                    continue
                voidclips.append("")
                voidclips.append(video.subclip(voidbegin[i], timestamp[2]))
                i = i+1
            i = 0
            voidclips.append("")
            if timestamps[len(timestamps)-1][2]+timestamps[len(timestamps)-1][1] < video.duration:
                voidclips.append(video.subclip(timestamps[len(
                    timestamps)-1][2]+timestamps[len(timestamps)-1][1], video.duration))
            print("")

        elif x=="Y" or x=="y":
            break

    final.write_videofile("./output/new_filename.mp4", fps=24)