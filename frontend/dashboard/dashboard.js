// Aqui você pode adicionar interações futuras com filtros, gráficos ou outras funcionalidades.
// Exemplo:
const filterButtons = document.querySelectorAll('.filter-btn');

filterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        filterButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    });
});
