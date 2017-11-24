import couchdb

couch = couchdb.Server("http://192.168.56.101:5984/")
db = couch['test']
