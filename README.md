# CMSScanner

CMSScanner | Checking Site CMS, Plugins, Component, Extensions, Modules, Themes | Python

### Find CMS

| CMS / Framework        | Vulnerablity / Possible To                          |
| :--------------------- | :-------------------------------------------------- |
| Balitbang              | `SQL Injection, SignIn With Default U/P`            |
| Chamilo                | -                                                   |
| CodeIgniter            | `phpUnitRCE, Debug Bar`                             |
| Computer Assisted Test | `SignIn With Default U/P`                           |
| Debug Bar              | `Laravel & CodeIgniter`                             |
| Drupal                 | `phpUnitRCE, AFU, etc`                              |
| Github                 | `Takeover Domain or Subdomain`                      |
| Index Of               | `Dirlisting`                                        |
| Joomla                 | `Find Refrence`                                     |
| Keenthemes             | `SQL Login`                                         |
| Laravel                | `Possible phpUnitRCE, APP_KEY RCE, Missconfig, etc` |
| Open Journal Systems   | `Arbitrary File Upload`                             |
| Open Monograph Press   | `Arbitrary File Upload`                             |
| OpenCart               | `Possible  Bruteforce Attack`                       |
| OpenSID                | `Arbitrary File Upload/RFM`                         |
| PHP Params             | `Possible SQL, LFI, Open Redirect, etc`             |
| PopojiCMS              | -                                                   |
| Prestashop             | `Find Refrence`                                     |
| Sekolahku.web.id       | `Possible SignIn With Default Username or Password` |
| Weebly                 | `Takeover Subdomain`                                |
| Wordpress              | `Find Refrence`                                     |
| X-Candy CBT            | -                                                   |
| vBulletin              | -                                                   |
| PlaySMS                | `RCE`                                               |
| Other CMS              | `Find Refrence`                                     |

## Usage

Run CMSScanner with python3, and setting up `config.json`

```bash
Params Helpers
---

options:
  -h   or  --help       :  show this help message and exit
  -u   or  --url        :  scan with single url (eg: http://target.com/) (default: None)
  -l   or  --list       :  scan with mass url list (default: None)
  -t   or  --thread     :  multithread proccess (default: None)
  -m   or   --method    :  method requests or scrapper (bypassing cloudflare) (default: None)
```
