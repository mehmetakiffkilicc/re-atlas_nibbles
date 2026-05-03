import { useAppStore } from '../store/useAppStore'

export function GridLoadingIndicator() {
  const { isGridFetching, viewMode } = useAppStore()

  if (!isGridFetching || viewMode !== 'heatmap') return null

  return (
    <div className="absolute top-0 left-0 right-0 z-[1000] h-[2px] bg-bg-secondary/80">
      <div className="h-full bg-gradient-to-r from-transparent via-accent-wind to-transparent animate-loading-bar" />
    </div>
  )
}
