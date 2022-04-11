from django.conf.urls import include, url
from lists import views as list_views
from lists import urls as list_urls

urlpatterns = [
    url(r'^$',
        list_views.home_page, name='home'),
    url(r'^lists/', include(list_urls)),
]
# включение include может быть частью регулярного выражения в URL
# как префикс, который будет применяться ко всем включенным URL-адресам
