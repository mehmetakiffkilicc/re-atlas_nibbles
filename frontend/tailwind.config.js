/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        'bg-primary': '#0B1220',
        'bg-secondary': '#111A2E',
        'bg-card': '#162035',
        'score-high': '#22C55E',
        'score-medium': '#FACC15',
        'score-low': '#EF4444',
        'accent-solar': '#F59E0B',
        'accent-wind': '#3B82F6',
        'accent-hybrid': '#8B5CF6',
        'text-primary': '#F1F5F9',
        'text-muted': '#94A3B8',
        'border-subtle': '#1E2D45',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}
