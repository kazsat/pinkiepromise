"""pinkiepromise URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from django.conf.urls import url
# from posts import views
from promises import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('promises/', include('promises.urls')),
    path('', include('promises.urls')),
    path('accounts/', include('django.contrib.auth.urls')), #  追加
    path('ca/', views.account, name='account'),
    # path('posts/', include('posts.urls')),
    # path('posts/<int:post_id>/', views.post_detail, name='post_detail')

    # path('posts/<int:post_id>/', views.post_detail, name='post_detail')
    # url(r'^posts/(?P<post_id>[0-9]+)/$', views.post_detail)
    # url(r'^posts/(?P<post_id>[0-9]+)/$', views.post_detail, name="post_detail")
    # path('', include('posts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
