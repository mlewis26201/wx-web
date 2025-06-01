FROM allinurl/goaccess:latest
CMD ["/bin/sh", "-c", "goaccess /logs/access.log -o /webstats/report.html --log-format=COMBINED --real-time-html --ws-url=ws://localhost:7890 --daemonize && tail -f /dev/null"]
