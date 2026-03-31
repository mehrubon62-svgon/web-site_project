// Wishlist Toggle Functionality
document.addEventListener('DOMContentLoaded', function() {
    const wishlistForms = document.querySelectorAll('.wishlist-form');
    const translateWishlistMessage = function(key, fallback) {
        if (window.BuildBoxI18n && typeof window.BuildBoxI18n.t === 'function') {
            return window.BuildBoxI18n.t(key);
        }
        return fallback;
    };
    
    wishlistForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const button = this.querySelector('button[type="submit"]');
            const svg = button.querySelector('svg');
            const formData = new FormData(this);
            
            // Disable button during request
            button.disabled = true;
            
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(data => {
                // Toggle heart state
                const isInWishlist = button.classList.contains('bg-red-500');
                
                if (isInWishlist) {
                    // Remove from wishlist - make it gray
                    button.classList.remove('bg-red-500');
                    button.classList.add('bg-gray-100/90');
                    svg.classList.remove('text-white');
                    svg.classList.add('text-gray-600');
                    svg.setAttribute('fill', 'none');
                } else {
                    // Add to wishlist - make it red
                    button.classList.remove('bg-gray-100/90');
                    button.classList.add('bg-red-500');
                    svg.classList.remove('text-gray-600');
                    svg.classList.add('text-white');
                    svg.setAttribute('fill', 'currentColor');
                }
                
                // Add pulse animation
                button.classList.add('animate-pulse');
                setTimeout(() => {
                    button.classList.remove('animate-pulse');
                    button.disabled = false;
                }, 300);
            })
            .catch(error => {
                console.error('Error:', error);
                button.disabled = false;
                alert(translateWishlistMessage('wishlist_update_failed', 'Failed to update wishlist. Please try again.'));
            });
            
            return false;
        });
    });
});
