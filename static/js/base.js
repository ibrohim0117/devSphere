// Base JavaScript - Umumiy funksiyalar barcha sahifalar uchun

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Dropdown hover muammosini hal qilish
document.addEventListener('DOMContentLoaded', function() {
    const profileDropdown = document.querySelector('.profile-dropdown');
    const dropdownContent = document.querySelector('.dropdown-content');
    
    if (profileDropdown && dropdownContent) {
        let timeout;
        
        profileDropdown.addEventListener('mouseenter', function() {
            clearTimeout(timeout);
            dropdownContent.style.display = 'block';
        });
        
        profileDropdown.addEventListener('mouseleave', function() {
            timeout = setTimeout(function() {
                dropdownContent.style.display = 'none';
            }, 200); // 200ms kechikish
        });
        
        dropdownContent.addEventListener('mouseenter', function() {
            clearTimeout(timeout);
            dropdownContent.style.display = 'block';
        });
        
        dropdownContent.addEventListener('mouseleave', function() {
            timeout = setTimeout(function() {
                dropdownContent.style.display = 'none';
            }, 200);
        });
    }
});
