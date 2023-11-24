from flask import redirect, Flask, render_template, request, Response, send_file
import re 
app = Flask(__name__)


@app.route('/video_iphone')
def video():
    range_header = request.headers.get('Range', None)
    video_file_path = '/home/manohar/Videos/personal/03_Flumserberg_ski_sunnyday/DJI_0371_001_320p.mp4'

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
