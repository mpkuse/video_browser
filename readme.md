# Web-based Video File Browser

This tool lets you view video files (mp4) from a server on the web browser. It renders the preview video in lower resolution. Download link shows up which lets you download the video in full resolution. 

Motivation: Earlier I used to use another open source web-based file viewer. Issue with it was that it showed full resolution video in preview which was often too slow to be useful.  

This is a flask based file viewer and video displayer. It lists all the folders. For videos it searches for video-thumbnails. Any displays that instead. To generate video thumbnails, run `script/generate_preview.py` 

![Alt Text](./static/screenshot.png)


## How to run 
I will recommend to run it only on https. Else the video streaming does not work on Apple devices. 
```
python3 files_and_folders.py
```

requirements:
- pip3 install Flask 
- pip3 install moviepy



## How to generare sslkeys
```
mkdir sslkeys && cd sslkeys 
openssl genpkey -algorithm RSA -out server.key
openssl req -new -key server.key -out server.csr
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
openssl x509 -text -noout -in server.crt
cd ..
```


## Contact
Manohar Kuse <mpkuse@connect.ust.hk>
