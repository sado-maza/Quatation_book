// Получаем CSRF токен из cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Функция toggle лайка/дизлайка
window.toggleVote = function(quoteId, action) {
    fetch(`/quote/${quoteId}/${action}/toggle/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Accept': 'application/json'
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Ошибка запроса: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        // Обновляем счетчики на странице
        document.getElementById(`likes-${quoteId}`).textContent = data.likes;
        document.getElementById(`dislikes-${quoteId}`).textContent = data.dislikes;
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}
