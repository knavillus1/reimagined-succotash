export const debugEnabled = import.meta.env.VITE_ENABLE_DEBUG === 'true'

export function debugLog(...args: unknown[]) {
  if (debugEnabled) {
    console.log('[DEBUG]', ...args)
  }
}
