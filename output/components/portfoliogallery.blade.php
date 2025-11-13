<!-- Portfolio Gallery Section -->
<section id="portfolio" class="py-20 px-6">
    <div class="container mx-auto max-w-6xl">
        <div class="fade-in">
            <h2 class="text-4xl font-bold font-display text-center mb-4">Portfolio</h2>
            <div class="w-24 h-1 bg-gradient-to-r from-purple-600 to-indigo-600 mx-auto mb-12"></div>
            
            <div class="flex justify-center mb-8 flex-wrap gap-4">
                <button class="filter-btn px-6 py-2 rounded-full bg-purple-600 text-white" data-filter="all">Semua</button>
                <button class="filter-btn px-6 py-2 rounded-full border border-gray-300 dark:border-gray-600 hover:bg-purple-600 hover:text-white transition-all" data-filter="web">Web App</button>
                <button class="filter-btn px-6 py-2 rounded-full border border-gray-300 dark:border-gray-600 hover:bg-purple-600 hover:text-white transition-all" data-filter="mobile">Mobile</button>
                <button class="filter-btn px-6 py-2 rounded-full border border-gray-300 dark:border-gray-600 hover:bg-purple-600 hover:text-white transition-all" data-filter="design">UI/UX</button>
            </div>
            
            <div class="masonry-grid">
                <div class="masonry-item project-item" data-category="web">
                    <div class="relative group overflow-hidden rounded-xl shadow-lg cursor-pointer">
                        <img src="https://picsum.photos/seed/project1/400/500" alt="E-Commerce Platform" class="w-full">
                        <div class="project-overlay absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-6">
                            <h3 class="text-white text-xl font-bold mb-2">E-Commerce Platform</h3>
                            <p class="text-gray-200 text-sm mb-3">Platform e-commerce modern dengan fitur payment gateway dan inventory management</p>
                            <div class="flex flex-wrap gap-2 mb-3">
                                <span class="px-3 py-1 bg-white/20 backdrop-blur text-white text-xs rounded-full">React</span>
                                <span class="px-3 py-1 bg-white/20 backdrop-blur text-white text-xs rounded-full">Node.js</span>
                                <span class="px-3 py-1 bg-white/20 backdrop-blur text-white text-xs rounded-full">MongoDB</span>
                            </div>
                            <a href="#" class="text-white flex items-center gap-2 hover:gap-3 transition-all">
                                Lihat Detail <i class="fas fa-arrow-right"></i>
                            </a>
                        </div>
                    </div>
                </div>
                
                <div class="masonry-item project-item" data-category="mobile">
                    <div class="relative group overflow-hidden rounded-xl shadow-lg cursor-pointer">
                        <img src="https://picsum.photos/seed/project2/400/300" alt="Fitness Tracker App" class="w-full">
                        <div class="project-overlay absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-6">
                            <h3 class="text-white text-xl font-bold mb-2">Fitness Tracker App</h3>
                            <p class="text-gray-200 text-sm mb-3">Aplikasi mobile untuk tracking aktivitas fitness dan nutrisi harian</p>
                            <div class="flex flex-wrap gap-2 mb-3">
                                <span class="px-3 py-1 bg-white/20 backdrop-blur text-white text-xs rounded-full">React Native</span>
                                <span class="px-3 py-1 bg-white/20 backdrop-blur text-white text-xs rounded-full">Firebase</span>
                            </div>
                            <a href="#" class="text-white flex items-center gap-2 hover:gap-3 transition-all">
                                Lihat Detail <i class="fas fa-arrow-right"></i>
                            </a>
                        </div>
                    </div>
                </div>
                
                <div class="masonry-item project-item" data-category="design">
                    <div class="relative group overflow-hidden rounded-xl shadow-lg cursor-pointer">
                        <img src="https://picsum.photos/seed/project3/400/400" alt="Banking Dashboard" class="w-full">
                        <div class="project-overlay absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-6">
                            <h3 class="text-white text-xl font-bold mb-2">Banking Dashboard</h3>
                            <p class="text-gray-200 text-sm mb-3">Desain dashboard perbankan dengan visualisasi data yang interaktif</p>
                            <div class="flex flex-wrap gap-2 mb-3">
                                <span class="px-3 py-1 bg-white/20 backdrop-blur text-white text-xs rounded-full">Figma</span>
                                <span class="px-3 py-1 bg-white/20 backdrop-blur text-white text-xs rounded-full">Prototyping</span>
                            </div>
                            <a href="#" class="text-white flex items-center gap-2 hover:gap-3 transition-all">
                                Lihat Detail <i class="fas fa-arrow-right"></i>
                            </a>
                        </div>
                    </div>
                </div>
                
                <div class="masonry-item project-item" data-category="web">
                    <div class="relative group overflow-hidden rounded-xl shadow-lg cursor-pointer">
                        <img src="https://picsum.photos/seed/project4/400/350" alt="SaaS Management Tool" class="w-full">
                        <div class="project-overlay absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-6">
                            <h3 class="text-white text-xl font-bold mb-2">SaaS Management Tool</h3>
                            <p class="text-gray-200 text-sm mb-3">Tool manajemen proyek dan tim untuk startup teknologi</p>
                            <div class="flex flex-wrap gap-2 mb-3">
                                <span class="px-3 py-1 bg-white/20 backdrop-blur text-white text-xs rounded-full">Vue.js</span>
                                <span class="px-3 py-1 bg-white/20 backdrop-blur text-white text-xs rounded-full">Laravel</span>
                            </div>
                            <a href="#" class="text-white flex items-center gap-2 hover:gap-3 transition-all">
                                Lihat Detail <i class="fas fa-arrow-right"></i>
                            </a>
                        </div>
                    </div>
                </div>
                
                <div class="masonry-item project-item" data-category="mobile">
                    <div class="relative group overflow-hidden rounded-xl shadow-lg cursor-pointer">
                        <img src="https://picsum.photos/seed/project5/400/450" alt="Food Delivery App" class="w-full">
                        <div class="project-overlay absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-6">
                            <h3 class="text-white text-xl font-bold mb-2">Food Delivery App</h3>
                            <p class="text-gray-200 text-sm mb-3">Aplikasi pesan antar makanan dengan real-time tracking</p>
                            <div class="flex flex-wrap gap-2 mb-3">
                                <span class="px-3 py-1 bg-white/20 backdrop-blur text-white text-xs rounded-full">Flutter</span>
                                <span class="px-3 py-1 bg-white/20 backdrop-blur text-white text-xs rounded-full">Google Maps API</span>
                            </div>
                            <a href="#" class="text-white flex items-center gap-2 hover:gap-3 transition-all">
                                Lihat Detail <i class="fas fa-arrow-right"></i>
                            </a>
                        </div>
                    </div>
                </div>
                
                <div class="masonry-item project-item" data-category="design">
                    <div class="relative group overflow-hidden rounded-xl shadow-lg cursor-pointer">
                        <img src="https://picsum.photos/seed/project6/400/320" alt="Social Media Redesign" class="w-full">
                        <div class="project-overlay absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-6">
                            <h3 class="text-white text-xl font-bold mb-2">Social Media Redesign</h3>
                            <p class="text-gray-200 text-sm mb-3">Redesign lengkap UI/UX untuk platform media sosial</p>
                            <div class="flex flex-wrap gap-2 mb-3">
                                <span class="px-3 py-1 bg-white/20 backdrop-blur text-white text-xs rounded-full">UI Design</span>
                                <span class="px-3 py-1 bg-white/20 backdrop-blur text-white text-xs rounded-full">User Research</span>
                            </div>
                            <a href="#" class="text-white flex items-center gap-2 hover:gap-3 transition-all">
                                Lihat Detail <i class="fas fa-arrow-right"></i>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>