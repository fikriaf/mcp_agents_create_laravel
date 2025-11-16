<!-- layout content -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>@yield('title', 'GenLaravel')</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            margin: 0;
            padding: 0;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .preview-container {
            flex: 1;
            overflow: hidden;
        }
    </style>
</head>
<body class="bg-gray-100">
    @yield('content')
    
    <script>
        function showPage(pageName) {
            // Hide all page containers
            document.querySelectorAll('div[id^="page-"]').forEach(div => {
                div.classList.add('hidden');
            });
            
            // Remove active state from all tabs
            document.querySelectorAll('button[id^="tab-"]').forEach(tab => {
                tab.classList.remove('bg-blue-600', 'text-white');
                tab.classList.add('bg-gray-200', 'text-gray-700');
            });
            
            // Show selected page
            document.getElementById('page-' + pageName).classList.remove('hidden');
            
            // Activate selected tab
            const activeTab = document.getElementById('tab-' + pageName);
            activeTab.classList.remove('bg-gray-200', 'text-gray-700');
            activeTab.classList.add('bg-blue-600', 'text-white');
        }
    </script>
</body>
</html>