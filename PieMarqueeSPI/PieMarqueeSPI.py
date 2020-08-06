#!/usr/bin/python

import os
from subprocess import *
from time import *
import xml.etree.ElementTree as ET

INTRO = "/home/pi/PieMarqueeSPI/intro.mp4"
VIEWER = "sudo fbi -T 2 -d /dev/fb0 -noverbose -cachemem 0 /tmp/pause.png /tmp/pause_1.png /tmp/pause_2.png > /dev/null 2>&1 &"

arcade = ['arcade', 'fba', 'mame-advmame', 'mame-libretro', 'mame-mame4all']

def run_cmd(cmd):
# runs whatever in the cmd variable
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

def kill_proc(name):
    ps_grep = run_cmd("ps -aux | grep " + name + "| grep -v 'grep'")
    if len(ps_grep) > 1: 
        os.system("killall " + name)
        
def is_running(pname):
    ps_grep = run_cmd("ps -ef | grep " + pname + " | grep -v grep")
    if len(ps_grep) > 1:
        return True
    else:
        return False

def get_publisher(romname):
    filename = romname+".zip"
    publisher = ""
    for item in root:
        if filename in item.findtext('path'):
            publisher = item.findtext('publisher')
            break
    if publisher == "":
        return ""
    words = publisher.split()
    return words[0].lower()
    
if os.path.isfile(INTRO) == True:
    run_cmd("mplayer -vo fbdev2:/dev/fb1 -zoom -xy 480 -demuxer lavf -framedrop " + INTRO + " </dev/null >/dev/null 2>&1")

doc = ET.parse("/opt/retropie/configs/all/PieMarqueeSPI/gamelist_short.xml")
root = doc.getroot()

if os.path.isfile("/tmp/pause.png") == False :
    os.system("touch /tmp/pause.png")
if os.path.isfile("/tmp/pause_1.png") == False :
    os.system("ln -s /tmp/pause.png /tmp/pause_1.png")
if os.path.isfile("/tmp/pause_2.png") == False :
    os.system("ln -s /tmp/pause.png /tmp/pause_2.png")

os.system("cp /home/pi/PieMarqueeSPI/marquee/maintitle.png /tmp/pause.png")
os.system(VIEWER)
    
cur_imgname = ""
while True:
    sleep_interval = 1
    ingame = ""
    romname = ""
    sysname = ""
    pubpath = ""
    instpath = ""
    ps_grep = run_cmd("ps -aux | grep emulators | grep -v 'grep'")
    if len(ps_grep) > 1:
        ingame="*"
        words = ps_grep.split()
        if 'advmame' in ps_grep:
            sysname = "mame-advmame"
            romname = words[-1]
        else:
            pid = words[1]
            if os.path.isfile("/proc/"+pid+"/cmdline") == False:
                continue
            path = run_cmd("strings -n 1 /proc/"+pid+"/cmdline | grep roms")
            if len(path.replace('"','').split("/")) < 2:
                continue
            sysname = path.replace('"','').split("/")[-2]
            if sysname in arcade:
                romname = "arcade/"+path.replace('"','').split("/")[-1].split(".")[0]
            else:
                romname = sysname+'/'+path.replace('"','').split("/")[-1].split(".")[0]

    elif os.path.isfile("/tmp/PieMarquee.log") == True:
        f = open('/tmp/PieMarquee.log', 'r')
        line = f.readline()
        f.close()
        words = line.split()
        if len(words) > 1 and words[0] == "Game:": # In the gamelist-> Game: /home/pi/.../*.zip
            path = line.replace('Game: ','')
            sysname = path.replace('"','').split("/")[-2]
            if sysname in arcade:
                romname = "arcade/"+path.replace('"','').split("/")[-1].split(".")[0]
            else:
                romname = sysname+'/'+path.replace('"','').split("/")[-1].split(".")[0]
            sleep_interval = 0.1 # for quick view
        elif len(words) == 1:
            if words[0] == "SystemView":
                romname = "maintitle"
            else:
                romname = words[0]

    else:
        romname = "maintitle"
   
    if os.path.isfile("/home/pi/PieMarqueeSPI/marquee/" + romname + ".png") == True:
        imgname = romname
        if ingame == "*":
            publisher = get_publisher(romname)
            if os.path.isfile("/home/pi/PieMarqueeSPI/marquee/publisher/" + publisher + ".png") == True:
                pubpath = "/home/pi/PieMarqueeSPI/marquee/publisher/" + publisher + ".png"
            if os.path.isfile("/home/pi/PieMarqueeSPI/marquee/instruction/" + romname + ".png") == True:
                instpath = "/home/pi/PieMarqueeSPI/marquee/instruction/" + romname + ".png"
    elif os.path.isfile("/home/pi/PieMarqueeSPI/marquee/" + sysname + ".png") == True:
        imgname = sysname
    else:
        imgname = "maintitle"
        
    if imgname+ingame != cur_imgname: # change marquee images
        kill_proc("mplayer")
        if imgname == "maintitle" and os.path.isfile("/home/pi/PieMarqueeSPI/marquee/maintitle.mp4") == True:
            os.system("mplayer -vo fbdev2:/dev/fb1 -zoom -xy 480 -demuxer lavf -framedrop /home/pi/PieMarqueeSPI/marquee/maintitle.mp4 </dev/null >/dev/null 2>&1 &")            
        else:
            imgpath = "/home/pi/PieMarqueeSPI/marquee/" + imgname + ".png"
            os.system('cp' + imgpath + '" /tmp/pause.png')
            sleep(0.2) 
            '''
            if is_running("omxiv-marquee") == False: # if omxiv failed, execute again
                os.system("clear > /dev/tty1")
                os.system('echo "' + imgpath + '" > /tmp/marquee.txt')
                os.system(VIEWER)
            cur_imgname = imgname+ingame
            '''
            continue

    sleep(sleep_interval)