---
title: Listing DelayedJob cron jobs and schedules
author: Keirua
layout: post
lang: en
image: cron-jobs-list.rb.png 
---

A small helper that I sometimes have to run on different machines. Out of all the jobs, it finds those registered as cron tasks, and displays their schedule in yaml (the `y` function).

```ruby
cron_jobs = Delayed::Job.where('cron is not null')
y (cron_jobs.map do |c| [c.handler.match("job_class: (.*)\n")[1], c.cron] end)
---
- - SomeJob
  - 0 6 * * *
- - SomeOtherJob
  - 0 0 * * *
- - AgainAnotherJob
  - "* * * * *"
- - YetAnotherJob
  - 0 0 1 * *
- - ComplexScheduleNotificationJob
  - 0 10 * * 1,2,3,4,5,6
```

Not the most robust code out there for sure. Yet robustness and clarity are not what you always need, and these 2 lines can be pasted in a rails console quite easily.