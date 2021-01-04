---
title: Ways to ensure an email is valid
layout: post
---

Todo:

 - add things about how bounces work, MX records (example with dig), and SPF/DKIM
 - see what https://github.com/afair/email_address/ does in more detail

In most applications, you may want to make sure that the email your users provide
is valid : you want to ensure they'll receive emails, because many things happen through email.
You may send account validation links, bills, notifications, reports… many things that
need to reach your customer. If they don't, they'll probably reach your customer support at some point, be angry, leave, or maybe all of that.

*Validating an email* can mean many things, so here we'll try to check:

 - if a string looks like a valid email
 - if the email is associated to a valid email domain
 - if said email can receive email

It turns out email validation is hard and that we won't succeed.

# Does it look like an email ?

## Suggesting a valid email/domain on the client side

The first option is to ensure that users type an email that look like a valid email.
If someone types john@gmil.com, they probably meant john@gmail.com so it makes sense
to suggest a change before they create an account.

There are various options to do so, we picked [email-butler](https://github.com/Serendipity-AI/email-butler/) which, at the moment of making this feature,
  had a reasonably good support for our needs.

https://github.com/betagouv/demarches-simplifiees.fr/pull/4598

## The regex way

Validation on the client side is a first step. You may want to ensure that what is supplied to your backend is valid too.

```
Devise.email_regexp
=> /\A[^@\s]+@[^@\s]+\z/

invalid_emails = email.select { |e| Devise.email_regexp.match?(e) == false }
```

# Is there an actual email server ?

## Checking the DNS MX and A records

One option is to check 

per [RFC 5321](https://tools.ietf.org/html/rfc5321), if no mx records exist you are to use the A/AAAA of the host name as implicit MX with pref 0.

```ruby
require 'resolv'
# from https://gist.github.com/colszowka/3a59633d54b6adb3e278
class DnsCheck
  attr_reader :host
  def initialize(host)
    @host = host
    @dns = Resolv::DNS.new
    @dns.timeouts = 3 # most of the time a 3 second timeout is enough to get an idea
  end

  def a
    @a ||= @dns.getresources(host, Resolv::DNS::Resource::IN::A)
  end

  def a?
    a.any?
  end

  def mx
    @mx ||= @dns.getresources(host, Resolv::DNS::Resource::IN::MX)
  end

  def mx?
    mx.any?
  end
end

emails = ["validdomain@yahoo.fr", "invalid@probably-do-not-exist-ecisecuiseiuet.com"]
domains = emails.map { |e| e.split('@')[1] }.sort.uniq
domains.each do |d|
    begin
        dns_check = DnsCheck.new(d)
        if !dns_check.mx?
            if !dns_check.a?
                print(d) 
                print("\n")
            end
        end
    rescue Encoding::CompatibilityError => e
        puts "Rescued: #{e.inspect} for #{d}"
    end
end
```

## The bad idea: sending a probe email


There are solutions like [kamilc/email_verifier](https://github.com/kamilc/email_verifier) that actually connects to a given mail server and ask if the address in question exists for real. This sounds promising, but this is asking for trouble with no garantee of results.

 - opening a random TCP connection for your web host is a great way to get the webhost blocked
 - the server may refuse to answer because you are not from whitelisted domain

## Blacklisting domains

One option to ensure your user will read your emails is to ensure it is not from a one-time domain, like yopmail.

There are dozens of such blacklists on the web, like this one.

https://gist.githubusercontent.com/adamloving/4401361/raw/db901ef28d20af8aa91bf5082f5197d27926dea4/temporary-email-address-domains

## Using bounces

Might look at something like VERP or other bounce automated bounce processing so if/when the verification email bounces you can use the information in the return path to do something with the account.

# The dark ways

Depending on the volume of emails, you can do things by hand to some extent.

This is not something we do, but it makes sense to know it exist: I'm writing this
both as a developper who want to ensure users receive emails, and as a user who make to protect its emails from spammers.

### Using open source intelligence

Tools like [theHarvester](https://github.com/laramies/theHarvester) will let you scan a domain using various search engines for email lying around.

### Using SaaS solutions

Some SaaS solutions do the same thing, build a database of emails, they can also cross-reference emails from multiple database, use emails from leaked databases, so… this is ethically very disputable. Be careful who you want to trust, and who you are sending your user emails in order to check their validity, because you may be giving your users a disservice.


# Ensuring your email can be received

Not to be a downer, but even if the target email is valid, your recipient may not receive it. There are so many things to do here. 

## properly configuring the server

 - DKIM, SPF… You server or email provider should be properly configured for sending trustable emails

## spam protection

 - warm up your domain ; recipient hate spikes out ouf nowhere.

## manual fixes

 - You can sometimes check if there was no hard bounce of the email/domain