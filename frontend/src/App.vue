<script setup>
import { ref, onMounted } from 'vue'

const appStatus = ref('Loading...')

const checkHealth = async () => {
  try {
    const response = await fetch('/api/health')
    const data = await response.json()
    appStatus.value = data.message || 'API Connected'
  } catch (error) {
    appStatus.value = 'API Connection Failed'
    console.error('Health check failed:', error)
  }
}

onMounted(() => {
  checkHealth()
})
</script>

<template>
  <div class="app">
    <header class="header">
      <h1>🎵 GOMORA</h1>
      <p class="tagline">Music Streaming Platform</p>
    </header>
    
    <main class="main">
      <div class="status-card">
        <h2>Welcome to GOMORA</h2>
        <p>API Status: <span class="status">{{ appStatus }}</span></p>
        <p class="info">Frontend with Vercel Analytics enabled ✅</p>
      </div>
      
      <div class="features">
        <h3>Features</h3>
        <ul>
          <li>🔐 User Authentication (JWT)</li>
          <li>🎼 Music Library & Search</li>
          <li>🎧 Music Player</li>
          <li>📝 Playlists Management</li>
          <li>⭐ Favorites System</li>
          <li>📊 Web Analytics (Vercel)</li>
        </ul>
      </div>
    </main>
    
    <footer class="footer">
      <p>Powered by Vue.js + Flask + Vercel Analytics</p>
    </footer>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.header {
  text-align: center;
  padding: 2rem 1rem;
}

.header h1 {
  font-size: 3rem;
  margin: 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.tagline {
  font-size: 1.2rem;
  margin: 0.5rem 0 0;
  opacity: 0.9;
}

.main {
  flex: 1;
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
  width: 100%;
}

.status-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.status-card h2 {
  margin-top: 0;
  font-size: 2rem;
}

.status {
  font-weight: bold;
  color: #a0f0b0;
}

.info {
  margin-top: 1rem;
  font-size: 0.9rem;
  opacity: 0.8;
}

.features {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.features h3 {
  margin-top: 0;
  font-size: 1.5rem;
}

.features ul {
  list-style: none;
  padding: 0;
}

.features li {
  padding: 0.5rem 0;
  font-size: 1.1rem;
}

.footer {
  text-align: center;
  padding: 2rem 1rem;
  opacity: 0.8;
}
</style>
