import requests


def activate_user(request, uid, token):
    domain = request.build_absolute_uri('/')[:-1]
    requests.post(f'{domain}/api/auth/users/activation/', data={
        'uid': uid,
        'token': token
    })
