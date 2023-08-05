import requests
from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='sdh_cdn_image')
def sdh_cdn_image(value, str_arg):
    kwargs = {}
    for arg in str_arg.split(','):
        [key, val] = arg.split('=')
        kwargs[key] = val
    width = kwargs.get('width', 100)
    height = kwargs.get('height', 100)
    cropping = kwargs.get('cropping', 0)

    url = settings.CUSTOM_STORAGE_OPTIONS['url']
    token = settings.CUSTOM_STORAGE_OPTIONS['token']
    headers = {'Authorization': 'Bearer {}'.format(token)}
    url = '{}/{}?width={}&height={}&cropping={}'.format(url, value.name, width, height, cropping)
    rc = requests.get(url, headers=headers)
    if rc.status_code != 200:
        return ''
    return rc.json()['url']



