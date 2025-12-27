// static/js/simple-scroll.js
// Минимальная версия с постоянной скоростью

document.addEventListener('DOMContentLoaded', function() {
    // Все ссылки с якорями
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const element = document.querySelector(targetId);
            if (!element) return;
            
            e.preventDefault();
            
            // Простая функция линейной анимации
            function scrollTo(element, duration = 800) {
                const start = window.pageYOffset;
                const to = element.getBoundingClientRect().top + start - 70;
                const change = to - start;
                let currentTime = 0;
                const increment = 20; // Частота обновления (20ms)
                
                function animateScroll() {
                    currentTime += increment;
                    const val = change * (currentTime / duration) + start;
                    
                    window.scrollTo(0, val);
                    
                    if (currentTime < duration) {
                        setTimeout(animateScroll, increment);
                    }
                }
                
                animateScroll();
            }
            
            // Вызываем с дефолтной скоростью 800ms
            scrollTo(element, 800);
            
            // Обновляем URL
            history.pushState(null, null, targetId);
        });
    });
});