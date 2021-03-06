"""djangosite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from homepage import views as homepage_views
from django.views.decorators.cache import cache_page

handler404 = 'homepage.views.handler404'

cache_homepage = 60*60*24 # 60*60*24 - 24h

urlpatterns = [
]

urlpatterns += i18n_patterns(
    path('admin/clearcache/', include('clearcache.urls')),
    path('admin/', admin.site.urls),
    path('', cache_page(cache_homepage)(homepage_views.index), name='index'),
    path('privacy-policy/' , cache_page(60*60*24)(homepage_views.privacy), name='privacy'),
    path('about/' , cache_page(60*60*24)(homepage_views.about), name='about'),
    path('contact/' , cache_page(60*60*24)(homepage_views.contact), name='contact'),
    prefix_default_language=False,
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls'))
    ]

