function showNavbar() {
  var nav = document.querySelector(".navbar-items");
  var icon = document.querySelector(".navbar-icon");

  if (nav && icon) {
    nav.classList.toggle("responsive");
    icon.classList.toggle("responsive");
  }
}
