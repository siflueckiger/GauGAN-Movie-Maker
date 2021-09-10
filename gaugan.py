from genericpath import isfile
import requests, re, shutil, os, base64, random, string
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-s', '--style', dest='style')
parser.add_argument('-if', '--import_folder', dest='import_folder')
args = parser.parse_args()

style = args.style
import_folder = args.import_folder
work_name = import_folder.replace('.','')
work_name = work_name.replace('\\', '')

print(style, import_folder)


def getUrl():
	print('Getting new server address...')
	r = requests.get('http://34.216.122.111/gaugan/demo.js')
	urls = re.findall(r'\'(http.*?://.*?/)\'', re.search(r'urls=.*?;', r.text)[0])
	return urls[0]

url = getUrl()

for img in os.listdir(import_folder):
	print(f'Processing image \'{img}\'')

	# get b64 encoded image
	with open(import_folder + img, "rb") as f:
		imgb64 = 'data:image/png;base64,' + str(base64.b64encode(f.read()))[2:-1]

	# generate name for requests
	name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))


	while True:
		try:
			# send map img to server
			POSTdata = {
				'imageBase64': imgb64,
				'name': name
			}

			requests.post(url + 'nvidia_gaugan_submit_map', data = POSTdata)

			# get generated img from server
			POSTdata = {
				'name': name,
				'style_name': str(style)
			}
			r = requests.post(url + 'nvidia_gaugan_receive_image', data = POSTdata, stream = True)
			break
		except:
			url = getUrl() # if there is an error getting the image, get a new server URL and try again

	r.raw.decode_content = True

	# write image to out folder
	with open(work_name + '_output_s' + style + '/output/' + img.split('.')[0] + '.jpg','wb') as f:
		shutil.copyfileobj(r.raw, f)