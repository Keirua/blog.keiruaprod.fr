---
title: Useful Unix debugging commands
layout: post
lang: en
---

I forget about this all the time, so here are some commands I often use for debugging/devops

# systemd

```bash
    systemctl list-units
    
    systemctl status unit_name
    service unit_name start|stop|status
```

Some apps have logs in a directory (often /var/log), some can be read directly using `journalctl`:

```bash
journalctl -u unit_name --since "2019-12-04 00:00:00" --until "2019-12-05 23:00" 

journalctl -u unit_name --follow
```

# network

```bash
$ netstat -ntlp
```

# Open files

```bash
ulimit -n
lsof -p 13 | wc -l
lsof -p $(pgrep ds_proxy) | wc -l
```

# htop

htop is pretty useful, it's interesting to see where the numbers come from under the hood: [htop explained](https://peteris.rocks/blog/htop/).

