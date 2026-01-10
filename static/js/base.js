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

// Dropdown hover va touch muammosini hal qilish (Desktop va Mobile uchun)
document.addEventListener('DOMContentLoaded', function() {
    const profileDropdown = document.querySelector('.profile-dropdown');
    const dropdownContent = document.querySelector('.dropdown-content');
    
    if (profileDropdown && dropdownContent) {
        let timeout;
        let isOpen = false;
        
        // Touch yoki click event'ni aniqlash
        const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
        
        // Outside click handler (Desktop)
        function closeOnOutsideClick(event) {
            if (!profileDropdown.contains(event.target) && !dropdownContent.contains(event.target)) {
                isOpen = false;
                dropdownContent.style.display = 'none';
                document.removeEventListener('click', closeOnOutsideClick);
            }
        }
        
        // Outside touch handler (Mobile)
        function closeOnOutsideTouch(event) {
            if (isOpen && !profileDropdown.contains(event.target) && !dropdownContent.contains(event.target)) {
                isOpen = false;
                dropdownContent.style.display = 'none';
                document.removeEventListener('touchstart', closeOnOutsideTouch);
                document.removeEventListener('click', closeOnOutsideClick);
            }
        }
        
        // Toggle funksiyasi (mobil uchun)
        function toggleDropdown() {
            isOpen = !isOpen;
            if (isOpen) {
                dropdownContent.style.display = 'block';
                // Click outside to close (Desktop)
                setTimeout(function() {
                    document.addEventListener('click', closeOnOutsideClick);
                }, 10);
                // Touch outside to close (Mobile)
                if (isTouchDevice) {
                    setTimeout(function() {
                        document.addEventListener('touchstart', closeOnOutsideTouch, { passive: true });
                    }, 50);
                }
            } else {
                dropdownContent.style.display = 'none';
                document.removeEventListener('click', closeOnOutsideClick);
                document.removeEventListener('touchstart', closeOnOutsideTouch);
            }
        }
        
        // Mobil qurilmalar uchun click/touch event
        if (isTouchDevice) {
            // Click event (barcha mobil browser'lar uchun asosiy)
            profileDropdown.addEventListener('click', function(e) {
                e.stopPropagation();
                toggleDropdown();
            });
            
            // Dropdown ichidagi link'larni bosilganda dropdown yopilishi uchun
            const dropdownLinks = dropdownContent.querySelectorAll('a');
            dropdownLinks.forEach(function(link) {
                link.addEventListener('click', function(e) {
                    // Link ishlagach, dropdown yopiladi
                    setTimeout(function() {
                        isOpen = false;
                        dropdownContent.style.display = 'none';
                        document.removeEventListener('click', closeOnOutsideClick);
                        document.removeEventListener('touchstart', closeOnOutsideTouch);
                    }, 150);
                });
            });
        } else {
            // Desktop uchun hover event'lar
            profileDropdown.addEventListener('mouseenter', function() {
                clearTimeout(timeout);
                dropdownContent.style.display = 'block';
                isOpen = true;
            });
            
            profileDropdown.addEventListener('mouseleave', function() {
                timeout = setTimeout(function() {
                    dropdownContent.style.display = 'none';
                    isOpen = false;
                }, 200); // 200ms kechikish
            });
            
            dropdownContent.addEventListener('mouseenter', function() {
                clearTimeout(timeout);
                dropdownContent.style.display = 'block';
                isOpen = true;
            });
            
            dropdownContent.addEventListener('mouseleave', function() {
                timeout = setTimeout(function() {
                    dropdownContent.style.display = 'none';
                    isOpen = false;
                }, 200);
            });
        }
    }
});
