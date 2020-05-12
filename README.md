# blog.keiruaprod.fr

This repositoy hosts my technical blog hosted on [blog.keiruaprod.fr](blog.keiruaprod.fr).

Todo:

 - [x] integrate social cards
 - [x] add contribution link
 - [] generate code social cards from code
 - [] generating blog post file (eg http://www.guyroutledge.co.uk/blog/automate-jekyll-post-creation-with-thor)
 - [] generate empty social cards from site title
 - [] htmlvalidator
 - [] add author card

## Tools

The blog uses [Jekyll](https://jekyllrb.com/)
The theme is [Contrast](https://github.com/niklasbuschmann/contrast-demo).

## Social cards

Code samples are generated with [`carbon-now`](https://github.com/mixn/carbon-now-cli). You need yarn, and node.

```bash
$ yarn global add carbon-now-cli
```

When you have it, you can run a script that will generate all the missing

```bash
python generate-social-cards.py
```