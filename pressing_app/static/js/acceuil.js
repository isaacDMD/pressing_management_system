document .addEventListener("DOMContentLoaded", function () {
    const select = document.getElementById("choix");
    const stock =localStorage.getItem("stock");
    if (stock) {
        select.value = stock;
    }

    const tableJour = document.getElementById("table-jour");
    const tableMois = document.getElementById("table-mois");
    const tableTout = document.getElementById("table-tout");

    select.addEventListener("change", function () {
        tableJour.style.display = "none";
        tableMois.style.display = "none";
        tableTout.style.display = "none";
        
        let v = select.value;
        localStorage.setItem("stock" , v);
        if (this.value === "A") {
            tableJour.style.display = "table";
        } 
        else if (this.value === "M") {
            tableMois.style.display = "table";
        } 
        else if (this.value === "T") {
            tableTout.style.display = "table";
        }
    });
});
