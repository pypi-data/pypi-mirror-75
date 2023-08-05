https-letsencrypt-libs:
  pkg.installed:
    - pkgs: 
      - libgit2-dev

https-letsencrypt-pip:
  pip.installed:
    - names:
      - pygit2
    - reload_modules: True
