
function filterBooks(category_id) {
    fetch('/cms', {
        method: 'POST',
        body: new URLSearchParams({ 'selected_category_id': category_id }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    }).then((_res) => { 
        window.location.href = "/cms/"+category_id;
    })
}



const categorySelect = document.getElementById('filter');
categorySelect.addEventListener('change', function () {
const selectedCategory_id = categorySelect.value;
filterBooks(selectedCategory_id);
})


