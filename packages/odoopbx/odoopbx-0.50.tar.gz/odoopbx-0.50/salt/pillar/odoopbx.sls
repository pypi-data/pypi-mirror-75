security_ports_udp: 5060,65060
security_ports_tcp: 80,443,5038,5039,5060,5061,65060,8088,8089
letsencrypt:
  use_package: false
  post_renew:
    cmds:
      - service asterisk reload
  config: |
    email = mailbox@odooist.com    
    # Testing
    # server = https://acme-staging-v02.api.letsencrypt.org/directory
    # Production
    server = https://acme-v02.api.letsencrypt.org/directory
    authenticator = standalone
    # Use only when having nginx
    # authenticator = webroot
    # webroot-path = /var/lib/www
    agree-tos = True
    renew-by-default = False 
  domainsets:
    www:
      - devmax.odoopbx.com
  cron:
    minute: 10
    hour: 2
    dayweek: 1
