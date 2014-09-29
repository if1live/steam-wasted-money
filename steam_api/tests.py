#-*-coding: utf-8 -*-

from django.test import TestCase

import unittest
import apis

class SteamIDApiTest(unittest.TestCase):
    def test_run(self):
        api = apis.SteamIDApi()
        actual = api.run('if1live')
        self.assertEqual('76561198032092535', actual)

    def test_not_exist(self):
        api = apis.SteamIDApi()
        actual = api.run('123fdsfdsfsdfsfsdfdwsf')
        self.assertEqual(None, actual)


class OwnedGameApiTest(unittest.TestCase):
    def test_run(self):
        api = apis.OwnedGameApi()
        actual = api.run('76561198032092535')
        self.assertEqual(38400 in actual, True)

    def test_cannot_access(self):
        api = apis.OwnedGameApi()
        actual = api.run('76561197986486958')
        self.assertEqual({}, actual)

class ProductApiTest(unittest.TestCase):
    def test_single(self):
        id_list = 57690
        api = apis.ProductApi()
        actual = api.run(id_list)

        expected = {
            57690: {
                'name': 'Tropico 4: Steam Special Edition',
                'price': 1999
            },
        }

    def test_multiple(self):
        id_list = [57690, 245730]
        api = apis.ProductApi()
        actual = api.run(id_list)

        expected = {
            57690: {
                'name': 'Tropico 4: Steam Special Edition',
                'price': 1999
            },
            245730: {
                'name': 'Flashback',
                'price': 999
            }
        }
