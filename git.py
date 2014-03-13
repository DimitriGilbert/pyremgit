#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess

def pull(remote, branch, out, verbose=1):
	if verbose > 0:
		print 'pulling repo '+remote+' '+branch
	ret = open(out, 'wt')
	subprocess.call('git pull '+remote+' '+branch, shell=True, stdout=ret)
	ret.close()
	if 'CONFLICT' in open(out, 'r+').read() or 'aborted' in open(out, 'r+').read():
		if verbose > 1:
			print 'conflict pulling '+repo
		return False
	else:
		return True

def push(remote, branch, out, verbose=1):
	if verbose > 0:
		print 'pushing repo '+remote+' '+branch
	ret = open(out, 'wt')
	subprocess.call('git push '+remote+' '+branch, shell=True, stdout=ret)
	ret.close()

def commit(flag, mess, out, verbose=1):
	if verbose > 0:
		print 'commiting repo '
	flag = '-'+flag+'m'
	if mess == '':
		mess = raw_input('commit message :')
	ret = open(out, 'wt')
	subprocess.call('git commit '+flag+' "'+mess+'"', shell=True, stdout=ret)
	ret.close()
	

def mergetool(tool, out):
	ret = open(out, 'wt')
	subprocess.call('git mergetool -t '+tool+' -y', shell=True, stdout=ret)
	ret.close()