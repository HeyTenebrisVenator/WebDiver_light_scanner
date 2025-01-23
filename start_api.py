import os
from flask import Flask as fk, send_file, jsonify, request
import requests


#PLEASE, MAKE SURE THIS FILE OS CONFIGURED
savepath = '/home/user/WebDiver_light_scanner'
IP = 'http://127.0.0.1:4444'

from flask_cors import CORS

working = False

try:
        os.mkdir(savepath + '/modules')
        os.mkdir(savepath + '/modules/data')
except:
        pass

app = fk(__name__)
cors = CORS(app)

@app.route('/reporter')
def reporter():
        arg = request.args.get('subdomain')
        arg2 = request.args.get('project')
        return send_file(savepath + "/modules/data/" + arg2 + "/report_" + arg)
@app.route('/style_principal_page.css')
def style():
        return send_file(savepath + '/page/style_principal_page.css')
@app.route('/style_report.css')
def style2():
        return send_file(savepath + '/page/style_report.css')
@app.route('/')
def home():
        return send_file(savepath + '/page/report.html')
@app.route('/script.js')
def js():
        return send_file(savepath + '/page/script.js')
@app.route('/get_report')
def report():
        arg = request.args.get('rep')
        return open(savepath + "/modules/data/" + arg + "/report_complete", 'r').read()
@app.route('/get_images')
def images():
        arg = request.args.get('proj')
        arg2 = request.args.get('get_image')
        return send_file(savepath + f'/modules/data/{arg}/{arg2}/output/screenshot/{arg2}/{os.listdir(savepath + f'/modules/data/{arg}/{arg2}/output/screenshot/{arg2}')[0]}')
@app.route('/start_scan')
def start_scan():
      return send_file(savepath + f'/page/start_scan.html') 
@app.route('/scan')
def scan():
        if 1==1:
            try:
                   out_of_scope = request.args.get('out').replace(',', ' ')
            except:
                   pass
            project_name = request.args.get('name')
            try:
                os.mkdir(savepath + '/modules/data/' + project_name)
                print('OK!')
            except FileExistsError:
                print('there is already a project with that name')
                return 'there is already a project with that name'
            wildcards = request.args.get('wildcards').split(',')
            for data in wildcards:
                  open(savepath + '/modules/data/' + project_name + '/wildcards','a').write(data + '\n')
            print('starting')
            os.system('sudo subfinder -silent -dL ' + savepath + '/modules/data/' + project_name + '/wildcards | tee -a ' + savepath + '/modules/data/' + project_name + '/subdomains')
            try:
                   subs_from_scan = request.args.get('subs')
                   subs_from_scan = subs_from_scan.split(',')
                   for sub in subs_from_scan:
                          open(savepath + '/modules/data/' + project_name + '/subdomains', 'a').write('\n' + sub)
            except:
                   pass
            os.system('sudo httpx -mc 200 -l ' + savepath + '/modules/data/' + project_name + '/subdomains | tee -a ' + savepath + '/modules/data/' + project_name + '/filtered')

            file = open(savepath + '/modules/data/' + project_name + '/filtered')
            for subdomain_url in file:
                                try:
                                        subdomain_url = subdomain_url.replace('\n', '')
                                        subdomains_no_url = subdomain_url.replace('https://', '').replace('http://', '').replace('/', '')
                                        if subdomain_url not in out_of_scope:
                                                try:
                                                        os.mkdir(savepath + '/modules/data/' + project_name + '/' + subdomains_no_url)
                                                except:
                                                        print('ERRO')
                                                        pass
                                                os.system('sudo httpx -td -u ' + subdomains_no_url + ' | tee -a ' + savepath + '/modules/data/' + project_name + '/' + subdomains_no_url + '/services')
                                                os.system('cd ' + savepath + '/modules/data/' + project_name + '/' + subdomains_no_url + '; sudo httpx -nc -ss -u ' + subdomains_no_url)
                                                os.system('sudo waybackurls -no-subs ' + subdomains_no_url + '| tee -a '  + savepath + '/modules/data/' + project_name + '/' + subdomains_no_url + '/directories')
                                                os.system(f'sudo nmap -T3 -sV -p 21,22,23,25,53,80,110,111,143,139,443,445,3306,3389,5900,8080,8443 ' + subdomains_no_url + ' | grep "open" | tee -a ' + savepath + "/modules/data/" + project_name + "/" + subdomains_no_url + "/open_ports")
                                                os.system(f'sudo wafw00f ' + subdomain_url + ' | grep "behind" | tee -a ' + savepath + "/modules/data/" + project_name + "/" + subdomains_no_url + "/firewall")
                                                REPORT = f"""        
                                                <div class="report">
                                                <img src="{IP}/get_images?get_image={subdomains_no_url}&proj={project_name}" alt="image">
                                                <div class="url">{subdomain_url}</div><br>
                                                <div class="dir_number">Directories Number: {len(open(savepath + '/modules/data/' + project_name + '/' + subdomains_no_url + '/directories','r').readlines())}</div><br>
                                                <div class="response_code">Status Code: {requests.get(subdomain_url).status_code}</div><br>
                                                <div class="firewall">Firewall: {open(savepath + "/modules/data/" + project_name + "/" + subdomains_no_url + "/firewall","r").read().replace('[+] The site [1;94m','').replace(subdomain_url, '').replace('[0m is behind [1;96m','').replace('[0m WAF.','')}</div><br>
                                                <div class="services">SERVICES: {open(savepath + "/modules/data/" + project_name + "/" + subdomains_no_url + "/services", 'r').read().replace('[[35m','').replace(subdomain_url,'').replace('[0m]','')}</div><br>
                                                <button onmousedown="var request = new XMLHttpRequest(); 
                                
                                        request.onreadystatechange = function() {{
                                                if (request.readyState === XMLHttpRequest.DONE) {{
                                                if (this.readyState == 4 && request.status === 200) {{
                                                        document.write(request.responseText);
                                                }}
                                                else {{
                                                        document.getElementById('Reports').innerHTML = 'ERROR';
                                                }}
                                        }}
                                        }}
                                        request.open('GET', '{IP}/reporter?project={project_name}&subdomain={subdomains_no_url}', true);
                                        request.send();">SHOW FULL REPORT</button>
                                                <br><br><br><br>
                                                </div>"""
                                                print(REPORT)
                                                open(savepath + "/modules/data/" + project_name + "/report_complete", 'a').write(REPORT + '\n')
                                
                                                Report2 = f"""
                                <!DOCTYPE html>
                                <html lang="en">
                                <head>
                                        <meta charset="UTF-8">
                                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                        <link rel="stylesheet" href="../style_report.css">
                                        <title>Report from url {subdomain_url}</title>
                                </head>
                                <body>
                                        <h1 class="report_from">{subdomain_url}</h1>
                                        <a class="anchor" href="../">Voltar</a>
                                        <div class="report_complete">
                                        <h1 class="report_from">Report From {project_name}</h1>
                                        <a href="{subdomain_url}">           <img class="report_image" src="{IP}/get_images?get_image={subdomains_no_url}&proj={project_name}" alt=""></a>
                                        <h1>Open ports</h1>
                                        {open(savepath + "/modules/data/" + project_name + "/" + subdomains_no_url + "/open_ports", "r").read()}
                                        <h1>
                                        FIREWALL: {open(savepath + "/modules/data/" + project_name + "/" + subdomains_no_url + "/firewall","r").read().replace('[+] The site [1;94m','').replace(subdomain_url, '').replace('[0m is behind [1;96m','').replace('[0m WAF.','')}
                                        </h1>
                                        <h1>Services</h1>
                                        {open(savepath + "/modules/data/" + project_name + "/" + subdomains_no_url + "/services", 'r').read().replace('[[35m','').replace(subdomain_url,'').replace('[0m]','')}
                                        </div>
                                        <br>
                                        <div class="dir_collected">
                                        <h1>Directories Collected</h1>
                                        {open(savepath + "/modules/data/" + project_name + "/" + subdomains_no_url + "/directories", "r").read().replace(' ', '\n')}
                                        </div>
                                </body>
                                </html>
                                                """
                                                print(Report2)
                                                open(savepath + "/modules/data/" + project_name + "/report_" + subdomains_no_url, 'a').write(Report2 + '\n') 
                                        else:
                                                pass
                                except:
                                        pass
        return 'OK'
app.run(debug=True, host='0.0.0.0', port=4444)

