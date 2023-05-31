import moviepy.editor as me
from moviepy.video.compositing.concatenate import concatenate_videoclips
import csv
import numpy as np

images=[]
captions=[]
timestamps=[]
positionstexts=[]
image_clips=[]
voidclips=[]
positionsimages=[(0.1, 0.9),(0.5, 0.9),(0.9, 0.9),
                 (0.1, 0.5),(0.5, 0.5),(0.9, 0.5),
                 (0.1, 0.1),(0.5, 0.1),(0.9, 0.1)]
positionsimagesstandard=[(0.5, 0.5),(0.1, 0.9),(0.9, 0.9),(0.1, 0.1),(0.9, 0.1)]
while True:
    try:
        x="./video/"+input("Enter name of the video file you wanna edit:")
        videopath=x
        video=me.VideoFileClip(videopath)
        break
    except OSError:
        print("File not found")
video=video.resize((1920,1080))
while True:
    try:
        x="./spreadsheets/"+input("Enter the name of the timestamp spreadsheet file you wanna use:")
        with open(x, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                timestamps.append(row)
        break
    except OSError:
        print("File not found")
for timestamp in timestamps:
    timestamp[0]=timestamp[0].replace("\"",'')
    timestamp[1]=timestamp[1].replace("\"",'')
    timestamp[1]=int(timestamp[1])
    h, m, s = timestamp[0].split(':')
    timestamp.append(int(h) * 3600 + int(m) * 60 + int(s))


while True:
    try:
        x="./spreadsheets/"+input("Enter the name of the images spreadsheet file you wanna use:")  
        with open(x, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                images.append(row)  
        break
    except OSError:
        print("File not found")    
while True:
    try:
        x="./spreadsheets/"+input("Enter the name of the captions spreadsheet file you wanna use:")  
        with open(x, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                captions.append(row) 
        break
    except OSError:
        print("File not found")   
i=0
if timestamps[0][2]!=0:
    voidclips.append(video.subclip(0,timestamps[0][2]))
voidbegin=[]
for timestamp in timestamps:
    voidbegin.append(timestamp[2]+timestamp[1])
print(voidbegin)
for index,timestamp in enumerate(timestamps):
    if index==0:
        continue
    voidclips.append("")
    voidclips.append(video.subclip(voidbegin[i],timestamp[2]))
    i=i+1
i=0
print(voidclips)
for timestamp in timestamps:
    standardornot=input("Type 'Standard' for standard positioning or 'Advanced' for non-standard positioning in time-stamp "+timestamp[0]+":")
    if standardornot=="Standard":
        while True:
            x=int(input("How many images/texts do you want to insert?"))
            if x>5:
                print("Can't insert more than 5 images in Standard positioning. Insert number again")
                continue
            if x==1:
                image=me.ImageClip("./images/"+images[i][0])
                clip=video.subclip(timestamp[2],timestamp[2]+timestamp[1])
                image_clips.append(me.CompositeVideoClip([clip,image]).set_position(positionsimagesstandard[0]))
                i=i+1
            elif x==2:
                clip1=me.ImageClip(images[i]).set_duration(timestamp[1]).set_position(positionsimagesstandard[0])
                i=i+1
                clip2=me.ImageClip(images[i]).set_duration(timestamp[1]).set_position(positionsimagesstandard[1])
                clips=concatenate_videoclips(clip1, clip2)
                image_clips.append(clips)
                i=i+1
            elif x==3:
                clip1=me.ImageClip(images[i]).set_duration(timestamp[1]).set_position(positionsimagesstandard[0])
                i=i+1
                clip2=me.ImageClip(images[i]).set_duration(timestamp[1]).set_position(positionsimagesstandard[1])
                i=i+1
                clip3=me.ImageClip(images[i]).set_duration(timestamp[1]).set_position(positionsimagesstandard[2])
                clips=concatenate_videoclips(clip1, clip2,clip3)
                image_clips.append(clips)
                i=i+1
            elif x==4:
                clip1=me.ImageClip(images[i]).set_duration(timestamp[1]).set_position(positionsimagesstandard[0])
                i=i+1
                clip2=me.ImageClip(images[i]).set_duration(timestamp[1]).set_position(positionsimagesstandard[1])
                i=i+1
                clip3=me.ImageClip(images[i]).set_duration(timestamp[1]).set_position(positionsimagesstandard[2])
                i=i+1
                clip4=me.ImageClip(images[i]).set_duration(timestamp[1]).set_position(positionsimagesstandard[3])
                clips=concatenate_videoclips(clip1, clip2,clip3,clip4)
                image_clips.append(clips)
                i=i+1
            elif x==5:
                clip1=me.ImageClip(images[i]).set_duration(timestamp[1]).set_position(positionsimagesstandard[0])
                i=i+1
                clip2=me.ImageClip(images[i]).set_duration(timestamp[1]).set_position(positionsimagesstandard[1])
                i=i+1
                clip3=me.ImageClip(images[i]).set_duration(timestamp[1]).set_position(positionsimagesstandard[2])
                i=i+1
                clip4=me.ImageClip(images[i]).set_duration(timestamp[1]).set_position(positionsimagesstandard[3])
                i=i+1
                clip5=me.ImageClip(images[i]).set_duration(timestamp[1]).set_position(positionsimagesstandard[4])
                clips=concatenate_videoclips(clip1, clip2,clip3,clip4)
                image_clips.append(clips)
                i=i+1
            else:
                print("This input is not recognizable. Enter your input again")
            break
j=0
for i in range(len(voidclips)):
    if voidclips[i]=='':
        voidclips[i]=image_clips[j]
        j=j+1

for void in voidclips:
    print(void)
final=concatenate_videoclips(voidclips)
final.write_videofile("./output/new_filename.mp4",fps=24)







