I spent way too much time trying not to spend too much time on a memory issue.



It's all quiet until we allocate a lot of memory. At one point, we had +10Gb in 2minutes.
A machine went from 15gb to 48Gb of memory usage at 11pm. Restarting puma solves the problem temporarily,
but I won't spend my life looking at grafana boards or waiting for notifications to reboot puma : we need to find the root cause.

On a web3 qui est monté de ~3Go après le restart à 13h30, à environ 40Go maintenant (17h30). Delayed_job est hors sujet. Ce qui me chagrine avec cette histoire, c'est que la montée mémoire soit pas uniforme, ya tjrs un serveur qui prend considérable plus de mémoire et plus vite que les autres (edited) 


j'ai aussi essayé de regarder l'usage mémoire d'une journée standard, cette notion existe pas trop :smile:
par contre on voit que c'est pas un problème tout nouveau, le 25/05 on était à fond les ballons de mémoire par ex aussi
http://localhost:9001/d/cnwfP-Diz/telegraf-metrics?panelId=12054&fullscreen&orgId=1&var-datasource=default&var-server=web1&var-server=web2&var-server=web3&var-server=web4&var-inter=$__auto_interval_inter&from=1590400800005&to=1590573600003
pareil le 10/05, web4 à 50Go. Le 30/04 c'est web1, le 14/04 web2…
on fait jouer des grosses tâches cron à certaines dates mais ce ne sont pas les dates où il y a des pics mémoires.
donc c'est pas nouveau qu'on monte en mémoire, mais avec la hausse du trafic, on monte plus vite


les suspects sont
exports
cartos
j'ai pas vu d'exports durant les pics de cette nuit (j'ai regardé quelques appels en particulier durant 2 pics de 2 mn ou on a pris +5 et +10Go). Si on ignore l'intuition, les candidats peuvent être:
archive zip
pdf d'un dossier
api v1 et graphQL



Looking at the logs didnt lead to anything:
 - Nothing seem obvious, even at night when trafic is reduced. We still have a lot of trafic though, so visual inspection is very tedious and error-prone.
 - Browsing for leaks in gems did not bring anything.


https://github.com/puma/puma/issues/1600#issuecomment-468291010

99% of memory "leak" issues in Ruby are:

    [Fragmentation](https://www.speedshop.co/2017/12/04/malloc-doubles-ruby-memory.html).
    An old C extension in your dependencies.

List of leaky gems:
https://github.com/ASoftCo/leaky-gems

Ca ne semble pas être:
 - les exports excel/csv: pas d'appel à download_export durant les pics mémoire
 - les exports pdf: peu de requêtes durant les pics mémoire, pas de leak connu
 - les zip: pas d'export zip durant 2 des pics mémoire
ça exclue pas mal de gems tierces et d'usages non web.


https://www.spacevatican.org/2019/5/4/debugging-a-memory-leak-in-a-rails-app/+


# 

Let's do some analysis

## Mini profiler

Turns out we have mini profiler

https://www.justinweiss.com/articles/a-new-way-to-understand-your-rails-apps-performance/

## Static analysis

$ bundle exec derailed bundle:mem
TOP: 117.4141 MiB

Loading our gems use some memory, but that's way less than the memory spikes we face

```bash
$ bundle exec derailed bundle:objects | head 
Measuring objects created by gems in groups [:default, "production"]
Total allocated: 106420853 bytes (1022737 objects)
Total retained:  24225277 bytes (219354 objects)

allocated memory by gem
-----------------------------------
  52905671  activesupport-5.2.4.2
   8188640  skylight-core-4.2.1
   6034358  mime-types-3.3.1
   2736597  mustermann-1.0.3
```

106420853 bytes = 0.106421Gb, so still not the order of magnitude we are looking for. It's normal.