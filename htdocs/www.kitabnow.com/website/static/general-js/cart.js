
function getCartBooks(booksIds) {
    fetch('/cartbooks', {
        "method": "POST",
        "headers": { "Content-Type": "application/json" },
        "body": JSON.stringify(booksIds),
    })
        .then(response => response.json())
        .then(data => {
            cartbooks = data['cartbooks']
            displayCartBooks(cartbooks)
        })
}

function displayCartBooks(cartbooks) {
    const currency = " درهم"
    const cartContainer = document.getElementById("cart-container");
    // Loop through the cart books and create elements for each book
    cartbooks.forEach(cartbook => {
        const bookElement = document.createElement("div");
        bookElement.className = "cart-book";
        bookElement.innerHTML = `

        <div class="cart-book-block" style="width:auto;">
            <div class="cart-book-content">
                <button class="cart-book-remove">
                    <img src="../../static/icons/remove-icon.svg" alt="${cartbook.title} remove">
                </button>
            </div>
        </div>
    
        <div class="cart-book-block">
            <div class="cart-book-content">
                <div class="cart-book-cover">
                    <img src="../../static/cms_books/${cartbook.cover}" alt="${cartbook.title} Cover">
                </div>
            </div>
        </div>

        <div class="cart-book-block">
            <div class="cart-book-header">العنوان</div>
            <div class="cart-book-content">${cartbook.title}</div>
        </div>

        <div class="cart-book-block">
            <div class="cart-book-header">السعر</div>
            <div class="cart-book-content">${cartbook.price} ${currency}</div>
        </div>

        <div class="cart-book-block">
            <div class="cart-book-header">الكمية</div>
            <div class="cart-book-content">
                <div class="cart-book-quantity">
                    <button class="qte-element cart-book-plus">+</button>
                    <div class="qte-element qte">${cartbook.quantity}</div>
                    <button class="qte-element cart-book-minus">-</button>
                </div>
            </div>
        </div>

        <div class="cart-book-block">
            <div class="cart-book-header" style="font-size: large;">المجموع</div>
            <div class="cart-book-content cart-book-total">${cartbook.price * cartbook.quantity}</div>
        </div>

        `;

        // Remove Button onclick handler
        const removeButton = bookElement.querySelector(".cart-book-remove");
        removeButton.addEventListener("click", function () {
            removeCartBook(cartbook.id, bookElement);
        });
        // Plus Button onclick handler
        const plusButton = bookElement.querySelector(".cart-book-plus");
        plusButton.addEventListener("click", function () {
            plusCartBook(cartbook, bookElement);
        });
        // Minus Button onclick handler
        const minusButton = bookElement.querySelector(".cart-book-minus");
        minusButton.addEventListener("click", function () {
            minusCartBook(cartbook, bookElement);
        });

        cartContainer.appendChild(bookElement);

        //Checkout button handler
        const checkoutButton = document.getElementById("checkout-btn")
        checkoutButton.addEventListener("click", function () {
            checkoutform();
        });
    });

    updateCartTotal();
}

/*
function addCartBooksLanguages(bookElement,languages){
        // Get a reference to the select element for language
        const languageSelect = bookElement.querySelector('select');
        // Remove the default placeholder option
        languageSelect.innerHTML = '';

        // Add the placeholder option
        const placeholderOption = document.createElement('option');
        placeholderOption.value = 'default';
        placeholderOption.textContent = 'Select Language';
        languageSelect.appendChild(placeholderOption);
        // Add the languages options
        for (const language of languages) {
            const languageOption = document.createElement('option');
            languageOption.value = language.id;
            languageOption.textContent = language.name;
            languageSelect.appendChild(languageOption);
        }
}
*/

function removeCartBook(cartbookId, bookElement) {
    cartbooksIds = JSON.parse(localStorage.cart)
    if (cartbooksIds[cartbookId]) {
        // Delete book
        quantity = cartbooksIds[cartbookId]
        delete cartbooksIds[cartbookId]
        localStorage.cart = JSON.stringify(cartbooksIds)

        // Update cart number
        cartbookQte = bookElement.querySelector(".qte");
        localStorage.cartnumber = Number(localStorage.cartnumber) - quantity
        cart_number = document.getElementById("cart-number")
        cart_number.innerHTML = localStorage.cartnumber

        // Update html
        bookElement.remove()

        // Update html Cart total
        updateCartTotal();
    }
}

function plusCartBook(cartbook, bookElement) {
    cartbooksIds = JSON.parse(localStorage.cart)
    if (cartbooksIds[cartbook.id]) {
        // Update quantity
        cartbooksIds[cartbook.id] += 1
        localStorage.cart = JSON.stringify(cartbooksIds)
        new_quantity = cartbooksIds[cartbook.id]

        // Update cart number
        localStorage.cartnumber = Number(localStorage.cartnumber) + 1
        cart_number = document.getElementById("cart-number")
        cart_number.innerHTML = localStorage.cartnumber

        // Update html Cart Book quantity
        cartbookQte = bookElement.querySelector(".qte");
        cartbookQte.innerHTML = new_quantity

        // Update html Cart Book total
        cartbookTotal = bookElement.querySelector(".cart-book-total");
        cartbookTotal.innerHTML = (cartbook.price * new_quantity)

        // Update html Cart total
        updateCartTotal();
    }
}

function minusCartBook(cartbook, bookElement) {
    cartbooksIds = JSON.parse(localStorage.cart)
    if (cartbooksIds[cartbook.id]) {
        // Ignore if qte=1
        if (cartbooksIds[cartbook.id] == 1) {
            pass
        }
        else {
            // Update quantity
            cartbooksIds[cartbook.id] -= 1
            localStorage.cart = JSON.stringify(cartbooksIds)
            new_quantity = cartbooksIds[cartbook.id]

            // Update cart number
            localStorage.cartnumber = Number(localStorage.cartnumber) - 1
            cart_number = document.getElementById("cart-number")
            cart_number.innerHTML = localStorage.cartnumber

            // Update html book quantity
            cartbookQte = bookElement.querySelector(".qte");
            cartbookQte.innerHTML = cartbooksIds[cartbook.id]

            // Update Cart Book total
            cartbookTotal = bookElement.querySelector(".cart-book-total");
            cartbookTotal.innerHTML = (cartbook.price * new_quantity);

            // Update html Cart total
            updateCartTotal();
        }
    }
}

function updateCartTotal() {
    cartbookstotals = document.getElementsByClassName("cart-book-total")
    total = 0
    for (cartbooktotal of cartbookstotals) {
        total = total + Number(cartbooktotal.innerHTML)
    }

    const carttotal = document.getElementById("order-total-value");
    const cartsubtotal = document.getElementById("order-subtotal-value");
    carttotal.innerHTML = total
    cartsubtotal.innerHTML = total
}


booksIds = localStorage.cart
getCartBooks(booksIds)
