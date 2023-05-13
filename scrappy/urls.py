from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),
    path('blank', views.blank, name='blank'),
    path('desc_scrapper/', views.link_File, name='Link_Or_File'),
    path('links/', views.links, name='links'),
    path('playlist/', views.playlist_files, name='Playlist_data_displayed'),
    path('channel/', views.channel_files, name='channel_data_displayed'),
    path('files/<str:file_type>/<int:file_id>/download/', views.download_file, name='download_file'),
    path('show_scrapped_data/', views.show_scrapped_data, name='show_scrapped_Data'),
    path('show_playlist_data/', views.show_playlist_data, name='show_playlist_data'),
    path('show_channel_data/', views.show_channel_data, name='show_channel_data'),
    path('register/', views.register, name='register'),
    path('register_data/', views.register_data, name='register_data'),
    path('login/', views.login, name='login'),
    # path('files/', views.file_list, name='file_list'),
    # path('files/<int:file_id>/download/', views.download_file, name='download_file'),
    # path('ufiles/', views.file_list, name='Display uploaded files'),
    # path('media/media/playlist/<str:file_name>/', views.download_file, name='download_file'),
    
]
if settings.DEBUG:
    urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)