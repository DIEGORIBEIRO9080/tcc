function toggleDropdown(id) {
    const dropdown = document.getElementById(id);
    dropdown.classList.toggle("active");
}

/* Fechar dropdown clicando fora */
document.addEventListener("click", function(event) {
    const dropdowns = document.querySelectorAll(".dropdown");

    dropdowns.forEach(drop => {
        if (!drop.contains(event.target)) {
            drop.classList.remove("active");
        }
    });
});
