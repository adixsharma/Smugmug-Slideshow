import initialize
import os

def populatedata():
    countOfInsertedRows = initialize.initializeURLs()
    return dict(count = countOfInsertedRows)

def purgedata():
    initialize.deleteURLs()
    countOfRows = str(initialize.getCountOfURLs())
    return dict(count=countOfRows)

def urls():
    offsetPrevious = 0
    offsetNext = 0
    limit = 5

    offset = request.vars.offset
    if (offset is None):
        offset = 0
    
    limit = request.vars.limit
    if (limit is None):
        limit = 5

    Images = initialize.getPageOfImages(offset,limit)
    # offsetPrevious = Images[0].row_id - (limit + 1) 

    return dict(images = Images)
