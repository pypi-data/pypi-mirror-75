# -*- coding: utf-8 -*-
# vim: ft=sls

{% from "caddy/map.jinja" import caddy with context %}

caddy-pkg-deps:
  pkg.installed:
    - pkgs: {{ caddy.pkgs }}
    - refresh: true

caddy-bindir:
  file.directory:
    - name: {{ caddy.bindir }}
    - state: present
    - mode: 755

caddy-download:
  archive.extracted:
    - name: {{ caddy.bindir }}
    - failhard: True
    - source: 'https://caddyserver.com/download/linux/{{ caddy.platform }}?license=personal&telemetry=off'
    - archive_format: tar
    - skip_verify: true
    - enforce_toplevel: false
    - options: '--exclude=init --exclude=README.txt --exclude=LICENSES.txt --exclude=CHANGES.txt'
{% if caddy.force_update %}
    - overwrite: True
{% else %}
    - unless:
      - ls {{ caddy.bindir }}/caddy
{% endif %}

caddy-setcap:
  cmd.run:
    - name: setcap 'cap_net_bind_service=+ep' {{ caddy.bindir }}/caddy
    - unless: getcap {{ caddy.bindir }}/caddy | grep -q 'cap_net_bind_service+ep'

caddy-identity:
  user.present:
    - name: {{ caddy.user }}
    - system: True
    - usergroup: True

caddy-ssl-dir:
  file.directory:
    - name: /etc/ssl/caddy
    - user: {{ caddy.user }}
    - group: {{ caddy.user }}
    - mode: 700
    - require:
      - user: caddy-identity

caddy-conf-default:
  file.managed:
    - name: /etc/caddy/Caddyfile
    - replace: False
    - makedirs: True
    - contents: "import Caddyfile.d/*.conf"

caddy-conf-import:
  file.replace:
    - name: /etc/caddy/Caddyfile
    - pattern: "^import .*Caddyfile.d/.*"
    - repl: "import Caddyfile.d/*.conf"
    - append_if_not_found: True

caddy-service:
  file.managed:
    - name: /etc/systemd/system/caddy.service
    - source: salt://caddy/caddy.service
    - user: root
    - group: root
    - mode: 0664
    - replace: {{ caddy.force_update }}
    - backup: minion
{% if grains.virtual != "container" %}
  service.running:
    - name: caddy
    - enable: {{ caddy.service_enable }}
    - require:
      - file: caddy-service
{% endif %}
