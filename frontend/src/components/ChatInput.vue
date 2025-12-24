<template>
  <div class="chat-input">
    <el-input
      v-model="inputText"
      type="textarea"
      :rows="3"
      placeholder="输入消息..."
      @keydown.ctrl.enter="handleSend"
      @keydown.meta.enter="handleSend"
      :disabled="loading"
    />
    <div class="input-actions">
      <el-button
        type="primary"
        :loading="loading"
        @click="handleSend"
        :disabled="!inputText.trim()"
      >
        发送 (Ctrl+Enter)
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Emits {
  (e: 'send', message: string): void
}

const emit = defineEmits<Emits>()

const inputText = ref('')
const loading = defineModel<boolean>('loading', { default: false })

const handleSend = () => {
  if (!inputText.value.trim() || loading.value) return
  
  const message = inputText.value.trim()
  inputText.value = ''
  emit('send', message)
}

defineExpose({
  clear: () => {
    inputText.value = ''
  }
})
</script>

<style scoped>
.chat-input {
  padding: 16px;
  background: white;
  border-top: 1px solid #e0e0e0;
}

.input-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 8px;
}
</style>

