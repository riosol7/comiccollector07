from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('about/', views.about, name='about'),
    # comic routes
    path('comics/', views.comics_index, name='index'),
    path('comics/<int:comic_id>/', views.comics_detail, name='detail'),
    path('comics/create/', views.ComicCreate.as_view(), name='comics_create'),
    path('comics/<int:pk>/update/', views.ComicUpdate.as_view(), name='comics_update'),
    path('comics/<int:pk>/delete/', views.ComicDelete.as_view(), name='comics_delete'),
    # add log
    path('comics/<int:comic_id>/add_log/', views.add_log, name='add_log'),
    #add photos
    path('comics/<int:comic_id>/add_photo/', views.add_photo, name='add_photo'),
    #associate funko with comic
    path('comics/<int:comic_id>/assoc_funko/<int:funko_id>/', views.assoc_funko, name = 'assoc_funko'),
    # add funko
    path('funkos/', views.FunkoList.as_view(), name = 'funkos_list'),
    path('funkos/create/', views.FunkoCreate.as_view(), name = 'funkos_create'),
    path('funkos/<int:pk>/', views.FunkoDetail.as_view(), name = 'funkos_detail'),
    path('funkos/<int:pk>/update/', views.FunkoUpdate.as_view(), name = 'funkos_update'),
    path('funkos/<int:pk>/delete/', views.FunkoDelete.as_view(), name = 'funkos_delete'),
    # users
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
