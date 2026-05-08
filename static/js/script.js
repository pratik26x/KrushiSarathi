// document.addEventListener("DOMContentLoaded", function () {
//     const coin = document.querySelector(".coin-container");

//     const observer = new IntersectionObserver((entries) => {
//         entries.forEach(entry => {
//             if (entry.isIntersecting) {
//                 coin.style.animation = "rollDown 5s ease forwards"; // Trigger the animation
//             }
//         });
//     });

//     observer.observe(document.querySelector(".Benefits-section"));
// });


document.addEventListener("DOMContentLoaded", function () {
    const coin = document.querySelector(".coin-container");
    const benefitsSection = document.querySelector(".Benefits-section");
    
    // Get the height of the viewport for calculation
    const windowHeight = window.innerHeight;

    // Add scroll event listener to trigger the animation
    window.addEventListener("scroll", function () {
        // Get the distance from the top of the page to the benefits section
        const sectionTop = benefitsSection.getBoundingClientRect().top;

        // Calculate the progress of scrolling into the section (0 to 1)
        let scrollProgress = (windowHeight - sectionTop) / windowHeight;

        // Ensure scrollProgress stays between 0 and 1
        scrollProgress = Math.min(1, Math.max(0, scrollProgress));

        // Rotate and move the coin based on scrollProgress
        const translateY = 300 * scrollProgress; // Coin will move down 300px
        const rotateDeg = 360 * scrollProgress; // Coin will rotate 360 degrees
        
        // Apply transform for movement and rotation
        coin.style.transform = `translateY(${translateY}px) rotate(${rotateDeg}deg)`;
        coin.style.opacity = scrollProgress; // Control opacity based on scroll position
    });
});
