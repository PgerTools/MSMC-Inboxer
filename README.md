# MSMC-Inbox
Simple addon for MSMC that inboxes valid mails for emails like Steam, Roblox, Discord and more.

## Adding to MSMC 
Adding this to MSMC is very simple.

Go to the root of MSMC and create a new folder called extra then download and place inbox.py there.
![](https://media.discordapp.net/attachments/1212680059119341578/1245922627743252490/image.png?ex=665a835e&is=665931de&hm=5be4e1bef01831ccbc98dab5b680f58c80c42d482d20654339109c6e930485dc&=&format=webp&quality=lossless)

Now open MSMC.py and add the following import.

```py
from extra.inbox import inboxmail
```
![](https://cdn.discordapp.com/attachments/1212680059119341578/1245923518533599252/image.png?ex=665a8432&is=665932b2&hm=ca1ea163ca1a218c3e88637e0dfde51fea9c740b3fe384c5711c615414349a80&)

Search for the validmail function. (You can do this using Ctrl+F)

Add the end of this function add the following code.

```py
inboxmail(email, password)
```
![](https://media.discordapp.net/attachments/1212680059119341578/1245924160539197461/image.png?ex=665a84cc&is=6659334c&hm=eed06bfb103947a32d7b7c88ceb64343205e43147d4a1982a578391038ef645a&=&format=webp&quality=lossless)

Now all you have to do is open inbox.py and edit the config. I will add a seperate proper config in the future.

You can pick to enable/disable each check and edit the discord webhook there.
