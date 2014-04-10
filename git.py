#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess

def pull(remote, branch, out = '/tmp/pyremogit_stdout', verbose=1):
	if verbose > 0:
		print 'pulling repo '+remote+' '+branch
	ret = open(out, 'wt')
	subprocess.call('git pull '+remote+' '+branch, shell=True, stdout=ret, stderr=subprocess.STDOUT)
	ret.close()
	ret = open(out, 'r+').read()
	if 'CONFLICT' in ret or 'aborted' in ret:
		if verbose > 0:
			print 'conflict pulling '+remote
			print ret
			if 'CONFLICT' in ret:
				mergetool('meld')
		return False
	else:
		if verbose > 0:
			print ret
		return True

def push(remote, branch, out = '/tmp/pyremogit_stdout', verbose=1):
	if verbose > 0:
		print 'pushing repo '+remote+' '+branch
	ret = open(out, 'wt')
	subprocess.call('git push '+remote+' '+branch, shell=True, stdout=ret, stderr=subprocess.STDOUT)
	ret.close()
	return True

def commit(flag, mess, out = '/tmp/pyremogit_stdout', verbose=1):
	if verbose > 0:
		print 'commiting repo '
	flag = '-'+flag+'m'
	if mess == '':
		mess = raw_input('commit message :')
	ret = open(out, 'wt')
	subprocess.call('git commit '+flag+' "'+mess+'"', shell=True, stdout=ret, stderr=subprocess.STDOUT)
	ret.close()
	if verbose > 0:
		print open(out, 'r+').read()
	return True

def mergetool(tool, out = '/tmp/pyremogit_stdout'):
	ret = open(out, 'wt')
	subprocess.call('git mergetool -t '+tool+' -y', shell=True, stdout=ret, stderr=subprocess.STDOUT)
	ret.close()
	return True

def branch(name, out = '/tmp/pyremogit_stdout', verbose=1):
	ret = open(out, 'wt')
	subprocess.call('git show-ref refs/heads/'+name+' --verify', shell=True, stdout=ret, stderr=subprocess.STDOUT)
	ret.close()
	ret = open(out, 'r+')
	r = ret.read()
	if 'valid' in r:
		ret.close()
		ret = open(out, 'wt')
		subprocess.call('git branch '+name, shell=True, stdout=ret, stderr=subprocess.STDOUT)
		ret.close()
		if verbose > 0:
			ret = open(out, 'r+')
			print ret.read()
			ret.close()
		return True
	else:
		print 'branch '+name+' already exists'
		return False

def checkout(branch, out = '/tmp/pyremogit_stdout', verbose=1):
	ret = open(out, 'wt')
	subprocess.call('git checkout '+branch, shell=True, stdout=ret, stderr=subprocess.STDOUT)
	ret.close()
	if verbose > 0:
		ret = open(out, 'r+')
		print ret.read()
		ret.close()

def branchout(name):
	exist = branch(name)
	checkout(name)
	return exist