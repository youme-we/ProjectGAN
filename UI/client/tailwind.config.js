** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        "white-brown": "#F5F9E9",
        "light-brown": "#C2C1A5",
        "dark-gray": "#515751",
        "blue-gray": "#596869",
        "dark-green": "#36453B",
      },
      gridTemplateColumns: {
        custom: "32px 1fr 1fr",
      },
    },
  },
  plugins: [],
};
