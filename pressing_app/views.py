from django.http import JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CommandeForm, DetailCommandeForm, SortieForm, ClientForm, VetementForm
from .models import Commande, Sortie , Vetement, Client, DetailCommande
from django.utils import timezone
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Sum, Q
import json

# Create your views here.
def enregistrer_commande(request):
    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            commande = form.save(commit=False)
            commande.etat = 'brouillon'
            commande.save()
            return redirect('ajouter_detail', commande.id)
        
    else:
        form = CommandeForm()
    
    client_form = ClientForm()
        
    return render(request, 'pressing/enregistrer_commande.html', {'form': form, 'client_form' : client_form})


def ajouter_detail(request, pk):
    """ ajouter detail commmande """
    commande = Commande.objects.get(pk = pk)
    
    if request.method == 'POST' :
        form = DetailCommandeForm(request.POST)
        if form.is_valid():
            detail = form.save(commit=False)
            detail.commande = commande
            detail.save()
            
            if 'ajouter_autre' in request.POST :
                return redirect('ajouter_detail', commande.pk)
            else:
                return redirect('recap_details', commande.pk)

    else :
        form = DetailCommandeForm()
    
    return render(request, 'pressing/ajouter_detail.html', {
        'form': form,
        'commande': commande
    })
    
    
def recap_details(request, pk):
    """ recapitulatif des details sassis """
    commande = Commande.objects.get(pk = pk)
    details = commande.details.all()
    
    if request.method == 'POST' :
        if 'confirmer' in request.POST:
            commande.recalculer_total()
            commande.etat = 'confirmee'
            commande.save()
            return redirect('voir_commande', commande.pk)
        
    return render(request, 'pressing/recap_details.html', {
        'commande' : commande,
        'details' : details
    })
    
    
def acceuil(request):
    find = None
    erreur = None
    if request.method == 'POST':
        search = request.POST.get("searchInput")
        
        if not search or not search.isdigit():
            erreur = "Veuillez entrer un identifiant correct "
        else :
            try:
                find = Commande.objects.filter(pk = int(search))    
                if not find.exists():
                    erreur = "Commande non trouvée "
            except Exception:
                erreur = "erreur lors de la recherche. Veuillez réesayer "      
        
    today = timezone.now().date()
    mois = timezone.now().date().month
    commandes_du_mois= Commande.objects.filter(date__month= mois)
    sortie_du_mois= Sortie.objects.filter(date__month = mois)
    comandes_du_jour = Commande.objects.filter(date__date = today)
    sorties_du_jour = Sortie.objects.filter(date= today)
    all_commande = Commande.objects.all()
    all_sorties = Sortie.objects.all()
    
    context = {
        'commandes_du_jour' : comandes_du_jour,
        'sorties_du_jour' : sorties_du_jour,
        'Commandes' : all_commande,
        'all_Sorties' : all_sorties,
        'sortie_du_mois':sortie_du_mois,
        'commande_du_mois' : commandes_du_mois,
        'commande' : find,
        'erreur' : erreur,
        
    }
    return render(request, 'pressing/acceuil.html', context)



def ajouter_sortie(request):
    if request.method == 'POST' :
        form = SortieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('acceuil')
        
    else:
        form = SortieForm()
    return render(request, 'pressing/ajouter_sortie.html', {'form': form})


def modifier_commande(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    
    if request.method == 'POST' :
        form = CommandeForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            commande.recalculer_total()
            return redirect('recap_details', pk = commande.pk)
    
    else:
        form = CommandeForm(instance=commande)
        
    return render(request, 'pressing/modifier_commande.html', {'form': form, 'commande': commande})



def ajax_ajouter_client(request):
    try:
        nom = request.POST.get("nom")
        telephone = request.POST.get("telephone")
        email = request.POST.get("email")
        adresse = request.POST.get("adresse")

        if not nom or not telephone:
            return JsonResponse({
                "success": False,
                "error": "Nom et téléphone obligatoires"
            })

        client = Client.objects.create(
            nom=nom,
            telephone=telephone,
            email=email,
            adresse=adresse
        )

        return JsonResponse({
            "success": True,
            "id": client.id,
            "nom": str(client)
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        })


@csrf_exempt
def ajax_ajouter_vetement(request):
    """ ajouter un vetement pour un client """
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            nom = data.get('nom')
            prix_repassage = data.get('prix_repassage')
            prix_lavage_repassage = data.get('prix_lavage_repassage')

            if not nom or not prix_repassage or not prix_lavage_repassage:
                return JsonResponse({
                    'success': False,
                    'error': 'Tous les champs doivent être remplis'
                })

            vetement = Vetement.objects.create(
                nom=nom,
                prix_repassage=prix_repassage,
                prix_lavage_repassage=prix_lavage_repassage
            )

            return JsonResponse({
                'success': True,
                'id': vetement.id,
                'nom': vetement.nom,
                'prix_repassage': vetement.prix_repassage,
                'prix_lavage_repassage': vetement.prix_lavage_repassage
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    return JsonResponse({'success': False}, status=400)


def creer_client(request):
    """ creer un client qui n'est pas dans la base  """
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_clients')
        
    else:
        form = ClientForm()
    
    return render(request, 'pressing/creer_client.html', {'form' : form})


def creer_vetement(request):
    """ creer un vetement qui n'existe pas dans la base """
    if request.method == 'POST' :
        form = VetementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_vetements')
        
    else :
        form = VetementForm()
        
    return render(request, 'pressing/creer_vetement.html', {'form' : form})


def liste_clients(request):
    find = None
    erreur = None
    if request.method == 'POST':
        search = request.POST.get("searchInput")
        
        if not search :
            erreur = "Veuillez entrer un nom correct "
        else :
            try:
                find = Client.objects.filter(nom__icontains = search)    
                if not find.exists():
                    erreur = "client non trouvé "
            except Exception:
                erreur = "erreur lors de la recherche. Veuillez réesayer" 

    Clients = Client.objects.all()
    return render(request, 'pressing/liste_clients.html', {'clients': Clients, 'client':find, 'erreur':erreur})


def liste_vetements(request):
    find = None
    erreur = None
    if request.method == 'POST':
        search = request.POST.get("searchInput").lower()
        
        if not search :
            erreur = "Veuillez entrer un nom correct "
        else :
            try:
                find = Vetement.objects.filter(nom__icontains = search)    
                if not find.exists():
                    erreur = "vetement non trouvé "
            except Exception:
                erreur = "erreur lors de la recherche. Veuillez réesayer" 
                
    Vetements = Vetement.objects.all()
    return render(request, 'pressing/liste_vetements.html', {'vetements': Vetements, 'vetement': find, 'erreur': erreur})

def supprimer_client(request, pk):
    client = Client.objects.get(pk=pk)
    client.delete()
    clients = Client.objects.all()
    return render(request, 'pressing/liste_clients.html', {'clients': clients})
    
    
def supprimer_vetements(request, pk):
    vetement = Vetement.objects.get(pk = pk)
    vetement.delete()
    vetements = Vetement.objects.all()
    return render(request, 'pressing/liste_vetements.html', {'vetements': vetements})



def modifier_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('liste_clients')
    else:
        form = ClientForm(instance=client)
    return render(request, 'pressing/modifier_client.html', {'form': form, 'client': client})

def modifier_vetement(request, pk):
    vetement = get_object_or_404(Vetement, pk=pk)
    if request.method == 'POST':
        form = VetementForm(request.POST, instance=vetement)
        if form.is_valid():
            form.save()
            return redirect('liste_vetements')
    else:
        form = VetementForm(instance=vetement)
    return render(request, 'pressing/modifier_vetement.html', {'form': form, 'vetement': vetement})



def statistiques(request):
    """
    Vue pour afficher les statistiques du pressing
    """
    # Date actuelle
    aujourd_hui = timezone.now()
    debut_mois = aujourd_hui.replace(day=1)
    debut_annee = aujourd_hui.replace(month=1, day=1)
    
    # ========================================
    # 1. CLIENT LE PLUS FRÉQUENT DU MOIS
    # ========================================
    client_mois = (
        Commande.objects
        .filter(date__gte=debut_mois)
        .values('client__nom', 'client__telephone')
        .annotate(nombre_commandes=Count('id'))
        .order_by('-nombre_commandes')
        .first()
    )
    
    # ========================================
    # 2. CLIENT LE PLUS FRÉQUENT DE L'ANNÉE
    # ========================================
    client_annee = (
        Commande.objects
        .filter(date__gte=debut_annee)
        .values('client__nom', 'client__telephone')
        .annotate(nombre_commandes=Count('id'))
        .order_by('-nombre_commandes')
        .first()
    )
    
    # ========================================
    # 3. TOP 5 CLIENTS DE TOUS LES TEMPS
    # ========================================
    top_clients = (
        Commande.objects
        .values('client__nom', 'client__telephone')
        .annotate(
            nombre_commandes=Count('id'),
            total_depense=Sum('total')
        )
        .order_by('-nombre_commandes')[:5]
    )
    
    # ========================================
    # 4. VÊTEMENTS LES PLUS APPORTÉS (LAVAGE)
    # ========================================
    # Filtrer les détails où option contient "lavage"
    vetements_lavage = (
        DetailCommande.objects
        .filter(Q(option__icontains='lavage'))
        .values('vetement__nom')
        .annotate(
            total_quantite=Sum('quantite')
        )
        .order_by('-total_quantite')[:10]
    )
    
    # ========================================
    # 5. VÊTEMENTS LES PLUS APPORTÉS (REPASSAGE)
    # ========================================
    vetements_repassage = (
        DetailCommande.objects
        .filter(Q(option__icontains='repassage') & ~Q(option__icontains='lavage'))
        .values('vetement__nom')
        .annotate(
            total_quantite=Sum('quantite')
        )
        .order_by('-total_quantite')[:10]
    )
    
    # ========================================
    # 6. RAPPORT ENTRÉES/SORTIES DU MOIS
    # ========================================
    # Entrées (total des commandes du mois)
    entrees_mois = (
        Commande.objects
        .filter(date__gte=debut_mois)
        .aggregate(total=Sum('total'))['total'] or 0
    )
    
    # Sorties du mois
    sorties_mois = (
        Sortie.objects
        .filter(date__gte=debut_mois)
        .aggregate(total=Sum('montant'))['total'] or 0
    )
    
    benefice_mois = entrees_mois - sorties_mois
    
    # ========================================
    # 7. RAPPORT ENTRÉES/SORTIES DE L'ANNÉE
    # ========================================
    entrees_annee = (
        Commande.objects
        .filter(date__gte=debut_annee)
        .aggregate(total=Sum('total'))['total'] or 0
    )
    
    sorties_annee = (
        Sortie.objects
        .filter(date__gte=debut_annee)
        .aggregate(total=Sum('montant'))['total'] or 0
    )
    
    benefice_annee = entrees_annee - sorties_annee
    
    # ========================================
    # 8. ÉVOLUTION MENSUELLE (12 DERNIERS MOIS)
    # ========================================
    evolution_mensuelle = []
    mois_labels = []
    
    for i in range(11, -1, -1):  # 12 derniers mois
        date_debut = (aujourd_hui - timedelta(days=30*i)).replace(day=1)
        if i == 0:
            date_fin = aujourd_hui
        else:
            date_fin = (aujourd_hui - timedelta(days=30*(i-1))).replace(day=1)
        
        # Entrées du mois
        entrees = (
            Commande.objects
            .filter(date__gte=date_debut, date__lt=date_fin)
            .aggregate(total=Sum('total'))['total'] or 0
        )
        
        # Sorties du mois
        sorties = (
            Sortie.objects
            .filter(date__gte=date_debut, date__lt=date_fin)
            .aggregate(total=Sum('montant'))['total'] or 0
        )
        
        evolution_mensuelle.append({
            'mois': date_debut.strftime('%b %Y'),
            'entrees': float(entrees),
            'sorties': float(sorties),
            'benefice': float(entrees - sorties)
        })
        mois_labels.append(date_debut.strftime('%b %Y'))
    
    # ========================================
    # 9. STATISTIQUES GÉNÉRALES
    # ========================================
    total_clients = Client.objects.count()
    total_commandes = Commande.objects.count()
    total_vetements = Vetement.objects.count()
    
    # Commandes par statut
    commandes_en_cours = Commande.objects.filter(status='En cours').count()
    commandes_terminees = Commande.objects.filter(status='Terminé').count()
    commandes_livrees = Commande.objects.filter(status='Livré').count()
    
    # ========================================
    # 10. DONNÉES POUR LES GRAPHIQUES (JSON)
    # ========================================
    # Graphique évolution
    graph_evolution = {
        'labels': mois_labels,
        'entrees': [e['entrees'] for e in evolution_mensuelle],
        'sorties': [e['sorties'] for e in evolution_mensuelle],
        'benefices': [e['benefice'] for e in evolution_mensuelle]
    }
    
    # Graphique top vêtements lavage
    graph_vetements_lavage = {
        'labels': [v['vetement__nom'] for v in vetements_lavage],
        'data': [v['total_quantite'] for v in vetements_lavage]
    }
    
    # Graphique répartition entrées/sorties mois
    graph_entrees_sorties_mois = {
        'labels': ['Entrées', 'Sorties', 'Bénéfice'],
        'data': [float(entrees_mois), float(sorties_mois), float(benefice_mois)]
    }
    
    context = {
        # Clients
        'client_mois': client_mois,
        'client_annee': client_annee,
        'top_clients': top_clients,
        
        # Vêtements
        'vetements_lavage': vetements_lavage,
        'vetements_repassage': vetements_repassage,
        
        # Finances
        'entrees_mois': entrees_mois,
        'sorties_mois': sorties_mois,
        'benefice_mois': benefice_mois,
        'entrees_annee': entrees_annee,
        'sorties_annee': sorties_annee,
        'benefice_annee': benefice_annee,
        
        # Évolution
        'evolution_mensuelle': evolution_mensuelle,
        
        # Statistiques générales
        'total_clients': total_clients,
        'total_commandes': total_commandes,
        'total_vetements': total_vetements,
        'commandes_en_cours': commandes_en_cours,
        'commandes_terminees': commandes_terminees,
        'commandes_livrees': commandes_livrees,
        
        # Données graphiques (JSON)
        'graph_evolution': json.dumps(graph_evolution),
        'graph_vetements_lavage': json.dumps(graph_vetements_lavage),
        'graph_entrees_sorties_mois': json.dumps(graph_entrees_sorties_mois),
    }
    
    return render(request, 'pressing/statistiques.html', context)
