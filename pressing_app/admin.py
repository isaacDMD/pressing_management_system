from django.contrib import admin
from .models import Vetement, Client, Commande, DetailCommande, Sortie

# Register your models here.

admin.site.register([Vetement,
                     Client,
                     Sortie
                     ])


class DetailCommandeInline(admin.TabularInline):
    model = DetailCommande
    extra = 1
    

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    inlines = [DetailCommandeInline]
    list_display = ('id', 'client', 'delai', 'status', 'total', 'date')
    readonly_fields = ('total',)