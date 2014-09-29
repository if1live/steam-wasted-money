#-*- coding: utf-8 -*-

from importd import d
import requests
from steam_api import apis

d(
    DEBUG=True,
    INSTALLED_APPS=(
        'django_nose',
        'steam_api',
    ),
    INTERNAL_IPS=('192.168.194.1',),
)

@d('/')
def index(request):
    return d.render_to_response('index.jinja2')

@d('/update/game/<slug:appids>')
def update_game(request, appids):
    from steam_api.models import Product

    api = apis.ProductApi()
    resp = api.run(appids.split('-'))

    for appid in resp.keys():
        data = resp[appid]

        try:
            obj = Product.objects.get(appid=appid)
            if obj.price != data['price']:
                obj.price = data['price']
                obj.save()

        except Product.DoesNotExist:
            obj = Product.objects.create(appid=appid, name=data['name'], price=data['price'])

    return d.JSONResponse({'success':True})


if __name__ == '__main__':
    d.main()
