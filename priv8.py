from fake_useragent import UserAgent
import requests, re, sys, json, argparse, cloudscraper
from multiprocessing.dummy import Pool
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

scraper = cloudscraper.create_scraper()
config = open('config.json')
exploiter = json.load(config)

confDebug = False
confVerify = True
confAllowRedirect = True
confTimeout = 15
confPayload = ''

help = '''
Params Helpers
---

options:
  -h   or  --help       :  show this help message and exit
  -u   or  --url        :  scan with single url (eg: http://target.com/)
  -l   or  --list       :  scan with mass url list
  -t   or  --thread     :  multithread proccess
  -m   or   --method    :  method requests or scrapper (bypassing cloudflare)
'''

def findPluginTheme(url, response):
    try:
        plugins = re.findall(r'/wp-content/plugins/(.*?)/', response)
        plugins = list(dict.fromkeys(plugins))
        for plugin in plugins:
            open(f'cms_plugins.txt', 'a').write(f'[{plugin}] {url}\n')
    except:pass
        
    try:
        themes = re.findall(r'/wp-content/themes/(.*?)/', response)
        themes = list(dict.fromkeys(themes))
        for theme in themes:
            open(f'cms_themes.txt', 'a').write(f'[{theme}] {url}\n')
    except:pass
    
    try:
        options = re.findall(r'/index.php?option=(.*?)&', response)
        options = list(dict.fromkeys(options))
        for option in options:
            open(f'cms_options.txt', 'a').write(f'[{option}] {url}\n')
    except:pass
    
    try:
        components = re.findall(r'components/(.*?)/', response)
        components = list(dict.fromkeys(components))
        for component in components:
            open(f'cms_components.txt', 'a').write(f'[{component}] {url}\n')
    except:pass
    
def exploit(url):
    if 'http://' not in url:
        url = 'http://'+ url
    else:
        url = url
    
    try:
        ua = UserAgent().chrome
    except:
        ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
    
    confHeaders = {"User-Agent": str(ua)}
    
    try:
        print (f'[!] [ CMS ] Check : {url}')
        
        check = requests.get(url, headers=confHeaders, timeout=confTimeout, allow_redirects=confAllowRedirect)
        
        for conf in exploiter:
            name = conf['name']
            output = conf['output']
            
            for flag in conf['flag']:
                flagCode = flag['code']
                flagCookies = flag['cookies']
                flagText = flag['text']
                flagHeaders = flag['headers']
                flagValue = flag['value']
                
                if flagText == True:
                    if flagValue in check.text:
                        open(output, 'a').write(url +'\n')
                        
                        if name == 'Wordpress' or name == 'Joomla':
                            findPluginTheme(url, check.text)
                        else:pass
                        
                        return True
                    else:pass
                else:pass
                
                if flagCode == True:
                    if flagValue in check.status_code:
                        open(output, 'a').write(url +'\n')
                        return True
                    else:pass
                else:pass
                
                if flagCookies == True:
                    if flagValue in check.cookies:
                        open(output, 'a').write(url +'\n')
                        return True
                    else:pass
                else:pass
                
                if flagHeaders == True:
                    if flagValue in check.headers:
                        open(output, 'a').write(url +'\n')
                        return True
                    else:pass
                else:pass
        
        
        # Consist Response
        if ".php?" in check.text:
            open('cms_foundparams.txt', 'a').write(url +'\n')
        else:pass
            
        if "Index of" in check.text:
            open('cms_indexof.txt', 'a').write(url +'\n')
        else:pass
            
        open('cms_other.txt', 'a').write(url +'\n')
    except Exception as err:
        pass
        
     
def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="Scan with single url (eg: http://target.com/)")
    parser.add_argument("-l", "--list", help="Scan with mass url list")
    parser.add_argument("-t", "--thread", help="Multithread Proccess")
    args = parser.parse_args()
    
    if args.url == None and args.list == None:
        print (help)
        return sys.exit()
    
    if args.url != None:
        exploit(args.url)
        return sys.exit()
    else:pass
    
    if args.list != None:
        try:
            open(args.list)
        except:
            print ('[!] SITELIST NOT FOUND')
            return sys.exit()
        
        if args.thread != None:
            thread = int(args.thread)
        else:
            thread = 25
        
        try:
            sites = open(args.list, "r", encoding='utf8').read().splitlines()
            try:
                pp = Pool(int(thread))
                pp.map(exploit, sites)
            except:
                print("[!] MULTITHREAD ERROR")
                return sys.exit()
        except:
            print ('[!] SITELIST NOT FOUND')
            return sys.exit()
        
    else:
        print (help)
        return sys.exit()

init()