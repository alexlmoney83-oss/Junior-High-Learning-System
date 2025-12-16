"""
URL configuration for middle_school_system project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API路由
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/courses/', include('apps.courses.urls')),
    path('api/v1/exercises/', include('apps.exercises.urls')),
    path('api/v1/ai/', include('apps.ai_services.urls')),
]

# 开发环境下提供媒体文件访问
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin站点配置
admin.site.site_header = '初中学习系统管理后台'
admin.site.site_title = '学习系统管理'
admin.site.index_title = '欢迎使用初中学习系统管理后台'

