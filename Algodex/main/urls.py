from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('page/<int:id>', views.algorithm_page, name="page"),
    path('post/', views.create_page, name="create"),
    path('practice/<int:id>', views.practice_page, name="practice"),

    path('logout/', views.logout_page, name="logout"),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),

    path('voting/<str:status>/<int:id>', views.voting, name="voting"),

    path('solve/', views.save_solve, name="save-solve"),

    path('profile/<str:id>', views.profile_page, name="profile"),
]