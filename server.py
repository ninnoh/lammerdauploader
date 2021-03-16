#!/bin/python3
import http.server
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from socketserver import ThreadingMixIn
import json, asyncio
from ninnobotapi import ninnobotapi
import random, os
import redis as rdis
import string, hashlib
redis = rdis.StrictRedis(host='localhost', port=6379)

def grs(length):
    return (hashlib.md5((''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(length))).encode()).hexdigest())[:length]



token = "Vaffanculo mi son ricordato di toglierlo"
chat = 'Inserisci un chatid dove ci sta il robots,.'
website = "https://diocane.ml"
class Handler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
    def do_GET(self):
        self._set_headers()
        self.wfile.write((json.dumps({'ok': False, 'received': 'no', "error": "ONLY POST REQUESTS ALLOWED."})).encode())

    def do_POST(self):
        self._set_headers()
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            import cgi
            from io import BytesIO
            ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            pdict['CONTENT-LENGTH'] = int(self.headers['Content-Length'])
            form_data = cgi.parse_multipart(BytesIO(post_data), pdict)
            bot = ninnobotapi(token=token,
                                  endpoint="https://botapi.giuseppem99.xyz")
            for name in form_data:   
                async def ei(mb, name):
                    mb = b''.join(mb)
                    gb = round(((len(mb)/1024)/1024)/1024, 200)
                    if gb <=2:
                        id = grs(20)
                        res = (await bot.sendDocument(document=mb, chat_id=chat,
                                                      caption=json.dumps({"id": id, "why?": "this is useless."}), filename=name))
                        for x in res:
                            if type(x) == str:
                                try:
                                    if "file_id" in res[x]:
                                        tipo = x 
                                except:
                                    pass
                        fid = res[tipo]['file_id']       
                        path = (await bot.getFile(file_id=fid))['file_path']
                        url = f"https://botapi.giuseppem99.xyz/file/bot{bot.token}/{path}"
                        rs = json.dumps({"update": res, "type": tipo, "url_internal":url, "url_external": f"{website}/?dl={id}"})
                        redis.set(f"{id}", rs)                         
                        self.wfile.write((json.dumps({'ok': True, 'received': 'yes', "download_url": f"{website}/?dl={id}"})).encode())
                    else:
                        self.wfile.write((json.dumps({'ok': False, 'received': 'no', "download_url": f"", "error": "File is larger than 2GB!"})).encode())
                asyncio.run(ei(form_data[name], name))
        except Exception as e:
            print(e)
            self.wfile.write((json.dumps({'ok': False, 'received': 'no', "error": str(e)})).encode())






class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle in un altro thread capisci"""


if __name__ == '__main__':
    server = ThreadedHTTPServer(('localhost', 1234), Handler)
    print('Server iniziato guaglion '+ f'{server.server_address}')
    server.serve_forever()

