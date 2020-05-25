# blog.keiruaprod.fr

This repositoy hosts my technical blog hosted on [blog.keiruaprod.fr](blog.keiruaprod.fr).

Todo:

 - [x] integrate social cards
 - [x] add contribution link
 - [x] generate code social cards from code
 - [ ] generating blog post file (eg http://www.guyroutledge.co.uk/blog/automate-jekyll-post-creation-with-thor)
 - [ ] generate empty social cards from site title
 - [x] html-proofer
  - [ ] fix issues ;)
 - [ ] add author card
 - [ ] better i18n (https://github.com/untra/polyglot ?)
 - [ ] add sitemap (https://github.com/jekyll/jekyll-sitemap ?)
 - [ ] see SEO tags https://github.com/jekyll/jekyll-seo-tag/blob/master/docs/usage.md ?
 - [ ] add/write a linter (https://github.com/plainionist/Plainion.JekyllLint)

## Tools

The blog uses [Jekyll](https://jekyllrb.com/)
The theme is [Contrast](https://github.com/niklasbuschmann/contrast-demo).

## Validation

[html-proofer](https://github.com/gjtorikian/html-proofer) helps to ensure the generated HTML is valid. It is available as a rake task.

```
bundle exec rake test
```

## Social cards

Code samples are generated with [`carbon-now`](https://github.com/mixn/carbon-now-cli). You need yarn, and node.

```bash
$ yarn global add carbon-now-cli
```

When you have it, you can run a script that will generate all the missing

```bash
python generate-social-cards.py
```