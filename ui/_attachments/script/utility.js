function setActiveLink(element){
    'use strict';
    $('#' + element)
    .parent()
        .siblings()
            .removeClass('active')
        .end()
    .addClass('active');
}

function hideMenu(){
    $('nav').hide();
}

function showMenu(){
    $('nav').show();
}
