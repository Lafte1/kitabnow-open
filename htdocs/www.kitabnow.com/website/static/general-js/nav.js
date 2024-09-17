function responsive_menu(){
    let menu_btn = document.querySelector('.menu-button');
    let menu = document.querySelector('.menu');
    let search_menu = document.querySelector('.search-menu')
    
    menu_btn.addEventListener('click', () => {
        toggle_menu(menu)
        toggle_menu(search_menu)
    })
    toggle_menu(menu)
}

function toggle_menu(element){
    if (element.style.display == 'none'){
        element.style.display = 'block'
        document.body.style.overflowY = 'hidden';
    }
    else{
        element.style.display = 'none'
        document.body.style.overflowY = 'visible';
    }
}


responsive_menu();

cart_number = document.getElementById("cart-number")
if (localStorage.cartnumber){
    cart_number.innerHTML = localStorage.cartnumber
}
else{
    cart_number.innerHTML = 0
}
