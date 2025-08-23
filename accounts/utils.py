from django.utils.text import slugify
from django.contrib.auth.models import User

def generate_unique_username(first, last):
    base_username = slugify(f"{first}_{last}")
    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}_{counter}"
        counter += 1
    return username
