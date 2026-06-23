import client from './client'

export interface Item {
  id: number
  title: string
  description: string | null
  created_at: string
}

export interface ItemCreate {
  title: string
  description?: string | null
}

export async function getItems(): Promise<Item[]> {
  const { data } = await client.get<Item[]>('/items')
  return data
}

export async function createItem(payload: ItemCreate): Promise<Item> {
  const { data } = await client.post<Item>('/items', payload)
  return data
}

export async function deleteItem(id: number): Promise<void> {
  await client.delete(`/items/${id}`)
}

export interface ComputeRequest {
  op: 'fibonacci' | 'hash'
  value: number
}

export interface ComputeResponse {
  task_id: string
  result: number | string | Record<string, string>
}

export async function computeTask(payload: ComputeRequest): Promise<ComputeResponse> {
  const { data } = await client.post<ComputeResponse>('/tasks/compute', payload)
  return data
}
