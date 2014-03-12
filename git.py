#!/usr/bin/python
# -*- coding: utf-8 -*-

def pull(remote, branch, out, verbose=1):
	if verbose > 0:
		print 'pulling repo '+remote+' '+branch
	ret = open(out, 'wt')
	subprocess.call('git pull '+repo+' '+branch, shell=True, stdout=ret)
	ret.close()
	if 'CONFLICT' in open(self.stdout, 'r+').read() or 'aborted' in open(self.stdout, 'r+').read():
		print 'conflict pulling '+repo
		return False
	else:
		return True

def push(remote, branch):
	print 'pushing repo '+repo+' '+branch
	ret = open(self.stdout, 'wt')
	subprocess.call('git push '+repo+' '+branch, shell=True, stdout=ret)
	ret.close()

def mergetool(tool, out):
	ret = open(out, 'wt')
	subprocess.call('git mergetool -t '+tool+' -y', shell=True, stdout=ret)
	ret.close()