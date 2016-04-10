from flask import Flask, jsonify, request, make_response
#from flask.ext.httpauth import HTTPBasicAuth
from flask import render_template, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from socket import gethostname
from Manually_Curated_Clusters import app_get_and_print_the_recipe, get_all_clusters

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback_database.db'
app.config['SECRET_KEY'] = 'HALO'

db = SQLAlchemy(app)
#auth = HTTPBasicAuth()

class RecipeFeedback(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    rating = db.Column(db.String)
    feedback = db.Column(db.String)
    email = db.Column(db.String)
    date = db.Column(db.String)
    recipeid = db.Column(db.String)

@app.route('/make/<cluster>')
def makeRandom(cluster):
	#sleep(1)
	#line = '{"cluster":"Dosa","ingredients":[{"ingredient":"boiled rice (ukda chawal)"},{"ingredient":"toovar (arhar) dal"},{"ingredient":"chana dal (split bengal gram)"},{"ingredient":"urad dal (split black lentils)"},{"ingredient":"roughly chopped ginger (adrak)"},{"ingredient":"red chillies (pandi)"},{"ingredient":"black peppercorns (kalimirch)"},{"ingredient":"cumin seeds (jeera)"},{"ingredient":"finely chopped onions"},{"ingredient":"asafoetida (hing)"},{"ingredient":"chopped curry leaves (kadi patta)"},{"ingredient":"grated coconut"},{"ingredient":"salt to taste"}],"recipe":[{"step":"Combine the rice, dals, ginger, red chillies, peppercorns and cumin seeds"},{"step":"Blend the mixture in a mixer to a coarse mixture using approx. 1 cup of water."},{"step":"Transfer the mixture into a deep bowl, add the onions, asafoetida, curry leaves, grated coconut and salt and mix well."},{"step":"Heat a non-stick tava (griddle), sprinkle a little water on the tava (griddle) and wipe it off gently using a muslin cloth."},{"step":"Pour a ladleful of the batter on it and spread it in a circular motion to make a 175 mm. (7) diameter thin circle."},{"step":"Smear a little coconut oil over it and along the edges and cook on a medium flame "},{"step":"Serve immediately with coconut chutney."}]}'
	line = app_get_and_print_the_recipe(cluster, -1)
	return line	

@app.route('/make/<cluster>/<recipeID>')
def makeSpecific(cluster, recipeID):
	line = app_get_and_print_the_recipe(cluster, int(recipeID))
	return line	

@app.route('/clusters')	
def getClusters():
	line = get_all_clusters()
	return line

@app.route('/feedback', methods = [u'POST', u'GET'])
def feedbacker():
	if request.method == u'POST':
		jsonData = request.json
		
		newFeedback = RecipeFeedback()
		newFeedback.rating = jsonData['rating']
		newFeedback.feedback = jsonData['feedback']
		newFeedback.email = jsonData['email']
		newFeedback.date = jsonData['date']
		newFeedback.recipeid = jsonData['recipeid']

		db.session.add(newFeedback)
		db.session.commit()

		return jsonify(result = 'created feedback successfully')

	elif request.method == u'GET':
		jsonData = []
		results = RecipeFeedback.query.all()
		for result in results :
			jsonData.append({'id':result.id,'email':result.email, 'rating':result.rating,'feedback':result.feedback, 'date' :result.date, 'recipeid': result.recipeid})
		return jsonify(feedback = jsonData)

@app.route('/feedback/delete/<id>')
def feedbackDelete(id):
	RecipeFeedback.query.filter_by(id=id).delete()
	db.session.commit()
	return redirect(url_for('feedbacker'))

if __name__ == '__main__' :
	db.create_all()
	app.run(host="192.168.150.1",port=8080, debug=True)
	#app.run(host="127.0.0.1",port=5000)
	#sudo app.run(debug=True)