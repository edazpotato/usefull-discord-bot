# usefull-discord-bot
A dsicord bot thats usefull


### Setup
- Create a file called `config.json`
- Paste the following into it:
```js
{
  "version": "",               // Version number of the bot. Shows up in info command (string not a number btw)
  "token": "",                 //Your Discord token goes here
  "ksoft_token": "",           // Your Ksoft.Si token goes here
  "hypixel_token": "",         // Your Hypixel API key goes here
  "join_message": "",          // Your bot's server join message
  "intents": {},               // Set privilged intents here
  "owners": [],                // An array with the Discord user IDs of people who you want to have ABSOLUTE POWER over your bot. Note: people with this perm could theoreticly wipe your server so please do be careful who you put in here
  "prefixes": [],              // Prefixes for the bot to respond to
  "emoji": {},                 // Custom emoji to use in varoius situations (can be animated or non-animated)
  "use_custom_activity": true, // Wether to use the *playing* activity defined below or not
  "activity": "",              // Text that displays after 'PLAYING '
  "activity_type": "",         // `playing`, `watching`, `listening` or `competing`
  "status_type": ""            // `online`, `idle` or `dnd`
}

```
- fill in the values. e.g.
```json
{
  "version": "6.9",
  "token": "uwuwhatsthishehe",
  "ksoft_token": "doeraymesofarsewlateadoe",
  "hypixel_token": "hehehehehehehehehehehehe",
  "join_message": "FEAR ME,  ***M O R T A L S ! ! !***",
  "intents": {
    "presences": false,
    "members": false
  },
  "owners": [
    569414372959584256
  ],
  "prefixes": [
    "!",
    "$"
  ],
  "emoji": {
    "yes": "<a:aye:713222235820654642>",
    "no": "<a:nay:713222235246035024>",
    "maybe": "<a:tylda:766836870424035399>",
    "loading": "<a:loading:732421120954990618>"
  },
  "use_custom_activity": true,
  "activity": "with yo mum",
  "activity_type": "playing",
  "status_type": "online"
}

```
- install required packages
```sh
pip install -r requirements.txt
```
- run `bot.py`
```sh
# Start it with this:
python3 bot.py
# Or this:
python bot.py
# Or this:
py bot.py
# Different commands seem to work for different people. Idk why though.
```
- Add it you your server with the url provided in console
