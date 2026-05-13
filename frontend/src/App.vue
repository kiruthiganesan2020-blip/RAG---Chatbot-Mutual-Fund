<template>
  <div id="app">
    <header class="app-header">
      <h1>HDFC Mutual Fund RAG Assistant</h1>
      <p>Your trusted advisor for mutual fund information</p>
    </header>
    
    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<script>
/**
 * Main Vue Application Component
 */
export default {
  name: 'App'
}
