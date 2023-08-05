{% from "agent/map.jinja" import agent with context %}

agent-pip-upgrade:
  cmd.run:
    - name: pip3 install --upgrade pip
    - reload_modules: true
    - onfail:
      - pip: agent-install

agent-install:
  pkg.installed:
    - pkgs: {{ agent.pkgs }}
    - refresh: true
  pip.installed:
    - pkgs: {{ agent.pip }}
    - require:
      - pkg: agent-install
    - retry: True

agent-service:
  file:
    - managed
    - name: /etc/systemd/system/odoopbx-agent.service
    - source: salt://agent/agent.service
{% if grains.virtual != "container" %}
  service:
    - running
    - name: odoopbx-agent
    - enable: True
    - require:
      - pip: agent-install
      - pkg: agent-install
      - file: agent-service
{% endif %}
