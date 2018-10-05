from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^illuminations$', views.index),
    url(r'^register$', views.register),
    url(r'^create_user$', views.create_user),
    url(r'^sign_in$', views.sign_in),
    url(r'^sign_me_in$', views.sign_me_in),
    url(r'^user_profile/(?P<user_id>\d+)$', views.user_profile),
    url(r'^logout$', views.logout),
    url(r'^artists$', views.artists),
    url(r'^artwork$', views.artwork),
    url(r'^new_artwork$', views.new_artwork),
    url(r'^create_item$', views.create_item),
    url(r'^product/(?P<art_id>\d+)$', views.product),
    url(r'^cart$', views.cart),
    url(r'^add_to_cart/(?P<art_id>\d+)/(?P<user_id>\d+)$', views.add_to_cart),
    url(r'^search$', views.search),
    url(r'^edit_product/(?P<art_id>\d+)$', views.edit_product),
    url(r'^edit_this_product/(?P<art_id>\d+)$', views.edit_this_product),
    url(r'^delete_product/(?P<art_id>\d+)/(?P<user_id>\d+)$', views.delete_product),
    url(r'^edit_profile/(?P<user_id>\d+)$', views.edit_profile),
    url(r'^delete_profile/(?P<user_id>\d+)$', views.delete_profile),
    url(r'^make_purchase$', views.make_purchase),
]