// Shopping Cart State
let cart = [];

// DOM Elements
const cartIcon = document.querySelector('.cart-icon');
const cartModal = document.getElementById('cart-modal');
const closeBtn = document.querySelector('.close');
const cartItemsContainer = document.getElementById('cart-items');
const totalPriceElement = document.getElementById('total-price');
const cartCountElement = document.getElementById('cart-count');
const addToCartButtons = document.querySelectorAll('.btn-add-cart');
const checkoutBtn = document.querySelector('.checkout-btn');
const contactForm = document.querySelector('.contact-form');

// Product Data
const products = {
    1: { name: 'Laptop Pro', price: 999.99, emoji: '💻' },
    2: { name: 'Smartphone X', price: 699.99, emoji: '📱' },
    3: { name: 'Casque Audio', price: 149.99, emoji: '🎧' },
    4: { name: 'Montre Connectée', price: 299.99, emoji: '⌚' },
    5: { name: 'Appareil Photo', price: 549.99, emoji: '📷' },
    6: { name: 'Écran 4K', price: 399.99, emoji: '🖥️' }
};

// Add to Cart Function
function addToCart(productId) {
    const product = products[productId];
    const existingItem = cart.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.quantity++;
    } else {
        cart.push({
            id: productId,
            name: product.name,
            price: product.price,
            emoji: product.emoji,
            quantity: 1
        });
    }
    
    updateCart();
    showNotification('Produit ajouté au panier!');
}

// Update Cart Display
function updateCart() {
    // Update cart count
    const totalCount = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCountElement.textContent = totalCount;
    
    // Update cart items display
    cartItemsContainer.innerHTML = '';
    let total = 0;
    
    if (cart.length === 0) {
        cartItemsContainer.innerHTML = '<p style="text-align: center; color: #999;">Votre panier est vide</p>';
    } else {
        cart.forEach(item => {
            const itemTotal = item.price * item.quantity;
            total += itemTotal;
            
            const cartItemElement = document.createElement('div');
            cartItemElement.className = 'cart-item';
            cartItemElement.innerHTML = `
                <div>
                    <span>${item.emoji}</span>
                    <strong>${item.name}</strong> x ${item.quantity}
                </div>
                <div>
                    <span>${itemTotal.toFixed(2)} €</span>
                    <button class="remove-item" data-id="${item.id}" style="background: #ff6b6b; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer; margin-left: 10px;">×</button>
                </div>
            `;
            cartItemsContainer.appendChild(cartItemElement);
        });
    }
    
    // Update total price
    totalPriceElement.textContent = total.toFixed(2);
    
    // Add event listeners to remove buttons
    document.querySelectorAll('.remove-item').forEach(btn => {
        btn.addEventListener('click', (e) => {
            removeFromCart(e.target.dataset.id);
        });
    });
}

// Remove from Cart
function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== parseInt(productId));
    updateCart();
}

// Show Notification
function showNotification(message) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        background: #4CAF50;
        color: white;
        padding: 15px 25px;
        border-radius: 5px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        z-index: 3000;
        animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 2000);
}

// Modal Functions
function openModal() {
    cartModal.style.display = 'block';
}

function closeModal() {
    cartModal.style.display = 'none';
}

// Event Listeners
cartIcon.addEventListener('click', openModal);
closeBtn.addEventListener('click', closeModal);

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    if (e.target === cartModal) {
        closeModal();
    }
});

// Add to cart buttons
addToCartButtons.forEach(button => {
    button.addEventListener('click', () => {
        const productId = button.closest('.product-card').dataset.id;
        addToCart(productId);
    });
});

// Checkout button
checkoutBtn.addEventListener('click', () => {
    if (cart.length === 0) {
        alert('Votre panier est vide!');
        return;
    }
    
    const total = totalPriceElement.textContent;
    alert(`Merci pour votre commande!\nTotal: ${total} €\n\nCeci est une démo. Dans un site réel, vous seriez redirigé vers le paiement.`);
    cart = [];
    updateCart();
    closeModal();
});

// Contact form submission
contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Merci pour votre message! Nous vous répondrons bientôt.');
    contactForm.reset();
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
            const headerOffset = 80;
            const elementPosition = targetElement.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
    
            window.scrollTo({
                top: offsetPosition,
                behavior: "smooth"
            });
        }
    });
});

// Initialize cart display
updateCart();

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

console.log('E-Commerce Site loaded successfully! 🛒');
