from model.config import DBSession
from model.device import Device
import mechanize, re, json, datetime, sys
from bs4 import BeautifulSoup
from base64 import b64encode

class Czyrksys(object):
    
    __url__ = 'http://192.168.1.1/status-devices.asp'

    def __init__(self, router_creds, mapping=None):
        self.router_creds = router_creds
        self.session = DBSession()
    
    def fetch_html_object(self, item, fields):
        """ 
        Grab the HTML from the provided url
        """
        if item == 'arplist':
            regexp = 'arplist = (.*?);'
        elif item == 'dhcpd_lease':
            regexp = 'dhcpd_lease = (.*?);'
        else:
            return NotImplementedError

        # Initialize browser
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders.append(('Authorization', 'Basic %s' % self.router_creds ))
        br.open(self.__url__)
        data = br.response().read()
        m = re.search(regexp, data)
        if m:
            text = m.groups()[0].replace("'", "\"")
            data = json.loads(text)
            return [dict(zip(fields, i)) for i in data]

    def fetch_arp(self):
        """
        Grab the arp table to get the current devices
        """
        mapping = ['ip', 'mac', 'interface']
        arp_data = self.fetch_html_object('arplist', mapping)
        return arp_data

    def fetch_devices(self, only_active=False):
        """
        Grab the dhcp lease table from the status page
        """
        ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        mapping = ['name', 'ip', 'mac', 'lease_time_remaining']
        dhcpd_data = self.fetch_html_object('dhcpd_lease', mapping) 
        if only_active:
            active_macs = [ i['mac'] for i in self.fetch_arp() ]
            data = [ f for f in dhcpd_data if f['mac'] in active_macs ]
        else:
            data = dhcpd_data
        # Note that we add the timestamp 
        for item in data:
            item['event_ts'] = ts
        return data

    def update_rows(self, only_active=False):
        active_macs = [ i['mac'] for i in self.fetch_arp() ]
        devices = self.fetch_devices(only_active)
        for d in devices:
            if d['mac'] in active_macs: 
                entry = Device(**d)
                self.session.add(entry)
        self.session.commit()
