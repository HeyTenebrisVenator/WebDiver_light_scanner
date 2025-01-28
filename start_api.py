import os
from flask import Flask as fk, send_file, jsonify, request
import requests
import shutil
from io import BytesIO
#PLEASE, MAKE SURE THIS FILE OS CONFIGURED
savepath = '/home/arthurjww/WebDiver_light_scanner'
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
        return send_file(savepath + "/modules/data/" + arg2 + "/report_" + arg  + '.txt', as_attachment=True)
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
@app.route('/get_notes')
def project_list():

        return open(savepath + '/modules/data/' + request.args.get('proj') + '/notes', 'r').read()
@app.route('/clear_notes')
def clear_notes():
        try:
                os.remove(f'{savepath + '/modules/data/' + request.args.get('proj') + '/notes'}')
                return 'OK'
        except:
                return 'Error'
@app.route('/delete_proj')
def remove_proj():
        try:
                shutil.rmtree(f'{savepath + '/modules/data/' + request.args.get('proj')}')
                return 'OK'
        except:
                return 'Error'
@app.route('/get_images')
def images():
        arg = request.args.get('proj')
        arg2 = request.args.get('get_image')
        return send_file(savepath + f'/modules/data/{arg}/{arg2}/output/screenshot/{arg2}/{os.listdir(savepath + f'/modules/data/{arg}/{arg2}/output/screenshot/{arg2}')[0]}')
@app.route('/start_scan')
def start_scan():
      return send_file(savepath + f'/page/start_scan.html') 
@app.route('/image/WD')
def image_wd():
        return send_file(savepath + '/images/WD.png')

@app.route('/note')
def notes():
        project = request.args.get('project')
        sub = request.args.get('subdomain')
        extra = request.args.get('extra')
        open(savepath + f'/modules/data/{project}/notes', 'a').write(sub + '-' + extra +'</br>' )
        return 'OK'
@app.route('/all_projects')
def all_proj():
        try:
                all = '<a href="..">return</a>'
                projects = os.listdir(savepath + '/modules/data')
                for proj in projects:
                        all += '<h1>'+proj + '</h1>'
                        for data in os.listdir(savepath + '/modules/data/' + proj):
                                try:
                                        if '.' in data:
                                                os.listdir(savepath + '/modules/data/' + proj + '/' + data)
                                                all += '&nbsp;&nbsp; &nbsp; &nbsp; '+data + '<br>'
                                except:
                                        pass
                return all
        except:
                return 'ERRO'
@app.route('/scan')
def scan():
        status_code = 0
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
                                directories = ''
                                status_code = 0
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
                                                os.system('sudo waybackurls -no-subs ' + subdomains_no_url + '| uro | tee -a '  + savepath + '/modules/data/' + project_name + '/' + subdomains_no_url + '/directories')
                                                os.system(f'sudo nmap -T3 -sV -p 21,22,23,25,53,80,110,111,143,139,443,445,3306,3389,5900,8080,8443 ' + subdomains_no_url + ' | grep "open" | tee -a ' + savepath + "/modules/data/" + project_name + "/" + subdomains_no_url + "/open_ports")
                                                os.system(f'sudo wafw00f ' + subdomain_url + ' | grep "behind" | tee -a ' + savepath + "/modules/data/" + project_name + "/" + subdomains_no_url + "/firewall")
                                                for dir in open(savepath + '/modules/data/' + project_name + '/' + subdomains_no_url + '/directories', 'r').readlines():
                                                        directories += dir.replace('\n', '') + '\n'
                                                try:
                                                        status_code = requests.get(subdomain_url).status_code
                                                except:
                                                        status_code = 'ERROR'
                                                REPORT = f"""        
                                                <div class="report" id="{subdomains_no_url}">
                                                <img src="{IP}/get_images?get_image={subdomains_no_url}&proj={project_name}" alt="image">
                                                <div class="url">{subdomain_url}</div><br>
                                                <div class="dir_number">Directories Number: {len(open(savepath + '/modules/data/' + project_name + '/' + subdomains_no_url + '/directories','r').readlines())}</div><br>
                                                <div class="response_code">Status Code: {status_code}</div><br>
                                                <div class="firewall">Firewall: {open(savepath + "/modules/data/" + project_name + "/" + subdomains_no_url + "/firewall","r").read().replace('[+] The site [1;94m','').replace(subdomain_url, '').replace('[0m is behind [1;96m','').replace('[0m WAF.','')}</div><br>
                                                <div class="services">SERVICES: {open(savepath + "/modules/data/" + project_name + "/" + subdomains_no_url + "/services", 'r').read().replace('[[35m','').replace(subdomain_url,'').replace('[0m]','')}</div><br>
                                                 <div class="services">PORTS: {open(savepath + "/modules/data/" + project_name + "/" + subdomains_no_url + "/open_ports", 'r').read()}</div><br>
                                                <a class="button" href="{IP}/reporter?project={project_name}&subdomain={subdomains_no_url}">DOWNLOAD REPORT</a>
                                                <button class="button" onmousedown="var request = new XMLHttpRequest(); 

                                                var inp = document.getElementById('input_note_{subdomains_no_url}').value
                                        request.onreadystatechange = function() {{
                                                if (request.readyState === XMLHttpRequest.DONE) {{
                                                if (this.readyState == 4 && request.status === 200) {{
                                                        console.log('ok')
                                                }}
                                                else {{
                                                        alert('erro')
                                                }}
                                        }}
                                        }}
                                        request.open('GET', '{IP}/note?project={project_name}&subdomain={subdomains_no_url}&extra=' + inp, true);
                                        request.send();">TAKE NOTE</button><input placeholder="Extra note" class="input" id="input_note_{subdomains_no_url}"></input>
                                        <button class="delete" onmousedown="document.getElementById('{subdomains_no_url}').innerHTML = ''">HIDE SUBDOMAIN</button>
                                                <br><br><br><br>
                                                </div>"""
                                                print(REPORT)
                                                open(savepath + "/modules/data/" + project_name + "/report_complete", 'a').write(REPORT + '\n')
                                
                                                Report2 = f"""Report From {project_name}
Open ports:
{open(savepath + "/modules/data/" + project_name + "/" + subdomains_no_url + "/open_ports", "r").read()}
FIREWALL: {open(savepath + "/modules/data/" + project_name + "/" + subdomains_no_url + "/firewall","r").read().replace('[+] The site [1;94m','').replace(subdomain_url, '').replace('[0m is behind [1;96m','').replace('[0m WAF.','')}
Services
{open(savepath + "/modules/data/" + project_name + "/" + subdomains_no_url + "/services", 'r').read().replace('[[35m','').replace(subdomain_url,'').replace('[0m]','')}
Directories Collected
{directories}
                                                """
                                                print(Report2)
                                                open(savepath + "/modules/data/" + project_name + "/report_" + subdomains_no_url + '.txt', 'a').write(Report2 + '\n') 
                                        else:
                                                pass
                                except:
                                        print('errors')
                                        pass
        return 'OK'
app.run(debug=True, host='0.0.0.0', port=4444)