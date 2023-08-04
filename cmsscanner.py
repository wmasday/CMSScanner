from fake_useragent import UserAgent
import requests
import re
import sys
from multiprocessing.dummy import Pool
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

confDebug = False
confVerify = True
confAllowRedirect = True
confTimeout = 15
confPayload = ''

help = '''
[!] python3 cmsscanner.py --target=site.com
[!] python3 cmsscanner.py --file=list.txt
[!] python3 cmsscanner.py --file=list.txt --thread=30
        
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
        if 'wp-content' in check.text or 'wp-includes' in check.text:
            open('cms_wordpress.txt', 'a').write(url +'\n')
            findPluginTheme(url, check.text)
        elif 'joomla' in check.text or 'Joomla' in check.text:
            open('cms_joomla.txt', 'a').write(url +'\n')
            findPluginTheme(url, check.text)
        elif 'po-includes' in check.text or 'po-content' in check.text:
            open('cms_popoji.txt', 'a').write(url +'\n')
        elif 'Keenthemes' in check.text:
            open('cms_keenthemes.txt', 'a').write(url +'\n')
        elif "sekolahku.web.id" in check.text or "cmssekolahku" in check.text:
            open('cms_sekolahku.txt', 'a').write(url +'\n')
        elif "OpenSID" in check.text or "OpenDesa" in check.text:
            open('cms_opensid.txt', 'a').write(url +'\n')
        elif "drupal" in check.text or "Drupal" in check.text:
            open('cms_drupal.txt', 'a').write(url +'\n')
        elif "prestashop" in check.text or "PrestaShop" in check.text:
            open('cms_prestashop.txt', 'a').write(url +'\n')
        elif "OpenCart" in check.text or "opencart" in check.text:
            open('cms_opencart.txt', 'a').write(url +'\n')
        elif "Balitbang" in check.text or "balitbang" in check.text:
            open('cms_balitbang.txt', 'a').write(url +'\n')
        elif "X-Candy CBT" in check.text:
            open('cms_xcandycbt.txt', 'a').write(url +'\n')
        elif "Computer Assisted Test" in check.text:
            open('cms_computerasisted.txt', 'a').write(url +'\n')
        elif "Open Journal Systems" in check.text:
            open('cms_openjournalsystem.txt', 'a').write(url +'\n')
        elif "vBulletin" in check.text or 'vbulletin' in check.text:
            open('cms_vbulletin.txt', 'a').write(url +'\n')
        elif ".php?" in check.text:
            open('cms_foundparams.txt', 'a').write(url +'\n')   
        elif "Index of" in check.text:
            open('cms_indexof.txt', 'a').write(url +'\n')
        elif "Chamilo" in check.text or 'chamilo' in check.text:
            open('cms_chamilo.txt', 'a').write(url +'\n')
        elif 'XSRF-TOKEN' in check.cookies or 'laravel_session' in check.cookies:
            open('cms_laravel.txt', 'a').write(url +'\n')
        else:
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
            open(sitelist, 'r').read()
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
            print (thread)
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
