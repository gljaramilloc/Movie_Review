from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from movie import views as movieViews 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', movieViews.home, name='home'),
    path('about/', movieViews.about, name='about'),
    path('statistics/', movieViews.statistics_view, name='statistics'),
    path('signup/', movieViews.signup, name='signup'),
    path('news/', include('news.urls')),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)


