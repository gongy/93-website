const defaultTheme = require('tailwindcss/defaultTheme')

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx,svelte}",
  ],
  theme: {
    screens: {
      '2xs': '250px',
      'xs': '400px',
      ...defaultTheme.screens,
    },
    extend: {},
  },
  plugins: [],
}
