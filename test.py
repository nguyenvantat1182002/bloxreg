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


with open('signup_links.txt', 'r+', encoding='utf-8') as file:
    print(file.read())
    file.truncate(0)