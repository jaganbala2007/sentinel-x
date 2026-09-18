const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;
const BACKEND_URL = process.env.BACKEND_URL || 'http://127.0.0.1:8080';

app.use(cors());

// Proxy API requests to the Python FastAPI backend
app.use(
    createProxyMiddleware({
        target: BACKEND_URL,
        changeOrigin: true,
        pathFilter: '/api',
    })
);

// Proxy WebSocket requests to the Python FastAPI backend
app.use(
    createProxyMiddleware({
        target: BACKEND_URL,
        changeOrigin: true,
        ws: true,
        pathFilter: '/ws',
    })
);

// Serve static files from the 'src' directory (and aliases)
app.use(express.static(path.join(__dirname, 'src')));
app.use('/src', express.static(path.join(__dirname, 'src')));
app.use('/frontend/src', express.static(path.join(__dirname, 'src')));

// Serve index.html for root landing page (Public Website)
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'src', 'index.html'));
});
app.get('/index.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'src', 'index.html'));
});

// Serve auth.html for Security Gate
app.get('/auth', (req, res) => {
    res.sendFile(path.join(__dirname, 'src', 'auth.html'));
});
app.get('/auth.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'src', 'auth.html'));
});

// Serve app.html for authenticated Operational Control Room
app.get('/console', (req, res) => {
    res.sendFile(path.join(__dirname, 'src', 'app.html'));
});
app.use('/console', (req, res) => {
    res.sendFile(path.join(__dirname, 'src', 'app.html'));
});
app.get('/app', (req, res) => {
    res.sendFile(path.join(__dirname, 'src', 'app.html'));
});
app.get('/app.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'src', 'app.html'));
});
app.get('/cockpit', (req, res) => {
    res.sendFile(path.join(__dirname, 'src', 'app.html'));
});

// Start the server
const server = app.listen(PORT, () => {
    console.log(`[Node.js Server] 3D Dashboard running at http://localhost:${PORT}`);
    console.log(`[Node.js Proxy] Routing /api and /ws to Python backend at ${BACKEND_URL}`);
});
