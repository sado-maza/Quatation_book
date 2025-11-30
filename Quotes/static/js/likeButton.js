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

// --- ФУНКЦИЯ ОБНОВЛЕНИЯ ИКОНКИ ---
function updateIcons(quoteId, action, data) {

    // data.state = "like" | "dislike" | "none"
    // Предполагается, что сервер возвращает текущее состояние пользователя
    // Если нужно — подгоню под твой ответ

    const likeImg = document.getElementById(`like-img-${quoteId}`);
    const dislikeImg = document.getElementById(`dislike-img-${quoteId}`);

    if (data.state === "like") {
        likeImg.src = "/static/img/likeActive.png";
        dislikeImg.src = "/static/img/dislike.png";
    }
    else if (data.state === "dislike") {
        likeImg.src = "/static/img/like.png";
        dislikeImg.src = "/static/img/dislikeActive.png";
    }
    else {
        // ничего не активно
        likeImg.src = "/static/img/like.png";
        dislikeImg.src = "/static/img/dislike.png";
    }
}


// --- ОСНОВНАЯ ФУНКЦИЯ toggle ---
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

        document.getElementById(`likes-${quoteId}`).textContent = data.likes;
        document.getElementById(`dislikes-${quoteId}`).textContent = data.dislikes;

        // Обновить иконки
        updateIcons(quoteId, action, data);

    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}
