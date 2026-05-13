<template>
  <div class="chat-interface">
    <div class="chat-container">
      <div class="messages" ref="messagesContainer">
        <div
          v-for="message in messages"
          :key="message.id"
          :class="['message', message.type]"
        >
          <div class="message-content">
            <p>{{ message.text }}</p>
            <div v-if="message.sources && message.sources.length" class="sources">
              <h4>Sources:</h4>
              <ul>
                <li v-for="source in message.sources" :key="source">
                  {{ source }}
                </li>
              </ul>
            </div>
          </div>
          <div class="message-time">
            {{ formatTime(message.timestamp) }}
          </div>
        </div>
        <div v-if="isLoading" class="message assistant loading">
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
      
      <div class="input-container">
        <form @submit.prevent="sendMessage" class="message-form">
          <div class="input-group">
            <input
              v-model="newMessage"
              type="text"
              placeholder="Ask about HDFC Mutual Funds..."
              class="message-input"
              :disabled="isLoading"
              maxlength="500"
            />
            <button
              type="submit"
              class="send-button"
              :disabled="isLoading || !newMessage.trim()"
            >
              <span v-if="!isLoading">Send</span>
              <span v-else>...</span>
            </button>
          </div>
        </form>
        
        <div class="sample-questions">
          <h4>Sample Questions:</h4>
          <div class="question-chips">
            <button
              v-for="question in sampleQuestions"
              :key="question"
              @click="askSampleQuestion(question)"
              class="question-chip"
              :disabled="isLoading"
            >
              {{ question }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { APIService } from '../services/api'

export default {
  name: 'ChatInterface',
  setup() {
    const messages = reactive([])
    const newMessage = ref('')
    const isLoading = ref(false)
    const messagesContainer = ref(null)
    
    const apiService = new APIService()
    
    const sampleQuestions = [
      'What is HDFC Large Cap Fund?',
      'What are the risks of mutual funds?',
      'How do I invest in HDFC funds?',
      'What is NAV in mutual funds?'
    ]
    
    const addMessage = (text, type, sources = []) => {
      messages.push({
        id: Date.now(),
        text,
        type,
        timestamp: new Date(),
        sources
      })
      
      nextTick(() => {
        scrollToBottom()
      })
    }
    
    const scrollToBottom = () => {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    }
    
    const sendMessage = async () => {
      if (!newMessage.value.trim() || isLoading.value) return
      
      const userMessage = newMessage.value.trim()
      addMessage(userMessage, 'user')
      newMessage.value = ''
      isLoading.value = true
      
      try {
        const response = await apiService.sendChatMessage(userMessage)
        
        addMessage(
          response.response,
          'assistant',
          response.source_documents || []
        )
      } catch (error) {
        console.error('Chat error:', error)
        addMessage(
          'Sorry, I encountered an error. Please try again.',
          'error'
        )
      } finally {
        isLoading.value = false
      }
    }
    
    const askSampleQuestion = (question) => {
      newMessage.value = question
      sendMessage()
    }
    
    const formatTime = (timestamp) => {
      return timestamp.toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    onMounted(() => {
      addMessage(
        'Hello! I\'m your HDFC Mutual Fund assistant. How can I help you today?',
        'assistant'
      )
    })
    
    return {
      messages,
      newMessage,
      isLoading,
      messagesContainer,
      sampleQuestions,
      sendMessage,
      askSampleQuestion,
      formatTime
    }
  }
}
</script>

<style scoped>
.chat-interface {
  max-width: 800px;
  margin: 0 auto;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin: 20px;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f8f9fa;
}

.message {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
}

.message.user {
  align-items: flex-end;
}

.message.assistant {
  align-items: flex-start;
}

.message.error {
  align-items: flex-start;
}

.message-content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 18px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.message.user .message-content {
  background: #007bff;
  color: white;
}

.message.assistant .message-content {
  background: white;
  border: 1px solid #e9ecef;
}

.message.error .message-content {
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  color: #721c24;
}

.message-time {
  font-size: 12px;
  color: #6c757d;
  margin-top: 4px;
  padding: 0 8px;
}

.sources {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #e9ecef;
}

.sources h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #495057;
}

.sources ul {
  margin: 0;
  padding-left: 20px;
  font-size: 12px;
  color: #6c757d;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 12px 16px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #6c757d;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.input-container {
  padding: 20px;
  background: white;
  border-top: 1px solid #e9ecef;
}

.message-form {
  margin-bottom: 16px;
}

.input-group {
  display: flex;
  gap: 8px;
}

.message-input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #ced4da;
  border-radius: 24px;
  font-size: 16px;
  outline: none;
  transition: border-color 0.2s;
}

.message-input:focus {
  border-color: #007bff;
}

.message-input:disabled {
  background: #f8f9fa;
  cursor: not-allowed;
}

.send-button {
  padding: 12px 24px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 24px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.send-button:hover:not(:disabled) {
  background: #0056b3;
}

.send-button:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.sample-questions h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #495057;
}

.question-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.question-chip {
  padding: 6px 12px;
  background: #e9ecef;
  border: 1px solid #ced4da;
  border-radius: 16px;
  font-size: 12px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.question-chip:hover:not(:disabled) {
  background: #dee2e6;
}

.question-chip:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .chat-container {
    margin: 10px;
  }
  
  .message-content {
    max-width: 85%;
  }
  
  .input-group {
    flex-direction: column;
  }
  
  .send-button {
    width: 100%;
  }
}
</style>
