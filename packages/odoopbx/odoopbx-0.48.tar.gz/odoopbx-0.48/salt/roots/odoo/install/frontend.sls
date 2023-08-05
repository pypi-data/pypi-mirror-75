odoo-caddyfile:
  file.managed:
    - name: /etc/caddy/Caddyfile.d/odoopbx.conf
    - source: salt://odoo/templates/caddy.conf
    - template: jinja
    - makedirs: True
