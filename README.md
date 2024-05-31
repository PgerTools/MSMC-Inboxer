# MSMC-Inbox
Simple addon for MSMC that inboxes valid mails for emails like Steam, Roblox, Discord and more.

https://github.com/MachineKillin/MSMC

msmc is a minecraft account checker that checks through microsoft xbox login instead of the older mojang login. it supports http(s), socks4, socks5 proxies but they must be pretty decent because microsofts authentication is very protective. it also uses tor proxies. it auto installs tor for you if selected.

## Current Checks
- Roblox
- Steam
- Discord (Estimated Year)
- Reddit (Estimated Year)
- Epic Games
- Riot Games
- Rockstar Games

More Checks will be added soon! I also hope to improve the captures.

## Installation (READ THIS)
Adding this to MSMC is very simple.

Go to the root of MSMC and create a new folder called extra then download and place inbox.py there.
![](https://media.discordapp.net/attachments/1212680059119341578/1245922627743252490/image.png?ex=665a835e&is=665931de&hm=5be4e1bef01831ccbc98dab5b680f58c80c42d482d20654339109c6e930485dc&=&format=webp&quality=lossless)

Now edit ``MSMC.py`` and add the following import.

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

Now all you have to do is edit ``Inbox/config.json``!

You can pick to enable/disable each check and edit the discord webhook there.

## Adding Custom Checks
I made adding your own checks extremely easy!

Simply edit ``Inbox/custom_checks.json`` and create a new check. 

**Note:** Each check ``}`` must end in an ``,``. EXCEPT: the last one must end with just the ``}``.

Here is an example custom check for PayPal, CashApp and Venmo:

```json
{
    "PayPal": {
        "email": "service@paypal.com"
    },
    "CashApp": {
        "email": "no-reply@cash.app"
    },
    "Venmo": {
        "email": "venmo@venmo.com"
    }
}
```
