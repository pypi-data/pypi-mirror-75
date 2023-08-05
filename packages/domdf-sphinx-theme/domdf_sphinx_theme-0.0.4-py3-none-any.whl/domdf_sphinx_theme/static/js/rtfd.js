const destination = document.getElementById("rtfd_button_dest");
const to_remove = document.getElementById("rtfd_button_to_remove");
const source = document.querySelector(".injected div.rst-versions div.rst-other-versions");

destination.onload = function(){
    to_remove.replaceWith(source)
};
