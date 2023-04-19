from flask import Flask, flash, render_template, request, redirect
import pandas as pd
import csv
from netmiko import ConnectHandler
from netmiko import Netmiko
import time
import os
#from ssh import connect_sw,send_cli
from credentials import switch_credentials


#################################################################################################
# Arch/Developer: sm@Devel                                                                      #
# This software released mainly for education and You may distribute and                        #
# you may develop it for your own purpose                                                       #
# Activities other than copying, distribution and modification are not covered by this License  #
# You may accept at your own risks of using this app                                           #
# Good day and happy coding                                                                     #
#################################################################################################


app = Flask(__name__)


#################################################
            # Flask Routes #
#################################################


################## MAIN MENU ####################
@app.route("/")
def home():
  # send variable user to local html
  return render_template('index.html')

@app.route("/verification")
def verification():
  return render_template("verification.html")

@app.route("/configuration")
def configuration():
  return render_template("configuration.html")

@app.route("/monitoring")
def monitoring():
  return render_template("monitoring.html")

@app.route("/filedir")
def filedir():
  return render_template("filedir.html")

@app.route("/about")
def about():
  return render_template("about.html")

################################################


########## 0.TOOLs for CLI (For a Quick Test Only) ###########
@app.route('/cli',methods = ['POST'])
def cli():
  if request.method == 'POST':
    try:
	pass

        show_cmd = request.form['web_show_cmd']

	# Netmiko
	'''
	# Init test #
	cisco_rtr = {
    		'device_type': 'cisco_ios',
    		'host': '10.1.1.1',
    		'username': 'admin',
    		'password': 'cisco',
		'secret': 'cisco',
	}

	net_connect = ConnectHandler(**cisco_rtr)
	net_connect.enable()
	
	output_cli = net_connect.send_command(show_cli)
	'''

	cisco_rtr = {
		'device_type':'cisco_ios',
		'ip':'10.1.1.1',
		'username':switch_credentials['username'],
		'password':switch_credentials['password'],
    'secret':switch_credentials['secret'],
	}

	net_connect = ConnectHandler(**cisco_rtr)
	net_connect.enable()

	output = net_connect.send_command(show_cmd)

	'''
	#print(output)
	with open ('%s.txt' % show_cmd, 'w') as wf:
	    wf.write(output)
	'''

	#################### Logging output to a file #####################

	curr_date = time.strftime('%Y-%m-%d_%H%M%S')
	file_cmd = (show_cmd) + "_" + (curr_date) + '.txt'
	dir_path = 'output/show_command'
	#Read dir > dir_path = '/home/sams/Desktop/Flask_Projects/PB21/output/show_command'
	file_name = os.path.join(dir_path, file_cmd)

	with open ('%s' %file_name, 'w') as wf:
	    wf.write(output)

	################## End of Logging output to a file #################

	        
    finally:
         return render_template('show_output.html', web_cli_list=show_cmd, web_print=output) 


##################################################################
######################## Verification  ###########################
##################################################################

########## 1.Verification Menu - using a CLI as input text ###########

@app.route('/cust_cli',methods = ['POST'])
def cust_cli():
  if request.method == 'POST':
    try:
        
        	ip_add = request.form['web_ip_add']
	
		### Netmiko
	        cisco_rtr = {
		   'device_type':'cisco_ios',
		   'ip':ip_add,
		   'username':switch_credentials['username'],
		   'password':switch_credentials['password'],
               	   'secret':switch_credentials['secret'],
	        }
		
	        net_connect = ConnectHandler(**cisco_rtr)
                net_connect.enable()
		
		# CLI file
		show_cli = request.form['web_cli']
		#output_cmd_cust2 = net_connect.send_command(show_cmd_cust2)
	        output_cli = net_connect.send_command(show_cli)
		time.sleep(2)

		#################### Logging output to a file #####################

		curr_date = time.strftime('%Y-%m-%d_%H%M%S')
		file_cmd = ip_add + "_" + (show_cli)+ "_" + (curr_date) + '.txt'
		dir_path = 'output/verification'
		#Read dir > dir_path = '/home/sams/Desktop/Flask_Projects/PB21/output/show_command'
		file_name = os.path.join(dir_path, file_cmd)

		with open ('%s' %file_name, 'w') as wf:
		    wf.write(output_cli)

		################## End of Logging output to a file #################
		        
    finally:
         return render_template('verification_output.html', web_cli=show_cli, web_print=output_cli)          
         #return render_template('custom_output.html', web_read_file=show_read_file)        



########## 2.Verification Menu - CLI using Pick List ###########

@app.route('/cust_pick_cli',methods = ['POST'])
def cust_pick_cli():
  if request.method == 'POST':
    try:
        
        	ip_add_pick = request.form['web_ip_add_pick']
	
		### Netmiko
	        cisco_rtr = {
		   'device_type':'cisco_ios',
		   'ip':ip_add_pick,
		   'username':switch_credentials['username'],
		   'password':switch_credentials['password'],
               	   'secret':switch_credentials['secret'],
	        }
		
	        net_connect = ConnectHandler(**cisco_rtr)
                net_connect.enable()
		
		# CLI file
		show_cli_pick = request.form['web_cli_pick']
	        output_cli_pick = net_connect.send_command(show_cli_pick)
		time.sleep(2)

		#################### Logging output to a file #####################

		curr_date = time.strftime('%Y-%m-%d_%H%M%S')
		file_cmd = ip_add + "_" + (show_cli_pick)+ "_" + (curr_date) + '.txt'
		dir_path = 'output/verification'
		#Read dir > dir_path = '/home/sams/Desktop/Flask_Projects/PB21/output/show_command'
		file_name = os.path.join(dir_path, file_cmd)

		with open ('%s' %file_name, 'w') as wf:
		    wf.write(output_cli_pick)

		################## End of Logging output to a file #################
		        
    finally:
         return render_template('verification_output.html', web_cli=show_cli_pick, web_print=output_cli_pick)          
         #return render_template('custom_output.html', web_read_file=show_read_file)        



########## 3.Verification Menu - READ Uploaded Files ###########

@app.route('/cli_file',methods = ['POST'])
def cli_file():
  if request.method == 'POST':
    try:
        
        ip_list = request.form['web_ip_list']
	upload_ip_file = ip_list
	upload_dir_path = 'transfer/upload'
	upload_fipname = os.path.join(upload_dir_path, upload_ip_file)

        with open ('%s' %upload_fipname, 'r') as ipf:
	      for y in ipf:
		ip = y.strip()
		print(ip)

	        ### Netmiko
	        cisco_rtr = {
		   'device_type':'cisco_ios',
		   'ip':ip,
		   'username':switch_credentials['username'],
		   'password':switch_credentials['password'],
       'secret':switch_credentials['secret'],
	        }
		
	        net_connect = ConnectHandler(**cisco_rtr)
                net_connect.enable()
		
		# cmd file
		cmd_list = request.form['web_cmd_list']
	        upload_file = cmd_list
		upload_dir_path = 'transfer/upload'
		upload_fname = os.path.join(upload_dir_path, upload_file)

        	with open ('%s' %upload_fname, 'r') as f:

	             for x in f:
                        
			show_read_file = x.strip()
			print(show_read_file)
		   	output_read_file = net_connect.send_command(show_read_file)
			time.sleep(2)

			#################### Logging output to a file #####################

			curr_date = time.strftime('%Y-%m-%d_%H%M%S')
			file_cmd = ip + "_" + (show_read_file) + "_" + (curr_date) + '.txt'
			dir_path = 'output/verification'
			#Read dir > dir_path = '/home/sams/Desktop/Flask_Projects/PB21/output/show_command'
			file_name = os.path.join(dir_path, file_cmd)

			with open ('%s' %file_name, 'w') as wf:
			    wf.write(output_read_file)

			################## End of Logging output to a file #################
		        
    finally:
         return render_template('verification_output.html', web_cli=show_read_file, web_print=output_read_file)          
         #return render_template('uat_output.html', web_read_file=show_read_file)        

##################################################################


##################################################################
################## UPLOAD Verification File ######################
##################################################################

#ALLOWED_EXTENSIONS = {'txt'}

#UPLOAD_FOLDER = 'transfer/upload'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["UPLOAD_FOLDER"] = "/home/sams/Documents/Flask_Projects/NetworX/transfer/upload"
#app.config["UPLOAD_FOLDER"] = "/home/sams/flask/UAT/transfer/upload/uat"
#~/flask/UAT/transfer/upload

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if request.files:

            upload_file = request.files['web_upload_file']
	    print(upload_file)
	    upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'], upload_file.filename))
	    return redirect(request.url)

    return render_template('verification.html')

##################################################################


##################################################################
######################## Configuration ###########################
##################################################################


########## 1.Configuration Menu - using a CLI as input text ###########

@app.route('/cli_config',methods = ['POST'])
def cli_config():
  if request.method == 'POST':
    try:
        
        	ip_add_config = request.form['web_ip_cli_config']
	
		### Netmiko
	        cisco_rtr = {
		   'device_type':'cisco_ios',
		   'ip':ip_add_config,
		   'username':switch_credentials['username'],
		   'password':switch_credentials['password'],
               	   'secret':switch_credentials['secret'],
	        }
		
	        net_connect = ConnectHandler(**cisco_rtr)
                net_connect.enable()
		
		# CLI file
		show_cli_config = request.form['web_cli_config']
		#output_cmd_cust2 = net_connect.send_command(show_cmd_cust2)
	        output_cli_config = net_connect.send_config_set(show_cli_config)
		time.sleep(2)

		#################### Logging output to a file #####################

		curr_date = time.strftime('%Y-%m-%d_%H%M%S')
		file_cmd = ip_add + "_" + (show_cli)+ "_" + (curr_date) + '.txt'
		dir_path = 'output/configuration'
		#Read dir > dir_path = '/home/sams/Desktop/Flask_Projects/PB21/output/show_command'
		file_name = os.path.join(dir_path, file_cmd)

		with open ('%s' %file_name, 'w') as wf:
		    wf.write(output_cli_config)

		################## End of Logging output to a file #################
		        
    finally:
         return render_template('configuration_output.html', web_cli_config=show_cli_config, web_cli_config_print=output_cli_config)          
         #return render_template('custom_output.html', web_read_file=show_read_file)        




########## 2.Configuration Menu - READ Uploaded Files ###########

@app.route('/cli_config_file',methods = ['POST'])
def cli_config_file():
  if request.method == 'POST':
    try:
        # IP List File
        ip_list_config = request.form['web_ip_config_list']
	upload_ip_config_file = ip_list_config
	upload_dir_path = 'transfer/upload'
	upload_config_fipname = os.path.join(upload_dir_path, upload_ip_config_file)

        with open ('%s' %upload_config_fipname, 'r') as ip_config_f:
	      for i in ip_config_f:
		ip_config_file = i.strip()
		print(ip_config_file)

	        ### Netmiko
	        cisco_rtr = {
		   'device_type':'cisco_ios',
		   'ip':ip_config_file,
		   'username':switch_credentials['username'],
		   'password':switch_credentials['password'],
               	   'secret':switch_credentials['secret'],
	        }
		
	        net_connect = ConnectHandler(**cisco_rtr)
                net_connect.enable()
		
		# CLI List File
		cli_config_list = request.form['web_cli_config_list']
	        upload_config_file = cli_config_list
		upload_dir_path = 'transfer/upload'
		upload_config_fname = os.path.join(upload_dir_path, upload_config_file)

        	with open ('%s' %upload_config_fname, 'r') as f:

	             for j in f:
                        
			show_read_config_file = j.strip()
			print(show_read_config_file)
		   	output_read_config_file = net_connect.send_config_set(show_read_config_file)
			#output_read_config_file = net_connect.send_command(show_read_config_file)
			time.sleep(2)

			#################### Logging output to a file #####################

			curr_date = time.strftime('%Y-%m-%d_%H%M%S')
			file_cmd = ip_config_file + "_" + (show_read_config_file) + "_" + (curr_date) + '.txt'
			dir_path = 'output/configuration'
			#Read dir > dir_path = '/home/sams/Desktop/Flask_Projects/PB21/output/show_command'
			config_file_name = os.path.join(dir_path, file_cmd)

			with open ('%s' %config_file_name, 'w') as wf:
			    wf.write(output_read_config_file)

			################## End of Logging output to a file #################
		        
    finally:
         return render_template('configuration_output.html', web_cli_config=show_read_config_file, web_cli_config_print=output_read_config_file)          
         #return render_template('uat_output.html', web_read_file=show_read_file)        

##################################################################


##################################################################
################## TOOLs for CLI (NOT Ready) #####################
##################################################################

@app.route('/clix',methods = ['POST'])
def clix():
  if request.method == 'POST':
    try:

        show_clix = request.form['web_show_clix']

	# Netmiko
	device = connect_sw('device_type','ip','username','password','secret')
	output_cli = send_cli('show_clix')


	################## Logging output to a file #################
	curr_date = time.strftime('%Y-%m-%d_%H%M%S')
	file_cmd = (show_clix) + "_" + (curr_date) + '.txt'
	dir_path = 'output/show_command'
	#Read dir > dir_path = '/home/sams/Desktop/Flask_Projects/PB21/output/show_command'

	file_name = os.path.join(dir_path, file_cmd)

	with open ('%s' %file_name, 'w') as wf:
	    wf.write(output_cli)

	############## End of Logging output to a file ##############
		        
    finally:
         #return render_template('show_cli.html', web_show_cli=show_cli, web_print=connect_ssh(device)) 
         return render_template('show_cli.html', web_show_cli=show_cli, web_print=send_cli(show_clix)) 

########################### End of Fucntion #####################################

  
if __name__ == "__main__":
  #app.run(debug=True)
  app.run(host='0.0.0.0', debug=True, port=5000)

