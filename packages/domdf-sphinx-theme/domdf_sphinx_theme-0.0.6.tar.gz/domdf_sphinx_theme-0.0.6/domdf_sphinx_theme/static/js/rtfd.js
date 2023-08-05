const destination = document.getElementById("rtfd_button_dest");

destination.onload = function(){
    $('#rtfd_button_to_remove').replaceWith($(".injected div.rst-versions div.rst-other-versions"))
};
