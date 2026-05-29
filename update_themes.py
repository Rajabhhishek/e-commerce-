import os, re

folder = r'c:\Users\Hp\OneDrive\Desktop\e- commerce\templates\customer'

new_head = """    <script>
        if (localStorage.getItem('theme') === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
        function toggleTheme() {
            if (document.documentElement.classList.contains('dark')) {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('theme', 'light');
                document.getElementById('theme-icon').innerText = 'dark_mode';
            } else {
                document.documentElement.classList.add('dark');
                localStorage.setItem('theme', 'dark');
                document.getElementById('theme-icon').innerText = 'light_mode';
            }
        }
    </script>
    <style>
        :root {
            --color-background: #f8fafc;
            --color-surface: #ffffff;
            --color-surface-container: #f1f5f9;
            --color-surface-container-low: #f8fafc;
            --color-surface-container-high: #e2e8f0;
            --color-surface-container-highest: #cbd5e1;
            --color-on-background: #0f172a;
            --color-on-surface: #0f172a;
            --color-on-surface-variant: #475569;
            --color-primary: #4f46e5;
            --color-primary-container: #e0e7ff;
            --color-on-primary: #ffffff;
            --color-secondary: #0d9488;
            --color-on-secondary: #ffffff;
            --color-tertiary: #d97706;
            --color-outline: #94a3b8;
            --color-outline-variant: #cbd5e1;
            --color-error: #ef4444;
        }
        .dark {
            --color-background: #050a17;
            --color-surface: #0d1426;
            --color-surface-container: #111a30;
            --color-surface-container-low: #090f1d;
            --color-surface-container-high: #1a2540;
            --color-surface-container-highest: #223154;
            --color-on-background: #dae2fd;
            --color-on-surface: #dae2fd;
            --color-on-surface-variant: #94a3b8;
            --color-primary: #bdc2ff;
            --color-primary-container: #818cf8;
            --color-on-primary: #131e8c;
            --color-secondary: #44e2cd;
            --color-on-secondary: #003731;
            --color-tertiary: #f7bd3e;
            --color-outline: #475569;
            --color-outline-variant: #334155;
            --color-error: #f87171;
        }
        body {
            background-color: var(--color-background);
            transition: background-color 0.3s ease, color 0.3s ease;
        }
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        .glass-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.4) 0%, rgba(255,255,255,0.1) 100%);
            backdrop-filter: blur(20px);
            border: 1px solid var(--color-outline-variant);
        }
        .dark .glass-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%);
            border: 1px solid rgba(255,255,255,0.05);
        }
        .premium-glass {
            background: linear-gradient(145deg, var(--color-surface-container), var(--color-surface));
            box-shadow: inset 0 1px 1px rgba(255,255,255,0.1), 0 8px 32px rgba(0,0,0,0.1);
        }
    </style>
    <script id="tailwind-config">
        tailwind.config = {
          darkMode: "class",
          theme: {
            extend: {
              "colors": {
                      "background": "var(--color-background)",
                      "surface": "var(--color-surface)",
                      "surface-container": "var(--color-surface-container)",
                      "surface-container-low": "var(--color-surface-container-low)",
                      "surface-container-high": "var(--color-surface-container-high)",
                      "surface-container-highest": "var(--color-surface-container-highest)",
                      "on-background": "var(--color-on-background)",
                      "on-surface": "var(--color-on-surface)",
                      "on-surface-variant": "var(--color-on-surface-variant)",
                      "primary": "var(--color-primary)",
                      "primary-container": "var(--color-primary-container)",
                      "on-primary": "var(--color-on-primary)",
                      "secondary": "var(--color-secondary)",
                      "on-secondary": "var(--color-on-secondary)",
                      "tertiary": "var(--color-tertiary)",
                      "outline": "var(--color-outline)",
                      "outline-variant": "var(--color-outline-variant)",
                      "error": "var(--color-error)"
              },
              "borderRadius": {
                      "DEFAULT": "0.25rem",
                      "lg": "0.5rem",
                      "xl": "0.75rem",
                      "2xl": "1rem",
                      "3xl": "1.5rem",
                      "full": "9999px"
              },
              "fontFamily": {
                      "body-md": ["Inter"],
                      "headline-lg-mobile": ["Hanken Grotesk"],
                      "title-md": ["Hanken Grotesk"],
                      "headline-lg": ["Hanken Grotesk"],
                      "label-sm": ["JetBrains Mono"]
              }
            }
          }
        }
    </script>
</head>"""

new_button = """            <button onclick="toggleTheme()" class="p-2 rounded-xl hover:bg-surface-container-high/60 transition-colors flex items-center justify-center relative">
                <span id="theme-icon" class="material-symbols-outlined text-primary">light_mode</span>
            </button>
            <button class="p-2 rounded-xl hover:bg-surface-container-high/60 transition-colors flex items-center justify-center relative">
                <span class="material-symbols-outlined text-primary">notifications</span>
                <span class="absolute top-1.5 right-1.5 w-2 h-2 bg-secondary rounded-full"></span>
            </button>"""

init_script = """
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            if (document.documentElement.classList.contains('dark')) {
                document.getElementById('theme-icon').innerText = 'light_mode';
            } else {
                document.getElementById('theme-icon').innerText = 'dark_mode';
            }
        });
    </script>
</body>"""

for filename in os.listdir(folder):
    if filename.endswith('.html'):
        filepath = os.path.join(folder, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace head section
        # Finds <style> up to </script>\s*</head>
        content = re.sub(r'<style>.*?</script>\s*</head>', new_head, content, flags=re.DOTALL)
        
        # Replace the notification button block with theme button + notification button
        content = re.sub(
            r'<button class="[^"]*?">\s*<span class="material-symbols-outlined text-primary">notifications</span>.*?</button>',
            new_button,
            content,
            flags=re.DOTALL
        )
        
        if 'theme-icon' not in content:
            pass # Handle gracefully
            
        # add script to bottom of page to init icon, only if not already added
        if "document.addEventListener('DOMContentLoaded', () => {" not in content:
            content = content.replace('</body>', init_script)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated {filename}')
