from django import forms
from .models import Commande, DetailCommande, Sortie, Client, Vetement

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['client', 'status', 'delai', 'remise', 'montant_paye']
        wigets = {
            'client': forms.Select(attrs={'id': 'id_lint'}),
            'status' : 'Status de la commande',
            'delai' : 'Délai de livraison ',
            'remise': forms.NumberInput(attrs={'min': 0}),
            'montant_paye' : forms.NumberInput(attrs={'min': 0}),
        }
    

class DetailCommandeForm(forms.ModelForm):
    class Meta:
        model = DetailCommande
        fields = ['vetement', 'option', 'quantite']
        vetement = forms.ModelChoiceField(queryset=Vetement.objects.all())
        labels = {
            'option': 'Type de service',
            'quantite': 'Quantité',
        }
        
        
class SortieForm(forms.ModelForm):
    class Meta:
        model = Sortie
        fields = ['date', 'description', 'montant']
        widgets ={
            'date' : forms.DateInput(attrs={'type': 'date'}),
        }
        
        
        
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'telephone', 'email', 'adresse']
        labels = {
            'nom': 'Nom du client',
            'telephone': 'Téléphone',
            'email': 'Email',
            'adresse': 'Adresse',
        }


class VetementForm(forms.ModelForm):
    class Meta:
        model = Vetement
        fields = ['nom', 'prix_repassage', 'prix_lavage_repassage']