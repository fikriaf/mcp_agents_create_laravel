<header class="fixed w-full z-50 bg-white shadow-md">
    <div class="container mx-auto px-6 py-4 flex justify-between items-center">
        <a href="#" class="text-2xl font-bold font-serif text-primary">Creative<span class="text-accent">.</span></a>

        <!-- Desktop Menu -->
        <nav class="desktop-menu flex space-x-8">
            <a href="#about" class="nav-link text-lg font-medium hover:text-primary">About</a>
            <a href="#skills" class="nav-link text-lg font-medium hover:text-primary">Skills</a>
            <a href="#projects" class="nav-link text-lg font-medium hover:text-primary">Projects</a>
            <a href="#testimonials" class="nav-link text-lg font-medium hover:text-primary">Testimonials</a>
            <a href="#contact" class="nav-link text-lg font-medium hover:text-primary">Contact</a>
        </nav>

        <!-- Mobile Menu Button -->
        <button class="mobile-menu hidden text-2xl focus:outline-none" id="mobile-menu-button">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
        </button>
    </div>

    <!-- Mobile Menu -->
    <div class="mobile-menu hidden bg-white shadow-lg" id="mobile-menu">
        <div class="container mx-auto px-6 py-4">
            <a href="#about" class="block py-2 text-lg font-medium hover:text-primary">About</a>
            <a href="#skills" class="block py-2 text-lg font-medium hover:text-primary">Skills</a>
            <a href="#projects" class="block py-2 text-lg font-medium hover:text-primary">Projects</a>
            <a href="#testimonials" class="block py-2 text-lg font-medium hover:text-primary">Testimonials</a>
            <a href="#contact" class="block py-2 text-lg font-medium hover:text-primary">Contact</a>
        </div>
    </div>
</header>