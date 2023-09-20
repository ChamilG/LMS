/* handle clicking of heart button */
const heartbtn = document.getElementById('heart-btn');
let clicked = heartbtn.getAttribute('rated') === 'True';
heartbtn.addEventListener('click', function() {
    const bookId = this.getAttribute('data-book-id');
    if (this.classList.contains('filled-btn')) {
        this.classList.remove('filled-btn');
        this.classList.add('follow-btn');
    } else {
        this.classList.remove('follow-btn');
        this.classList.add('filled-btn');
    }
    if(!clicked){
        clicked = true;  
        fetch(`/user_ratings_create/${bookId}/`)
        .then(response => response.json())
        .then(data => {
            console.log(data.message); // Display the response message
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    else{
        clicked= false;
        fetch(`/user_ratings_delete/${bookId}/`)
        .then(response => response.json())
        .then(data => {
            console.log(data.message); // Display the response message
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});

const readbtn = document.getElementById('read-btn');

readbtn.addEventListener('click', function() {
    const bookId = this.getAttribute('data-book-id');
    console.log("clicked")
    fetch(`/increase_no_of_views/${bookId}/`)
        .then(response => response.json())
        .then(data => {
            console.log(data.message); // Display the response message
        })
        .catch(error => {
            console.error('Error:', error);
        });
})