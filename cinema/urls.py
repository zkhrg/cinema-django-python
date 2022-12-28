from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from cms.views import start_page, movies_page, halls_page, order_page, login_page, profile_page, register_page, \
                      logout_user, movie_page, seance_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', start_page, name="start"),

    path('movies/', movies_page, name="movies"),
    path('movies/<str:movie_slug>/', movie_page, name="movie"),
    path('movies/<str:movie_slug>/<str:seance_slug>/', seance_page, name='seance'),

    path('halls/', halls_page, name="halls"),
    path('buy/', order_page, name="buy"),
    path('profile/', profile_page, name="profile"),
    path('login/', login_page, name="login"),
    path('register/', register_page, name="register"),
    path('logout/', logout_user, name="logout"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
