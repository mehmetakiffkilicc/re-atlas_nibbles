import { Component, type ReactNode } from 'react'

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error?: Error
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, info: { componentStack: string }) {
    console.error('[RE-Atlas] Component error:', error, info.componentStack)
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? (
        <div className="flex items-center justify-center w-full h-full bg-bg-primary">
          <div className="glass-panel p-6 rounded-2xl border border-red-500/20 max-w-md text-center">
            <div className="text-red-400 text-2xl mb-2">⚠</div>
            <p className="text-text-primary font-semibold mb-1">Bağlantı hatası</p>
            <p className="text-text-muted text-sm">Backend API'ye ulaşılamıyor. Backend'in çalıştığından emin olun.</p>
            <button
              onClick={() => this.setState({ hasError: false })}
              className="mt-4 px-4 py-2 text-xs bg-accent-wind/10 border border-accent-wind/30 text-accent-wind rounded-lg hover:bg-accent-wind/20 transition-colors"
            >
              Yeniden dene
            </button>
          </div>
        </div>
      )
    }
    return this.props.children
  }
}
