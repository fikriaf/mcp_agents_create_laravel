<div class="project-card bg-white rounded-lg shadow-md overflow-hidden transition-all duration-300 hover:transform hover:-translate-y-1 hover:shadow-lg">
    <img src="{{ $image }}" alt="{{ $title }}" class="w-full h-52 object-cover">
    <div class="p-6">
        <h3 class="text-xl font-bold mb-2">{{ $title }}</h3>
        <p class="text-secondary mb-4">{{ $description }}</p>
        <a href="{{ $link }}" class="btn inline-block bg-primary text-white px-6 py-2 rounded hover:bg-gray-800 transition">View Project</a>
    </div>
</div>