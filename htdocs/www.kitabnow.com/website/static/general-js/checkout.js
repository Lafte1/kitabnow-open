/* Hidden form value of order books */
document.getElementById('orderbooks').value = localStorage.cart;

/* Refresh cart after order submit */
function refreshCart(){
    localStorage.removeItem("cart");
    localStorage.removeItem("cartnumber");
}
