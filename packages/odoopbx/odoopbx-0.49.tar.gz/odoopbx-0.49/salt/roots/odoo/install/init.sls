include:
  - .server
  - .addons
  - .frontend

{% if grains.virtual != 'container' %}
odoo-service-start:
  service.running:
    - name: odoo
    - enable: true
    - require:
      - cmd: odoo-addons-init
{% endif %}
