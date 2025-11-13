<header id="navbar" class="fixed top-0 left-0 right-0 z-50 transition-all duration-300">
    <nav class="container mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
            <div class="text-2xl font-bold font-display">
                <span class="gradient-text">AR.</span>
            </div>
            
            <div class="hidden md:flex items-center space-x-8">
                <a href="#home" class="nav-link hover:text-purple-600 dark:hover:text-purple-400 transition-colors">Beranda</a>
                <a href="#about" class="nav-link hover:text-purple-600 dark:hover:text-purple-400 transition-colors">Tentang</a>
                <a href="#skills" class="nav-link hover:text-purple-600 dark:hover:text-purple-400 transition-colors">Keahlian</a>
                <a href="#portfolio" class="nav-link hover:text-purple-600 dark:hover:text-purple-400 transition-colors">Portfolio</a>
                <a href="#experience" class="nav-link hover:text-purple-600 dark:hover:text-purple-400 transition-colors">Pengalaman</a>
                <a href="#contact" class="nav-link hover:text-purple-600 dark:hover:text-purple-400 transition-colors">Kontak</a>
            </div>
            
            <div class="flex items-center space-x-4">
                <button id="darkModeToggle" class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
                    <i class="fas fa-moon dark:hidden text-xl"></i>
                    <i class="fas fa-sun hidden dark:block text-xl"></i>
                </button>
                
                <button id="mobileMenuToggle" class="md:hidden p-2">
                    <i class="fas fa-bars text-xl"></i>
                </button>
            </div>
        </div>
        
        <!-- Mobile Menu -->
        <div id="mobileMenu" class="hidden md:hidden mt-4 pb-4">
            <a href="#home" class="block py-2 hover:text-purple-600 dark:hover:text-purple-400 transition-colors">Beranda</a>
            <a href="#about" class="block py-2 hover:text-purple-600 dark:hover:text-purple-400 transition-colors">Tentang</a>
            <a href="#skills" class="block py-2 hover:text-purple-600 dark:hover:text-purple-400 transition-colors">Keahlian</a>
            <a href="#portfolio" class="block py-2 hover:text-purple-600 dark:hover:text-purple-400 transition-colors">Portfolio</a>
            <a href="#experience" class="block py-2 hover:text-purple-600 dark:hover:text-purple-400 transition-colors">Pengalaman</a>
            <a href="#contact" class="block py-2 hover:text-purple-600 dark:hover:text-purple-400 transition-colors">Kontak</a>
        </div>
    </nav>
</header>