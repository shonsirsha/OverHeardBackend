from __future__ import unicode_literals
from flask import Flask, request, jsonify, make_response
import youtube_dl
import os

app = Flask(__name__)


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print("DOnE!!!!!!")
        
    
    if d['status'] == 'downloading':
        print(d['filename'], d['_percent_str'], d['_eta_str'])

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '100',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
     'outtmpl': os.path.dirname(os.path.abspath(__file__))+'/%(id)s.%(ext)s'
    
}

@app.route('/test/', methods=['POST'])
def test():
    data = request.get_json()

    url = data['link']
    return jsonify({'wow': url})

@app.route('/test2/', methods=['POST'])
def test2():
    data = request.get_json()

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            url = data['link']
            info_dict = ydl.extract_info(url, download=False)
            video_id = info_dict.get('id', None)
            video_uploader = info_dict.get('uploader', None)
            video_title = info_dict.get('title', None)
            video_duration = info_dict.get('duration', None)

        return jsonify({'status': 'success', 'video_id': video_id, 'path': os.path.dirname(os.path.abspath(__file__)), 'uploader': video_uploader, 'title': video_title, 'duration': video_duration})


    except Exception as e:
        return jsonify({'status': e})

@app.route('/download/', methods=['POST'])
def download():
    newTitle = ''
    data = request.get_json()
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            url = data['link']
            info_dict = ydl.extract_info(url, download=False)
            ydl.download([url])
            video_id = info_dict.get('id', None)
            video_uploader = info_dict.get('uploader', None)
            video_title = info_dict.get('title', None)
            video_duration = info_dict.get('duration', None)

        return jsonify({'status': 'success', 'video_id': video_id, 'uploader': video_uploader, 'title': video_title, 'duration': video_duration, 'path': os.path.dirname(os.path.abspath(__file__))})


    except Exception as e:
        return jsonify({'status': e})


app.run(port=80, host='localhost')