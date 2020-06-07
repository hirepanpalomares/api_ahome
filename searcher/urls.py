from django.urls import path
from rest_framework import routers
from . import views


app_name = 'searcher'

router = routers.DefaultRouter()

# view set para obtener el topten
router.register('topten', views.TopTenViewSet, basename="property")


urlpatterns = router.urls


# normal_view para hacer que la base de datos se alimente con los de excel, 
# por ejemplo la primera vez que se construye la base de datos o para 
# checar que se haya añadido alguna otra propiedad
urlpatterns.append(path('load', views.load_data_base, name='initial_load')) 


# view set para  los datos del buscador (acepta un JSON)
urlpatterns.append(path('<str:id_>/specific', views.resultsSearcher_single, name='results_single'))


# view set para obtener las opciones del footer
urlpatterns.append(path('<str:where>/<str:operationType>/<str:propertyType>/<int:check>/<int:check_bath>/<int:price>/results', views.resultsSearcher, name='results'))

# view set para obtener las imagenes
urlpatterns.append(path('<str:id_ahome>/images', views.imagesSearcher, name='images'))



