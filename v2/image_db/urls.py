from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^user_home_page/$', user_home, name='user_home_page_url'),
    url(r'^logout/$', logout, name='logout_url'),
    url(r'^registration/$', registration, name='registration_url'),
    url(r'^gallery/$', images, name='gallery_url'),
    url(r'^gallery/(?P<image_id>\d+)/$', image, name='image_detail_url'),
    url(r'^add_image/$', add_image, name='add_image_url'),
    url(r'^$', home_page, name='home'),
]