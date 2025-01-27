<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <header class="header">
    <div class="container">
      <div class="brand">
        <HelloWorld msg="Welcome to MyBank" />
      </div>
      <nav class="nav">
        <RouterLink to="/Register" class="nav-link">Register</RouterLink>
        <RouterLink to="/Login" class="nav-link">Login</RouterLink>
      </nav>
    </div>
  </header>

  <main class="main">
    <RouterView />
    <section class="hero">
      <h1>Banking Made Easy</h1>
      <p>Your financial future starts here. Join us today!</p>
      <RouterLink to="/CreateAccountoption" class="cta-button">Get Started</RouterLink>
    </section>

    <section class="features">
      <div class="feature-card">
        <h3>Secure Transactions</h3>
        <p>Experience top-notch security for all your financial transactions.</p>
      </div>
      <div class="feature-card">
        <h3>Easy Access</h3>
        <p>Manage your accounts anywhere, anytime with our modern platform.</p>
      </div>
      <div class="feature-card">
        <h3>24/7 Support</h3>
        <p>We’re here to help, day or night, to ensure your peace of mind.</p>
      </div>
    </section>
  </main>
</template>

<style scoped>
:root {
  --background-color: #000; 
  --text-color: #fff; 
  --header-shadow: 0 4px 12px rgba(255, 255, 255, 0.1);
  --border-radius: 12px; 
  --transition-speed: 0.3s;
  --font-family: 'Poppins', sans-serif;
}

body {
  margin: 0;
  font-family: var(--font-family);
  background-color: var(--background-color);
  color: var(--text-color);
}

.header {
  position: sticky;
  top: 0;
  background-color: #000; 
  box-shadow: var(--header-shadow);
  padding: 1rem 2rem;
  z-index: 1000;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  font-size: 1.8rem; 
  font-weight: bold;
}

.nav {
  display: flex;
  gap: 2rem;
}

.nav-link {
  text-decoration: none;
  padding: 0.5rem 1rem;
  color: var(--text-color); 
  font-weight: 500;
  border-radius: var(--border-radius);
  transition: all var(--transition-speed);
}

.nav-link:hover {
  color: #ccc; 
}

.hero {
  text-align: center;
  padding: 5rem 2rem; 
  background-color: #000; 
  color: var(--text-color); 
  border-radius: var(--border-radius);
  margin: 2rem;
  box-shadow: var(--header-shadow);
}

.hero h1 {
  font-size: 3rem; 
  margin-bottom: 1rem;
}

.hero p {
  font-size: 1.5rem; 
  margin-bottom: 2rem;
}

.cta-button {
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  background-color: #fff; 
  color: #000; 
  font-weight: bold;
  border-radius: var(--border-radius);
  transition: background-color var(--transition-speed), color var(--transition-speed);
}

.cta-button:hover {
  background-color: #ccc; 
  color: #000;
}

.features {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem  padding 2rem;
  justify-content: center;
}

.feature-card {
  flex: 1 1 calc(30% - 2rem);
  background: #111; 
  border-radius: var(--border-radius);
  box-shadow: var(--header-shadow);
  padding: 2rem; 
  text-align: center;
  transition: transform var(--transition-speed), box-shadow var(--transition-speed);
}

.feature-card:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.2); 
}

.feature-card h3 {
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
  color: var(--text-color); 
}

.feature-card p {
  color: var(--text-color);
  font-size: 1.1rem; 
}

@media (max-width: 768px) {
  .nav {
    flex-direction: column;
    gap: 1rem;
  }

  .features {
    flex-direction: column;
    gap: 1rem;
  }

  .feature-card {
    flex: 1 1 100%;
  }
}
</style> ```vue
