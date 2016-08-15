from flask import Flask,url_for,request,json,render_template,Markup,Response
from flask_restful import reqparse, abort, Api, Resource
import json as JSON

app=Flask(__name__)
api = Api(app)

global z
global list_of_id
global list_of_cry

class employee_by_id(Resource) :
    def get(self,emp_id):
        try:
            emp_id = int(emp_id)
	except:
	    return "Not an valid employee id"
	
	if not emp_id in list_of_id:
	    ret = 'Record not found with the given id'
	    return ret
	else:
	    for record in z:
	        if record['id']==emp_id:
		    ret_string = JSON.dumps(record)
	            return Response(ret_string,mimetype='text/plain')
class emp(Resource):
    def get(self):
        global z
	ret_string = "\n".join(JSON.dumps(item,separators=(',',':')) for item in z)
        return Response(ret_string,mimetype='text/plain')


class root(Resource):
    def get(self):
        return Response(render_template('index.htm'),mimetype='text/html')

class employee_by_country(Resource):
    def get(self):
        parser = reqparse.RequestParser()
	parser.add_argument('country',type=str)
	args = parser.parse_args()
	country = args.get('country')
	country=country.lower()
	records = []
	if not country in list_of_cry:
	    ret = 'No records with country:'+country
	    return ret
	else:
	    for record in z:
	        check = record['country'].encode('ascii','ignore')
		check = check.lower()
		if check==country:
		    records.append(record)
	    ret_string = "\n".join(JSON.dumps(item,separators=(',',':')) for item in records)
	    return Response(ret_string,mimetype='text/plain')
	    
class emp_ids(Resource):
    def get(self):
        global list_of_id
        return list_of_id

api.add_resource(emp,'/emp')
api.add_resource(emp_ids,'/emp/emp-ids')
api.add_resource(employee_by_id, '/emp/emp-id/<emp_id>')
api.add_resource(employee_by_country,'/emp/emp-country',endpoint='emp-country')
api.add_resource(root,'/')

if __name__=='__main__':
    global z
    global list_of_id
    z = json.loads(open('dataset.json','r').read())
    list_of_id = [record['id'] for record in z]
    list_of_cry = [record['country'].lower() for record in z]
    list_of_cry = [record.encode('ascii','ignore') for record in list_of_cry]
    app.run()
    

