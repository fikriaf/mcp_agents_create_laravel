<!-- HomeComponent.blade.php -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AI Agent Pro - Home</title>
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
<body class="bg-[var(--secondary)] text-[var(--text-primary)] font-sans">
  <!-- Navbar -->
  <header class="fixed w-full bg-[var(--secondary)] z-50 shadow-lg">
    <div class="container mx-auto px-4 py-4 flex justify-between items-center">
      <div class="text-2xl font-bold text-[var(--primary)]">AI Agent Pro</div>
      <nav class="hidden md:flex space-x-8">
        <a href="#features" class="text-[var(--text-secondary)] hover:text-[var(--primary)] transition">Features</a>
        <a href="#testimonials" class="text-[var(--text-secondary)] hover:text-[var(--primary)] transition">Testimonials</a>
        <a href="#" class="text-[var(--text-secondary)] hover:text-[var(--primary)] transition">Use Cases</a>
        <a href="#" class="text-[var(--text-secondary)] hover:text-[var(--primary)] transition">Contact</a>
      </nav>
      <button id="menuToggle" class="md:hidden text-[var(--text-secondary)]">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
        </svg>
      </button>
    </div>
    <!-- Mobile Menu -->
    <div id="mobileMenu" class="md:hidden hidden bg-[var(--secondary)] py-4 px-4">
      <div class="flex flex-col space-y-4">
        <a href="#features" class="text-[var(--text-secondary)] hover:text-[var(--primary)]">Features</a>
        <a href="#testimonials" class="text-[var(--text-secondary)] hover:text-[var(--primary)]">Testimonials</a>
        <a href="#" class="text-[var(--text-secondary)] hover:text-[var(--primary)]">Use Cases</a>
        <a href="#" class="text-[var(--text-secondary)] hover:text-[var(--primary)]">Contact</a>
        <a href="#" class="text-center py-2 px-4 rounded-full neon-btn">Get Started</a>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="pt-24 md:pt-32 pb-16 md:pb-24 relative overflow-hidden">
    <div class="absolute inset-0 bg-[var(--secondary)] opacity-70 z-0"></div>
    <div class="container mx-auto px-4 relative z-10">
      <div class="flex flex-col md:flex-row items-center justify-between">
        <div class="md:w-1/2 mb-10 md:mb-0">
          <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 leading-tight">
            Revolutionize Your Workflow with AI Agent Pro
          </h1>
          <p class="text-lg md:text-xl text-[var(--text-secondary)] mb-8">
            Automate tasks, analyze data, and make smarter decisions in real-time with our advanced AI solutions.
          </p>
          <div class="flex flex-col sm:flex-row gap-4">
            <a href="#" class="py-3 px-6 rounded-full neon-btn text-black font-medium">Try Free Demo</a>
            <a href="#" class="py-3 px-6 rounded-full border border-[var(--primary)] text-[var(--primary)] hover:bg-[var(--primary)] hover:text-black transition flex items-center justify-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              Watch Demo Video
            </a>
          </div>
        </div>
        <div class="md:w-1/2">
          <div class="relative w-full max-w-lg mx-auto">
            <img src="https://picsum.photos/600/400" alt="AI Agent Pro Demo" class="rounded-lg shadow-2xl transform hover:scale-105 transition duration-500" />
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Features Section -->
  <section id="features" class="py-16 md:py-24">
    <div class="container mx-auto px-4">
      <h2 class="text-3xl md:text-4xl font-bold text-center mb-16">Why Choose AI Agent Pro?</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-10">
        <div class="feature-card p-8 rounded-xl text-center fade-in" style="animation-delay: 0.2s">
          <div class="w-16 h-16 mx-auto mb-6 bg-[var(--primary)] rounded-full flex items-center justify-center text-black">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold mb-4">Smart Automation</h3>
          <p class="text-[var(--text-secondary)]">
            Reduce manual work by 80% with intelligent task scheduling and workflow optimization.
          </p>
        </div>
        <div class="feature-card p-8 rounded-xl text-center fade-in" style="animation-delay: 0.4s">
          <div class="w-16 h-16 mx-auto mb-6 bg-[var(--accent)] rounded-full flex items-center justify-center text-black">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold mb-4">Real-Time Analytics</h3>
          <p class="text-[var(--text-secondary)]">
            Process terabytes of data in seconds with predictive insights and machine learning models.
          </p>
        </div>
        <div class="feature-card p-8 rounded-xl text-center fade-in" style="animation-delay: 0.6s">
          <div class="w-16 h-16 mx-auto mb-6 bg-[var(--primary)] rounded-full flex items-center justify-center text-black">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold mb-4">Enterprise Security</h3>
          <p class="text-[var(--text-secondary)]">
            Military-grade encryption and compliance with GDPR/ISO 27001 standards for data protection.
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- Testimonials Section -->
  <section id="testimonials" class="py-16 md:py-24 bg-[var(--secondary)]">
    <div class="container mx-auto px-4">
      <h2 class="text-3xl md:text-4xl font-bold text-center mb-16">Trusted by Industry Leaders</h2>
      <div class="relative max-w-4xl mx-auto">
        <div class="testimonial-card p-8 rounded-xl mb-6">
          <p class="text-[var(--text-secondary)] italic mb-6">"AI Agent Pro transformed our operations. The automation capabilities alone saved us 200+ hours monthly."</p>
          <div class="flex items-center">
            <img src="https://picsum.photos/100/100" alt="John Doe" class="w-12 h-12 rounded-full mr-4" />
            <div>
              <p class="font-medium">John Doe</p>
              <p class="text-sm text-[var(--text-secondary)]">CTO, TechCorp</p>
            </div>
          </div>
        </div>
        <div class="testimonial-card p-8 rounded-xl mb-6">
          <p class="text-[var(--text-secondary)] italic mb-6">"The predictive analytics helped us reduce costs by 35% in just three months. Truly game-changing technology."</p>
          <div class="flex items-center">
            <img src="https://picsum.photos/101/100" alt="Jane Smith" class="w-12 h-12 rounded-full mr-4" />
            <div>
              <p class="font-medium">Jane Smith</p>
              <p class="text-sm text-[var(--text-secondary)]">CEO, DataSolutions</p>
            </div>
          </div>
        </div>
        <div class="testimonial-card p-8 rounded-xl">
          <p class="text-[var(--text-secondary)] italic mb-6">"Our team's productivity increased by 60% after implementing AI Agent Pro. It's the best investment we've made."</p>
          <div class="flex items-center">
            <img src="https://picsum.photos/102/100" alt="Michael Johnson" class="w-12 h-12 rounded-full mr-4" />
            <div>
              <p class="font-medium">Michael Johnson</p>
              <p class="text-sm text-[var(--text-secondary)]">Operations Director, HealthTech</p>
            </div>
          </div>
        </div>
        <div class="flex justify-center mt-8 space-x-3">
          <button id="prevTestimonial" class="text-[var(--text-secondary)] hover:text-[var(--primary)]">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
            </svg>
          </button>
          <div class="flex space-x-2">
            <div id="dot1" class="dot active"></div>
            <div id="dot2" class="dot"></div>
            <div id="dot3" class="dot"></div>
          </div>
          <button id="nextTestimonial" class="text-[var(--text-secondary)] hover:text-[var(--primary)]">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </section>

  <!-- CTA Section -->
  <section class="py-16 md:py-24 bg-[var(--primary)] text-white text-center">
    <div class="container mx-auto px-4">
      <h2 class="text-3xl md:text-4xl font-bold mb-6">Ready to Transform Your Business?</h2>
      <p class="text-lg md:text-xl mb-8 max-w-2xl mx-auto">
        Join 500+ companies using AI Agent Pro to automate tasks, analyze data, and make smarter decisions.
      </p>
      <a href="#" class="py-3 px-8 rounded-full neon-btn text-black font-medium">Get Started Free</a>
    </div>
  </section>

  <!-- Footer -->
  <footer class="bg-[var(--secondary)] text-[var(--text-secondary)] py-12">
    <div class="container mx-auto px-4">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <div class="md:col-span-1">
          <h3 class="text-xl font-bold text-[var(--primary)] mb-4">AI Agent Pro</h3>
          <p class="text-sm">
            Empowering businesses with intelligent automation and data-driven insights since 2024.
          </p>
        </div>
        <div>
          <h4 class="text-lg font-semibold mb-4 text-[var(--primary)]">Quick Links</h4>
          <ul class="space-y-2">
            <li><a href="{{ route('home') }}" class="hover:text-[var(--primary)]">Home</a></li>
            <li><a href="#" class="hover:text-[var(--primary)]">Features</a></li>
            <li><a href="#" class="hover:text-[var(--primary)]">Contact</a></li>
          </ul>
        </div>
        <div>
          <h4 class="text-lg font-semibold mb-4 text-[var(--primary)]">Contact Us</h4>
          <ul class="space-y-2">
            <li>Email: support@aiagentpro.com</li>
            <li>Phone: +1 (555) 123-4567</li>
            <li>Address: 123 Innovation Drive, Tech City</li>
          </ul>
        </div>
        <div>
          <h4 class="text-lg font-semibold mb-4 text-[var(--primary)]">Newsletter</h4>
          <p class="mb-4">Subscribe for the latest updates and AI insights</p>
          <form class="flex flex-col sm:flex-row gap-2">
            <input type="email" placeholder="Your email" class="px-4 py-2 rounded-lg text-black" required />
            <button type="submit" class="py-2 px-4 rounded-lg neon-btn text-black">Subscribe</button>
          </form>
        </div>
      </div>
      <div class="border-t border-[var(--text-secondary)] mt-12 pt-8 flex flex-col md:flex-row justify-between items-center">
        <p class="text-sm mb-4 md:mb-0">© 2024 AI Agent Pro. All rights reserved.</p>
        <div class="flex space-x-4">
          <a href="#" class="text-[var(--text-secondary)] hover:text-[var(--primary)]">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
              <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"></path>
            </svg>
          </a>
          <a href="#" class="text-[var(--text-secondary)] hover:text-[var(--primary)]">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.8