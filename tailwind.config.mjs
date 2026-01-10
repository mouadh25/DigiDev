/** @type {import('tailwindcss').Config} */
export default {
    content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
    theme: {
        extend: {
            colors: {
                'void': '#050505',
                'cyan': {
                    500: '#06b6d4',
                },
                'lime': {
                    500: '#84cc16',
                },
                'orange': {
                    500: '#f97316',
                },
            },
            fontFamily: {
                'display': ['Space Grotesk', 'sans-serif'],
                'body': ['Inter', 'sans-serif'],
                'mono': ['JetBrains Mono', 'monospace'],
            },
            backgroundImage: {
                'gradient-innovation': 'linear-gradient(135deg, #06b6d4 0%, #84cc16 50%, #f97316 100%)',
            },
        },
    },
    plugins: [],
};
