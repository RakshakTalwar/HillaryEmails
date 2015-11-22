"""
Copyright (c) 2015 Victor Graf
Author: Victor Graf
Serve Hillary's Emails Web App
"""


from flask import Flask, request, send_from_directory, jsonify
from pymongo import MongoClient
import json
import os

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

client = MongoClient();
client = MongoClient("mongodb://localhost:27017")
db = client.hillary

all_emails = db['emails'].find({},{'RawText':1, 'ExtractedSubject':1, 'ExtractedFrom':1, 'ExtractedTo':1, "cluster":1, "classification":1, '_id':0})

@app.route('/emails', methods=['GET'])
def get_emails():
	res = []
	all_emails.rewind();
	for item in all_emails:
		res.append(item)
	
	return jsonify({'results':res})
	
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def get_resource(path):  # pragma: no cover
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
		".jpg": "image/jpeg",
    }
	
    complete_path = os.path.join(root_dir(), path)
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    content = get_file(complete_path)
    return Response(content, mimetype=mimetype)
	
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
