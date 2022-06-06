from v2.models import Admin, Rector, Professor

def auth(collection, content):
    user = collection.objects.get()
