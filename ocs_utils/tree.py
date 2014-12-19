from os import *
from os.path import *
import re
from ocs_utils.obj import *
from sublime import active_window
def getDelimiter():
	try:
		return re.search('/|\\\\', __file__).group(0)
	except:
		return "\\"
globals()['delimiter'] = getDelimiter()
def dirStr(dir_name):
	s = ''
	def rec(path, deep):
		folders = [fn for fn in listdir(path) if isdir(path+delimiter+fn)]
		files = [fn for fn in listdir(path) if isfile(path+delimiter+fn)]
		s = '\t'*(deep-1) + path.split(delimiter)[-1]+' : \n'
		for fn in files:
			s+= '\t'*deep + fn+'\n'
		for dn in folders:
			s += rec(path+delimiter+dn, deep+1)
		return s
	return rec(dir_name, 1)

def chainToPath(chain):
	"""
	Chain is just string like admin/controller
	We need it for finding location of folders with controller/model/etc files
	Chain's definitions look at settings file
	"""
	folders = active_window().folders()
	def split(splistr):
		return [x for x in filter(lambda x:x, re.split('/|\\\\', splistr))]
	chainlen = len(split(chain))
	rechain = '/'.join(split(chain))
	def rec(path):
		r = []
		if '/'.join(split(path)[-chainlen:]) == rechain:
			r += [path]
		folders = [fn for fn in listdir(path) if isdir(path+delimiter+fn)]
		for dn in folders:
			r += rec(path+delimiter+dn)
		return r
	r = []
	for dn in folders:
		r += rec(dn)
	return r

def absolutizeChains(chains):
	for k in chains:
		v = chains[k]
		if type(v) is str:
			abses = chainToPath(v)
			if not len(abses):
				raise "Cannot find absolete path for chain %s (look chain definition in this module)"%(v)
			chains[k] = abses[0]
		else:
			absolutizeChains(v)
	return chains
