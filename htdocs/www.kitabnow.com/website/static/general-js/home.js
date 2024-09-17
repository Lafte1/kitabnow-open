function updateCards(books) {
    const currency = " درهم"
    const filteredCards = document.getElementById('filtered-cards');
    const cardElements = filteredCards.querySelectorAll('.card');

    for (let i = 0; i < 3; i++) {
        const book = books[i];
        
        const card = cardElements[i];
        card.href = '/book/' + book.title;
        
        const img = card.querySelector('img');
        const title = card.querySelector('.title');
        const price = card.querySelector('.price');

        // Update the content of the existing card elements with book data
        if (book){
            img.src = '../../static/cms_books/' + book.cover;
            img.alt = book.title;
            title.textContent = book.title;
            price.textContent = book.price + currency;
        }
        else{
            console.log(book)
            img.src = '../../static/images/indisponible.png';
            img.alt = 'indisponible';
            title.textContent = 'غير متوفر حاليا...';
            price.textContent = '';
        }
    }
}


function filterBooks(category_id) {
    fetch('/filter', {
        method: 'POST',
        body: new URLSearchParams({ 'category_id': category_id }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("cat-desc").innerHTML = data.description
        books = data.books

        updateCards(books);
    })

}


const categorySelect = document.getElementById('category');
categorySelect.addEventListener('change', function () {
const selectedCategory_id = categorySelect.value;
filterBooks(selectedCategory_id);
})

const selectedCategory_id = 1
filterBooks(selectedCategory_id);
