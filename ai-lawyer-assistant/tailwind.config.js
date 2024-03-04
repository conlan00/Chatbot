/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'kanit': ['Kanit', 'cursive']
      },
      width: {
        '85-screen': '85vw',
        '60-screen': '60vw',
      },
    },
  },
  plugins: [],
}

