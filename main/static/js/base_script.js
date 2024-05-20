// BASE_URL = 'http://localhost:8000/'
BASE_URL = 'http://213.171.7.167/'



function get_text(filename, id){
    fetch(filename)
        .then(response => response.text())
        .then(text => {
            document.getElementById(id).innerHTML = text;
        })
        .catch(error => {
            console.error('Ошибка при загрузке текста:', error);
            document.getElementById(id).innerHTML = 'Ошибка при загрузке текста.'
        });
}


function swipe_menu_response(url){
    url = 'http://127.0.0.1:8000/' + url;
    fetch(url)
        .then(response => {
            if (!response.ok) {
                console.log('errorr: ');
                throw new Error('Сетевая ошибка');
            }
            console.log('response: ' + response);
            return response.json(); // Парсим ответ как JSON
        })
        .then(data => {
            // Обрабатываем полученные данные
            console.log('get: ' + data);
        })
        .catch(error => {
            // Обрабатываем ошибку
            console.error('Произошла ошибка:', error);
        });

    console.log('READY')
}

function generateStartHTML(rating){
    const startRatingDiv = document.createElement('div');
    startRatingDiv.classList.add('star-rating-display');

    startRatingDiv.innerHTML = `
        <span class="star">&#9733;</span>
        <span class="star">&#9733;</span>
        <span class="star">&#9733;</span>
        <span class="star">&#9733;</span>
        <span class="star">&#9733;</span>
    `;

    const stars = startRatingDiv.querySelectorAll('.star');

    stars.forEach((star, index) => {
        if (index < Math.floor(rating)) {
            star.classList.add('filled');
            star.classList.remove('partial');
        } else if (index < Math.ceil(rating)) {
            star.classList.add('partial');
            star.classList.remove('filled');
            const percentage = (rating - Math.floor(rating)) * 100;
            star.style.setProperty('--width', `${percentage}%`);
        } else {
            star.classList.remove('filled', 'partial');
        }
    });

    return startRatingDiv.outerHTML;
}