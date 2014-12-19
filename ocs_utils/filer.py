import ocs_utils.tree, ocs_utils.lang, ocs_utils.obj
import sublime
import json
import os
import airspeed
def silent_makedirs(dirPath):
	try:
		os.makedirs(dirPath)
	except:
		pass
	return dirPath
def renderTemplate(path, params):
	with open(path) as f:
		t = airspeed.Template(f.read())
	params['up1'] = lambda s:s[0].upper() + s[1:]
	params['nop'] = lambda s:s
	return t.merge(params)
def createEntity(entity, isAdmin, route, path, delimiter, tplDir):
	# if isAdmin:
	newDir = silent_makedirs(path + delimiter + route[0])
	tplFile = tplDir + delimiter + entity
	fileName = newDir + delimiter + route[1]+('.tpl' if entity == 'view' else '.php')
	
	return (fileName, renderTemplate(tplFile, {'route1':route[0], 'route2':route[1]}))
	# else:

def makeFiles(command):
	delimiter = ocs_utils.tree.getDelimiter()
	BASE_PATH = os.path.abspath(os.path.dirname(__file__)+delimiter+'..')
	parsed = ocs_utils.lang.parse(command)
	sets = sublime.load_settings('Prefs.sublime-settings')
	chainsRaw = sets.get('chains')
	chains = ocs_utils.tree.absolutizeChains(chainsRaw)
	dirs = chains['admin' if parsed['admin'] else 'catalog']
	tplDir = BASE_PATH + delimiter + 'templates' + delimiter +('admin' if parsed['admin'] else 'catalog')
	filesToOpen = []
	if parsed['command'] == 'create':
		for ct in parsed['types']:
			filesToOpen += [createEntity(ct, parsed['admin'], parsed['route'], dirs[ct], delimiter, tplDir)]
	for fto in filesToOpen:
		with open(fto[0], 'w') as f:
			f.write(fto[1])
		sublime.active_window().open_file(fto[0])
	return json.dumps(parsed)