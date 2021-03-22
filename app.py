from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask,request,jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Swagger Specifications #
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Buscaminas PvP"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix = SWAGGER_URL)
# End Swagger Specifications #

# MySQL Connection
app.config['MYSQL_HOST'] = 'b9l7iiupadf8mvxind2z-mysql.services.clever-cloud.com'
app.config['MYSQL_USER'] = 'uajht2lef1p3tiby'
app.config['MYSQL_PASSWORD'] = 'zARsW6mMsMhwD6Awvgp3'
app.config['MYSQL_DB'] = 'b9l7iiupadf8mvxind2z'

mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

@app.route('/api/users', methods=['POST'])
def add_user():
  if(request.method == 'POST'):
    body = request.json
    email = body['email']
    username = body['username']
    uid = body['id']
    img = body['img']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (email,username,id,img,last_matches,last_scores) VALUES (%s,%s,%s,%s,%s,%s)", (email,username,uid,img,'',''))
    mysql.connection.commit()
    return jsonify(({
      'id': uid,
      'username': username,
      'email': email,
      'img': img,
      'last_matches': '',
      'last_scores': ''
    }))

@app.route('/api/users/<id>', methods=['GET'])
def get_user(id):
  if(request.method == 'GET'):
    cur = mysql.connection.cursor()
    newQuery = """SELECT * FROM users WHERE users.id = '%s'""" % (id)
    cur.execute(newQuery)
    result = cur.fetchall()
    field = cur.description
    column = []
    for i in field:
      column.append(i[0])
    data_user = {}
    for row in result:
      for i in range(len(column)):
        data_user[column[i]] = row[i]
    return jsonify(data_user)

@app.route('/api/feedback', methods=['POST'])
def add_feedback():
  if(request.method == 'POST'):
    body = request.json
    name = body['name']
    email = body['email']
    message = body['message']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO feedback(name,email,message) VALUES (%s,%s,%s)", (name,email,message))
    mysql.connection.commit()
    return jsonify({'response':True})

@app.route('/api/ranking', methods = ['POST','GET'])
def manage_rankings():
  if(request.method == 'POST'):
    body = request.json
    uuid = body['id']
    username = body['username']
    img = body['img']
    time = body['time']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO ranking(id,username,img,time) VALUES (%s,%s,%s,%s)", (uuid,username,img,time))
    cur.execute("INSERT INTO users(last_scores) VALUES (%s) WHERE users.id = '%s'", (time, id))
    mysql.connection.commit()
    return jsonify({
      'id': uuid,
      'username': username,
      'img': img,
      'time': time
    })
  elif(request.method == 'GET'):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ranking ORDER BY time ASC")
    results = cur.fetchall()
    field = cur.description
    column = []
    for i in field:
      column.append(i[0])
    data_ranking = {}
    for row in results:
      for i in range(len(column)):
        data_ranking[column[i]] = row[i]
    return jsonify(data_ranking)

if __name__ == '__main__':
    app.run(port = 5000, debug = True)