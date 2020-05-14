cron_jobs = Delayed::Job.where('cron is not null')
y (cron_jobs.map do |c| [c.handler.match("job_class: (.*)\n")[1], c.cron] end)