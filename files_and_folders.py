from flask import redirect, Flask, render_template, request, Response, send_file
import os
import math
import re 

app = Flask(__name__)

VIDEO_FOLDER = "/home/manohar/Videos/personal"

#----- Video Streaming


def generate(videopath):
    with open(videopath, 'rb') as video_file:
        while True:
            data = video_file.read(1024)
            if not data:
                break
            yield data


@app.route('/video')
def video():
    videopath = request.args.get('videopath', '')
    if videopath == '':
        return "ERROR"
    return Response(generate(videopath), mimetype='video/mp4')


@app.route('/video_iphone')
def video_iphone():
    video_file_path = request.args.get('videopath', '')
    if video_file_path == '':
        return "ERROR"
    #video_file_path = '/home/manohar/Videos/personal/03_Flumserberg_ski_sunnyday/DJI_0371_001_320p.mp4'

    range_header = request.headers.get('Range', None)

    with open(video_file_path, 'rb') as video_file:
        video_file.seek(0, 2)
        total_size = video_file.tell()

        if range_header:
            start, end = parse_range_header(range_header, total_size)
            video_file.seek(start)
            length = end - start + 1
            data = video_file.read(length)
            response = Response(data, status=206, mimetype='video/mp4', content_type='video/mp4')
            response.headers.add('Content-Range', 'bytes {}-{}/{}'.format(start, end, total_size))
        else:
            response = Response(video_file.read(), mimetype='video/mp4')

        return response

def parse_range_header(header, total_size):
    range_match = re.match(r'bytes=(\d+)-(\d*)', header)

    if range_match:
        start = int(range_match.group(1))
        end = int(range_match.group(2)) if range_match.group(2) else total_size - 1
        return start, end

    return 0, None

#--------- Download file
@app.route('/download', methods=['GET'])
def download_file():
    file_name = request.args.get('file')
    # Check if the 'file' parameter is present
    if file_name is None:
        return "Error: 'file' parameter is missing."
    file_path = os.path.join('path/to/your/files', file_name)
    if not os.path.exists(file_path):
        return "Error: File not found."
    # Return the file as a response for download
    return send_file(file_path, as_attachment=True)


#-----List Files on HTML Page


@app.route('/')
def list_files_and_folders():
    directory_path = request.args.get('path', VIDEO_FOLDER)
    contents = get_directory_contents(directory_path)
    contents_videos = get_videofiles_with_vthumbs(directory_path)
    parent_directory = os.path.dirname(directory_path)
    return render_template('list.html',
                           contents_videos=contents_videos,
                           contents=contents,
                           current_path=directory_path,
                           parent_directory=parent_directory)


def get_human_readable_size(file_path):
    size_bytes = os.path.getsize(file_path)
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    size = round(size_bytes / p, 2)
    return f"{size} {size_name[i]}"


def get_directory_contents(path):
    try:
        entries = os.listdir(path)
        entries = [
            entry for entry in entries if not entry.startswith('.')
            and os.path.isdir(os.path.join(path, entry))
        ]  # Exclude hidden files/folders
        full_paths = [os.path.join(path, entry) for entry in entries]
        is_directories = [os.path.isdir(full_path) for full_path in full_paths]
        contents = list(zip(entries, full_paths, is_directories))
        return contents
    except FileNotFoundError:
        return []


def get_videofiles_with_vthumbs(path):
    video_list = []
    video_fullpath_list = []
    vthumbs_fullpath_list = []
    file_size = []

    try:
        entries = os.listdir(path)
        for entry in entries:
            if entry.startswith('.'):
                continue

            if (entry.endswith('.mp4') or entry.endswith('.MP4')
                ) and not entry.endswith('_320p.mp4'):
                entry_vthumb = entry[0:-4] + '_320p.mp4'
                if os.path.isfile(os.path.join(path, entry_vthumb)):
                    video_list.append(entry)
                    video_fullpath_list.append(os.path.join(path, entry))
                    vthumbs_fullpath_list.append(
                        os.path.join(path, entry_vthumb))

                    file_size.append(
                        get_human_readable_size(os.path.join(path, entry)))

        contents = list(
            zip(video_list, video_fullpath_list, vthumbs_fullpath_list, file_size))

        return contents

    except FileNotFoundError:
        return []


if __name__ == '__main__':
    #     #app.run(debug=True)

    #     #app.run(debug=True, ssl_context='adhoc')
    #     #app.run(host='0.0.0.0', port=5000 )

    #     # need to run on https for iphone
    #     app.config.update(dict(PREFERRED_URL_SCHEME='https'))
    #app.config['SERVER_NAME'] = '192.168.178.22'  # Update with your domain
    app.config['SESSION_COOKIE_SECURE'] = True

    context = ('sslkeys/server.crt', 'sslkeys/server.key'
               )  #certificate and key files
    app.run(debug=False, host='0.0.0.0', port=4343, ssl_context=context)
