#!/usr/bin/python
# -*- coding: utf-8 -*-

import remote, git, json, subprocess, os, sys, interactive_shell

class pyremogit():
	"""python remote admin and git automation tool
	Usage: 
		pyremogit connect <server>
		pyremogit cmd <server> <command | file> <command | file>
		pyremogit put <server> </path/to/local/file=>/path/to/remote/file> </path/to/local/file=>/path/to/remote/file>
		pyremogit get <server> </path/to/remote/file=>/path/to/local/file> </path/to/remote/file=>/path/to/local/file>
		pyremogit pull <remote:branch | key>
		pyremogit push <remote:branch | key>
		pyremogit commit <flag> <message>
	"""
	def __init__(self, config = ''):
		self.stdout='/tmp/pyremgit'
		self.bin_dir=os.path.dirname(os.path.realpath(__file__))
		self.cwd=os.getcwd()
		if config == '':
			if os.path.isfile(self.cwd+'/pyremogit.json'):
				self.config=json.load(open(self.cwd+'/pyremogit.json'))
			else:
				self.config=json.load(open(self.bin_dir+'/config.json'))
		else:
			self.config=json.load(open(config))

################################### Remote part ###################################

	def connect(self, server):
		if server in self.config['servers']:
			return remote.connect(self.config['servers'][server])
		else:
			print 'unknown server'

	def cmd(self, server, commands = []):
		ssh = self.connect(server)
		return remote.cmd(ssh, commands)

	def put(self, server, files):
		ssh = self.connect(server)
		return remote.put(ssh, files)

	def get(self, server, files):
		ssh = self.connect(server)
		return remote.get(ssh, files)
	
	def shell(self, server):
		if 'key' in self.config['servers'][server]:
			print 'erf, sorry, work in progress so you cannot connecy using ssh keys'
		else:
			host = self.config['servers'][server]['host']
			password = self.config['servers'][server]['password']
			user = self.config['servers'][server]['user']
			interactive_shell.interactive_shell(host, user, password)

################################### GIT part ###################################

	def pull(self, what):
		if type(what) is list:
			for w in what:
				p=w.split(':')
				git.pull(p[0], p[1], self.stdout)
		elif ':' in what:
			p=what.split(':')
			git.pull(p[0], p[1], self.stdout)
		elif what in self.config['git']['pull']:
			for key, val in self.config['git']['pull'][what].iteritems():
				git.pull(key, val, self.stdout)
		else:
			print 'we do not know what you are trying to do here...'

	def push(self, what):
		if type(what) is list:
			for w in what:
				p=w.split(':')
				git.push(p[0], p[1], self.stdout)
		elif ':' in what:
			p=what.split(':')
			git.push(p[0], p[1], self.stdout)
		elif what in self.config['git']['push']:
			for key, val in self.config['git']['push'][what].iteritems():
				git.push(key, val, self.stdout)
		else:
			print 'we do not know what you are trying to do here...'

	def commit(self, flag, message=''):
		git.commit(flag, message, self.stdout)


	def doc__(self):
		return self.__doc__

	def help__(self):
		print self.__doc__
