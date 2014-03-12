#!/usr/bin/python
# -*- coding: utf-8 -*-

def pull(remote, branch, out, verbose=1):
	if verbose > 0:
		print 'pulling repo '+remote+' '+branch
	ret = open(out, 'wt')