import requests

url = 'http://localhost:3000/'
wordlist = [
    'api', 'rest', 'v1', 'v2', 'admin', 'administration', 'assets', 
    'auth', 'backups', 'config', 'configuration', 'console', 'dashboard', 
    'data', 'db', 'debug', 'download', 'external', 'files', 'graphql', 
    'internal', 'login', 'metrics', 'monitoring', 'old', 'private', 
    'public', 'root', 'scripts', 'secrets', 'server-status', 'settings', 
    'setup', 'static', 'status', 'storage', 'temp', 'tmp', 'user', 'users', 
    'utils', 'webapi', 'whoami', 'xml', 'hints', 'uploads', 'assets', 'public',
    'images'
]

baseline_size = 75032
path_list_index = wordlist[0]

def discover_resources(base_path, words, depth = 0):
   if depth > 2: 
        return

   for word in words:
        if not word or word in base_path:
            continue

        target_endpoint = base_path + word + '/'
        full_url = url + target_endpoint
        
        try:
            request = requests.get(full_url)
            if request.status_code == 500:
                #print('API -> ' + full_url)
                discover_resources(target_endpoint, words, depth + 1)
            elif request.status_code == 200 and len(request.content) != baseline_size:
                print('PAGE -> ' + full_url)
        except:
            pass

discover_resources('', wordlist)