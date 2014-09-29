#-*- coding: utf-8 -*-

from importd import d
import requests
from steam_api import apis

# 14/09/29 기준
CURRENTY_RATIO = 1049.3

d(
    DEBUG=True,
    INSTALLED_APPS=(
        'django_nose',
        'steam_api',
    ),
    INTERNAL_IPS=('192.168.194.1',),
)

from babel.numbers import format_currency
from django_jinja import library
import jinja2

@library.filter
@jinja2.contextfilter
def usd2krw(ctx, value):
    if type(value) in (str, unicode):
        value = float(value)

    value *= CURRENTY_RATIO
    return format_currency(value, 'KRW', format='#,###', locale='ko')


class SteamException(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message


COMMON_CONTEXT = {
    'currency_ratio': CURRENTY_RATIO
}


def view_empty(request):
    return d.render_to_response('index.jinja', COMMON_CONTEXT)

def view_user(request, username):
    from steam_api.models import Product

    ctx = {
        'username': username
    }

    try:
        if len(username) == 0:
            raise SteamException(u'스팀아이디가 올바르지 않습니다.')

        user_api = apis.SteamIDApi()
        steamid = user_api.run(username)
        ctx['steamid'] = steamid

        if not steamid:
            raise SteamException(u'스팀아이디가 올바르지 않습니다.')

        purchased_api = apis.OwnedGameApi()
        purchased_list = purchased_api.run(steamid)

        saved_product_list = Product.objects.filter(appid__in=purchased_list)
        saved_appid_list = [x.appid for x in saved_product_list]

        required_appid_list = list(set(purchased_list) - set(saved_appid_list))
        api = apis.ProductApi()
        new_feteched_product_dict = api.run(required_appid_list)

        for appid, data in new_feteched_product_dict.items():
            obj = Product.objects.create(appid=appid, name=data['name'], price=data['price'])

        product_list = Product.objects.filter(appid__in=purchased_list)
        ctx['success'] = True

        # 결국 찾아내지 못한 데이터는 0원으로 설정, 가짜 상품으로 넣기
        not_valid_product_list = list(set(purchased_list) - set(x.appid for x in product_list))
        for appid in not_valid_product_list:
            obj = Product.objects.create(appid=appid, name='', price=0)

        product_list = [x for x in product_list if x.price > 0]
        ctx['product_list'] = product_list
        ctx['total_usd'] = sum([x.price for x in product_list]) / 100.0

    except SteamException as e:
        ctx['success'] = False
        ctx['error_message'] = e.message

    data = dict(COMMON_CONTEXT.items() + ctx.items())
    return d.render_to_response('index.jinja', data)



@d('/')
def index(request):
    if 'username' in request.GET:
        username = request.GET.get('username')
        return view_user(request, username)
    else:
        return view_empty(request)


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
