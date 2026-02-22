// 🔐 Récupération du token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {

    const btnNouveauVetement = document.getElementById('btnNouveauVetement');
    const formVetement = document.getElementById('formVetement');
    const btnSaveVetement = document.getElementById('btnSaveVetement');

    // Afficher le mini formulaire
    btnNouveauVetement.addEventListener('click', function () {
        formVetement.style.display = 'block';
    });

    // Enregistrer le vêtement via AJAX
    btnSaveVetement.addEventListener('click', function () {

        const nom = document.getElementById('vetement_nom').value.trim();
        const prix_repassage = document.getElementById('prix_repassage').value;
        const prix_lavage_repassage = document.getElementById('prix_lavage_repassage').value;

        if (!nom || !prix_repassage || !prix_lavage_repassage) {
            alert("Tous les champs sont obligatoires");
            return;
        }

        fetch(AJAX_AJOUTER_VETEMENT_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
                nom: nom,
                prix_repassage: prix_repassage,
                prix_lavage_repassage: prix_lavage_repassage
            })
        })
        .then(response => response.json())
        .then(data => {

            if (data.success) {
                const select = document.getElementById("id_vetement");

                const option = document.createElement("option");
                option.value = data.id;
                option.textContent = data.nom;
                option.selected = true;

                select.appendChild(option);

                // reset + cacher
                formVetement.style.display = "none";
                document.getElementById('vetement_nom').value = '';
                document.getElementById('prix_repassage').value = '';
                document.getElementById('prix_lavage_repassage').value = '';
            } else {
                alert(data.error);
            }
        })
        .catch(error => {
            console.error("Erreur AJAX :", error);
        });
    });

});
