from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage),
    path('login',views.login),
    path('signup',views.signup),
    path('about',views.about),
    path('logout',views.logout),
    path('viewsSection/<id>', views.viewsSection),
    path('showPets/<id>',views.showPets),
    path('readMore/<id>',views.readMore),
    path('addTocart',views.addTocart),
    path('showAllCart',views.showAllCart),
    path('remove',views.removeItem),
    path('MakePayment',views.MakePayment),
    path('contact',views.contact),
    path('gallary',views.gallary),

]