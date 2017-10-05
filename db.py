import couchdb

couch = couchdb.Server("http://192.168.1.111:5984/")
db = couch['test']
