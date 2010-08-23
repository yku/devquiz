import hashlib
import hmac
import base64
import time
import random
import urllib
import urllib2

# POST http://gdd-2010-quiz-japan.appspot.com/oauth/c50914409537e03670800db8&hello=world
# Authorization: OAuth realm="devquiz"
# oauth_consumer_key="c50914409537e03670800db8",
# oauth_signature_method="HMAC-SHA1",
# oauth_signature="XXXXXXXXXXXXXXXXXXXXXX",
# oauth_timestamp="1244636076",
# oauth_nonce="5c261539688b2a591aad",
# oauth_version="1.0"

def get_signature(method, url, params, key, secret):
    l = []
    l.append("hello=world")
    for k in sorted(params):
        l.append("%s=%s" % (k, params[k]))
    s = "&".join(l)
    msg = "%s&%s&%s" % (method, urllib2.quote(url, ""), urllib2.quote(s, ""))
    print msg
    h = hmac.new("%s&" % secret, msg, hashlib.sha1)
    signature = h.digest().encode("base64").strip()
    return signature

def oauth_header(params):
    l = []
    for k in sorted(params):
        l.append('%s="%s"' % (k, params[k]))
    return 'OAuth realm="devquiz", %s' % (", ".join(l)) 


url = "http://gdd-2010-quiz-japan.appspot.com/oauth/c50914409537e03670800db8"
key = "c50914409537e03670800db8"
secret = "c006c3e2ae8ab4589a262fcf"
method = "POST"

param = { "oauth_consumer_key": key, 
          "oauth_nonce": str(random.getrandbits(64)),
          "oauth_signature_method": "HMAC-SHA1",
          "oauth_timestamp": str(int(time.time())),
          "oauth_version": "1.0" }
sig = get_signature(method, url, param, key, secret)
param["oauth_signature"] = sig
hdr = oauth_header(param)
val = {'hello': 'world'}

data = urllib.urlencode(val)
req = urllib2.Request(url, data)
req.add_header("Authorization", hdr)
res = urllib2.urlopen(req)
print res.read()
