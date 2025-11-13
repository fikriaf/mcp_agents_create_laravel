<!-- Experience Timeline Component -->
<section id="experience" class="py-20 px-6 bg-gray-50 dark:bg-gray-800">
    <div class="container mx-auto max-w-4xl">
        <div class="fade-in">
            <h2 class="text-4xl font-bold font-display text-center mb-4">{{ $title ?? 'Pengalaman' }}</h2>
            <div class="w-24 h-1 bg-gradient-to-r from-purple-600 to-indigo-600 mx-auto mb-12"></div>
            
            <div class="relative">
                <div class="absolute left-1/2 transform -translate-x-1/2 w-1 h-full timeline-line"></div>
                
                <div class="space-y-12">
                    @foreach($experiences as $index => $experience)
                        <div class="flex items-center justify-between">
                            @if($index % 2 == 0)
                                <div class="w-5/12 text-right slide-left">
                                    <div class="bg-white dark:bg-gray-900 p-6 rounded-xl shadow-lg">
                                        <h3 class="text-xl font-bold mb-2">{{ $experience['position'] }}</h3>
                                        <div class="text-purple-600 dark:text-purple-400 mb-2">{{ $experience['company'] }}</div>
                                        <div class="text-sm text-gray-600 dark:text-gray-400 mb-3">{{ $experience['period'] }}</div>
                                        <p class="text-gray-600 dark:text-gray-300">{{ $experience['description'] }}</p>
                                    </div>
                                </div>
                                <div class="w-2/12 flex justify-center">
                                    <div class="w-6 h-6 bg-purple-600 rounded-full border-4 border-white dark:border-gray-900"></div>
                                </div>
                                <div class="w-5/12"></div>
                            @else
                                <div class="w-5/12"></div>
                                <div class="w-2/12 flex justify-center">
                                    <div class="w-6 h-6 bg-purple-600 rounded-full border-4 border-white dark:border-gray-900"></div>
                                </div>
                                <div class="w-5/12 slide-right">
                                    <div class="bg-white dark:bg-gray-900 p-6 rounded-xl shadow-lg">
                                        <h3 class="text-xl font-bold mb-2">{{ $experience['position'] }}</h3>
                                        <div class="text-purple-600 dark:text-purple-400 mb-2">{{ $experience['company'] }}</div>
                                        <div class="text-sm text-gray-600 dark:text-gray-400 mb-3">{{ $experience['period'] }}</div>
                                        <p class="text-gray-600 dark:text-gray-300">{{ $experience['description'] }}</p>
                                    </div>
                                </div>
                            @endif
                        </div>
                    @endforeach
                </div>
            </div>
        </div>
    </div>
</section>