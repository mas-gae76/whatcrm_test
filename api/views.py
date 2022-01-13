from django.shortcuts import render
from .models import IdToken, Contact
import requests


header = {'X-Tasktest-Token': 'f62cdf1e83bc324ba23aee3b113c6249'}
server = 'https://dev.whatsapp.sipteco.ru/v3/'
id = None
token = None
phone = None


def get_chat(request):
    url = server + 'chat/spare?crm=TEST&domain=test'
    response = requests.get(url=url, headers=header)
    global id, token
    id = response.json()['id']
    token = response.json()['token']
    if not IdToken.objects.filter(id=id, token=token).exists():
        obj = IdToken(id=id, token=token)
        obj.save()
        return render(request, 'index.html', {'chat': obj})


def get_qr(request):
    url = server + 'instance{}/qr_code?token={}'.format(id, token)
    with requests.get(url=url, headers=header) as response:
        return render(request, 'index.html', {'qr_code': response.json()['qr']})


def remove_chat(request):
    url = server + 'instance{}/removeChat?token={}'.format(id, token)
    response = requests.get(url, headers=header)
    IdToken.objects.filter(id=id, token=token).delete()
    return render(request, 'index.html', {'delete_status': 'Чат успешно удалён!'})


def get_status(request):
    url = server + 'instance{}/status?full=1&token={}'.format(id, token)
    response = requests.get(url=url, headers=header)
    if response.json()['state'] == 'CONNECTED':
        contact_url = server + 'instance{}/contacts?token={}'.format(id, token)
        contact_info = requests.get(url=contact_url, headers=header)
        global phone
        phone = contact_info.json()['number']
        obj = Contact(name=contact_info.json()['name'], phone=phone)
        obj.save()
        return render(request, 'index.html', {'contact': obj})
    return render(request, 'index.html', {'info': 'Аккаунт не активирован!'})


def send_message(request):
    send_url = server + 'instance{}/sendMessage?token={}'.format(id, token)
    data = {
        'phone': phone,
        'typeMsg': 'text',
        'body': 'Hello, World!',
        'sendSeen': '1',
    }
    response = requests.post(url=send_url, headers=header, data=data)
    if response.json()['sent']:
        return render(request, 'index.html', {'sent': 'Сообщение успешно отправлено!'})
    return render(request, 'index.html', {'sent': 'Сообщение не отправлено!'})
