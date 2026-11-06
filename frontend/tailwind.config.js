/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        aviation: {
          dark: '#0B0F19',
          card: '#161F30',
          surface: '#25283A',
          muted: '#565A74',
          subtext: '#8B93A7',
          lightBg: '#F8FCFF',
          accentBlue: '#2563EB',
          accentCyan: '#38BDF8',
          borderLight: '#DFEDF8',
          tagBg: '#EFF7FE',
        }
      },
      fontFamily: {
        display: ['Unbounded', 'system-ui', 'sans-serif'],
        benzin: ['Benzin-Bold', 'Benzin-Medium', 'Benzin', 'sans-serif'],
        benzinBold: ['Benzin-Bold', 'Benzin', 'sans-serif'],
        benzinMedium: ['Benzin-Medium', 'Benzin', 'sans-serif'],
        montserratAlt: ['"Montserrat Alternates"', 'sans-serif'],
        travels: ['TT Travels', 'Inter', 'system-ui', 'sans-serif'],
        body: ['Inter', 'system-ui', 'sans-serif'],
        script: ['Caveat', 'cursive'],
      },
      borderRadius: {
        '3xl': '1.75rem',
        '4xl': '2.25rem',
      }
    },
  },
  plugins: [],
}

