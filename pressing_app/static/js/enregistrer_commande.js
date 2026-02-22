// 🔐 CSRF
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

document.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById("clientModal");
    const openBtn = document.getElementById("openModal");
    const closeBtn = document.getElementById("closeModal");
    const clientForm = document.getElementById("client-form");
    const messageDiv = document.getElementById("client-message");

    // Ouvrir modal
    openBtn.addEventListener("click", function () {
        modal.style.display = "block";
    });

    // Fermer modal
    closeBtn.addEventListener("click", function () {
        modal.style.display = "none";
        messageDiv.innerHTML = "";
    });

    // SUBMIT AJAX
    clientForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(clientForm);

        fetch(AJAX_AJOUTER_CLIENT_URL, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: formData
        })
        .then(res => res.json())
        .then(data => {

            if (data.success) {
                const select = document.getElementById("id_client");

                const option = document.createElement("option");
                option.value = data.id;
                option.textContent = data.nom;
                option.selected = true;

                select.appendChild(option);

                clientForm.reset();
                modal.style.display = "none";
            } else {
                messageDiv.innerHTML = `<p style="color:red;">${data.error}</p>`;
            }
        })
        .catch(err => {
            console.error("Erreur AJAX client :", err);
        });
    });

});
