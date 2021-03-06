from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext as _


# Create your views here.
def index(request):
    site = get_current_site(request)
    title = _('Djangosite sample app')
    description = _('Djangosite description')
    context = {
        'site_name' : site.name,
        'title' : title,
        'description' : description,
        'social_image' : str('https://' + str(request.get_host())+ '/static/img/homepage.png'),
        'homepage' : True,
    }
    return render(request, 'homepage/homepage.html', context)

def handler404(request, exception):
    site = get_current_site(request)
    title = _('Page not Found - 404')
    description = _('Page not Found - 404. Try search or go to the homepage')
    context = {
        'site_name' : site.name,
        'title' : title,
        'description' : description,
    }

    response = render(request, "404.html", context=context)
    response.status_code = 404
    return response

def privacy(request):
    site = get_current_site(request)
    title = _('Privacy Policy')
    description = _('Privacy Policy') + ' - ' + site.name
    context = {
        'site_name' : site.name,
        'title' :  title,
        'description' : description,
    }
    return render(request, 'homepage/privacy.html', context)

def about(request):
    site = get_current_site(request)
    title = _('About Us')
    description = _('About Us Page') + ' - ' + site.name
    context = {
        'site_name' : site.name,
        'title' :  title,
        'description' : description,
    }
    return render(request, 'homepage/about.html', context)

def contact(request):
    site = get_current_site(request)
    title = _('Contact Us')
    description = _('Contact Us Page') + ' - ' + site.name
    context = {
        'site_name' : site.name,
        'title' :  title,
        'description' : description,
    }
    return render(request, 'homepage/contact.html', context)



