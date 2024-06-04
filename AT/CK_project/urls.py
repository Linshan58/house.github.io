from django.contrib import admin
from django.urls import path, include
from myapp import views  # 修改这里，确保正确导入了视图模块
from myapp.views import product_list,all_favorites,member_favorites
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),    # 自己的應用程式網址
    path('login/', views.login_view, name='login'),  # 修改这里，使用正确的视图函数
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),  # 修改这里，使用正确的视图函数
     path('products/', product_list, name='product_list'),
     path('all_favorites/',all_favorites,name='all_favorites'),
     path('member_favorites/',member_favorites,name='member_favorites')
]

