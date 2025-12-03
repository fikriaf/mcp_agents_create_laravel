/**
 * GenLaravel Frontend Configuration
 * 
 * For production deployment:
 * - Backend: Railway (set BACKEND_URL below)
 * - Frontend: Vercel (this file)
 */

const CONFIG = {
    // ============================================
    // 🔧 PRODUCTION CONFIG - UPDATE THESE!
    // ============================================
    
    // Railway backend URL (update after deployment)
    // Example: 'https://genlaravel-backend-production.up.railway.app'
    RAILWAY_BACKEND_URL: null,  // Set this after Railway deployment!
    
    // ============================================
    
    // Backend WebSocket/API URL (auto-detect)
    get BACKEND_URL() {
        // 1. Use Railway URL if configured
        if (this.RAILWAY_BACKEND_URL) {
            return this.RAILWAY_BACKEND_URL;
        }
        
        // 2. Local development
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return 'http://localhost:8080';
        }
        
        // 3. Vercel preview/production - need Railway URL
        console.warn('⚠️ RAILWAY_BACKEND_URL not configured! Set it in config.js');
        return 'http://localhost:8080';  // Fallback
    },

    // WebSocket protocol (auto-detect based on backend URL)
    get WS_PROTOCOL() {
        if (this.BACKEND_URL.startsWith('https://')) {
            return 'wss:';
        }
        return 'ws:';
    },

    // Laravel preview URL (only works locally)
    LARAVEL_URL: 'http://localhost:8000',

    // Unified WebSocket endpoint (recommended)
    WS_UNIFIED_ENDPOINT: '/ws/generate',
    
    // Legacy endpoints (kept for backward compatibility)
    WS_SINGLE_ENDPOINT: '/ws/generate/single',
    WS_MULTI_ENDPOINT: '/ws/generate/multi',

    // Get WebSocket URL
    getWebSocketUrl(endpoint) {
        const host = this.BACKEND_URL.replace(/^https?:\/\//, '');
        return `${this.WS_PROTOCOL}//${host}${endpoint}`;
    },
    
    // Get unified WebSocket URL
    getUnifiedWebSocketUrl() {
        return this.getWebSocketUrl(this.WS_UNIFIED_ENDPOINT);
    },

    // Get API URL
    getApiUrl(endpoint) {
        return `${this.BACKEND_URL}${endpoint}`;
    },
    
    // Check queue status before connecting
    async checkQueueStatus() {
        try {
            const response = await fetch(this.getApiUrl('/api/queue/status'));
            return await response.json();
        } catch (error) {
            console.error('Failed to check queue status:', error);
            return { is_busy: false, queue_size: 0, message: 'Unknown' };
        }
    },
    
    // Check if running in production
    isProduction() {
        return this.RAILWAY_BACKEND_URL !== null;
    },
    
    // Debug: log current config
    debug() {
        console.log('🔧 GenLaravel Config:');
        console.log('  BACKEND_URL:', this.BACKEND_URL);
        console.log('  WS_PROTOCOL:', this.WS_PROTOCOL);
        console.log('  WS_URL:', this.getUnifiedWebSocketUrl());
        console.log('  isProduction:', this.isProduction());
    }
};

// Auto-debug in development
if (window.location.hostname === 'localhost') {
    CONFIG.debug();
}
