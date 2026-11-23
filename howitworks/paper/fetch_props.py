"""Fetch transparent Pixabay props listed in props_requests.json into library/.
Each request: {"name": "onion", "q": "onion", "id": optional Pixabay id to pin, "type": "all|photo|illustration|vector"}.
Skips names already in library/. Prefers real photos, then illustrations, then vectors, and only keeps images
that actually have a transparent background (so the paper-cutout border hugs the object)."""
import json, os, sys, io, time, urllib.request, urllib.parse
from PIL import Image
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); LIB=os.path.join(HERE,'library'); os.makedirs(LIB,exist_ok=True)
KEY=os.environ.get('PIXABAY_KEY');
if not KEY: sys.exit('PIXABAY_KEY secret is missing')
def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'whatif-props/1.0'})
    with urllib.request.urlopen(req,timeout=60) as r: return r.read()
def api(**p):
    p['key']=KEY; p.setdefault('safesearch','true'); p.setdefault('per_page',20)
    return json.loads(get('https://pixabay.com/api/?'+urllib.parse.urlencode(p)))
def transparent_ok(data):
    im=Image.open(io.BytesIO(data))
    if im.mode not in ('RGBA','LA','P'): return False
    a=np.asarray(im.convert('RGBA'))[...,3]
    clear=(a<16).mean(); return 0.08<clear<0.92
reqs=json.load(open(os.path.join(HERE,'props_requests.json')))
log=[]
for r in reqs:
    name=r['name']; out=os.path.join(LIB,name+'.png')
    if os.path.exists(out): continue
    try:
        if r.get('id'): hits=api(id=r['id'])['hits']
        else:
            hits=[]
            for t in ([r['type']] if r.get('type') else ['photo','illustration','vector']):
                hits+=api(q=r['q'],image_type=t,colors='transparent').get('hits',[])
        saved=False
        for h in hits[:15]:
            data=get(h['largeImageURL'])
            if not r.get('id') and not transparent_ok(data): continue
            Image.open(io.BytesIO(data)).convert('RGBA').save(out)
            json.dump({'pixabay_id':h['id'],'page':h['pageURL'],'user':h['user'],'tags':h['tags'],'query':r.get('q')},open(out[:-4]+'.json','w'),indent=1)
            log.append(f"OK {name} <- {h['id']} ({h['type']})"); saved=True; break
        if not saved: log.append(f"MISS {name} ({r.get('q')})")
    except Exception as e: log.append(f"ERR {name}: {e}")
    time.sleep(0.7)
print('\n'.join(log) or 'nothing to fetch')
open(os.path.join(LIB,'_last_fetch.log'),'w').write('\n'.join(log)+'\n')
