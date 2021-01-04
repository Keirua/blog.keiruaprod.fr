# Monitoring and Improving performances in a web app

The generic idea is a top down approach:

 - use a monitoring tool to identify the performance issues
 - pick a performance problem you want to tackle
 - find ways to reproduce the scenarios you want to improve
 - find the local performances bottleneck, and improve them


# Monitoring

Rails has a very good service for that: skylight.

Download a gem, setup your account, and you are done.

After a while, it'll show you the pains points of your apps based on the most frequent pages used

# pick a performance problem you want to tackle

We have limited resources, so we can't focus on everything. So we picked a very frequent page: the dashboard page

# find ways to reproduce the scenarios you want to improve

In a rails console:

    $ Instructeur.joins(:follows).group(:id).order('COUNT(follows.id) DESC').limit(10)
    # yay
    $ Instructeur.find(9499).follows.count
    => 131482 # wait what

# find the local performances bottleneck, and improve them

## Caching data

    i = Instructeur.find(some_id)
    # before
    i.followed_dossiers.with_notifications(i)
    ActiveRecord::QueryCanceled (PG::QueryCanceled: ERROR:  canceling statement due to statement timeout)
    # after
    Flipper.enable(:cached_notifications, i)
    i.followed_dossiers.with_notifications(i)
    Dossier Load (2378.0ms)


    if I take another user, the gap is pretty impressive:
    # sans le flag
      Dossier Load (33563.8ms)
    # avec
      Dossier Load (204.9ms)


    i = Instructeur.find some_id
    i.procedures_with_notifications(:en_cours)
    Procedure Load (32000.8ms)
    Flipper.enable(:cached_notifications, i)
    i.procedures_with_notifications(:en_cours)
    Procedure Load (1118.6ms)
