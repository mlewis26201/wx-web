FROM allinurl/goaccess:latest
ENTRYPOINT []
CMD ["goaccess", "/logs/access.log", "-o", "/webstats/report.html", "-p", "/etc/goaccess/goaccess.conf"]
