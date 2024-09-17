function getbooksbyCategory() {
    fetch('/getcategories', {
        method: 'POST'
    })
        .then(response => response.json())
        .then(data => {
            categories = data['categories']
            displaybyCategory(categories)
        })
}


function displaybyCategory(categories) {
    const currency = " درهم"
    const categoriesContainer = document.getElementById("categories-frame");

    // Loop through the categories data and create elements for each category
    categories.forEach(category => {
        const categoryElement = document.createElement("div");
        categoryElement.className = "category";
        
        categoryElement.innerHTML = `
                <div class="category-title">
                    <h1>${category.name}</h1>
                </div>
                <div class="category-quote">
                    <p>${category.description}</p>
                </div>
                <div id="category-books">
                    ${category.books.map(book => `
                        <div class="card">
                            <a class="book-cover" href="/book/${book.title}">
                                <img src="../../static/cms_books/${book.cover}" alt="${book.title} Cover">
                            </a>

                            <div class="book-info">
                                <div class="book-title">
                                    <p>${book.title}</p>
                                </div>
                                <div class="book-price">
                                    <p>${book.price} ${currency}</p>
                                </div>
                            </div>
                            <button class="add-to-cart-button" onclick="addtoCart('${book.id}')">
                            <i class="fa-solid fa-cart-plus add-cart-icon"></i>
                            <span class="add-to-cart-text">أضف الكتاب</span>
                            </button>

                        </div>
                    `).join('')}
                </div>
                <a href="/category/${category.name}" class="category-link">المزيد...</a>
            `;

        categoriesContainer.appendChild(categoryElement);
    });
}


getbooksbyCategory()