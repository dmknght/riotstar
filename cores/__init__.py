lab_images = [
    ("phpLdapAdmin", "phpLdapAdmin multiple vulns", "vulnerables/phpldapadmin-remote-dump"),  # OK
    ("DVWA", "PHP/MySQL vulnerable web app. Login: admin/password", "vulnerables/web-dvwa"),  # OK
    # ("RailsGoat", "Vulnerable WebApp in Ruby on Rails Framework", "vulnerables/web-owasp-railsgoat"),
    # ("SambaCry", "SambaCry RCE vulnerability (CVE-2017-7494 Samba 4.5.9)", "vulnerables/cve-2017-7494"), broken proto
    # ("HarakaMail", "Haraka mail 2.8.9 RCE", "vulnerables/mail-haraka-2.8.9-rce"),
    # ("Shellshock", "CVE 2014-6271 Bashdoor", "vulnerables/cve-2014-6271"),
    # ("Heartbleed", "CVE-2014-0160 OpenSSL Data leak", "vulnerables/cve-2014-0160"),
    ("SpringSecurityOauth", "CVE-2016-4977 Spring Security Oauth RCE", "vulnerables/cve-2016-4977"), # seems ok
    ("OpenSSHDenialofService", "CVE-2016-6515 OpenSSH before 7.3 CPU consumption", "vulnerables/cve-2016-6515"), # seems ok
    ("RoundcubeRCE", "Roundcube WebMail server 1.0.0 - 1.2.2 RCE", "vulnerables/web-roundcube-1.2.2-rce"), # http error redirect to https but no https
    # ("WebGoatPHP", "Vulnerable PHP Web App", "vulnerables/web-owasp-phpgoat"), manifest unknown
    # ("NodeGoat", "Vulnerable NodeJS Web App", "vulnerables/web-owasp-nodegoat"), manifest unknown
    # ("Mutillidae2", "OWASP's Mutillidae 2 vulnerable Web app", "vulnerables/web-owasp-mutillidae2"), manifest unknown
    # ("bWAPP", "Vulnerable PHP Web App", "vulnerables/web-bwapp"), manifest unknown
    # ("BrokenWebApp", "OWASP Broken Web Applications", "vulnerables/web-owasp"), manifest unknown
    ("PHPMailer", "PHPMailer < 5.2.18 RCE", "vulnerables/cve-2016-10033"), # ok
    ("ApacheStruts2", "CVE-2017-5638 Apache Struts 2 File Upload", "jrrdev/cve-2017-5638"), # ok
    # ("OracleWebLogic", "CVE-2017-10271 Oracle WebLogic 10.3.6.0.0 WLS-WSAT Deserialization", "kkirsche/cve-2017-10271"), # manifest unknown
    ("Drupal8RCE", "CVE-2019-6340 Drupal RCE", "knqyf263/cve-2019-6340"),  # OK
    ("gruyere", "google-gruyere vulnerable web app", "karthequian/gruyere") # OK
]
