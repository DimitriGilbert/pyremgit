#!/usr/bin/python
# -*- coding: utf-8 -*-

import paramiko, select

def connect(server, verbose=1):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	if verbose > 0:
		print 'trying to connect to '+server['name']+' ('+server['host']+')'
	if 'key' in server:
		if verbose > 1:
			print 'using private key '+server['key']
		k = paramiko.RSAKey.from_private_key_file(server['key'])
		try:
			ssh.connect( 
				hostname = server['host'],
				username = server['user'],
				pkey = k
			)
		except Exception, e:
			print 'failed to connect to '+server['name']+' ('+server['host']+')'
			print e
			return False
	elif 'password' in server:
		try:
			ssh.connect( 
				hostname = server['host'],
				username = server['user'],
				password = server['password'],
			)
		except Exception, e:
			print 'failed to connect to '+server['name']+' ('+server['host']+')'
			print e
			return False
	else:
		print 'server '+server['name']+' has neither a key nor a password'
		return False
	if verbose > 0:
		print 'connected to '+server['name']
	return ssh

def cmd(ssh, commands, verbose = 2):
	if ssh is not False:
		# unification of command type (string or list)
		if type(commands) is not list:
			commands = [commands]

		cmds = []
		if verbose > 1:
			for c in commands:
				cmds.append('echo "'+c+' : "')
				cmds.append(c)
		else:
			cmds=commands

		cmd = '\n'.join(cmds)

		out = ''
		#for long running process to receive data on the fly
		channel = ssh.get_transport().open_session()
		
		# sending the commands
		channel.exec_command(cmd)
		while True:
		    if channel.exit_status_ready():
		        break
		    rl, wl, xl = select.select([channel], [], [], 0.0)
		    if len(rl) > 0:
		    	o = channel.recv(1024)
		    	if o != '':
		    		print o
		        	out += o
		ssh.close()
		return out
	else:
		print 'ssh connexion is down !'
		return False
