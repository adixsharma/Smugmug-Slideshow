class Image(object):
	row_id = None
	date_taken = None
	album_name = None
	url = None

	def __init__(self, row):
		print "Consturctor being invoked for " + row[1]
		self.row_id = row[0]
		self.url = row[1]
		self.date_taken = row[2]
		self.album_name = row[3]

