document.addEventListener('DOMContentLoaded', () => {
  // Product form logic for saving product, removing extra options
  const productForm = document.querySelector('.product-form form');
  productForm.addEventListener('submit', function(event) {
      event.preventDefault();

      // Collect product data
      const productName = document.getElementById('product-name').value;
      const productBarcode = document.getElementById('product-barcode').value;
      const productPrice = document.getElementById('product-price').value;
      const productCategory = document.getElementById('product-category').value;
      const productSupplier = document.getElementById('product-supplier').value;
      const productStock = document.getElementById('product-stock').value;
      const productMinStock = document.getElementById('product-min-stock').value;

      // Process the collected data (for now just log it)
      console.log({
          productName,
          productBarcode,
          productPrice,
          productCategory,
          productSupplier,
          productStock,
          productMinStock
      });

      // Clear form after submission
      productForm.reset();
  });
});
