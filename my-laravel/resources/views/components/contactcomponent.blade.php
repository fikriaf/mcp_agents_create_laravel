<!-- resources/views/components/contact-component.blade.php -->
<main class="bg-dark-800 py-12 px-6">
  <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12">
    <!-- Contact Form -->
    <div class="bg-dark-700 rounded-xl p-8 shadow-neon-blue">
      <h2 class="text-3xl font-bold text-white mb-6">Get in Touch</h2>
      <form class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-gray-300 mb-2" for="name">Name</label>
            <input class="w-full px-4 py-3 bg-dark-600 border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-neon-blue text-white" 
                   type="text" id="name" required>
          </div>
          <div>
            <label class="block text-gray-300 mb-2" for="email">Email</label>
            <input class="w-full px-4 py-3 bg-dark-600 border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-neon-blue text-white" 
                   type="email" id="email" required>
          </div>
        </div>
        <div>
          <label class="block text-gray-300 mb-2" for="company">Company</label>
          <input class="w-full px-4 py-3 bg-dark-600 border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-neon-blue text-white" 
                 type="text" id="company">
        </div>
        <div>
          <label class="block text-gray-300 mb-2" for="message">Message</label>
          <textarea class="w-full px-4 py-3 bg-dark-600 border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-neon-blue text-white h-32 resize-none" 
                    id="message" required></textarea>
        </div>
        <button class="w-full py-3 px-6 bg-neon-blue hover:bg-neon-blue/90 text-dark-800 font-medium rounded-lg transition-transform hover:scale-105 transform-gpu">
          Submit Request
        </button>
      </form>
    </div>

    <!-- Office Information -->
    <div class="space-y-8">
      <h2 class="text-3xl font-bold text-white">Our Offices</h2>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- New York Office -->
        <div class="bg-dark-700 p-6 rounded-xl border border-gray-800">
          <div class="flex items-center mb-4">
            <div class="w-10 h-10 rounded-full bg-neon-blue/20 flex items-center justify-center mr-4">
              <svg class="w-5 h-5 text-neon-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white">New York</h3>
          </div>
          <p class="text-gray-300 mb-4">123 AI Street, Tech Tower 456, New York, NY 10001</p>
          <a class="text-neon-blue hover:text-neon-blue/80 flex items-center mb-4" 
             href="https://maps.google.com" target="_blank">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
            </svg>
            View on Google Maps
          </a>
          <p class="text-gray-400 text-sm">Mon-Fri: 9:00 AM - 6:00 PM EST</p>
        </div>

        <!-- Berlin Office -->
        <div class="bg-dark-700 p-6 rounded-xl border border-gray-800">
          <div class="flex items-center mb-4">
            <div class="w-10 h-10 rounded-full bg-neon-green/20 flex items-center justify-center mr-4">
              <svg class="w-5 h-5 text-neon-green" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white">Berlin</h3>
          </div>
          <p class="text-gray-300 mb-4">456 Neural Lane, Innovation District, 10115 Berlin</p>
          <a class="text-neon-green hover:text-neon-green/80 flex items-center mb-4" 
             href="https://maps.google.com" target="_blank">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
            </svg>
            View on Google Maps
          </a>
          <p class="text-gray-400 text-sm">Mon-Fri: 8:00 AM - 5:00 PM CET</p>
        </div>
      </div>

      <!-- Social Proof -->
      <div class="bg-dark-700 p-6 rounded-xl border border-gray-800">
        <div class="flex items-center mb-6">
          <div class="w-10 h-10 rounded-full bg-neon-purple/20 flex items-center justify-center mr-4">
            <svg class="w-5 h-5 text-neon-purple" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold text-white">Trusted by Industry Leaders</h3>
        </div>
        <div class="flex flex-wrap gap-6 mb-6">
          <img class="h-8 w-auto" src="https://tailwindui.com/img/logos/tailwindcss-logo.svg" alt="Tailwind CSS">
          <img class="h-8 w-auto" src="https://tailwindui.com/img/logos/algolia-logo.svg" alt="Algolia">
          <img class="h-8 w-auto" src="https://tailwindui.com/img/logos/segment-logo.svg" alt="Segment">
          <img class="h-8 w-auto" src="https://tailwindui.com/img/logos/intercom-logo.svg" alt="Intercom">
          <img class="h-8 w-auto" src="https://tailwindui.com/img/logos/vimeo-logo.svg" alt="Vimeo">
        </div>
        <a class="inline-flex items-center text-neon-purple hover:text-neon-purple/80 font-medium" 
           href="#brochure">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
          </svg>
          Download Full Brochure
        </a>
      </div>
    </div>
  </div>
</main>