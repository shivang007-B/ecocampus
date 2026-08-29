/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cyberBg: "#080c0e",
        cyberCard: "rgba(14, 22, 26, 0.85)",
        neonEmerald: "#10F0A0",
        neonCyan: "#00E5FF",
        primary: "#10F0A0",
        secondary: "#059669",
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['Fira Code', 'monospace'],
        display: ['Orbitron', 'sans-serif'],
      },
      boxShadow: {
        'neon-emerald': '0 0 20px rgba(16, 240, 160, 0.3)',
        'neon-cyan': '0 0 20px rgba(0, 229, 255, 0.3)',
        'cyber-glass': '0 8px 32px 0 rgba(0, 0, 0, 0.4)',
      },
      animation: {
        fadeIn: "fadeIn 0.4s ease-in-out",
        cyberPulse: "cyberPulse 2s ease-in-out infinite",
      },
      keyframes: {
        fadeIn: {
          from: { opacity: "0", transform: "translateY(4px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        cyberPulse: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.5" },
        },
      },
    },
  },
  plugins: [],
}
