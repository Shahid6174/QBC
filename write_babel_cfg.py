with open('babel.cfg', 'w', encoding='utf-8') as f:
    f.write('[python: **.py]\n')
    f.write('[jinja2: **/templates/**.html]\n')
    f.write('extensions=jinja2.ext.autoescape,jinja2.ext.with_\n') 