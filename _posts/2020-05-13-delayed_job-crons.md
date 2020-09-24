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

Another option when you want to mess with this jobs in the console is to parse the `job_class` using the Yaml component:

```ruby
Delayed::Job.pluck(:handler).map { |h|  YAML.load(h).job_data["job_class"] }.group_by{|x| x}.map {|k, v| [k, v.count] }
```

Aaaaand another useful command is to list the error count. Here is a quick and dirty way: it takes the first line of the stack trace, strips the numbers (ids) and sorts the errors by count:

```ruby
y Delayed::Job.where.not(last_error: nil).pluck(:last_error).map {|e| e&.lines[0].tr('0123456789', '')}.tally.sort_by(&:last)
```

Also, sometimes you want the objects that lead to these errors:

```ruby
y Delayed::Job.where("last_error ilike '%worksheet%'").pluck(:handler).map { |h|  YAML.load(h).job_data["arguments"] }
---
- - _aj_globalid: gid://app/SomeModel/23648
- - _aj_globalid: gid://app/SomeModel/2364
```