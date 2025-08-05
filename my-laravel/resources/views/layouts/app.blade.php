<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Creative Portfolio</title>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            primary: '#6C5CE7',
            secondary: '#A29BFE',
            dark: '#2D3436',
            light: '#F5F6FA',
            accent: '#FD79A8',
          },
          fontFamily: {
            sans: ['Poppins', 'sans-serif'],
            serif: ['Playfair Display', 'serif'],
          },
          animation: {
            'fade-in': 'fadeIn 1s ease-in-out',
            'slide-up': 'slideUp 0.5s ease-out',
          },
          keyframes: {
            fadeIn: {
              '0%': { opacity: '0' },
              '100%': { opacity: '1' },
            },
            slideUp: {
              '0%': { transform: 'translateY(20px)', opacity: '0' },
              '100%': { transform: 'translateY(0)', opacity: '1' },
            },
          },
        },
      },
    }
  </script>
  <style>
    .hero-bg {
      background: linear-gradient(135deg, #6C5CE7 0%, #A29BFE 100%);
    }
    .about-img {
      clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%);
    }
    .skill-chart {
      background: conic-gradient(#FD79A8 var(--progress), #F5F6FA 0);
    }
    .project-card {
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .project-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    }
    .testimonial-card {
      transition: all 0.3s ease;
    }
    .testimonial-card:hover {
      transform: translateY(-5px);
    }
    .btn-primary {
      transition: all 0.3s ease;
    }
    .btn-primary:hover {
      transform: translateY(-2px);
      box-shadow: 0 5px 15px rgba(108, 92, 231, 0.4);
    }
    .nav-link {
      position: relative;
      transition: color 0.3s ease;
    }
    .nav-link::after {
      content: '';
      position: absolute;
      width: 0;
      height: 2px;
      bottom: -2px;
      left: 0;
      background-color: #FD79A8;
      transition: width 0.3s ease;
    }
    .nav-link:hover::after {
      width: 100%;
    }
    .fade-in {
      animation: fadeIn 1s ease-in-out;
    }
    .slide-up {
      animation: slideUp 0.5s ease-out;
    }
    @media (max-width: 768px) {
      .mobile-menu {
        display: block;
      }
      .desktop-menu {
        display: none;
      }
    }
  </style>
</head>
<body class="font-sans bg-light text-dark">
  @yield('content')
</body>
</html>