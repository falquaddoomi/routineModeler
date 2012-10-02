from celery import task
from ohmagekit.clients.ohmage import OhmageApi

@task()
def add(x, y):
    return x + y

@task
def ohmage_authenticate(username, password):
    # get a handle to ohmage, run the thing
    api = OhmageApi()
    api.login(username, password)
    api.auth_hashedpass, api.auth_token