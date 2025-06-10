// main.js - JavaScript for PyConNG 2025 website

document.addEventListener('DOMContentLoaded', () => {
  // Cache DOM elements
  const hamburger = document.querySelector('.hamburger');
  const mainNav = document.querySelector('.main-nav');
  const body = document.body;
  const header = document.querySelector('.site-header');
  const dropdowns = document.querySelectorAll('.dropdown');
  const dropdownLinks = document.querySelectorAll('.dropdown > a');
  
  // ======= MOBILE MENU HANDLING =======
  // Toggle the main nav open/close on mobile
  if (hamburger) {
    hamburger.addEventListener('click', () => {
      mainNav.classList.toggle('nav-open');
      header.classList.toggle('nav-open');
      
      // Prevent body scrolling when menu is open
      body.style.overflow = mainNav.classList.contains('nav-open') ? 'hidden' : '';
      
      // Reset dropdowns when closing menu
      if (!mainNav.classList.contains('nav-open')) {
        dropdowns.forEach(dropdown => {
          dropdown.classList.remove('active');
        });
      }
    });
  }

  // Close menu when clicking outside on mobile
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.main-nav') && !e.target.closest('.hamburger')) {
      mainNav.classList.remove('nav-open');
      header.classList.remove('nav-open');
      body.style.overflow = '';
      
      // Reset all dropdowns
      dropdowns.forEach(dropdown => {
        dropdown.classList.remove('active');
      });
    }
  });

  // Close menu when pressing escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && mainNav.classList.contains('nav-open')) {
      mainNav.classList.remove('nav-open');
      header.classList.remove('nav-open');
      body.style.overflow = '';
      
      // Reset all dropdowns
      dropdowns.forEach(dropdown => {
        dropdown.classList.remove('active');
      });
    }
  });
  
  // ======= DROPDOWN HANDLING =======
  // Mobile dropdown handling - need to use click instead of hover
  dropdownLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      // Only for mobile view
      if (window.innerWidth <= 768) {
        e.preventDefault(); // Prevent navigation
        e.stopPropagation(); // Prevent event bubbling
        
        const currentDropdown = link.parentNode;
        const isActive = currentDropdown.classList.contains('active');
        
        // Close all dropdowns first
        dropdowns.forEach(dropdown => {
          if (dropdown !== currentDropdown) {
            dropdown.classList.remove('active');
          }
        });
        
        // Toggle current dropdown
        currentDropdown.classList.toggle('active');
      }
    });
  });
  
  // Handle clicks inside dropdown menus - prevent closing on mobile
  document.querySelectorAll('.dropdown-menu').forEach(menu => {
    menu.addEventListener('click', (e) => {
      if (window.innerWidth <= 768) {
        e.stopPropagation();
      }
    });
  });
  
  // ======= WINDOW RESIZE HANDLING =======
  // Handle window resize - reset menu state when switching between mobile/desktop
  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      if (window.innerWidth > 768) {
        // Reset mobile menu state when switching to desktop
        mainNav.classList.remove('nav-open');
        header.classList.remove('nav-open');
        body.style.overflow = '';
        
        // Reset all dropdowns
        dropdowns.forEach(dropdown => {
          dropdown.classList.remove('active');
        });
      }
    }, 250);
  });
  
  // ======= ANIMATION HANDLING =======
  // Make sure animations for floating islands are applied
  const island1 = document.querySelector('.island-1');
  const island2 = document.querySelector('.island-2');
  
  if (island1 && !island1.style.animation) {
    island1.style.animation = 'float 3s ease-in-out 0s infinite';
  }
  
  if (island2 && !island2.style.animation) {
    island2.style.animation = 'float 4s ease-in-out 1s infinite';
  }
  
  // Ensure train animation works
  const train = document.querySelector('.train');
  if (train && !train.style.animation) {
    train.style.animation = 'moveTrain 15s linear infinite';
  }
});