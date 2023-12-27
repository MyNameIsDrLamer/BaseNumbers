from django.contrib import admin
from django.urls import path
from phonesapp.views import *
from phones import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('<str:pk>/edit', edit_number),
    path('files-rostelekom/', parser_rostelecom),
    path('files-avantel/', parser_avantel),
    path('reports/', report),
    path('login/', LoginUser.as_view()),
    path('logout/', logout_user),
    path('report/export_excel', export_excel, name='export_excel'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)