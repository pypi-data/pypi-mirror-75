{%- from "odoo/map.jinja" import odoo with context -%}

odoo-pkg-deps:
  pkg.installed:
    - pkgs: [python3-apt,]
    - refresh: true
    - require_in:
      - pkgrepo: odoo-pkgs

odoo-pkgs:
  pkgrepo.managed:
    - humanname: Odoo Official Repository
    - name: deb https://nightly.odoo.com/{{ odoo.rev }}/nightly/deb/ ./
    - file: /etc/apt/sources.list.d/odoo.list
    - key_url: https://nightly.odoo.com/odoo.key
  pkg.installed:
    - pkgs:
      - odoo
    - require:
      - pkgrepo: odoo-pkgs

odoo-configs:
  file.managed:
    - names:
      - /etc/odoo/odoo.conf:
        - source: salt://odoo/templates/odoo.conf
        - group: {{ odoo.user }}
        - mode: 640
      - /etc/systemd/system/odoo.service:
        - source: salt://odoo/templates/odoo.service
    - user: root
    - mode: 644
    - template: jinja
    - context: {{ odoo }}
    - backup: minion
    - require:
      - pkg: odoo-pkgs

{% if grains.virtual == 'container' %}
odoo-postgresql:
  cmd.run:
    - name: pg_ctlcluster {{ odoo.pg_ver }} main start
    - runas: postgres
    - unless:
      - pidof postgres
    - require:
      - pkg: odoo-pkgs
    - require_in:
      - postgres_user: odoo-dbuser
{% else %}
odoo-service-stop:
  service.dead:
    - name: odoo
    - require:
      - file: odoo-configs
{% endif %}

odoo-dbuser:
  postgres_user.present:
    - name: {{ odoo.user }}
    - createdb: True
    - encrypted: True
    - db_user: postgres
    - require:
      - pkg: odoo-pkgs

odoo-init:
  cmd.run:
    - name: odoo -d {{ odoo.dbname }} -c /etc/odoo/odoo.conf --no-http --stop-after-init  -i base
    - runas: {{ odoo.user }}
    - shell: /bin/bash
    - unless: echo "env['res.users']" | odoo shell -c /etc/odoo/odoo.conf --no-http
    - require:
      - postgres_user: odoo-dbuser
