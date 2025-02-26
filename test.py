# import socket
# import os

# from contextlib import closing
# from DrissionPage import ChromiumPage, ChromiumOptions


# def random_port(host: str = None):
#     if not host:
#         host = ''
#     with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
#         s.bind((host, 0))
#         s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         return s.getsockname()[1]
    

# options = ChromiumOptions()

# port = random_port()
# options.set_local_port(port)
# options.set_user_data_path(os.path.join(os.getcwd(), 'profiles', str(port)))

# page = ChromiumPage(addr_or_opts=options)

# page.listen.start('https://auth.roblox.com/v2/signup')
# for packet in page.listen.steps():
#     packet.request.postData.update({'username': 'nguyenvantat123332'})
#     print(packet.request.postData)

from seleniumwire import webdriver
import json


def interceptor(request):
    if 'roblox' in request.url:
        print(request.url)

        if request.method == 'POST' and request.url == 'https://auth.roblox.com/v2/signup':
            body = request.body.decode('utf-8')
            data = json.loads(body)
            print(data)

            data['username'] = 'nguyenvantat223ijjng3'
            
driver = webdriver.Chrome()
driver.request_interceptor = interceptor
driver.get('https://chromewebstore.google.com/detail/browsec-vpn-free-vpn-for/omghfjlpggmjjaagoclmmobgdodcjboh')
# driver.get('https://www.roblox.com/signup?dataToken=JTWCVM44JDH76M7XGGD66HBMHB3XF4B4&source=VerifiedParentalConsent&requestType=LinkToChild&sessionId=051868df-961c-494d-b3f0-72658021c9c9')