"""
URL configuration for leaderboard_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings  # Correct import for settings
from leaderboard import views

urlpatterns = [
    path('', views.leaderboard_view, name='leaderboard'),
    path('admin/', admin.site.urls),
    path('create_player/', views.create_player_view, name='create_player'),
    path('new_game/', views.new_game_view, name='new_game'),
    path('complete_game/<int:game_id>/', views.complete_game_view, name='complete_game'),
    path('game_history/', views.game_history_view, name='game_history'),
    path('set-token/', views.set_auth_token, name='set_auth_token'),
    path('player/<int:player_id>/history/', views.player_history_view, name='player_history'),
    path('edit_player/', views.edit_player, name='edit_player'),  # Add this line
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

