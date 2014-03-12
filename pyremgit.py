#!/usr/bin/python
# -*- coding: utf-8 -*-

import remote, git, json, subprocess, os, sys

class pyremgit():
	"""python remote admin and git automation tool"""
	def __init__(self, config = ''):
		self.stdout='/tmp/pyremgit'
		self.bin_dir=os.path.dirname(os.path.realpath(__file__))
		self.cwd=os.getcwd()
		if config == '':
			if os.path.isfile(self.cwd+'/pyremgit.json'):
				self.config=json.load(open(self.cwd+'/pyremgit.json'))
			else:
				self.config=json.load(open(self.bin_dir+'/config.json'))
		else:
			self.config=json.load(open(config))

	def connect(self, server):
		if server in self.config['servers']:
			return remote.connect(self.config['servers'][server])
		else:
			print 'unknown server'

	def cmd(self, server, commands = []):
		ssh=self.connect(server)
		out=remote.cmd(ssh, commands)

	def pull(self, what):
		if type(what) is list:
			for w in what:
				p=w.split(':')
				git.pull(p[0], p[1], self.stdout)
		elif ':' in what:
			p=what.split(':')
			git.pull(p[0], p[1], self.stdout)
		elif what in self.config['git']['pull']:
			for key, val in self.config['git']['pull']:
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
		elif what in self.config['git']['pull']:
			for key, val in self.config['git']['pull']:
				git.push(key, val, self.stdout)
		else:
			print 'we do not know what you are trying to do here...'





	def help__(self):
		print 'usage :'
		print '	pyremgit <command> [args]'
		print 'available command :'
		print '	connect <server>'
		print '	cmd <server> <"command1" "command2" ...> or cmd <server> <file1 file2 ...>'