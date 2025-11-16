/**
 * GenLaravel Frontend Configuration
 * 
 * For production, update these URLs to match your deployment
 */

const CONFIG = {
    // Backend WebSocket/API URL
    BACKEND_URL: window.location.hostname === 'localhost'
        ? 'http://localhost:8080'
        : window.location.origin, // Use same origin in production

    // WebSocket protocol
    WS_PROTOCOL: window.location.protocol === 'https:' ? 'wss:' : 'ws:',

    // Laravel preview URL
    LARAVEL_URL: 'http://localhost:8000',

    // Get WebSocket URL
    getWebSocketUrl(endpoint) {
        const host = this.BACKEND_URL.replace(/^https?:\/\//, '');
        return `${this.WS_PROTOCOL}//${host}${endpoint}`;
    },

    // Get API URL
    getApiUrl(endpoint) {
        return `${this.BACKEND_URL}${endpoint}`;
    }
};

// For production, you can override via environment or build process
if (typeof PRODUCTION_CONFIG !== 'undefined') {
    Object.assign(CONFIG, PRODUCTION_CONFIG);
}
