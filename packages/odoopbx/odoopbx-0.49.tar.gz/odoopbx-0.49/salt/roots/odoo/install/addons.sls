{%- from "odoo/map.jinja" import odoo with context -%}

odoo-pip-upgrade:
  cmd.run:
    - name: pip3 install --upgrade pip
    - reload_modules: true
    - onfail:
      - pip: odoo-addons

odoo-addons:
  git.latest:
    - name: git@gitlab.com:odoopbx/addons.git
    - branch: {{ odoo.rev }}
    - depth: 1
    - fetch_tags: False
    - rev: {{ odoo.rev }}
    - target: /var/lib/odoo/addons/{{ odoo.rev }}
    - identity: salt://files/id_rsa
  pip.installed:
    - upgrade: {{ odoo.upgrade }}
    - requirements: /var/lib/odoo/addons/{{ odoo.rev }}/requirements.txt
    - require:
      - git: odoo-addons
    - retry: True

odoo-addons-init:
  cmd.run:
    - name: odoo -c /etc/odoo/odoo.conf --no-http --stop-after-init  -i asterisk_base_sip,asterisk_calls_crm
    - runas: {{ odoo.user }}
    - shell: /bin/bash
    - unless: echo "env['asterisk_base.server']" | odoo shell -c /etc/odoo/odoo.conf --no-http
    - require:
      - pip: odoo-addons
