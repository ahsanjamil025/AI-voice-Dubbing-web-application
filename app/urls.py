from django.urls import path
from app import views
from OWL import settings
from django.conf.urls.static import static


urlpatterns = [
  path('', views.home,name='home'),
  path('about', views.about,name='about'),
  path('contact', views.contact,name='contact'),
  path('service', views.service,name='service'),
  path('serviceOne', views.serviceOne,name='serviceOne'),
  path('serviceTwo', views.serviceTwo,name='serviceTwo'),
  path('serviceThree', views.serviceThree,name='serviceThree'),
  path('login', views.logins,name='login'),
  path('signUp', views.signUp,name='signUp'),
  path('logout', views.Logouts,name='logout'),
]
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)