/**
 * 轮询工具函数
 */

export interface PollingOptions {
  interval?: number // 轮询间隔（毫秒），默认1000ms
  maxAttempts?: number // 最大尝试次数，默认60次
  onSuccess?: (data: any) => void // 成功回调
  onError?: (error: any) => void // 错误回调
  onTimeout?: () => void // 超时回调
  shouldStop?: (data: any) => boolean // 判断是否停止轮询的函数
}

/**
 * 轮询函数
 * @param pollFn 轮询函数，返回Promise
 * @param options 轮询选项
 * @returns 停止轮询的函数
 */
export function poll(
  pollFn: () => Promise<any>,
  options: PollingOptions = {}
): () => void {
  const {
    interval = 1000,
    maxAttempts = 60,
    onSuccess,
    onError,
    onTimeout,
    shouldStop = (data: any) => data.status === 'completed' || data.status === 'failed'
  } = options

  let attempts = 0
  let isStopped = false

  const stop = () => {
    isStopped = true
  }

  const execute = async () => {
    if (isStopped) return

    try {
      const data = await pollFn()
      attempts++

      if (shouldStop(data)) {
        if (onSuccess) {
          onSuccess(data)
        }
        return
      }

      if (attempts >= maxAttempts) {
        if (onTimeout) {
          onTimeout()
        }
        return
      }

      setTimeout(execute, interval)
    } catch (error) {
      if (onError) {
        onError(error)
      }
    }
  }

  execute()

  return stop
}

