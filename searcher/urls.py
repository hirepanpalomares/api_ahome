from rest_framework import routers
from .api import SearcherViewSet

#from django.urls import path

#from . import views

app_name = 'searcher'

router = routers.DefaultRouter()
router.register('api/searcher', SearcherViewSet, 'searcher')

urlpatterns = router.urls
#urlpatterns = [

#]