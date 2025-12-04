// Service Worker para PWA
const CACHE_NAME = 'vendavoa-v1';
const STATIC_ASSETS = [
    '/',
    '/dashboard',
    '/static/css/style.css',
    '/static/js/app.js',
    '/static/manifest.json'
];

// Instalação do Service Worker
self.addEventListener('install', event => {
    console.log('Service Worker: Instalando...');
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Service Worker: Cache aberto');
                return cache.addAll(STATIC_ASSETS);
            })
            .then(() => {
                console.log('Service Worker: Arquivos estáticos cacheados');
                return self.skipWaiting();
            })
    );
});

// Ativação do Service Worker
self.addEventListener('activate', event => {
    console.log('Service Worker: Ativando...');
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Service Worker: Removendo cache antigo:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => {
            console.log('Service Worker: Ativado');
            return self.clients.claim();
        })
    );
});

// Interceptação de requests (estratégia Network First para APIs, Cache First para assets)
self.addEventListener('fetch', event => {
    const { request } = event;
    
    // Pular requisições que não são HTTP/HTTPS
    if (!request.url.startsWith('http')) {
        return;
    }

    // Estratégia para APIs (sempre tentar rede primeiro)
    if (request.url.includes('/api/') || request.url.includes('/auth/') || 
        request.url.includes('/cars/') || request.url.includes('/clients/') || 
        request.url.includes('/docs/')) {
        
        event.respondWith(
            fetch(request)
                .then(response => {
                    // Se a resposta for válida, cache ela
                    if (response.status === 200) {
                        const responseClone = response.clone();
                        caches.open(CACHE_NAME).then(cache => {
                            cache.put(request, responseClone);
                        });
                    }
                    return response;
                })
                .catch(() => {
                    // Se falhar, tenta buscar no cache
                    return caches.match(request).then(response => {
                        if (response) {
                            return response;
                        }
                        // Se não tiver no cache, retorna uma resposta de erro
                        return new Response(
                            JSON.stringify({ error: 'Sem conexão e dados não disponíveis offline' }),
                            {
                                status: 503,
                                statusText: 'Service Unavailable',
                                headers: { 'Content-Type': 'application/json' }
                            }
                        );
                    });
                })
        );
        return;
    }

    // Estratégia Cache First para assets estáticos
    event.respondWith(
        caches.match(request)
            .then(response => {
                if (response) {
                    return response;
                }
                
                // Se não estiver no cache, busca na rede
                return fetch(request)
                    .then(response => {
                        // Só cachear respostas válidas
                        if (response.status === 200 && response.type === 'basic') {
                            const responseClone = response.clone();
                            caches.open(CACHE_NAME).then(cache => {
                                cache.put(request, responseClone);
                            });
                        }
                        return response;
                    })
                    .catch(() => {
                        // Se for uma página HTML e não conseguir carregar, retorna página offline
                        if (request.headers.get('Accept').includes('text/html')) {
                            return new Response(
                                `
                                <!DOCTYPE html>
                                <html>
                                <head>
                                    <title>VendaVoa - Offline</title>
                                    <meta charset="UTF-8">
                                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                    <style>
                                        body { 
                                            font-family: Arial, sans-serif; 
                                            text-align: center; 
                                            padding: 50px; 
                                            background: #f5f5f5;
                                        }
                                        .offline-message {
                                            background: white;
                                            padding: 2rem;
                                            border-radius: 8px;
                                            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                                            max-width: 400px;
                                            margin: 0 auto;
                                        }
                                        h1 { color: #2563eb; }
                                        .retry-btn {
                                            background: #2563eb;
                                            color: white;
                                            border: none;
                                            padding: 10px 20px;
                                            border-radius: 5px;
                                            cursor: pointer;
                                            margin-top: 20px;
                                        }
                                    </style>
                                </head>
                                <body>
                                    <div class="offline-message">
                                        <h1>📱 VendaVoa</h1>
                                        <h2>Você está offline</h2>
                                        <p>Verifique sua conexão com a internet e tente novamente.</p>
                                        <button class="retry-btn" onclick="window.location.reload()">
                                            Tentar Novamente
                                        </button>
                                    </div>
                                </body>
                                </html>
                                `,
                                { 
                                    headers: { 'Content-Type': 'text/html' }
                                }
                            );
                        }
                    });
            })
    );
});

// Escutar mensagens do cliente (para atualizações)
self.addEventListener('message', event => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});

// Sincronização em background (quando voltar online)
self.addEventListener('sync', event => {
    if (event.tag === 'background-sync') {
        console.log('Service Worker: Sincronização em background');
        // Aqui você pode implementar lógica para sincronizar dados quando voltar online
    }
});