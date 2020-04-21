Diffie-Hellman Key Exchange

Diffie-Hellman key exchange is a way to agree on a shared secret between 2 entities who never talked to each other, and without ever sending this secret over an insecure channel. This is particularly useful for any kind of security on a public network. It is for instance used in some variants of SSL/TLS, which is used to encrypt communications on HTTPS websites. Let's see how it works:

Alice and Bob want to agree on a secret color. They first choose a common base color, which is public (anyone can access it). Let's say it's yellow. They also each choose a personnal secret, respectively As and Bs. Let's say As = blue, and Bs = Red
Alice and Bob can now prepare their mixes Am and Bm, by adding the public color to their personnal secret color.
Am = yellow + As = yellow + blue = green
Bm = yellow + Bs = yellow + red = orange

Now, A and B can send their mixed colors to each other. They can compute the shared secret (As = Bs = S) by adding their personnal secret to the 
As = Bm + As = orange + blue = brown
Bs = Am + Bs = green + red = brown

Now A and B both have the same secret As = Bs, which can then be used for encrypting the upcoming communications. This work because yellow + blue + red = yellow + red + blue, that is to say because adding colors is **commutative**.

You can also note that they never sent it over the wire: Alice and Bob only sent the mixed color. 

One important property is that it should be hard to reverse the process. In this example, it's easy to add colors: yellow + blue = green, but it's generally hard to substract colors: yellow - green does not really make sense, so finding the secret color out of the mixed color is hard to do.

Let's summarize the process:

 - Users decide on some public color over the public communication channel
 - You create your own private secret. It won't be exchanged
 - You generate a public "mix" color using the previously agreed upon public value, combined with your private color. You can send it to the other person.
 - You compute the shared secret your partner's public color, your private color, and the shared public color initially chosen
 - Your result will match that of your partner, who did the same thing.
 - Done! You now have a shared secret, and it never crossed the public medium!

The actual algorithm does not involve colors, but numbers. Very large prime numbers, where the main operation − modular exponentiation − is hard to reverse. Interestingly, mathematicians have good reasons to think it is, but it has not been proven whether they are right or wrong.
 
This algorithm is very important, but it lacks a major property: authentication. What proves Alice is actually preparing a secret with Bob? Nothing. A malicious Mallory could be between Alice and Bob without them knowing it (this is called a man in the middle attack). Mallory could perform this key exchange with both genuine users in order to listen to the secured communications. Mallory could then decrypt the communications in order understand them, then recrypt them in order for Alice and Bob to think they are having a secured communication with each other, while they actually are having an insecure one with Mallory.