class database:
	def __init__(s, m):
		s.main = m

	#read data from a given file, return as a dictionary
	def fileTOdict(s, filename, sep):
		try:
			file = open(filename,"r", encoding='utf-8')
		except:
			file = open(filename,"a", encoding='utf-8')
			file = open(filename,"r", encoding='utf-8')
		line = file.readline()
		result = {}
		while line:
			l = line.replace("\n","").replace("\ufeff","").split(sep)
			result[l[0]] = l[1:]
			line = file.readline()
		return result
		file.close()

	#update given file from a dictionary
	def updateFile(s, filename, data, sep):
		try:
			file = open(filename,"w", encoding='utf-8')
		except:
			file = open(filename,"a", encoding='utf-8')
			file = open(filename,"w", encoding='utf-8')
		if not s.keyExist(s.main.mymusic.copy(), "filename"):
			file.write("filename,\n")
		for key, value in data.items():
			if type(value) is list:
				val = ",".join(value)
			else:
				val = value
			file.write("%s%s%s\n" % (key.replace(sep,""),sep,val))
		file.close()

	#checks if a key exists in a dictionary
	def keyExist(s, dictt, key):
		try:
			a = dictt[key]
			return True
		except:
			return False