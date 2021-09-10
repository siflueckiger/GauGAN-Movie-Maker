import os
import re
import shutil
import subprocess
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-s', '--style', dest='style')
parser.add_argument('-if', '--import_folder', dest='import_folder')
parser.add_argument('-fr', '--frame_rate', dest='frame_rate')
args = parser.parse_args()

style = args.style
import_folder = args.import_folder

# remove . and \ from import folder
work_name = import_folder.replace('.','')
work_name = work_name.replace('\\', '')

frame_rate = args.frame_rate

# get path to input and output directory
cwd = os.getcwd()
input_directory = cwd + '\\' + work_name
project_directory = cwd + '\\' + work_name + '_output_s' + style
output_directory = project_directory + '\\output'
project_input_directory = project_directory + '\\input'

# get extension from inputfiles
file = os.listdir(work_name)[0]
file_name, file_extension = os.path.splitext(file)




# ---- FUNCTIONS ----

def make_output_folder():
    if not os.path.exists(project_directory):
        os.mkdir(project_directory)   
    else:
        print('---> project directory already exists.')
        exit()

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)   
    else:
        print('---> output directory already exists.')
        exit()

    if not os.path.exists(project_input_directory):
        os.mkdir(project_input_directory)   
    else:
        print('---> output directory already exists.')
        exit()

    # copy input files into project folder
    src_files = os.listdir(input_directory)
    for filename in src_files:
        full_file_name = os.path.join(input_directory, filename)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, project_input_directory)

    print('---> project folder created')


def rename_files():
    # rename file with pattern three digits start 001
    for count, filename in enumerate(os.listdir(work_name)):
        new_filename = f"{count+1:03}"
        src = work_name + '\\' + filename
        dst = work_name + '\\' + new_filename + file_extension
        os.rename(src, dst)
    
    print('---> input files renamed')



def make_movies():
    name_input_file = work_name + '_input.mp4'
    os.chdir(input_directory)
    print('ffmpeg', '-framerate', frame_rate, '-i', '%03d' + file_extension, name_input_file)
    subprocess.call(['ffmpeg', '-framerate', frame_rate, '-i', '%03d' + file_extension, name_input_file])
    
    name_output_file = work_name + '_output_s' + style + '.mp4'
    os.chdir(output_directory)
    print('ffmpeg', '-framerate', frame_rate, '-i', '%03d.jpg', name_output_file)
    subprocess.call(['ffmpeg', '-framerate', frame_rate, '-i', '%03d.jpg', name_output_file])
    
    shutil.move(input_directory +'\\' + name_input_file, project_directory + '\\' + name_input_file)
    shutil.move(output_directory +'\\' + name_output_file, project_directory + '\\' + name_output_file)




# ---- START SCRIPT ----

rename_files()
make_output_folder()

os.system("gaugan.py -s " + style + " -i " + import_folder)
print('---> all output images generated')

make_movies()
print('---> DONE !!!')