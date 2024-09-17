
function addtoCart(bookId) {
    if (localStorage.cart){
        cart = JSON.parse(localStorage.cart)
        if ( !(cart[bookId]) ){
            cart[bookId] = 1
            localStorage.cartnumber = Number(localStorage.cartnumber) + 1
        }
        else{
            // pass
        }
    }
    else{
        cart = {}
        cart[bookId] = 1
        localStorage.setItem("cart", JSON.stringify(cart));
        localStorage.setItem("cartnumber", Object.keys(cart).length);
    }

    localStorage.cart = JSON.stringify(cart)

    cart_number = document.getElementById("cart-number")
    cart_number.innerHTML = localStorage.cartnumber
    
    added_message = document.getElementById("added_message")
    if (added_message.style.display != 'flex'){
        added_message.style.display = 'flex'
        document.body.style.overflowY = 'hidden';
    }
}

function closePopup(){
    added_message = document.getElementById("added_message")
    added_message.style.display = 'none'
    document.body.style.overflowY = 'visible';
}