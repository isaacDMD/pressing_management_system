from django.db import models, transaction
from django.utils import timezone


# Create your models here.

class Vetement(models.Model):
    NOM_CHOICES = [
        ('chemise', 'Chemises'),
        ('pantalon', 'Pantalons'),
        ('robe', 'Robes'),
        ('jupe', 'Jupes'),
        ('tshirt', 'T-shirts'),
        ('pull', 'Pulls'),
        ('veste', 'Vestes'),
        ('manteau', 'Manteaux'),
        ('short', 'Shorts'),
        ('corsage', 'Corsages'),
        ('drap', 'Draps'),
        ('costume', 'Costumes'),
        ('cravate', 'Cravates'),
        ('autre', 'Autres')
    ]     
    nom = models.CharField(max_length=50)
    prix_lavage_repassage = models.DecimalField(max_digits=6, decimal_places=2)
    prix_repassage = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return self.nom
    

class Client(models.Model):
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    email = models.EmailField()
    adresse = models.TextField()
    
    def __str__(self):
        return self.nom
    

class Commande(models.Model):
    DELAI_CHOICES = [
        ('normal', 'Normal'),
        ('express', 'Express'),
    ]
    
    STATUS_CHOICES = [
        ('paye_livre', 'Payé/Livré'),
        ('paye_non_livre', 'Payé/Non Livré'),
        ('non_paye_non_livre', 'Non Payé/Non livre')
    ]
    
    etat = models.CharField(
    max_length=20,
    choices=[('brouillon','Brouillon'), ('confirmee','Confirmée')],
    default='brouillon'
)

    client = models.ForeignKey(Client , on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=60, default='non_paye_non_livre')
    delai = models.CharField(choices=DELAI_CHOICES, max_length=60, default='normal')
    date = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    remise = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    montant_paye = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    
    def recalculer_total(self):
        total_brut = sum(detail.montant for detail in self.details.all())
        self.total = max(total_brut - self.remise, 0)
        self.save(update_fields=['total'])
    
    def __str__(self):
        return f"Commande {self.id}"
    
    
    @property
    def reste_a_payer(self):
        return max(self.total - self.remise - self.montant_paye, 0)
    
    @property
    def est_solde(self):
        return self.reste_a_payer == 0
    
    
class DetailCommande(models.Model):
    
    OPTIONS = [
        ('lavage_repassage' , 'Lavage et Repassage'),
        ('repassage_seul', 'Repassage seul')
    ]

    option = models.CharField(choices=OPTIONS, max_length=60)
    commande = models.ForeignKey(Commande, related_name='details', on_delete=models.CASCADE)
    vetement = models.ForeignKey(Vetement, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    montant = models.DecimalField(max_digits=8, decimal_places=2 , default=0)
    
    def save(self, *args, **kwargs):
        if self.option == 'lavage_repassage':
            prix = self.vetement.prix_lavage_repassage
        else:
            prix = self.vetement.prix_repassage
        
        if self.commande.delai == 'express' :
            prix += prix*7/10
        
        ancien_montant = None
        if self.pk :
            ancien_montant = DetailCommande.objects.get(pk=self.pk).montant
        
        self.montant = prix*self.quantite
        with transaction.atomic():
            super().save(*args, **kwargs)
            if ancien_montant != self.montant:
                self.commande.recalculer_total()
        
        
    def delete(self, *args, **kwargs):
        commande = self.commande
        with transaction.atomic():
            super().delete(*args, **kwargs)
            commande.recalculer_total()
    

class Sortie(models.Model) :
    date = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length= 300)
    montant = models.DecimalField(max_digits=8, decimal_places=2, default=0)
     
    def __str__(self):
        return f"{self.description} pour un montant de {self.montant}"
    
