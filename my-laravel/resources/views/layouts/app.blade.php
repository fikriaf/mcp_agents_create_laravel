<!-- layout content -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>@yield('title', 'GenLaravel')</title>
    <script src="https://cdn.tailwindcss.com"></script>
        <style>
:root {
      --primary: #00F3FF;
      --secondary: #12263F;
      --accent: #7CFC00;
      --text-primary: #FFFFFF;
      --text-secondary: #B0BEC5;
    }

    .neon-btn {
      background-color: var(--primary);
      color: #000000;
      border: 2px solid var(--primary);
      box-shadow: 0 0 10px var(--primary);
      transition: all 0.3s ease;
    }

    .neon-btn:hover {
      box-shadow: 0 0 20px var(--primary);
      transform: scale(1.05);
    }

    .feature-card {
      border: 1px solid rgba(255, 255, 255, 0.1);
      transition: transform 0.3s ease;
    }

    .feature-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }

    .testimonial-card {
      border: 1px solid rgba(255, 255, 255, 0.05);
      background: rgba(255, 255, 255, 0.02);
      transition: transform 0.3s ease;
    }

    .testimonial-card:hover {
      transform: translateY(-3px);
    }

    .dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background-color: rgba(255, 255, 255, 0.3);
      transition: background-color 0.3s ease;
    }

    .dot.active {
      background-color: var(--primary);
      width: 16px;
      border-radius: 8px;
    }

    @keyframes slideIn {
      0% { opacity: 0; transform: translateY(20px); }
      100% { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
      animation: slideIn 0.6s ease-out forwards;
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