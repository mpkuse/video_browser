import os
import subprocess
from moviepy.editor import VideoFileClip
import argparse


def create_video_thumbs_in_folder(input_folder ):
    output_folder = input_folder
    horizontal_resolution = '320:240'  # 16:9 for horizontal videos
    vertical_resolution = '240:320'    # 9:16 for vertical videos

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # List all MP4 files in the input folder
    input_files = [file for file in os.listdir(input_folder) if (file.endswith('.mp4') or file.endswith('MP4')) and not file.endswith("_320p.mp4") ]

    for input_file in input_files:
        input_path = os.path.join(input_folder, input_file)
        output_file = f"{os.path.splitext(input_file)[0]}_320p.mp4"
        output_path = os.path.join(output_folder, output_file)

        if os.path.isfile( output_path):
            print( 'skip: ', input_file, ' because ', output_file, ' already exists' )
            continue

        # Use moviepy to get the video's width and height
        clip = VideoFileClip(input_path)
        width, height = clip.size

        # Determine the resolution based on the aspect ratio
        if width > height:
            resolution = horizontal_resolution
        else:
            resolution = vertical_resolution

        # Use FFmpeg to resize the video
        command = f"ffmpeg -i {input_path} -vf 'scale={resolution}' -c:v libx264 -crf 23 -c:a aac -strict experimental -b:a 128k {output_path}"
        subprocess.run(command, shell=True)

    print("Conversion complete.")


def list_folders_recursive(path='.'):
    folders = []
    for root, dirs, files in os.walk(path):
        for dir_name in dirs:
            folder_path = os.path.join(root, dir_name)
            folders.append(folder_path)
    return folders


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process a base folder.")
    parser.add_argument("base_folder", help="Path to the base folder")
    args = parser.parse_args()

    if not os.path.exists(args.base_folder):
        print("Error: The specified base folder does not exist.")
        exit(1)


    base_fld = '/home/manohar/Videos/personal'
    base_fld = args.base_folder
    for folder in list_folders_recursive( base_fld ):
        print( '>>>>>>>', folder )
        create_video_thumbs_in_folder( folder )