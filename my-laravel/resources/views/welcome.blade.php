<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GenLaravel - AI Laravel Generator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 min-h-screen flex items-center justify-center">
    <div class="container mx-auto px-6">
        <div class="max-w-4xl mx-auto text-center">
            <!-- Logo -->
            <div class="mb-8 flex justify-center">
                <img src="{{ asset('GenLaravel.png'}}" alt="GenLaravel Logo" class="w-32 h-32 object-contain">
            </div>

            <!-- Title -->
            <h1 class="text-6xl font-bold text-white mb-4">
                GenLaravel
            </h1>
            <p class="text-2xl text-gray-300 mb-8">
                AI-Powered Laravel Generator
            </p>

            <!-- Status -->
            <div class="bg-white bg-opacity-10 backdrop-blur-lg rounded-2xl p-8 mb-8 border border-white border-opacity-20">
                <div class="flex items-center justify-center space-x-3 mb-4">
                    <div class="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                    <span class="text-white text-lg font-semibold">Ready to Generate</span>
                </div>
                <p class="text-gray-300">
                    Your Laravel project is ready. Run GenLaravel to generate pages.
                </p>
            </div>

            <!-- Quick Start -->
            <div class="grid md:grid-cols-2 gap-6 mb-8">
                <div class="bg-white bg-opacity-10 backdrop-blur-lg rounded-xl p-6 border border-white border-opacity-20 hover:bg-opacity-20 transition">
                    <div class="text-red-400 text-3xl mb-3">
                        <i class="fas fa-file"></i>
                    </div>
                    <h3 class="text-white font-bold text-lg mb-2">Single Page</h3>
                    <p class="text-gray-300 text-sm mb-3">Generate one page at a time</p>
                    <code class="bg-black bg-opacity-50 text-green-400 px-3 py-1 rounded text-sm">
                        python main.py
                    </code>
                </div>

                <div class="bg-white bg-opacity-10 backdrop-blur-lg rounded-xl p-6 border border-white border-opacity-20 hover:bg-opacity-20 transition">
                    <div class="text-red-400 text-3xl mb-3">
                        <i class="fas fa-layer-group"></i>
                    </div>
                    <h3 class="text-white font-bold text-lg mb-2">Multi Page</h3>
                    <p class="text-gray-300 text-sm mb-3">Generate multiple pages</p>
                    <code class="bg-black bg-opacity-50 text-green-400 px-3 py-1 rounded text-sm">
                        python main_multi_page.py
                    </code>
                </div>
            </div>

            <!-- Features -->
            <div class="flex flex-wrap justify-center gap-4 text-gray-300">
                <div class="flex items-center space-x-2">
                    <i class="fas fa-check-circle text-green-400"></i>
                    <span>AI-Powered</span>
                </div>
                <div class="flex items-center space-x-2">
                    <i class="fas fa-check-circle text-green-400"></i>
                    <span>Tailwind CSS</span>
                </div>
                <div class="flex items-center space-x-2">
                    <i class="fas fa-check-circle text-green-400"></i>
                    <span>Blade Components</span>
                </div>
                <div class="flex items-center space-x-2">
                    <i class="fas fa-check-circle text-green-400"></i>
                    <span>Auto Routes</span>
                </div>
            </div>

            <!-- Footer -->
            <div class="mt-12 text-gray-400 text-sm">
                <p>Powered by AI Agents | Built with ❤️</p>
            </div>
        </div>
    </div>
</body>
</html>
