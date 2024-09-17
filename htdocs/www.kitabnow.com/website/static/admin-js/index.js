function deleteNote(noteId){
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId })
    }).then((_res) => {
        window.location.href = "/dashboard";
    })
}



function deleteBook(bookId){
    fetch('/delete-book', {
        method: 'POST',
        body: JSON.stringify({ bookId: bookId })
    }).then((_res) => {
        window.location.href = "/cms";
    })
}

function deleteAuthor(authorId){
    fetch('/delete-author', {
        method: 'POST',
        body: JSON.stringify({ authorId: authorId })
    }).then((_res) => {
        window.location.href = "/cms";
    })
}


function deleteCategory(categoryId){
    fetch('/delete-category', {
        method: 'POST',
        body: JSON.stringify({ categoryId: categoryId })
    }).then((_res) => {
        window.location.href = "/cms";
    })
}

function deleteLanguage(languageId){
    fetch('/delete-language', {
        method: 'POST',
        body: JSON.stringify({ languageId: languageId })
    }).then((_res) => {
        window.location.href = "/cms";
    })
}