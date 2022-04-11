from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name="Detector"
urlpatterns = [
path('',views.home,name='home'),
path('diabetes/',views.diabetes,name='diabetes'),
path('heart/',views.heart,name='heart'),
path('kidney/',views.kidney,name='kidney'),
path('liver/',views.liver,name='liver'),
path('covid/',views.covid,name='covid'),
path('api/',views.apiView,name='api'),
path('api/diabetes',views.diabetesApi,name='diabetesApi'),
path('api/liver_disease',views.liverApi,name='liverApi'),
path('api/kidney_disease',views.kidneyApi,name='kidneyApi'),
path('api/heart_disease',views.heartApi,name='heartApi'),
path('api/covid',views.covidApi,name='covidApi'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)