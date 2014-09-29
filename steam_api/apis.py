#-*- coding: utf-8 -*-

import requests
import json
import re

KEY = '5F6C6024AD9BDF457D4FB3FB312DDE46'

class SteamIDApi(object):
    def run(self, user_id):
        url = 'http://steamcommunity.com/id/{0}'.format(user_id)
        r = requests.get(url)
        content = r.text

        for line in content.splitlines():
            line = line.strip()
            if 'g_rgProfileData' in line:
                uid = self.read_id(line)
                return uid
        return None

    def read_id(self, line):
        u'''
        g_rgProfileData = {"url":"http:\/\/steamcommunity.com\/id\/if1live\/","steamid":"76561198032092535","personaname":"if1live","summary":"No information given."};
        '''
        m = re.search(r'"steamid":"(?P<id>\d+)"', line)
        return m.groups()[0]


class ProductApi(object):
    u'''
    http://store.steampowered.com/api/appdetails?appids=57690,245730
    '''
    def run(self, appid_list):
        url = 'http://store.steampowered.com/api/appdetails'

        if type(appid_list) not in (tuple, list):
            appids = [unicode(appid_list)]
        else:
            appids = [unicode(x) for x in appid_list]

        params = {
            'appids': ','.join(appids)
        }
        r = requests.get(url, params=params)
        data = r.json()

        retval = {}
        for x in appids:
            if x not in data:
                continue
            if 'data' not in data[x]:
                continue
            if 'price_overview' not in data[x]['data']:
                continue

            name = data[x]['data']['name']
            raw_price = data[x]['data']['price_overview']['final']
            elem = {
                'name': name,
                'price': raw_price
            }
            retval[int(x)] = elem
        return retval


class OwnedGameApi(object):
    def run(self, steamid):
        url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
        params = {
            'key': KEY,
            'steamid': steamid,
            'format': 'json'
        }
        r = requests.get(url, params=params)
        if 'games' not in r.json()['response']:
            return []

        data = r.json()['response']['games']
        retval = []
        for x in data:
            appid = x['appid']
            retval.append(appid)
        return retval
