module.exports = {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        'light-bg': '#F4E7E1',
        'primary': '#FF9B45',
        'secondary': '#D5451B',
        'dark-accent': '#521C0D',
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui'],
      },
      typography: (theme) => ({
        DEFAULT: {
          css: {
            color: theme('colors.dark-accent'),
            a: {
              color: theme('colors.primary'),
              '&:hover': { color: theme('colors.secondary') },
            },
            h1: { color: theme('colors.dark-accent') },
            h2: { color: theme('colors.dark-accent') },
            h3: { color: theme('colors.secondary') },
            blockquote: {
              borderLeftColor: theme('colors.secondary'),
              color: theme('colors.dark-accent'),
            },
            code: {
              backgroundColor: theme('colors.light-bg'),
              padding: '0.25rem 0.375rem',
              borderRadius: '0.25rem',
            },
            'code::before': { content: 'none' },
            'code::after': { content: 'none' },
          },
        },
      }),
    },
  },
  plugins: [require('@tailwindcss/typography')],
}
