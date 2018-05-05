#!/usr/bin/python3
#YOUTUBE API:
import os
import datetime
from array import array
import serial
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import vlc
import sys
import pulsectl
pulse = pulsectl.Pulse('my-client-name')
import gi
import bluetooth
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('GdkX11', '3.0')
from gi.repository import GdkX11
import ctypes
import gobject
import dbus
from gi.repository import GLib
import threading
import time
import urllib
from urllib.request import urlopen
from gi.repository.GdkPixbuf import Pixbuf
from gi.repository import GdkPixbuf
import PIL.Image
import requests
from io import BytesIO
from io import StringIO
from oauth2client.contrib.flask_util import UserOAuth2
import json
import logging
import subprocess
import base64
from gi.repository import GObject
import dbus.mainloop.glib
import NetworkManager

oauth2 = UserOAuth2()

class MyException(Exception): pass
#-------DEFINE GLOBAL VARIABLES------#
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
global timer
timer = 0
global current
current = 0
global d
d = 0
global pg
pg = 1
global yttype
yttype = 0
global rec
rec = 0
b = 1
npage = []
filename = 'data.txt'
#-------END DEFINE GLOBAL VARIABLES------#
#------DEFINE GLOBAL INFO REQUIRING PRIOR VARIABLES------#
with open(filename) as f:
    data = f.readlines()
f = open(filename)
data = f.readlines()
try:
    ser = serial.Serial('/dev/ttyACM0')

    print("done!")
    ard = 1
except serial.SerialException:
    ard = 0
    print("Arduino integration failed!")
    pass
#------END DEFINE GLOBAL INFO REQUIRING PRIOR VARIABLES------#
class resultsWindow(Gtk.Window):
    def __init__(self):
        #-------DEFINE INITIALIZE GTK WINDOW------#
        Gtk.Window.__init__(self, title="Home")
        self.connect("destroy",self.Destroy)
    def pickval(self, inp, data):
        #-------DEFINE YOUTUBE SEARCH TYPE-------#
        global yttype
        inputs = data
        #-------DEFINE WHAT SEARCH TYPE IS ON SEARCH-------#
        if data == "vid":
            yttype = 1
            self.select2.set_label("Videos")
            self.select3.set_label("Playlists")
            self.select4.set_label("Both")
        elif data == "pl":
            yttype = 2
            self.select2.set_label("Playlists")
            self.select3.set_label("Videos")
            self.select4.set_label("Both")
        elif data == "both":
            yttype = 3
            self.select2.set_label("Both")
            self.select3.set_label("Videos")
            self.select4.set_label("Playlists")
        #-------END DEFINE WHAT SEARCH TYPE IS ON SEARCH-------#
    def show(self):
        #-------DEFINE GLOBAL SHOW COMMAND-------#
        self.show_all()
    def play(self, id, name, data):
        #--------DEFINE START YOUTUBE PLAYBACK-------#
        global nptitle
        nptitle = name
        m = 1
        link = str(data)
        link = link.replace("[","")
        link = link.replace("]","")
        link = link.replace("''","")
        while m == 1:
                global MRL
                MRL = "https://www.youtube.com/embed/%s" % data
                #import soundcloud
                #client = soundcloud.Client(client_id='YOUR_CLIENT_ID')
                #track = client.get('/pulse8/best-of-chillstep-september-2015')
                #MRL = client.get(track.stream_url, allow_redirects=False)
                #MRL = "https://soundcloud.com/pulse8/best-of-chillstep-september-2015"
                print(MRL)
                if __name__ == '__main__':
                    self.vbox.destroy()
                    self.setup_objects_and_eventsp()
                    self.show()
                    self.main()
                    Gtk.main()
                    window.player.stop()
                    window.vlcInstance.release()
    def search(self, inputs):
        #-------DEFINE SETUP FOR PRINT SEARCH RESULTS IN YOUTUBE-------#
        data = self.message.get_text()
        global text
        text = str(data)
        global npage
        npage = []
        #with open("data.txt", "r") as fo:
        #    txt = fo.readlines()

        # modify
        #    path_i = None
        #    for i, line in enumerate(txt):
        #        if "VOL " in line:
        #            global wait
        #            wait = fo.readline()
        #            print(wait)
        #        if "PPOS " in line:
        #            global path_i
        #            path_i = i
        #            fo.seek(path_i, 0)
        #            line = fo.readline()
        #            print(line)
        #            line = line[line.find("PPOS ") + len("PPOS "):]
        #            print(line)
        #            global pos
        #            pos = int(line)
        #            print(pos)
        #            global txt2
        #            txt2 = fo.readlines()
        #            break
        #with open('data.txt', 'w') as fo:
        #    global path_i
        #    global txt2
        #    global wait
        #    global pos
        #    fo.seek(path_i, 0)
        #    fo.writelines("PPOS %s" % str(pos+1))
        #    for i, line in enumerate(txt2):
        #        if "S%s" % pos in line:
        #            path = i
        #            print(i)
        #            fo.seek(path, 0)
        #            fo.writelines("S%s" % pos + " %s" %text)
        #            break
        global rec
        global yttype
        if yttype == 0:
            yttype = 1
        rec = 1
        self.vbox.destroy()
        self.setup_objects_and_events()
        self.show()
        Gtk.main()

    def setup_objects_and_events(self):
        #------DEFINE DISPLAY YOUTUBE RESULTS------#
        global text
        global rec
        global npage
        global pg
        #------DEFINE WINDOW TITLE BASED OFF SEARCH TYPE------#
        if rec == 1:
            self.set_title("Search: " + text + ", Page " + str(pg))
        elif rec == 0 and pg != 1:
            self.set_title("Recommended Videos, Page " + str(pg))
        elif rec == 0 and pg == 1:
            self.set_title("Recommended Videos")
        #------END DEFINE WINDOW TITLE BASED OFF SEARCH TYPE------#
        #------DEFINE YOUTUBE API ACCESS (CURRENTLY DEVKEY)------#
        #http = httplib2.Http()
        #credentials.authorize(http)
        #resp, content = http.request(
        #    'https://www.googleapis.com/youtube/v3/')
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey='xxxxx')
        #-------END DEFINE YOUTUBE API ACCESS (CURRENTLY DEVKEY)-------#
        #-------DEFINE REQUIRED VARIABLES------#
        global H
        H = 600
        global W
        W = 900
        global y
        y = 30
        global f
        f = 30
        global x
        x = 0
        i = 0
        videos = []
        link = []
        rect = []
        bottom = []
        recfl = []
        botfl = []
        title = []
        images = []
        global ntoken
        global ptoken
        ptoken = []
        ntoken = []
        author = []
        screen = self.get_screen()
        global WI
        global SH
        WI = screen.get_width()
        SH = screen.get_height()
        L = 52
        orig = round(WI/350)
        ll = round(SH/300)
        mx = round(orig*ll)
        global r
        r = H/2
        #-------END DEFINE REQUIRED VARIABLES------#
        #-------DEFINE SEARCH ARGUMENTS BASED OFF SEARCH TYPE------#
        global yttype
        global tk
        if yttype == 0 and npage == []:
            search_response = youtube.search().list(
            q="",
            part="id,snippet",
            type="video",
            maxResults=mx
            ).execute()
        elif yttype == 1 and npage == []:
            search_response = youtube.search().list(
            q=text,
            part="id,snippet",
            type="video",
            maxResults=mx
            ).execute()
        elif yttype == 2 and npage == []:
            search_response = youtube.search().list(
            q=text,
            part="id,snippet",
            type="playlist",
            maxResults=mx
            ).execute()
        elif yttype == 3 and npage == []:
            search_response = youtube.search().list(
            q=text,
            part="id,snippet",
            type="playlist,video",
            maxResults=mx
            ).execute()
        elif npage != [] and yttype > 0:
            search_response = youtube.search().list(
            q=text,
            part="id,snippet",
            type="video",
            maxResults=mx,
            pageToken=tk
            ).execute()
        elif npage != [] and yttype == 0:
            search_response = youtube.search().list(
            q="",
            part="id,snippet",
            type="video",
            maxResults=mx,
            pageToken=tk
            ).execute()
        #-------END DEFINE SEARCH ARGUMENTS BASED OFF SEARCH TYPE------#
        #-----DEFINE PARSE SEARCH RESULTS FROM PRIOR SECTION------#
        for search_result in search_response.get("nextPageToken"):
            ntoken = search_response.get("nextPageToken")
        try:
            for search_result in search_response.get("prevPageToken"):
                ptoken = search_response.get("prevPageToken")
        except:
            print("On first page, ignoring prev page!")
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                videos.append("%s" % (search_result["snippet"]["title"]))
                link.append("%s" % (search_result["id"]["videoId"]))
                images.append("%s" % (search_result["snippet"]["thumbnails"]["medium"]["url"]))
                author.append("%s" % (search_result["snippet"]["channelTitle"]))
                i = i + 1
            if search_result["id"]["kind"] == "youtube#playlist":
                videos.append("%s" % (search_result["snippet"]["title"]))
                link.append("%s" % (search_result["id"]["playlistId"]))
                images.append("%s" % (search_result["snippet"]["thumbnails"]["medium"]["url"]))
                author.append("%s" % (search_result["snippet"]["channelTitle"]))
                i = i + 1
        #-----END DEFINE PARSE SEARCH RESULTS FROM PRIOR SECTION------#
        #-----DEFINE BASE ELEMENTS FOR YOUTUBE SEARCH PRINT-----#
        h = 0
        f = 0
        self.draw_area = Gtk.DrawingArea()
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.back = Gtk.Button("Return to main menu")
        self.back.connect("clicked", self.backtomain)
        self.message = Gtk.Entry()
        self.srch = Gtk.Button("Search")
        self.srch.connect("clicked", self.search)
        self.mb = Gtk.MenuBar()
        self.select = Gtk.Menu()
        self.select2 = Gtk.MenuItem("Videos")
        self.select2.connect("activate", self.pickval, "vid")
        self.select3 = Gtk.MenuItem("Playlists")
        self.select3.connect("activate", self.pickval, "pl")
        self.select4 = Gtk.MenuItem("Both")
        self.select4.connect("activate", self.pickval, "both")
        self.select2.set_submenu(self.select)
        self.pg = Gtk.Label("Page %s" % pg + " ")
        if yttype > 0:
            self.serch = Gtk.Label("Search: %s" % text)
        elif yttype == 0:
            self.serch = Gtk.Label("Recommended Videos")
        self.select.append(self.select3)
        self.select.append(self.select4)
        self.mb.append(self.select2)
        self.pbox = Gtk.Box.new(0,2)
        self.pbox.pack_start(self.back, False, False, 2)
        self.pbox.pack_start(self.message, False, False, 2)
        self.pbox.pack_start(self.srch, False, False, 2)
        self.pbox.pack_start(self.mb, False, False, 2)
        self.pbox.pack_start(self.serch, True, True, 2)
        self.pbox.pack_start(self.pg, False, False, 5)
        self.vbox.pack_start(self.pbox, False, False, 2)
        self.add(self.vbox)
        self.hbox = Gtk.Box.new(0,0)
        self.kbox = Gtk.Box.new(0,0)
        #-----END DEFINE BASE ELEMENTS FOR YOUTUBE SEARCH PRINT-----#
        #-----DEFINE YOUTUBE SEARCH RESULT PRINT-----#
        for l in range (0, int(mx)):
            if f >= int(orig):
                self.vbox.pack_start(self.kbox, False, False, 0)
                self.vbox.pack_start(self.hbox, False, False, 0)
                self.hbox = Gtk.Box.new(0,0)
                self.kbox = Gtk.Box.new(0,0)
                f = 0
            nm = "/tmp/" + str(h) + ".jpg"

            uename = str(videos[h] + ", By " + author[h])
            name = '\n'.join(uename[i:i+L] for i in range(0, len(uename), L))
            k = L - len(uename)
            #if L > len(uename):
            #    name = '{:53}'.format(name)
            self.playback_button = Gtk.Button(name)
            self.playback_button.set_size_request(320, 10)
            self.playback_button.connect("clicked", self.play, videos[h], link[h])
            urllib.request.urlretrieve(images[h], nm)
            self.image1 = Gtk.Image()
            pb = Pixbuf.new_from_file(nm)
            self.image1.set_from_pixbuf(pb)
            self.playback_button.set_relief(2)
            self.playback_button.set_always_show_image(True)
            self.playback_button.set_image(self.image1)
            self.playback_button.set_image_position(2)
            #self.image1.connect("button-press-event", self.play, videos[h], link[h])
            #self.kbox.pack_start(self.image1, True, True, 5)
            self.hbox.pack_start(self.playback_button, True, True, 0)
            h = h + 1
            f = f + 1
        self.vbox.pack_start(self.kbox, False, False, 0)
        self.vbox.pack_start(self.hbox, False, False, 0)
        #-----END DEFINE YOUTUBE SEARCH RESULT PRINT-----#
        #-----DEFINE BOTTOM BUTTON BASE ELEMENTS FOR YOUTUBE SEARCH PRINT-----#
        self.lbox = Gtk.Box.new(0,0)
        self.forwardbutton = Gtk.Button("Next Videos")
        self.forwardbutton.connect("clicked", self.next, "next")
        self.backwardbutton = Gtk.Button("Previous videos")
        if pg > 1:
            self.backwardbutton.connect("clicked", self.next, "prev")
        self.lbox.pack_start(self.backwardbutton, True, True, 0)
        self.lbox.pack_start(self.forwardbutton, True, True, 0)
        self.vbox.pack_start(self.lbox, False, False, 0)
        #-----END DEFINE BOTTOM BUTTON BASE ELEMENTS FOR YOUTUBE SEARCH PRINT-----#
    def next(self, data, stat):
        #--------DEFINE YOUTUBE NEXT PAGE-------#
        print(data)
        print(stat)
        global npage
        global ntoken
        global ptoken
        global tk
        global pg
        if stat == "next":
            npage = "1"
            pg = pg + 1
            tk = ntoken
            self.vbox.destroy()
            self.setup_objects_and_events()
            self.show()
            Gtk.main()
        elif stat == "prev":
            npage = "2"
            pg = pg - 1
            tk = ptoken
            self.vbox.destroy()
            self.setup_objects_and_events()
            self.show()
            Gtk.main()
    def show(self):
        #-------DEFINE GLOBAL SHOW COMMAND-------#
        self.show_all()
    def setup_objects_and_eventsp(self):
        #-------DEFINE SETUP MEDIA PLAYER OBJECTS PRINT-------#
        global nptitle
        self.set_title("Now playing:" + nptitle)
        global RN
        RN = 1
        self.player_paused=False
        self.is_player_active = False
        self.playback_button = Gtk.Button()
        self.stop_button = Gtk.Button()
        self.play_image = Gtk.Image.new_from_icon_name(
                "gtk-media-play",
                Gtk.IconSize.MENU
            )
        self.pause_image = Gtk.Image.new_from_icon_name(
                "gtk-media-pause",
                Gtk.IconSize.MENU
            )
        self.stop_image = Gtk.Image.new_from_icon_name(
                "gtk-media-stop",
                Gtk.IconSize.MENU
            )
        self.playback_button.set_image(self.play_image)
        self.stop_button.set_image(self.stop_image)
        self.playback_button.connect("clicked", self.toggle_player_playback)
        self.stop_button.connect("clicked", self.stop_player)
        self.playback_button.set_relief(2)
        self.stop_button.set_relief(2)
        self.draw_area = Gtk.DrawingArea()
        self.draw_area.set_size_request(800,600)
        self.vol = Gtk.Label()
        self.draw_area.connect("realize",self._realized2)
        self.scale = Gtk.Scale()
        self.scale.set_draw_value(False)
        self.scale.set_range(0, 100)
        self.scale.set_size_request(320, 10)
        self.scale.set_value(100)
        self.scale.connect("value-changed", self.vol_slider)
        self.now = Gtk.Scale()
        self.now.set_range(0, 100)
        self.now.set_size_request(320, 10)
        self.now.set_value(0)
        self.now.connect("value-changed", self.current_time)
        self.time = Gtk.Label()
        self.now.set_draw_value(False)
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox.pack_start(self.draw_area, True, True, 0)
        self.hbox = Gtk.Box(spacing=0)
        self.hbox.pack_start(self.playback_button, False, False, 0)
        self.hbox.pack_start(self.stop_button, False, False, 0)
        self.hbox.pack_start(self.vol, False, False, 3)
        self.hbox.pack_start(self.scale, False, False, 0)
        self.hbox.pack_start(self.time, False, False, 3)
        self.hbox.pack_start(self.now, True, True, 0)
        self.vbox.pack_start(self.hbox, False, False, 0)
        self.add(self.vbox)
        #self.vbox.connect("motion_notify_event", self.bar)
        self.show_all()
        global fullscreen
        fullscreen = 0
    def stop_player(self, widget, data=None):
        #------DEFINE DESTROY MEDIA PLAYER AND RETURN TO YOUTUBE-------#
        savevol = self.player.audio_get_volume()
        savevol = "VOL " + str(savevol)
        self.player.stop()
        self.is_player_active = False
        self.playback_button.set_image(self.play_image)
        MRL = []
        global RN
        RN = 0
        fo = open("data.txt", "w")
        fo.seek(0, 0)
        write = fo.writelines( str(savevol) )
        fo.close()
        self.vbox.destroy()
        global text
        self.setup_objects_and_events()
        self.show()
        Gtk.main()
    def toggle_player_playback(self, widget, data=None):
        #-------DEFINE CHECK IF MEDIA PLAYER PLAY/PAUSE BUTTON PRESS------#
        #-------DEFINE IF MEDIA PLAYER NOT PAUSED AND NOT ACTIVE-----#
        if self.is_player_active == False and self.player_paused == False:
            self.player.play()
            self.playback_button.set_image(self.pause_image)
            self.is_player_active = True
        #-------END DEFINE IF MEDIA PLAYER NOT PAUSED AND NOT ACTIVE-----#
        #-------DEFINE IF MEDIA PLAYER PAUSED AND ACTIVE-----#
        elif self.is_player_active == True and self.player_paused == True:
            self.player.play()
            self.playback_button.set_image(self.pause_image)
            self.player_paused = False
        #-------END DEFINE IF MEDIA PLAYER PAUSED AND ACTIVE-----#
        #-------DEFINE IF MEDIA PLAYER NOT PAUSED AND ACTIVE-----#
        elif self.is_player_active == True and self.player_paused == False:
            self.player.pause()
            self.playback_button.set_image(self.play_image)
            self.player_paused = True
        #-------END DEFINE IF MEDIA PLAYER NOT PAUSED AND ACTIVE-----#
        #-------DEFINE EXCEPTION-------#
        else:
            pass
    def _realized2(self, widget, data=None):
        #-------DEFINE MEDIA PLAYER CONFIG AND PRINT------#
        #-----DEFINE SETTINGS FOR MEDIA PLAYER-----#
        x11 = ctypes.cdll.LoadLibrary('libX11.so.6')
        x11.XInitThreads()
        self.vlcInstance = vlc.Instance()
        self.player = self.vlcInstance.media_player_new()
        win_id = widget.get_window().get_xid()
        media = self.vlcInstance.media_new(MRL)
        media_list = self.vlcInstance.media_list_new([MRL])
        self.player.set_media(media)
        self.list_player =  self.vlcInstance.media_list_player_new()
        self.list_player.set_media_player(self.player)
        self.list_player.set_media_list(media_list)
        self.player.set_xwindow(win_id)
        self.player.play()
        self.playback_button.set_image(self.pause_image)
        self.is_player_active = True
        #-----END DEFINE SETTINGS FOR MEDIA PLAYER-----#
        #-----DEFINE VOLUME OF MEDIA PLAYER FROM CONFIG-----#
        self.now_time()
        fo = open("data.txt", "r")
        fo.seek(0, 0)
        for index in range(1):
            line = fo.readline()
            line = line[line.find("VOL ") + len("VOL "):]
        self.scale.set_value(int(line))
        time.sleep(0.2)
        self.vol.set_text(str(line))
        self.player.audio_set_volume(int(line))
        fo.close()
        #-----END DEFINE VOLUME OF MEDIA PLAYER FROM CONFIG-----#
    def vol_slider(self, w):
        #-------DEFINE CHANGE VOLUME OF MEDIA PLAYER FROM SLIDER------#
        l = int(w.get_value())
        self.vol.set_text(str(l))
        self.player.audio_set_volume(l)
    def current_time(self, w):
        #--------DEFINE CHANGE TIME OF PLAYBACK ON MEDIA PLAYER-------#
        l = int(w.get_value())
        c = round(l)
        global d
        if (d == 0):
            self.player.set_time(c)
        else:
            d = 0
    def now_time(self):
        #--------DEFINE MEDIA PLAYER CURRENT AND TOTAL TIME-------#
        #--------DEFINE VARIABLES NEEDED--------#
        global timer
        global old
        global oldc
        global current
        old = timer
        oldc = current
        #--------END DEFINE VARIABLES NEEDED--------#
        #--------DEFINE TOTAL TIME-------#
        timer = round(self.player.get_length()/1000)
        if timer != old:
            self.now.set_range(0, timer)
        #--------END DEFINE TOTAL TIME-------#
        #--------DEFINE CURRENT TIME-------#
        current = round(self.player.get_time()/1000)
        if current != oldc:
            nw = round(self.player.get_time()/1000)
            times = str(datetime.timedelta(seconds=current))
            times = " " + times
            total = str(datetime.timedelta(seconds=timer))
            total = " " + total
        #--------END DEFINE CURRENT TIME-------#
        #--------DEFINE POSITION FOR TIME SLIDER-------#
            if " 0:" in times:
                times = times[times.find("0:") + len("0:"):]
            if " 0:" in total:
                total = total[total.find("0:") + len("0:"):]
            self.time.set_text("%s /" % times + "%s" % total )
            self.now.set_value(nw)
            nw = []
            global d
            d = 1
            time.sleep(0.2)
        #--------END DEFINE POSITION FOR TIME SLIDER-------#
    def main(self):
        #---------DEFINE MEDIA PLAYER MAIN LOOP--------#
        global RN
        while RN == 1:
        #your code
            self.now_time()
            self.arducheck()
            while Gtk.events_pending():
                Gtk.main_iteration()
    def bar(self,widget,events):
        #--------DEFINE HIDE BOTTOM BAR (NOT ACTIVE)--------#
        self.show_all()
        self.hbox.show()
        print("Up")
        time.sleep(2)
        #self.hbox.hide()
        print("Down")
        events = []
    def Destroy(self, obj):
        #---------DEFINE KILL APP-------#
        global RN
        try:
            GObject.MainLoop().quit()
        except:
            pass
        RN = 0
        sys.exit()
    def arducheck(self):
        #--------DEFINE CHECK FOR ARDUINO INPUT IF CONNECTED--------#
        global ard
        if ard == 1:
            #-----DEFINE VOLUME FROM ARDUINO-----#
            sr = ser.read(100)
            if "VOL " in sr and ard == 1:
                sre = sr[text.find("VOL "): + len("VOL ")]
                srst = int(sre)
                #print(srst)
                self.player.audio_set_volume(srst)
            #-----END DEFINE VOLUME FROM ARDUINO-----#
            #-----DEFINE VOLUME TO ARDUINO-----#
            elif sr == "GET VL" and ard == 1:
                prn = self.player.audio_get_volume()
                ser.write("IS " + prn)
            #-----END DEFINE VOLUME TO ARDUINO-----#
            #-----DEFINE TITLE TO ARDUINO-----#
            elif sr == "GET TL" and ard == 1:
                global nptitle
                ser.write("IS " + nptitle)
            #-----END DEFINE TITLE TO ARDUINO-----#
    def setup_main(self):
        #----------DEFINE SETUP FOR MAIN MENU PRINT--------#
        #----------DEFINE MAIN MENU ITEMS--------#
        global names
        names = ["Youtube", "Bluetooth", "Folders", "Discord", "Settings", "Quit"]
        tt = 6
        files = ["bin/ytlogo.png", "bin/btlogo.png", "bin/fold.png", "bin/disc.png", "bin/settings.png", "bin/exit.png"]
        #----------END DEFINE MAIN MENU ITEMS---------#
        #----------DEFINE SCREEN INFO---------#
        screen = self.get_screen()
        WI = screen.get_width()
        SH = screen.get_height()
        L = 52
        orig = round(WI/370)
        ll = round(SH/300)
        #----------END DEFINE SCREEN INFO---------#
        #----------DEFINE PRINT MAIN MENU ITEMS--------#
        self.hbox = Gtk.Box(spacing=0)
        self.lbox = Gtk.Box(spacing=0)
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        m = 0

        for k in range (0, tt):
            if m == orig:
                self.vbox.pack_start(self.lbox, False, False, 0)
                self.vbox.pack_start(self.hbox, False, False, 0)
                self.hbox = Gtk.Box(spacing=0)
                self.lbox = Gtk.Box(spacing=0)
            if m == (orig)*2:
                self.vbox.pack_start(self.lbox, False, False, 0)
                self.vbox.pack_start(self.hbox, False, False, 0)
                self.hbox = Gtk.Box(spacing=0)
                self.lbox = Gtk.Box(spacing=0)
            self.appbut = Gtk.Button(names[m])
            self.appbut.set_size_request(320, 10)
            pbm = Pixbuf.new_from_file(files[m])
            self.image = Gtk.Image()
            self.image.set_from_pixbuf(pbm)
            self.appbut.set_always_show_image(True)
            self.appbut.set_image(self.image)
            self.appbut.set_image_position(2)
            self.appbut.connect("clicked", self.pick, m+1)
            self.appbut.set_relief(2)
            self.hbox.pack_start(self.appbut, True, True, 0)
            if m == tt-1:
                self.vbox.pack_start(self.lbox, False, False, 0)
                self.vbox.pack_start(self.hbox, False, False, 0)
            m = m + 1
            #----------DEFINE LINE 1 ROLLOVER--------#
            if tt < orig and m == tt:
                #print(orig*2)
                #print(tt)
                #print(int(orig+(tt-m)))
                #print(int(m))
                #----------DEFINE LINE 1 ROLLOVER AMOUNT--------#
                for k in range (int(m), int(orig)):
                    self.appbut = Gtk.Button("")
                    self.appbut.set_size_request(320, 10)
                    pbm = Pixbuf.new_from_file("bin/ph.png")
                    self.image = Gtk.Image()
                    self.image.set_from_pixbuf(pbm)
                    self.appbut.set_always_show_image(True)
                    self.appbut.set_image(self.image)
                    self.appbut.set_image_position(2)
                    self.appbut.set_relief(2)
                    self.hbox.pack_start(self.appbut, True, True, 0)
                #----------END DEFINE LINE 1 ROLLOVER AMOUNT--------#
        #----------END DEFINE LINE 1 ROLLOVER--------#
        #----------DEFINE LINE 2 ROLLOVER--------#
            elif tt < orig*2 and m == tt:
                #print(orig*2)
                #print(tt)
                #print(int((orig+(orig))))
                #print(int(m))
                #----------DEFINE LINE 2 ROLLOVER AMOUNT--------#
                for k in range (int(m), int((orig+(orig)))):
                    self.appbut = Gtk.Button("")
                    self.appbut.set_size_request(320, 10)
                    pbm = Pixbuf.new_from_file("bin/ph.png")
                    self.image = Gtk.Image()
                    self.image.set_from_pixbuf(pbm)
                    self.appbut.set_always_show_image(True)
                    self.appbut.set_image(self.image)
                    self.appbut.set_image_position(2)
                    self.appbut.set_relief(2)
                    self.hbox.pack_start(self.appbut, True, True, 0)
                #----------END DEFINE LINE 2 ROLLOVER AMOUNT--------#
        #----------END DEFINE LINE 2 ROLLOVER--------#
        self.draw_area = Gtk.DrawingArea()
        self.draw_area.set_size_request(400,200)
        self.vbox.pack_start(self.draw_area, True, True, 0)
        self.add(self.vbox)
        #----------END DEFINE PRINT MAIN MENU ITEMS--------#
    def pick(self, data, var):
        #-------DEFINE PICK BUTTON PRESSED FROM MAIN-------#
        global names
        if var == 1:
            self.op_yt("ok")
        elif var == 2:
            self.set_title(names[var-1])
            self.op_bt("yes")
        elif var == 3:
            print("Not integrated!")
        elif var == 4:
            print("Not integrated! Also the fact that im doing this is really stupid!")
            self.discconnect()
        elif var == 5:
            self.set_title(names[var-1])
            self.op_st("ok")
        elif var == 6:
            self.Destroy("kill")
    def op_yt(self, data):
        #-------DEFINE SWITCH TO YOUTUBE FROM MAIN-------#
        self.vbox.destroy()
        self.setup_objects_and_events()
        self.show()
        Gtk.main()
    def op_bt(self, data):
        #--------DEFINE SWITCH TO BLUETOOTH CONFIG FROM MAIN--------#
        self.vbox.destroy()
        self.setup_bt()
        self.show()
        Gtk.main()
    def setup_bt(self):
        #---------DEFINE DISPLAY BLUETOOTH CONFIG PRINT-------#
        self.draw_area = Gtk.DrawingArea()
        self.draw_area.set_size_request(800,400)
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.vbox)
        self.hbox = Gtk.Box(spacing=6)
        self.lbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.back = Gtk.Button("Return to main menu")
        self.back.connect("clicked", self.backtomain)
        self.vbox.pack_start(self.back, False, False, 0)
        #------DEFINE FIND BLUETOOTH DEVICES------#
        try:
            p3 = subprocess.Popen(["bt-device", "--list"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
            (stdout, stdin) = (p3.stdout, p3.stdin)
            data = stdout.readlines()
            olddata = []
            try:
                from bluetooth.ble import DiscoveryService
                service = bluetooth.discover_devices(lookup_names=True)
                print("Found ",len(service), " devices")
                print(service)
        #------END DEFINE FIND BLUETOOTH DEVICES------#
        #------DEFINE PARSE AND PRINT BLUETOOTH DEVICES------#
                if len(service) > 0:
                    for u,n in service:
                        print(1)
                        self.btitem = Gtk.Button(n)
                        self.btitem.set_size_request(150, 20)
                        self.lbox.pack_start(self.btitem, False, False, 5)
        #------END DEFINE PARSE AND PRINT BLUETOOTH DEVICES------#
        #------DEFINE FAILED TO FIND BLUETOOTH DEVICES-----#
            except:
                if data == []:
                    self.error = Gtk.Label()
                    self.error.set_text("No adapter found.")
                    self.vbox.pack_start(self.error, True, True, 0)
                    self.hbox.pack_start(self.lbox, False, False, 0)
                    self.vbox.pack_start(self.hbox, False, False, 0)
                    k = 1
                else:
                    print("No new discoverable devices found!")
        #------END DEFINE FAILED TO FIND BLUETOOTH DEVICES-----#
        #------DEFINE PRINT AND CORRECT BLUETOOTH DEVICES-----#
            i = 0
            for line in data:
                if olddata == data:
                    print("Device displays twice, ignoring!")
                else:
                    i = i + 1
                    olddata = data
                    datastr = str(data[i])
                    print(datastr)
                    o = datastr.find("b'")
                    o = o + 2
                    f = datastr.find('(')
                    f = f - 1
                    name = datastr[o:f]
                    self.btitem = Gtk.Button(name)
                    self.btitem.set_size_request(150, 20)
                    self.lbox.pack_start(self.btitem, False, False, 0)
                    olddata = data
        #------END DEFINE PRINT AND CORRECT BLUETOOTH DEVICES-----#
        #------DEFINE ERROR CONTROL-----#
            if k != 1:
                self.hbox.pack_start(self.lbox, False, False, 0)
                self.hbox.pack_start(self.draw_area, False, False, 0)
                self.vbox.pack_start(self.hbox, False, False, 0)
        #------END DEFINE ERROR CONTROL-----#
        #------DEFINE NO ADAPTER ERROR EXCEPTION-----#
        except:
            self.error = Gtk.Label()
            self.error.set_text("No adapter found.")
            self.vbox.pack_start(self.error, True, True, 0)
            self.hbox.pack_start(self.lbox, False, False, 0)
            self.vbox.pack_start(self.hbox, False, False, 0)
        #------END DEFINE NO ADAPTER ERROR EXCEPTION-----#
    def backtomain(self, data):
        #---------DEFINE UNIVERSAL RETURN TO MAIN MENU---------#
        self.vbox.destroy()
        #------DEFINE CONTROL MAINLOOP ERROR-----#
        try:
            GObject.MainLoop().quit()
        except:
            pass
        #------END DEFINE CONTROL MAINLOOP ERROR-----#
        self.set_title("Home")
        self.setup_main()
        self.show()
        Gtk.main()
    def logout():
        #------DEFINE FUTURE OAUTH INTEGRATION------#
        del session['profile']
        session.modified = True
        oauth2.storage.delete()
        return redirect(request.referrer or '/')
    def setup_st(self):
        #-------DEFINE SETUP FOR SETTINGS MENU-------#
        #-----DEFINE SETUP GLOBAL SETTINGS BOXES-----#
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.lbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.kbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.fbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.vbox)
        self.hbox = Gtk.Box(spacing=6)
        self.draw_area = Gtk.DrawingArea()
        self.draw_area.set_size_request(800,400)
        #-----END DEFINE SETUP GLOBAL SETTINGS BOXES-----#
        #-----DEFINE SETTINGS MENUS-----#
        self.back = Gtk.Button("Return To Main Menu")
        self.back.connect("clicked", self.backtomain)
        self.display = Gtk.Button("Display")
        self.display.set_relief(2)
        self.display.connect("clicked", self.dspconf)
        self.sound = Gtk.Button("Sounds")
        self.sound.set_relief(2)
        self.sound.connect("clicked", self.sndconf)
        self.gui = Gtk.Button("GUI")
        self.gui.set_relief(2)
        self.gui.connect("clicked", self.guiconf)
        self.ext = Gtk.Button("External Devices")
        self.ext.set_relief(2)
        self.ext.connect("clicked", self.extconf)
        self.net = Gtk.Button("Network")
        self.net.set_relief(2)
        self.net.connect("clicked", self.netconf)
        #-----END DEFINE SETTINGS MENUS-----#
        #-----DEFINE PACK BOXES-----#
        self.lbox.pack_start(self.back, False, False, 5)
        self.lbox.pack_start(self.display, False, False, 5)
        self.lbox.pack_start(self.sound, False, False, 5)
        self.lbox.pack_start(self.gui, False, False, 5)
        self.lbox.pack_start(self.ext, False, False, 5)
        self.lbox.pack_start(self.net, False, False, 5)
        self.hbox.pack_start(self.lbox, False, False, 0)
        self.hbox.pack_start(self.kbox, False, False, 0)
        self.obox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.obox.pack_start(self.fbox, False, False, 0)
        self.hbox.pack_start(self.obox, False, False, 0)
        self.hbox.pack_start(self.draw_area, False, False, 0)
        self.vbox.pack_start(self.hbox, False, False, 0)
        #-----END DEFINE PACK BOXES-----#
    def op_st(self, data):
        #----------DEFINE SETTINGS MENU PRINT---------#
        self.vbox.destroy()
        self.setup_st()
        self.show()
        Gtk.main()
    def dspconf(self, data):
        #------DEFINE DISPLAY DISPLAY SETTINGS MENU PRINT------#
        #------DEFINE CLEAR OLD MENU ITEMS------#
        try:
            self.m1.destroy()
            self.m2.destroy()
            self.m3.destroy()
        except:
            pass
        try:
            self.fbox.destroy()
            self.fbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            #self.obox.pack_start(self.fbox, False, False, 0)
        except:
            pass
        try:
            GObject.MainLoop().quit()
        except:
            pass
        #------END DEFINE CLEAR OLD MENU ITEMS------#
        #------DEFINE ATTEMPT CLEAR UNEEDED-----#
        try:
            self.obox.destroy()
            self.draw_area.destroy()
            self.draw_area.set_size_request(800,400)
            self.obox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.obox.pack_start(self.fbox, False, False, 0)
            self.hbox.pack_start(self.obox, False, False, 0)
            self.hbox.pack_start(self.draw_area, False, False, 0)
        except:
            self.obox.pack_start(self.fbox, False, False, 0)
        #------END DEFINE ATTEMPT CLEAR UNEEDED-----#
        self.m1 = Gtk.Button("Display Scale")
        self.m1.set_relief(2)
        self.m2 = Gtk.Button("Resolution")
        self.m2.set_relief(2)
        self.m3 = Gtk.Button("Display")
        self.m3.set_relief(2)
        self.m1.connect("clicked", self.dsppick, 1)
        self.m2.connect("clicked", self.dsppick, 2)
        self.m3.connect("clicked", self.dsppick, 3)
        self.kbox.pack_start(self.m1, False, False, 5)
        self.kbox.pack_start(self.m2, False, False, 5)
        self.kbox.pack_start(self.m3, False, False, 5)
        self.show()
        self.display.set_relief(1)
        self.sound.set_relief(2)
        self.gui.set_relief(2)
        self.ext.set_relief(2)
        self.net.set_relief(2)
    def sndconf(self, data):
        #-----------DEFINE DISPLAY SOUND SETTINGS MENU PRINT----------#
        try:
            self.m1.destroy()
            self.m2.destroy()
            self.m3.destroy()
        except:
            pass
        try:
            self.fbox.destroy()
            self.fbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            #self.obox.pack_start(self.fbox, False, False, 0)
        except:
            pass
        try:
            GObject.MainLoop().quit()
        except:
            pass
        #------END DEFINE CLEAR OLD MENU ITEMS------#
        #------DEFINE ATTEMPT CLEAR UNEEDED-----#
        try:
            self.obox.destroy()
            self.draw_area.destroy()
            self.draw_area.set_size_request(800,400)
            self.obox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.obox.pack_start(self.fbox, False, False, 0)
            self.hbox.pack_start(self.obox, False, False, 0)
            self.hbox.pack_start(self.draw_area, False, False, 0)
        except:
            self.obox.pack_start(self.fbox, False, False, 0)
        #------END DEFINE ATTEMPT CLEAR UNEEDED-----#
        self.sound.set_relief(1)
        self.m1 = Gtk.Button("Audio Output")
        self.m1.set_relief(2)
        self.m2 = Gtk.Button("Audio Modes")
        self.m2.set_relief(2)
        self.m3 = Gtk.Button("Audio Input")
        self.m3.set_relief(2)
        self.m1.connect("clicked", self.sndpick, 1)
        self.m2.connect("clicked", self.sndpick, 2)
        self.m3.connect("clicked", self.sndpick, 3)
        self.kbox.pack_start(self.m1, False, False, 5)
        self.kbox.pack_start(self.m2, False, False, 5)
        self.kbox.pack_start(self.m3, False, False, 5)
        self.show()
        self.display.set_relief(2)
        self.gui.set_relief(2)
        self.ext.set_relief(2)
        self.net.set_relief(2)
    def guiconf(self, data):
        #----------DEFINE DISPLAY GUI SETTINGS MENU PRINT----------#
        #------DEFINE CLEAR OLD MENU ITEMS------#
        try:
            self.m1.destroy()
            self.m2.destroy()
            self.m3.destroy()
        except:
            pass
        try:
            self.fbox.destroy()
            self.fbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            #self.obox.pack_start(self.fbox, False, False, 0)
        except:
            pass
        try:
            GObject.MainLoop().quit()
        except:
            pass
        #------END DEFINE CLEAR OLD MENU ITEMS------#
        #------DEFINE ATTEMPT CLEAR UNEEDED-----#
        try:
            self.obox.destroy()
            self.draw_area.destroy()
            self.draw_area.set_size_request(800,400)
            self.obox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.obox.pack_start(self.fbox, False, False, 0)
            self.hbox.pack_start(self.obox, False, False, 0)
            self.hbox.pack_start(self.draw_area, False, False, 0)
        except:
            self.obox.pack_start(self.fbox, False, False, 0)
        #------END DEFINE ATTEMPT CLEAR UNEEDED-----#
        self.m1 = Gtk.Button("Display Modes")
        self.m1.set_relief(2)
        self.m2 = Gtk.Button("Home Menu")
        self.m2.set_relief(2)
        self.m3 = Gtk.Button("Colors")
        self.m3.set_relief(2)
        self.m1.connect("clicked", self.guipick, 1)
        self.m2.connect("clicked", self.guipick, 2)
        self.m3.connect("clicked", self.guipick, 3)
        self.gui.set_relief(1)
        self.kbox.pack_start(self.m1, False, False, 5)
        self.kbox.pack_start(self.m2, False, False, 5)
        self.kbox.pack_start(self.m3, False, False, 5)
        self.show()
        self.display.set_relief(2)
        self.sound.set_relief(2)
        self.ext.set_relief(2)
        self.net.set_relief(2)
    def extconf(self, data):
        #------------DEFINE DISPLAY EXTERNAL DEVICES SETTINGS MENU PRINT----------#
        #------DEFINE CLEAR OLD MENU ITEMS------#
        try:
            self.m1.destroy()
            self.m2.destroy()
            self.m3.destroy()
        except:
            pass
        try:
            self.fbox.destroy()
            self.fbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            #self.obox.pack_start(self.fbox, False, False, 0)
        except:
            pass
        try:
            GObject.MainLoop().quit()
        #------END DEFINE CLEAR OLD MENU ITEMS------#
        #------DEFINE ATTEMPT CLEAR UNEEDED-----#
        except:
            pass
        try:
            self.obox.destroy()
            self.draw_area.destroy()
            self.draw_area.set_size_request(800,400)
            self.obox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.obox.pack_start(self.fbox, False, False, 0)
            self.hbox.pack_start(self.obox, False, False, 0)
            self.hbox.pack_start(self.draw_area, False, False, 0)
        except:
            self.obox.pack_start(self.fbox, False, False, 0)
        #------END DEFINE ATTEMPT CLEAR UNEEDED-----#
        self.m1 = Gtk.Button("Arduino Port")
        self.m1.set_relief(2)
        self.m2 = Gtk.Button("Arduino Arguments")
        self.m2.set_relief(2)
        self.m3 = Gtk.Button("")
        self.m3.set_relief(2)
        self.m1.connect("clicked", self.extpick, 1)
        self.m2.connect("clicked", self.extpick, 2)
        self.m3.connect("clicked", self.extpick, 3)
        self.ext.set_relief(1)
        self.kbox.pack_start(self.m1, False, False, 5)
        self.kbox.pack_start(self.m2, False, False, 5)
        #self.kbox.pack_start(self.m3, False, False, 5)
        self.show()
        self.display.set_relief(2)
        self.sound.set_relief(2)
        self.gui.set_relief(2)
        self.net.set_relief(2)
    def netconf(self, data):
        #---------DEFINE DISPLAY NETWORK SETTINGS MENU PRINT--------#
        try:
            self.m1.destroy()
            self.m2.destroy()
            self.m3.destroy()
        except:
            pass
        try:
            self.obox.destroy()
            self.draw_area.destroy()
            self.draw_area.set_size_request(800,400)
            self.obox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.obox.pack_start(self.fbox, False, False, 0)
            self.hbox.pack_start(self.obox, False, False, 0)
            self.hbox.pack_start(self.draw_area, False, False, 0)
        except:
            self.obox.pack_start(self.fbox, False, False, 0)
        try:
            GObject.MainLoop().quit()
        except:
            pass
        self.m1 = Gtk.Button("Connections")
        self.m1.set_relief(2)
        self.m2 = Gtk.Button("Wireless")
        self.m2.set_relief(2)
        self.m3 = Gtk.Button("")
        self.m3.set_relief(2)
        self.m1.connect("clicked", self.netpick, 1)
        self.m2.connect("clicked", self.netpick, 2)
        self.m3.connect("clicked", self.netpick, 3)
        self.net.set_relief(1)
        self.kbox.pack_start(self.m1, False, False, 5)
        self.kbox.pack_start(self.m2, False, False, 5)
        #self.kbox.pack_start(self.m3, False, False, 5)
        self.show()
        self.display.set_relief(2)
        self.sound.set_relief(2)
        self.gui.set_relief(2)
        self.ext.set_relief(2)
    def dsppick(self, data, num):
        #-------------DEFINE DISPLAY SETTINGS MENU PRINT------------#
        self.m1.set_relief(2)
        self.m2.set_relief(2)
        self.m3.set_relief(2)
        data = []
        try:
            self.fbox.destroy()
            self.fbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.obox.pack_start(self.fbox, False, False, 0)
        except:
            pass
        if num == 1:
            print("DisplayScale")
            self.m1.set_relief(1)
        elif num == 2:
            #--------------DEFINE RESOLUTION MODES PRINT------------#
            #print("Res")
            self.m2.set_relief(1)
            cmd = ['xrandr']
            cmd2 = ['grep', '    ']
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout=subprocess.PIPE)
            data = p.stdout.readlines()
            if data == []:
                #print("trying again!")
                self.dsppick("ok", 2)
            i = -1
            for line in data:
                i = i + 1
                datastr = str(data[i])
                if "     " in datastr:
                    #print(datastr)
                    r = datastr.find("b'   ")
                    r = r + 5
                    k = datastr.find("     ")
                    #print(r)
                    datastr = datastr[r:k]
                    self.but1 = Gtk.Button(datastr)
                    if "*+" in str(data[i]):
                        self.but1.set_relief(1)
                    else:
                        self.but1.set_relief(2)
                    self.fbox.pack_start(self.but1, False, False, 5)
                self.show()
        elif num == 3:
            print("Disp Props")
            self.m3.set_relief(1)
    def sndpick(self, data, num):
        #-------------DEFINE SOUND SETTINGS MENU PRINT-------------#
        self.m1.set_relief(2)
        self.m2.set_relief(2)
        self.m3.set_relief(2)
        dev = pulse.source_list()
        try:
            self.fbox.destroy()
            self.fbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.obox.pack_start(self.fbox, False, False, 0)
        except:
            pass
        if num == 1:
            #---------------DEFINE SOUND OUTPUT DEVICES PRINT-----------#
            #print("Output")
            dev = pulse.source_list()
            devk = pulse.sink_list()
            #print(dev)
            i = 0
            for source in dev:
                devr = str(dev[i])
                #print(devr)
                r = devr.find("description=")
                r = r + 13
                k = devr.find("',")
                devr = devr[r:k]
                if "Monitor of" in devr:
                    r = devr.find("Monitor of")
                    r = r + 11
                    devr = devr[r:]
                    devr = ("Output of " + devr)
                self.but1 = Gtk.Button(devr)
                if "output" in str(dev[i]):
                    devs = str(devk[i])
                    #print(devs)
                    r = devs.find("name=")
                    r = r + 6
                    devs = devs[r:]
                    k = devs.find("',")
                    devs = devs[:k]
                    ok = pulse.server_info().default_sink_name
                    if ok == devs:
                        self.but1.set_relief(1)
                    else:
                        self.but1.set_relief(2)
                    self.but1.connect("clicked", self.choose, pulse.sink_list()[i])
                    self.fbox.pack_start(self.but1, False, False, 5)
                i = i + 1
            self.show()
            self.m1.set_relief(1)
        elif num == 2:
            #---------------DEFINE AUDIO MODE PRINT-------------#
            #print("Modes")
            self.m2.set_relief(1)
            self.draw_area.set_size_request(300,300)
            card = pulse.card_list()[0]
            dev = card.profile_list
            check = pulse.card_info(index=0)
            check = str(check)
            r = check.find("active=[")
            r = r + 8
            check = check[r:]
            k = check.find("]")
            check = check[:k]
            #print(check)
            i = 0
            for profile in dev:
                #print(dev[i])
                devr = str(dev[i])
                #print(devr)
                r = devr.find("description=")
                r = r + 13
                #print(r)
                k = devr.find("',")
                #print(k)
                devr = devr[r:k]
                #print(devr)
                self.but1 = Gtk.Button(devr)
                devs = str(dev[i])
                #print(devs)
                r = devs.find("name=")
                r = r + 6
                devs = devs[r:]
                k = devs.find("',")
                devs = devs[:k]
                #print(devs)
                if check == devs:
                    self.but1.set_relief(1)
                else:
                    self.but1.set_relief(2)
                self.but1.connect("clicked", self.modepk, devs, card)
                self.fbox.pack_start(self.but1, False, False, 5)
                i = i + 1
            self.show()
        elif num == 3:
            #-------------DEFINE SOUND INPUT DEVICES PRINT-------------#
            #print("Input")
            self.m3.set_relief(1)
            dev = pulse.source_list()
            #print(dev)
            check = pulse.card_info(index=0)
            #print(check)
            check = str(check)
            r = check.find("+input:")
            r = r + 7
            check = check[r:]
            k = check.find("]")
            check = check[:k]
            #print(check)
            i = 0
            for source in dev:
                #print(dev[i])
                if "input" in str(dev[i]):
                    devr = str(dev[i])
                    #print(devr)
                    r = devr.find("description=")
                    r = r + 13
                    #print(r)
                    k = devr.find("',")
                    #print(k)
                    devr = devr[r:k]
                    if "input" in str(dev) and "output" in str(dev):
                        devr = ("Input of " + devr)
                    self.but1 = Gtk.Button(devr)
                    if check in str(check):
                        self.but1.set_relief(1)
                    else:
                        self.but1.set_relief(2)
                    #self.but1.connect("clicked", self.choose, pulse.sink_list()[i])
                    self.fbox.pack_start(self.but1, False, False, 5)
                i = i + 1
            self.show()
    def guipick(self, data, num):
        #-------------DEFINE GUI SETTINGS MENU PRINT----------#
        self.m1.set_relief(2)
        self.m2.set_relief(2)
        self.m3.set_relief(2)
        try:
            self.fbox.destroy()
            self.fbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.obox.pack_start(self.fbox, False, False, 0)
        except:
            pass
        if num == 1:
            print("Modes")
            self.m1.set_relief(1)
        elif num == 2:
            print("Home")
            self.m2.set_relief(1)
        elif num == 3:
            print("Colors")
            self.m3.set_relief(1)
    def extpick(self, data, num):
        #------------DEFINE EXTERNAL DEVICES MENU PRINT-----------#
        self.m1.set_relief(2)
        self.m2.set_relief(2)
        self.m3.set_relief(2)
        try:
            self.fbox.destroy()
            self.fbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.obox.pack_start(self.fbox, False, False, 0)
        except:
            pass
        if num == 1:
            print("Port")
            self.m1.set_relief(1)
        elif num == 2:
            print("Docs")
            self.m2.set_relief(1)
        elif num == 3:
            print("N/A")
            self.m3.set_relief(1)
    def netpick(self, data, num):
        #------------DEFINE NETWORK SETTINGS MENU PRINT------------#
        self.m1.set_relief(2)
        self.m2.set_relief(2)
        self.m3.set_relief(2)
        try:
            self.fbox.destroy()
            self.fbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            #self.obox.pack_start(self.fbox, False, False, 0)
            k = 0
        except:
            pass
        try:
            GObject.MainLoop().quit()
        except:
            pass
        try:
            self.obox.destroy()
            self.draw_area.destroy()
            self.draw_area.set_size_request(800,400)
            self.obox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.obox.pack_start(self.fbox, False, False, 0)
            self.hbox.pack_start(self.obox, False, False, 0)
            self.hbox.pack_start(self.draw_area, False, False, 0)
            k = 0
        except:
            self.obox.pack_start(self.fbox, False, False, 0)
        if num == 1:
            #------------DEFINE AVAILABLE NETWORK PRINT-----------#
            #print("Unpicked")
            self.m1.set_relief(1)
            #ssids = []
            ssids = {}
            apold = []
            oldssids = []
            dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
            for dev in NetworkManager.Device.all():
                if dev.DeviceType == NetworkManager.NM_DEVICE_TYPE_WIFI:
                    dev.OnAccessPointAdded(ap_added)
                    dev.OnAccessPointRemoved(ap_removed)
            try:
                for ap in NetworkManager.AccessPoint.all():
                    ssids[ap.object_path] = ap.Ssid
                    #print(apold)
                    #print(ap.Ssid)
                    if apold != ap.Ssid:
                        #print("%-30s %s %s%%" % (ap.Ssid, ap.HwAddress, ap.Strength))
                        if ap.Ssid not in oldssids and ap.Ssid != "":
                            self.fbox = Gtk.Box(spacing=6)
                            self.but1 = Gtk.Button(ap.Ssid)
                            self.but1.set_relief(2)
                            self.fbox.pack_start(self.but1, True, True, 5)
                            self.obox.pack_start(self.fbox, False, False, 5)
                            #print(ap.Ssid)
                    else:
                        print("ERROR")
                        pass
                    oldssids.append(ap.Ssid)
                    apold = ap.Ssid
                    #print(apold)
                    #print(oldssids)
            except:
                self.error = Gtk.Label("No Networks.")
                self.obox.destroy()
                self.draw_area.destroy()
                self.draw_area.set_size_request(800,400)
                self.obox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
                self.hbox.pack_start(self.obox, True, True, 0)
                self.fbox.pack_start(self.error, True, True, 0)
                self.obox.pack_start(self.fbox, True, True, 5)
            self.show()
            try:
                GObject.MainLoop().quit()
            except:
                pass
            time.sleep(0.2)
            GObject.MainLoop().run()
            #self.show()
                    #print(apold)
            apold = []
        elif num == 2:
            #print("Wireless")
            self.m2.set_relief(1)
            #----------DEFINE WIRELESS CONFIG PRINT----------#
            connections = NetworkManager.Settings.ListConnections()
            for conn in NetworkManager.NetworkManager.ActiveConnections:
                settings = str(conn.Connection.GetSettings()['connection']['id'])
                #print(settings)
            i = 0
            devices = NetworkManager.NetworkManager.GetDevices()
            for dev in devices:
                if dev.DeviceType == NetworkManager.NM_DEVICE_TYPE_WIFI:
                    #print("OK")
                    break
            for x in connections:
                conn = connections[i].GetSettings()['connection']['id']

                if "Wired connection" not in conn:
                    self.fbox = Gtk.Box(spacing=6)
                    self.but1 = Gtk.Button(conn)
                    self.fbox.pack_start(self.but1, True, True, 5)
                    #print(conn)
                    #print(settings)
                    if settings == conn:
                        self.but1.set_relief(1)
                    else:
                        self.but1.set_relief(2)
                        self.but1.connect("clicked", self.con, connections[i], dev)
                    self.but1 = Gtk.Button("X")
                    self.but1.set_relief(2)
                    self.fbox.pack_start(self.but1, False, False, 5)
                    self.obox.pack_start(self.fbox, False, False, 5)
                i = i + 1
            self.show()
        elif num == 3:
            print("N/A")
            self.m3.set_relief(1)
    def choose(self, data, args):
        try:
            pulse.default_set(args)
            print("Set!")
        except:
            print("Failed!")
    def modepk(self, data, args, card):
        try:
            pulse.card_profile_set(card, args)
            self.sndpick("ok", 2)
            print("Set!")
        except:
            print("Failed!")


    def get_token(self):
        data = {
        'grant_type': 'client_credentials',
        'scope': 'identify connections messages.read rpc.notifications.read'
        }
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = requests.post('%s/oauth2/token' % API_ENDPOINT, data, headers, auth=(CLIENT_ID, CLIENT_SECRET))
        r.raise_for_status()
        return r.json()
    def discconnect(self):
        global ret
        ret = str(self.get_token())
        print(ret)
        r = ret.find("'access_token': '")
        r = r + 17
        ret = ret[r:]
        r = ret.find("'")
        ret = ret[:r]
        print(ret)
    def con(self, data, con, dev):
        try:
            print(dev)
            print(con)
            NetworkManager.NetworkManager.ActivateConnection(con, dev, "/")
            self.netpick("ok", 2)
        except:
            pass


def ap_added(dev, interface, signal, access_point):
    ssids[access_point.object_path] = access_point.Ssid
    print("+ %-30s %s %sMHz %s%%" % (access_point.Ssid, access_point.HwAddress, access_point.Frequency, access_point.Strength))
    access_point.OnPropertiesChanged(ap_propchange)

def ap_removed(dev, interface, signal, access_point):
    print("- %-30s" % ssids.pop(access_point.object_path))



API_ENDPOINT = 'https://discordapp.com/api/v6'


if __name__ == '__main__':

    window = resultsWindow()
    window.setup_main()
    window.show()
    Gtk.main()
