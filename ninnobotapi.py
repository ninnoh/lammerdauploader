import requests, json, httpx, asyncio, sys, requests


class ninnobotapi:
    # StartPolling function
    def startPolling(self):
        loop = asyncio.get_event_loop()
        try:
            f = loop.run_until_complete(self.Polling())
        except KeyboardInterrupt:
            print("\nBye, cya tacabros")
            sys.exit()

    async def webRequest(self, url=False, r='json', params={}):
        if url != False:
            try:
                async with httpx.AsyncClient() as session:
                    resp = await session.get(url, params=params)
                    if r == 'json':
                        data = resp.json()
                    else:
                        data = resp
                    return data
            except Exception as e:
                print(e)
                return False

    async def getMe(self):
        return (self.bot_info)

    # ASYNC Api Requests

    async def apiRequest(self, method='getme', params=[], files=False):
        url = '{}/bot{}/{}'.format(self.endpoint, self.token, method)
        # Init aiohttp
        async with httpx.AsyncClient() as client:
            if params != []:
                if files != False:
                    try:
                        r = await client.post(url, params=params, files=files)
                    except:
                        pass
                else:
                    r = await client.post(url, data=params)
            else:
                r = await client.post(url)
            # print(r.json)
            try:
                if r:
                    data = r.json()
            except:
                return {"ok": False}
        if data["ok"] == False:
            print(data["error_code"], data["description"])
            return
        return data["result"]

    # Methods
    def __getattr__(self, method):
        async def function(**kwargs):
            file = {}
            pop = []
            kw = {}
            # Polling method
            if "document" in kwargs and "filename" in kwargs:
                filename=kwargs["filename"]
            else:
                filename="document"
            for x in kwargs:
                x = x.lower()
                if x in ["document", "photo", "video", "media", "voice", "audio", "animation"]:
                    if "media" not in x:
                        if "buffer" in str(type(kwargs[x])).lower() or isinstance(kwargs[x], bytes):
                            if "audio" in x:
                                try:
                                    import soundfile as sf
                                    import eyed3
                                    import os
                                    # print("guaglions")
                                    from mutagen.mp3 import MP3

                                    direct = (os.path.realpath(kwargs[x].name))
                                    audio = MP3(direct)
                                    # print("APERTO MUTAGENICO")
                                    kw["duration"] = round(audio.info.length)
                                    audiofile = eyed3.load(direct)
                                    if audiofile.tag.title:
                                        kw["title"] = audiofile.tag.title
                                    if audiofile.tag.artist:
                                        kw["performer"] = audiofile.tag.artist
                                    if audiofile.tag.images[0].image_data:
                                        kw["thumb"] = audiofile.tag.images[0].image_data

                                except Exception as e:
                                    print(e)
                                    pass


                            if isinstance(kwargs[x], bytes):
                                #guess = {"voice": ".ogg", "audio": ".mp3", "photo": '.jpg', 'video': '.mp4'}[x]
                                #print(filename)
                                file[x] = (filename, kwargs[x])
                                pop.append(x)
                            else:
                                file[x] = (kwargs[x].name, kwargs[x])
                                pop.append(x)
            for x in kw:
                kwargs[x] = kw[x]
                if "thumb" in kwargs and "bytes" in str(type(kwargs["thumb"])):
                    file["thumb"] = kwargs["thumb"]
                    kwargs.pop("thumb")

            for y in pop:
                kwargs.pop(y)

            if method.lower == "webrequest":
                return
            if method == "Polling":
                if self.handler != None:
                    update_id = 0
                    while True:
                        funct = self.handler
                        try:
                            update = await self.getUpdates(offset=update_id)
                            if len(update) > 0:
                                try:
                                    update_id = update[0]['update_id'] + 1
                                except:
                                    update_id = 0
                                    pass
                                try:
                                    loop = asyncio.get_event_loop()
                                    asyncio.ensure_future(funct(update[0]))
                                except Exception as e:
                                    print(f"New exception: {str(e)}")
                                    pass
                        except Exception as e:
                            raise Exception(e)

            if 'media' in kwargs:
                kwargs['media'] = json.dumps(kwargs['media'])
            if 'reply_markup' in kwargs:
                kwargs['reply_markup'] = json.dumps(kwargs['reply_markup'])
            if 'results' in kwargs:
                kwargs['results'] = json.dumps(kwargs['results'])
            if 'mask_position' in kwargs:
                kwargs['mask_position'] = json.dumps(kwargs['mask_position'])
            if 'shipping_options' in kwargs:
                kwargs['shipping_options'] = json.dumps(kwargs['shipping_options'])
            return (await self.apiRequest(method, kwargs, files=file))

        return function

    # Init
    def __init__(self, token=None, endpoint="https://api.telegram.org", handler_function=None, startup_info=False):
        self.token = token
        self.endpoint = endpoint
        self.handler = handler_function
        try:
            try:
                loop = asyncio.get_event_loop()
            except:
                loop = asyncio.new_event_loop()
            bot_info = loop.run_until_complete(self.apiRequest('getMe', []))
            self.bot_info = bot_info
            if startup_info:
                print(
                f"Welcome back!\n\nBot name: {bot_info['first_name']}\nBot username: @{bot_info['username']}\nBot ID: {bot_info['id']}")
        except:
            raise Exception("Invalid token")

