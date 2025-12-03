<div class="space-y-1 relative">
    <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
    <input 
        type="password" 
        id="password" 
        name="password" 
        required 
        class="input w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-primary focus:border-transparent text-sm transition-all duration-200"
        placeholder="••••••••"
    />
    <button type="button" id="togglePassword" class="password-toggle">Show</button>
    <p id="passwordError" class="error-message text-sm text-red-600">Password must be at least 8 characters</p>
</div>