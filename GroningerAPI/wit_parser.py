import urllib2
import json

WIT_ACCESS_TOKEN='GE3WFS7X5FGREBMX7WA46XIHMO2ES7WC'
WIT_API_HOST = 'https://api.wit.ai'
WIT_API_VERSION = '20160516'

class WitParser:
    def parse(self, message):
        req = urllib2.Request(WIT_API_HOST + '/message?q=' + urllib2.urlencode(message))
        req.add_header('authorization', 'Bearer ' + WIT_ACCESS_TOKEN)
        req.add_header('accept', 'application/vnd.wit.' + WIT_API_VERSION + '+json')
        resp = urllib2.urlopen(req)
        return json.loads(resp.read())
