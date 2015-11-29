from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from product_app import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^google/', include('google_login.urls')),
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.IndexView.as_view(), name="index"),
    #url(r'^detail/(?P<productID>(\d+))/$', views.detail, name='detail'),
    url(r'^detail/(?P<productID>(\d+))/$', views.DetailView.as_view(), name='detail'),
    #url(r'^purchase/(?P<productID>(\d+))/$', views.purchase, name='purchase'),
    url(r'^purchase/(?P<productID>(\d+))/$', views.PurchaseView.as_view(), name='purchase'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^success/(?P<pk>(\d+))/$', views.SuccessView.as_view(), name='success'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

