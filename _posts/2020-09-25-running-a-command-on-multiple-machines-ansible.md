---
title: Running a shell command on multiple machines using ansible
layout: post
lang: en
---

I always forget **how to run a command on multiples machines**:

```bash
# Running a shell command on a bunch of machines
ansible -i inventories/dev webservers -m shell -a 'systemctl stop delayed_job' --become
```

It's also useful to be able to run a task by tag:

```bash
# Listing what will be run
ansible-playbook -t delayed_job -i inventories/dev webservers.yml --list-tasks
# dry-run of a task 
ansible-playbook -t delayed_job -i inventories/dev webservers.yml --check --diff
# Really running a task
ansible-playbook -t delayed_job -i inventories/dev webservers.yml
```
