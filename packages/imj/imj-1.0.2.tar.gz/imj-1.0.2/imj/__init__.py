import requests

BASE = 'https://img.marcusweinberger.repl.co'

class IMJ(object):
    def __init__(self, img_id, base_url='https://img.marcusweinberger.repl.co',
    disp_url='https://i.marcusj.tech'):
        self.id = img_id
        self.base = base_url
        self.disp = disp_url

    @property
    def viewer(self):
        return f"{self.disp}/view/{self.id}"
    
    @property
    def url(self):
        return f"{self.disp}/image/{self.id}"
    
    def shorten(self):
        return requests.get(f"{self.base}/shorten/{self.id}").url.replace(self.base, self.disp)
    

def upload_file(fn):
    r = requests.post(f"{BASE}/upload", files={
        'image': open(fn, 'rb')
    })
    return IMJ(r.url.split('/')[-1])

def upload(raw, fn='image.png', mimetype='image/png'):
    r = requests.post(f"{BASE}/upload", files={
        'image': (
            fn,
            raw,
            mimetype,
        )
    })
    return IMJ(r.url.split('/')[-1])
