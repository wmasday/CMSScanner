# Open Monograph Press Access : /files/presses/1/monographs/
from fake_useragent import UserAgent
import requests
import re
import sys, json
from multiprocessing.dummy import Pool
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

config = open('config.json')
exploiter = json.load(config)

confDebug = False
confVerify = True
confAllowRedirect = True
confTimeout = 15
confPayload = ''

help = '''
use --target=site.com
use --file=list.txt
use --file=list.txt --thread=30
        
    --help HELP
    --target Scan Single URL
    --file Scan From File
        --thread Multiproccess Thread
'''

def debug(url, err):
    if confDebug == True:
        if 'ConnectTimeout' in err:
            open('cms_ConnectTimeout.log', 'a').write(f'[ERR] {url} : {err}\n')
        elif 'ConnectionError' in err:
            open('cms_ConnectionError.log', 'a').write(f'[ERR] {url} : {err}\n')
        else:
            open('cms_dbug.log', 'a').write(f'[ERR] {url} : {err}\n')
    else:pass
       

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
        UserAgent = UserAgent().chrome
    except:
        UserAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
    
    confHeaders = {"User-Agent": str(UserAgent)}
    
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
        print ('[!] Errors : '+ url)
        open('cms_errors.txt', 'a').write(url +'\n')
        debug(url, str(err))
        
     
def init():
    if len(sys.argv) == 1:
        print (help)
        return sys.exit()
        
    
    command = sys.argv[1]
    if command == '--help':
        print (help)
        return sys.exit()
    
    if '--target=' in command:
        target = command.replace('--target=', '')
        exploit(target)
        
    elif '--file=' in command:
        sitelist = command.replace('--file=', '')
        try:
            open(sitelist, 'r', encoding='utf8').read()
        except:
            print ('[!] Sitelist Not Found')
            return sys.exit()
        
        if len(sys.argv) == 3:    
            if '--thread=' in sys.argv[2]:
                thread = sys.argv[2].replace('--thread=', '')
            else:pass
        else:
            thread = 25
    
        try:
            sites = open(sitelist, "r", encoding='utf8').read().splitlines()
            try:
                pp = Pool(int(thread))
                pp.map(exploit, sites)
            except:
                print("[!] Multithread Error")
                return sys.exit()
        except:
            print("[!] Sitelist not found!")
            return sys.exit()


init()
