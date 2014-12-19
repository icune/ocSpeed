ocSpeed
=======

Speed up development for OpenCart: automation tool for creating model/view/controller/language file with simple commands.

Easy to use:

Press Ctrl+Shift+C ->

	create * test/it
	
		creates model/view/controller/language in catalog: you can acces it via http://host/index.php?route=test/it
		
			if you want to create only model or view type
			
	create model test/it
	
		or
		
	create model view test/it
	
		for creation in admin panel prepend command with su:
		
	su create * test/it
