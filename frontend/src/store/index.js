import { createStore } from 'vuex';

/**
 * Vuex Store for Chat Application
 * Manages application state including messages, user session, and UI state
 */
const store = createStore({
  state: {
    messages: [],
    currentUser: null,
    sessionId: localStorage.getItem('sessionId') || null,
    isLoading: false,
    isTyping: false,
    theme: localStorage.getItem('theme') || 'light',
    sidebarOpen: false
  },
  
  mutations: {
    // Message mutations
    ADD_MESSAGE(state, payload) {
      state.messages.push({
        id: Date.now().toString(),
        type: 'user',
        content: payload.content,
        timestamp: new Date().toISOString()
      });
    },
    
    // UI state mutations
    SET_LOADING(state, isLoading) {
      state.isLoading = isLoading;
    },
    
    SET_TYPING(state, isTyping) {
      state.isTyping = isTyping;
    },
    
    SET_THEME(state, theme) {
      state.theme = theme;
    },
    
    SET_SIDEBAR_OPEN(state, isOpen) {
      state.sidebarOpen = isOpen;
    },
    
    SET_CURRENT_USER(state, user) {
      state.currentUser = user;
    },
    
    SET_SESSION_ID(state, sessionId) {
      state.sessionId = sessionId;
    }
  },
  
  actions: {
    // Message actions
    addMessage({ commit }, message) {
      store.commit('ADD_MESSAGE', { message });
    },
    
    // UI actions
    setLoading({ commit }, isLoading) {
      store.commit('SET_LOADING', { isLoading });
    },
    
    setTyping({ commit }, isTyping) {
      store.commit('SET_TYPING', { isTyping });
    },
    
    setTheme({ commit }, theme) {
      store.commit('SET_THEME', { theme });
    },
    
    toggleSidebar({ commit }) {
      store.commit('SET_SIDEBAR_OPEN', { isOpen: !store.state.sidebarOpen });
    },
    
    setCurrentUser({ commit }, user) {
      store.commit('SET_CURRENT_USER', { user });
    },
    
    setSessionId({ commit }, sessionId) {
      store.commit('SET_SESSION_ID', { sessionId });
    }
  },
  
  getters: {
    // Message getters
    allMessages: (state) => state.messages,
    lastMessage: (state) => state.messages[state.messages.length - 1] || null,
    currentUser: (state) => state.currentUser,
    sessionId: (state) => state.sessionId,
    isLoading: (state) => state.isLoading,
    isTyping: (state) => state.isTyping,
    theme: (state) => state.theme,
    sidebarOpen: (state) => state.sidebarOpen
  }
});

export default store;
