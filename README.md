## Update
Sorry there hasnt been an update in awhile. This was not my plan. I have had a lot of stuff happen in real life and haven't had the time for this. I like making stuff like this and I will hopefully be back soon to continue it. Currently it should be fully functional but I have experienced some issues that may skip over some logs. I will hopefully have the time to fix all issues soon and add some new features. If you want to help out please make a pull request and an issue if you find any issues or have a suggestion. Updates will be coming soon! I have about a week until school starts.

# MSMC-Inboxer
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

More Checks can be added by checking out ``Custom Checks.md``!

## Installation (READ THIS)
Adding this to MSMC is very simple.

**Video:** 

https://github.com/PgerTools/MSMC-Inboxer/assets/160817198/7a5d6288-67d9-46a2-b7fa-350d6009e4f3

**Step By Step:**

1. Go to the root of MSMC and create a new folder called addons then download and place ``inbox.py`` there.

   Make sure to also download and place the ``Inbox`` folder.

3. Now edit ``MSMC.py`` and add the following import.
   ```py
   from addons.inbox import inboxmail
   ```

3. Search for the validmail function. (You can do this using Ctrl+F)

4. Add the end of this function add the following code.

   ```py
   inboxmail(email, password)
   ```

5. Now all you have to do is edit ``Inbox/config.json``!

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

A lot more custom configs can be found in ``Custom Configs.md``!
