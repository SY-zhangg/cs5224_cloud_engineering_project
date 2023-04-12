const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function (app) {
    app.use(
        '/setup',
        createProxyMiddleware({
            target: 'https://test-vedhika.d186pebvqnkz8n.amplifyapp.com/',
            changeOrigin: true,
        })
    );
    app.use(
        '/search',
        createProxyMiddleware({
            target: 'https://test-vedhika.d186pebvqnkz8n.amplifyapp.com/',
            changeOrigin: true,
        })
    );
    app.use(
        '/predict',
        createProxyMiddleware({
            target: 'https://test-vedhika.d186pebvqnkz8n.amplifyapp.com/',
            changeOrigin: true,
        })
    );
};