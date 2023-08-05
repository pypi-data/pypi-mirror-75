const destination = $('#rtfd_button_dest');
const to_remove = $('#rtfd_button_to_remove');
const source = $(".injected div.rst-versions div.rst-other-versions");

destination.onload = function(){
    to_remove.replaceWith(source)
};
