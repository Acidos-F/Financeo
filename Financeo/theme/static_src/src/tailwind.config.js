/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../../templates/**/*.html',
    '../../**/templates/**/*.html',
    './src/**/*.js'
  ],
  theme: {
    extend: {
      colors: {
        'custom-green-bg': '#318f76',       // Main background green
        'custom-sidebar': '#3a4a46',        // Darker sidebar green-gray
        'custom-sidebar-active': '#2a3633', // Darkest active item
      },
    },
  },
  plugins: [],
}
