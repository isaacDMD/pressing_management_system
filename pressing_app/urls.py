from django.urls import path
from . import views

urlpatterns = [
    path('', views.acceuil, name='acceuil'),
    path('enregistrer/', views.enregistrer_commande, name='enregistrer_commande'),
    path('ajouter_detail/<int:pk>/', views.ajouter_detail, name='ajouter_detail'),
    path('recap_details/<int:pk>/', views.recap_details, name='recap_details'),
    path('sortie/ajouter/', views.ajouter_sortie, name='ajouter_sortie'),
    path('commande/<int:pk>/modifier/', views.modifier_commande, name='modifier_commande'),
    path("ajax/ajouter-client/", views.ajax_ajouter_client, name="ajax_ajouter_client"),
    path('ajax/ajouter-vetement/', views.ajax_ajouter_vetement, name='ajax_ajouter_vetement'),
    path('client/creer/', views.creer_client, name='creer_client'),
    path('vetement/creer/', views.creer_vetement, name='creer_vetement'),
    path('clients/', views.liste_clients, name= 'liste_clients'),
    path('vetements/', views.liste_vetements, name='liste_vetements'),
    path('supprimer_client/<int:pk>', views.supprimer_client, name='supprimer_client'),
    path('supprimer_vetements/<int:pk>', views.supprimer_vetements, name='supprimer_vetement'),
    path('modifier-client/<int:pk>/', views.modifier_client, name='modifier_client'),
    path('modifier-vetement/<int:pk>/', views.modifier_vetement, name='modifier_vetement'),
    path('statistiques/', views.statistiques, name='statistiques'),
]
