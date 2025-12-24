<template>
  <div class="loading-spinner">
    <div class="spinner"></div>
    <span class="loading-text">AI正在思考...</span>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.loading-spinner {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  justify-content: flex-start;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-text {
  color: #666;
  font-size: 14px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>

