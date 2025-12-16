@section('projects')
<section id="projects" class="py-20">
    <div class="container mx-auto px-6">
        <h2 class="text-3xl font-bold text-center mb-12">My Work</h2>
        <div class="flex justify-center mb-8">
            <button class="px-4 py-2 mr-2 bg-gray-200 rounded-full font-medium active:bg-gray-300">All</button>
            <button class="px-4 py-2 mr-2 bg-gray-200 rounded-full font-medium active:bg-gray-300">Web</button>
            <button class="px-4 py-2 mr-2 bg-gray-200 rounded-full font-medium active:bg-gray-300">Mobile</button>
            <button class="px-4 py-2 bg-gray-200 rounded-full font-medium active:bg-gray-300">Branding</button>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div class="card-hover overflow-hidden rounded-lg shadow-md hover:shadow-lg transition-all">
                <img src="https://picsum.photos/600/400" alt="Project 1" class="w-full h-48 object-cover" />
                <div class="p-6">
                    <h3 class="text-xl font-bold mb-2">E-Commerce Platform</h3>
                    <p class="text-gray-600 mb-4">A modern e-commerce solution with React and Node.js</p>
                    <a href="#" class="text-blue-600 hover:underline">View Details →</a>
                </div>
            </div>
            <div class="card-hover overflow-hidden rounded-lg shadow-md hover:shadow-lg transition-all">
                <img src="https://picsum.photos/600/401" alt="Project 2" class="w-full h-48 object-cover" />
                <div class="p-6">
                    <h3 class="text-xl font-bold mb-2">Mobile App UI Kit</h3>
                    <p class="text-gray-600 mb-4">Figma design system for mobile applications</p>
                    <a href="#" class="text-blue-600 hover:underline">View Details →</a>
                </div>
            </div>
            <div class="card-hover overflow-hidden rounded-lg shadow-md hover:shadow-lg transition-all">
                <img src="https://picsum.photos/600/402" alt="Project 3" class="w-full h-48 object-cover" />
                <div class="p-6">
                    <h3 class="text-xl font-bold mb-2">Portfolio Website</h3>
                    <p class="text-gray-600 mb-4">Personal portfolio using Tailwind CSS and React</p>
                    <a href="#" class="text-blue-600 hover:underline">View Details →</a>
                </div>
            </div>
        </div>
    </div>
</section>
@endsection