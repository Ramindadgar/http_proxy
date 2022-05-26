import re
from http import server
import urllib.request
import webbrowser
from database import db

"""
HTTP PROXY, WEB BLOCKER

    Website I test on:
    localhost:8000/http://httpvshttps.com

    Server running on localhost port 8000. So to test entering a http website enter in the browser
    localhost:8000/http://example.com (example.com is also a test http website)
"""

"""
httpd
    Fetching the URL from conn-class and do_GET function,
    Then printing listening to let the user know the server is active,
    Then uses the serve_forever module. And only breaks the connection when user stops it, with command, ctrl + C
"""


class MyProxy(server.SimpleHTTPRequestHandler):

    def redirect_to_new_website(self):
        """
        Simple function to redirect user to another
        website when trying to enter a blocked domain.
        """
        newUrl = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        return newUrl


    def do_GET(self):
        """
        Connection function
        Fetching the URL from path.
        checks if the URL is in BLOCK_DOMAIN.
        If all is good, sends response and header and connects.

        plz using this pattern in url for test:
        'http://www.test.com'
        'm.google.com',
        'google.com',
        'www.someisotericdomain.innersite.mall.co.uk',
        'www.ouruniversity.department.mit.ac.us',
        'www.somestrangeurl.shops.relevantdomain.net',
        'www.example.info'
        """
        res = re.findall(r'(?<=\.)([^.]+)(?:\.(?:co\.uk|ac\.us|[^.]+(?:$|\n)))', self.path)
        all_domains = db.get_all_name_web_sites()
        block_list = [item[0] for item in all_domains]
        try:
            if res[0] in block_list:
                newurl = self.redirect_to_new_website()
                webbrowser.open(newurl)
                self.wfile.write('Blocked website...!!!'.encode())
                self.send_response(403)

            else:
                self.send_response(200)
                self.end_headers()
                self.copyfile(urllib.request.urlopen(res[0]), self.wfile)
        except Exception as ex:
            print(ex)
