"""rrs_s URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import path, include
from django.views.decorators.cache import never_cache

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('main.urls', 'main'), namespace='main')),
    path('social/', include('social_django.urls', namespace='social')),
    path('api-auth/', include('rest_framework.urls')),  # Для админки рест фреймворк
    path('api/', include(('api.urls', 'api'), namespace='api')),
    path('auth/', include('rest_framework_social_oauth2.urls')),  # для регистрации через соц. сети
    path('auth/', include('djoser.urls.authtoken')),  # для создания токенов
    path('auth/', include('djoser.urls.jwt')),  # для жвт токенов
    path('auth/', include('djoser.urls')),  # для остальных действий по регистрации, аутентефикации и тд
]

if settings.DEBUG:
    urlpatterns.append(path('static/<path:path>',
                            never_cache(serve)))

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
