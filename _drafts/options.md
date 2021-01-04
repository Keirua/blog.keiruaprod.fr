options.md

Options for deploying and running a web application

I've spent a lot of time recently trying… not to spend a lot of time doing devops. Let's see what the options are regarding 3 problems:

 - provisionning the machines in order to run your application
 - deploying a new version of the code in production
 - monitoring that everything is alright

That's a very, very high level overview

# The rejected options

The base of SRE, 

 - **manual configuration of the server**: if you lose your server (it happens), you may need to bring a new one. If you do that by hand, the odds are low that you'll setup your machine(s) in the same way. Some kind of automation is desirable for 
 - **manual development, or deployment of code**, via ftp. It's 2020, we want at least to have some kind of versionning of our code.