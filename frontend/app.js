document.addEventListener('DOMContentLoaded', function() {
    const productList = document.getElementById('productList');
    const productForm = document.getElementById('productForm');
    const productNameInput = document.getElementById('productName');
    const productPriceInput = document.getElementById('productPrice');

    // Load existing products (if stored)
    const storedProducts = localStorage.getItem('products');
    const products = storedProducts ? JSON.parse(storedProducts) : [];

    renderProducts();

    productForm.addEventListener('submit', function(e) {
        e.preventDefault();
        addProduct(productNameInput.value, productPriceInput.value);
        productNameInput.value = '';
        productPriceInput.value = '';
    });

    function addProduct(name, price) {
        products.push({ name: name, price: parseFloat(price) });
        saveProducts();
        renderProducts();
    }

    function removeProduct(index) {
        products.splice(index, 1);
        saveProducts();
        renderProducts();
    }

    function saveProducts() {
        localStorage.setItem('products', JSON.stringify(products));
    }

    function renderProducts() {
        productList.innerHTML = '';
        products.forEach((product, index) => {
            const li = document.createElement('li');
            li.textContent = `${product.name} - €${product.price.toFixed(2)}`;
            const removeButton = document.createElement('button');
            removeButton.textContent = 'Remove';
            removeButton.addEventListener('click', () => removeProduct(index));
            li.appendChild(removeButton);
            productList.appendChild(li);
        });
    }
});
