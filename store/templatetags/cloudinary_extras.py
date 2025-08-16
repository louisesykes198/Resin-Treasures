from django import template

register = template.Library()

@register.filter(name='cloudinary_url')
def cloudinary_url(public_id, transformation=''):
    cloud_name = 'dprjwdfdq'  # Your actual Cloudinary cloud name
    base_url = f'https://res.cloudinary.com/{cloud_name}/image/upload/'

    if transformation:
        return f'{base_url}{transformation}/{public_id}'
    return f'{base_url}{public_id}'
