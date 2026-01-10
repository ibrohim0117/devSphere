// Home Page JavaScript

// React to post function
function react(span) {
    const emoji = span.innerText;
    const postId = span.closest('.emojis').dataset.postId;
    const csrftoken = getCookie('csrftoken');
    
    // URL ni o'zgartirish - Django template URL bilan ishlash uchun
    const reactUrlElement = document.querySelector('[data-react-url]');
    let url;
    if (reactUrlElement) {
        url = reactUrlElement.getAttribute('data-react-url').replace('0', postId);
    } else {
        url = `/blog/post/${postId}/react/`;
    }
    
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({emoji: emoji})
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert(data.error || 'Xatolik yuz berdi');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Xatolik yuz berdi');
    });
}
