import os, re

code = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-R1B1HL5W61"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-R1B1HL5W61');
</script>"""

for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root: continue
    for file in files:
        if file.endswith('.html') or file.endswith('.py'):
            p = os.path.join(root, file)
            try:
                content = open(p, 'r', encoding='utf-8', errors='ignore').read()
                if 'G-R1B1HL5W61' not in content and '</head>' in content:
                    open(p, 'w', encoding='utf-8').write(content.replace('</head>', code + '\n</head>'))
            except Exception: pass
