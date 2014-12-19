import re

def parse(line):
	def preparse(line):
		commands = ['create']
		types = ['model', 'controller', 'view', 'language']
		parts = [x for x in filter(lambda x:x, re.split('\s+', line))]
		r = {}
		try:
			if parts[0] == 'su':
				r['admin'] = True
				parts.pop(0)
			else:
				r['admin'] = False
		except:
			raise Exception('Empty input')

		try:
			if parts[0] not in commands:
				raise Exception("Unknown command %s"%(parts[0]))
			r['command'] = parts[0]
			parts.pop(0)
		except:
			raise Exception('Empty input: expected command (%s)' % (' OR '.join(commands)))			

		try:
			route = parts.pop(-1)
			if not re.match('[a-z]+/[a-z]+', route):
				raise Exception('Wrong route format (%s) must be [a-z]+/[a-z]+'%(route))
			r['route'] = route.split('/')
		except:
			raise Exception('Where route at the end? Must have format [a-z]+/[a-z]+')

		if '*' in parts:
			r['all'] = True
			r['types'] = types
		else:
			r['types'] = []
			for p in parts:
				if p in types:
					r['types'] += [p]
				else:
					raise Exception("Unknown type %s" % (p))
		return r

	r = preparse(line)
	return r