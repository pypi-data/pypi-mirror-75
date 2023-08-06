import sys

import requests

s = requests.Session()
post_url = 'http://127.0.0.1:5000/'
post_url += sys.argv[1].split(',')[0] + '/' + sys.argv[1].split(',')[1] + '/' + 'post'
s.post(post_url, data={'msg': "quit"})
