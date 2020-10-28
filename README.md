# usefull-discord-bot
A dsicord bot thats usefull


### Setup
<details>
  <summary>Deatils on seeting up the bot</summary>
  - `config.json` layout
  ```js
  {
    "version": "",               // Version number of the bot. Shows up in info command (string not a number btw)
    "token": "",                 // Your Discord production bot token goes here
    "dev_token": "",             // Your Discord development bot token goes here
    "ksoft_token": "",           // Your Ksoft.Si token goes here
    "hypixel_token": "",         // Your Hypixel API key goes here
    "statcord_token": "",        // Your bot's statcord token
    "join_message": "",          // Your bot's server join message
    "intents": {},               // Set privilged intents here
    "owners": [],                // An array with the Discord user IDs of people who you want to have ABSOLUTE POWER over your bot. Note: people with this perm could theoreticly wipe your server so please do be careful who you put in here
    "prefixes": [],              // Prefixes for the bot to respond to
    "dev_prefixes": [],          // Prefixes for the dev version of the bot to respond to
    "emoji": {},                 // Custom emoji to use in varoius situations (can be animated or non-animated)
    "use_custom_activity": true, // Wether to use the *playing* activity defined below or not
    "activity": "",              // Text that displays after 'PLAYING '
    "activity_type": "",         // `playing`, `watching`, `listening` or `competing`
    "status_type": ""            // `online`, `idle` or `dnd`
  }
  ```
  - example values:
  ```json
  {
    "version": "6.9",
    "token": "uwuwhatsthishehe",
    "dev_token": "aaaaaaaaaaaaaaaa",
    "ksoft_token": "doeraymesofarsewlateadoe",
    "hypixel_token": "hehehehehehehehehehehehe",
    "statcord_token": "statcord.com-uwuowouwuowo",
    "join_message": "FEAR ME,  ***M O R T A L S ! ! !***",
    "intents": {
      "presences": false,
      "members": true
    },
    "owners": [
      569414372959584256
    ],
    "prefixes": [
      "$"
    ],
    "dev_prefixes": [
      "!"
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
  > **IMPORTANT NOTE:** If you don't have the `members` intent enabled, commands that use a `discord.User` or `discord.Member` converter will only work with mentions
</details>

# Self Hosting
No support will be provided if you try and self host this bot. It is open source for educational purposes only

# Licence
This project is licenced under the MIT LICENCE. You can read more in the [License file](LICENSE).
