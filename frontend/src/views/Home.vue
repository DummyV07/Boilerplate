<template>
  <div class="min-h-screen bg-neutral-50 p-8">
    <div class="mx-auto max-w-3xl">
      <header class="mb-8">
        <h1 class="text-3xl font-bold text-neutral-900">Fullstack Template</h1>
        <p class="mt-2 text-neutral-600">FastAPI + Vue 3 全栈项目模版</p>
      </header>

      <section class="mb-8 rounded-xl bg-white p-6 shadow-sm">
        <h2 class="mb-4 text-lg font-semibold">创建 Item</h2>
        <form class="space-y-4" @submit.prevent="handleCreate">
          <div>
            <label class="mb-1 block text-sm font-medium text-neutral-700">标题</label>
            <input
              v-model="title"
              type="text"
              required
              data-testid="item-title-input"
              class="w-full rounded-lg border border-neutral-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
              placeholder="输入标题"
            />
          </div>
          <div>
            <label class="mb-1 block text-sm font-medium text-neutral-700">描述</label>
            <textarea
              v-model="description"
              data-testid="item-description-input"
              class="w-full rounded-lg border border-neutral-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
              placeholder="可选描述"
              rows="3"
            />
          </div>
          <button
            type="submit"
            data-testid="item-create-button"
            class="rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
            :disabled="appStore.loading"
          >
            创建
          </button>
        </form>
      </section>

      <section class="mb-8 rounded-xl bg-white p-6 shadow-sm">
        <div class="mb-4 flex items-center justify-between">
          <h2 class="text-lg font-semibold">Item 列表</h2>
          <button
            data-testid="item-refresh-button"
            class="text-sm text-blue-600 hover:underline"
            @click="loadItems"
          >
            刷新
          </button>
        </div>
        <p v-if="appStore.loading" class="text-neutral-500">加载中...</p>
        <p v-else-if="items.length === 0" class="text-neutral-500">暂无数据</p>
        <ul v-else class="divide-y divide-neutral-100">
          <li
            v-for="item in items"
            :key="item.id"
            class="flex items-start justify-between py-3"
            :data-testid="`item-row-${item.id}`"
          >
            <div>
              <p class="font-medium text-neutral-900">{{ item.title }}</p>
              <p v-if="item.description" class="mt-1 text-sm text-neutral-600">
                {{ item.description }}
              </p>
            </div>
            <button
              class="text-sm text-red-600 hover:underline"
              :data-testid="`item-delete-${item.id}`"
              @click="handleDelete(item.id)"
            >
              删除
            </button>
          </li>
        </ul>
      </section>

      <section class="rounded-xl bg-white p-6 shadow-sm">
        <h2 class="mb-4 text-lg font-semibold">CPU 任务演示 (multiprocessing)</h2>
        <div class="flex items-end gap-4">
          <div>
            <label class="mb-1 block text-sm font-medium text-neutral-700">Fibonacci(n)</label>
            <input
              v-model.number="fibN"
              type="number"
              min="0"
              max="40"
              data-testid="fib-input"
              class="w-32 rounded-lg border border-neutral-300 px-3 py-2"
            />
          </div>
          <button
            data-testid="fib-compute-button"
            class="rounded-lg bg-neutral-800 px-4 py-2 text-white hover:bg-neutral-900 disabled:opacity-50"
            :disabled="appStore.loading"
            @click="handleCompute"
          >
            计算
          </button>
        </div>
        <p v-if="computeResult" class="mt-4 text-sm text-neutral-700">
          结果: <code class="rounded bg-neutral-100 px-2 py-1">{{ computeResult }}</code>
        </p>
      </section>

      <p v-if="appStore.error" class="mt-4 text-sm text-red-600">{{ appStore.error }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import {
  computeTask,
  createItem,
  deleteItem,
  getItems,
  type Item,
} from '@/api/items'
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()
const items = ref<Item[]>([])
const title = ref('')
const description = ref('')
const fibN = ref(20)
const computeResult = ref<string | number | null>(null)

async function loadItems() {
  appStore.setLoading(true)
  appStore.setError(null)
  try {
    items.value = await getItems()
  } catch (err) {
    appStore.setError(err instanceof Error ? err.message : '加载失败')
  } finally {
    appStore.setLoading(false)
  }
}

async function handleCreate() {
  appStore.setLoading(true)
  appStore.setError(null)
  try {
    await createItem({
      title: title.value,
      description: description.value || null,
    })
    title.value = ''
    description.value = ''
    await loadItems()
  } catch (err) {
    appStore.setError(err instanceof Error ? err.message : '创建失败')
  } finally {
    appStore.setLoading(false)
  }
}

async function handleDelete(id: number) {
  appStore.setLoading(true)
  appStore.setError(null)
  try {
    await deleteItem(id)
    await loadItems()
  } catch (err) {
    appStore.setError(err instanceof Error ? err.message : '删除失败')
  } finally {
    appStore.setLoading(false)
  }
}

async function handleCompute() {
  appStore.setLoading(true)
  appStore.setError(null)
  computeResult.value = null
  try {
    const response = await computeTask({ op: 'fibonacci', value: fibN.value })
    computeResult.value = response.result
  } catch (err) {
    appStore.setError(err instanceof Error ? err.message : '计算失败')
  } finally {
    appStore.setLoading(false)
  }
}

onMounted(() => {
  loadItems()
})
</script>
