import initialize
import web
import time
import webbrowser
import urllib

urls = (
	'/insertURLs','InsertURLs','/geturls','GetURLs','/deleteurls','deleteURLs'
)

class InsertURLs:
	def GET(self):
		URLS_browser = initialize.initializeURLs()
		return URLS_browser

class GetURLs:
	def GET(self):
		offsetPrevious = 0
		offsetNext = 0
		limit = 5
		previousLink = ""

		query_param_data = web.input(offset=0)
		if not (query_param_data is None):
			qparam_offset = query_param_data.offset
			if (qparam_offset is None): 
				offset = 0
			else:
				offset = qparam_offset

		Images = initialize.getPageOfImages(offset,limit)
		offsetPrevious = Images[0].row_id - (limit + 1) 
		print offsetPrevious
		output = '<html><body><table>'
		for image in Images:
			output = output + "<tr><td>" + str(image.row_id) + "</td><td><a href='" + image.url + "' target='_new'>" + image.album_name + "</a></td><td>" + image.date_taken + "</td></tr>"
			offset = image.row_id
		output = output + "</table>"
		if (offsetPrevious >= 0):
			previousLink = "<a href='/geturls?offset=" + str(offsetPrevious) + "'>Get Previous Batch</a><br />"
		nextLink = "<a href='/geturls?offset=" + str(offset) + "'>Get Next Batch</a>"
		output += previousLink + nextLink + "</body></html>"
		return output


class deleteURLs():
	def GET(self):
		initialize.deleteURLs()
		return "All URLs have been deleted!"


if __name__ == "__main__":
	app = web.application( urls, globals())
	app.run()

