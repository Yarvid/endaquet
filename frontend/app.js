document.addEventListener('DOMContentLoaded', function() {
    const productList = document.getElementById('productList');
    const productForm = document.getElementById('productForm');
    const productNameInput = document.getElementById('productName');
    const productPriceInput = document.getElementById('productPrice');

    fetchProducts();

    productForm.addEventListener('submit', function(e) {
        e.preventDefault();
        addProduct(productNameInput.value, productPriceInput.value);
        productNameInput.value = '';
        productPriceInput.value = '';
    });

    function fetchProducts() {
        fetch('http://localhost:5000/products')
            .then(response => response.json())
            .then(data => renderProducts(data))
            .catch(error => console.error('Error fetching products:', error));
    }

    function addProduct(name, price) {
        fetch('http://localhost:5000/products', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: name, price: parseFloat(price) }),
        })
        .then(() => fetchProducts())
        .catch(error => console.error('Error adding product:', error));
    }

    function removeProduct(index) {
        fetch(`http://localhost:5000/product/${index}`, { method: 'DELETE' })
        .then(() => fetchProducts())
        .catch(error => console.error('Error removing product:', error));
    }

    function renderProducts(products) {
        productList.innerHTML = '';
        Object.entries(products).forEach(([name, price], index) => {
            const li = document.createElement('li');
            li.textContent = `${name} - €${price.toFixed(2)}`;
            const removeButton = document.createElement('button');
            removeButton.textContent = 'Remove';
            removeButton.addEventListener('click', () => removeProduct(index));
            li.appendChild(removeButton);
            productList.appendChild(li);
        });
    }    
});
