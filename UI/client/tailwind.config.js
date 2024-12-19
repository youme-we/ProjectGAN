/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    colors: {
      "white-brown":"#F5F9E9",
      "light-brown":"#C2C1A5",
      "dark-gray":"#515751",
      "blue-gray":"#596869",
      "dark-green":"#36453B",
    },
    extend: {
      gridTemplateColumns: {
        'custom': '32px 1fr 1fr',
      }
    },
  },
  plugins: [],
}
