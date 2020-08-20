# import os
import psycopg2
import json
# from os.path import exists
# from os import makedirs
from flask import Flask, jsonify, render_template, Response, request
app = Flask(__name__)
# config = {
#         user: process.env.PG_USER || null, //env var: PGUSER
#         password: process.env.DATABASE_SECRET || null, //env var: PGPASSWORD
#         host: process.env.DATABASE_SERVER || 'localhost', // Server hosting the postgres database
#         port: process.env.DATABASE_PORT || 5432, //env var: PGPORT
#         database: process.env.DATABASE_NAME || 'saga_movies_weekend', //env var: PGDATABASE or the name of your database (e.g. database: process.env.DATABASE_NAME || 'koala_holla',)
#         max: 10, // max number of clients in the pool
#         idleTimeoutMillis: 30000, // how long a client is allowed to remain idle before being closed
#     };

#  Original code:
# url = urlparse.urlparse(os.environ.get('DATABASE_URL'))
# db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
db = "dbname=%s host=%s " % ('pet_hotel', 'localhost')
schema = "schema.sql"
# conn = None
conn = psycopg2.connect(db)
conn.autocommit = True

cur = conn.cursor()


# Get the pets
@app.route('/pets/', methods=['GET', 'POST'])
def petRouter():
  try:
    if(request.method =='GET'):
      cur.execute("""SELECT * FROM pet ORDER BY id ASC""")
      rows = cur.fetchall()
      colnames = [desc[0] for desc in cur.description]
      # cur.close()
      conn.commit()

      print(colnames)
      response = []
      for x in range( 0, len(rows) ):
        response.append({'id':rows[x][0]})
        for y in range(1, len(colnames)):
          response[x].update({colnames[y]:rows[x][y]})

      return jsonify(response)
    elif request.method=='POST' :
      #data = request.data
      # conn.autocommit = False
      data = request.get_json()
      print("request data", data['name'])

      cur.execute("""INSERT INTO "pet" ("name", "breed", "color")
                  VALUES 
                  ('{}', '{}', '{}') RETURNING id;""".format(data['name'], data['breed'], data['color']))
      petId = cur.fetchone()[0]
      print("petID is:", petId)
      cur.execute("""INSERT INTO "pet_owner" ("pet_id", "owner_id")
                  VALUES ({}, {})""".format( petId, data['owner'] ))
    #   conn.commit()
      # conn.close()
      return Response('', status=201, mimetype='application/json')

  except Exception as e:
    print(e)
    return Response(e)
  finally:
    # if conn is not None:
    print('inside finally')
    conn.close()


# add an owner
@app.route('/owners/<name>', methods=['POST'])
def addOwnerRouter(name):
  try:
    cur.execute("""INSERT INTO "owner" ("name")
VALUES 
('{}');""".format(name))
    conn.commit()

    print(name)

    return Response('', status=201, mimetype='application/json')
  except Exception as e:
    print(e)
    return []
  finally:
    if conn is not None:
      conn.close()


# Add a pet
# pet = {
#     name: '',
#     breed: '',
#     color: ''
# }

# dictionary, but you can't pass a dictionary via url

# @app.route('/pets/<pet>', methods=['POST'])
# def addPetRouter(pet):
#     # trying something
#       try:
#     new_pet = (
#         name=request.json['name'],
#         breed=request.json['breed'],
#         color=request.json['color']
#     )
#     data = request.data
#     print("request data", data)
#     print("new_pet", new_pet)
#     cur.execute("""INSERT INTO "owner" ("name")
# VALUES 
# ('{}');""".format(name))

#     print(name)

#     return Response('', status=201, mimetype='application/json')
#   except Exception as e:
#     print(e)
#     return []

# delete pets
@app.route('/pets/<id>', methods=['DELETE'])
def deletePetRouter(id):
  try:
    cur.execute("""DELETE FROM pet WHERE id ={};""".format(id))
    print(id)
    conn.commit()

    return Response('', status=201, mimetype='application/json')
  except Exception as e:
    print(e)
    return []
  finally:
    if conn is not None:
      conn.close()


@app.route('/pets/<id>', methods=['PUT'])
def checkInPetRouter(id):
  try:
    cur.execute("""UPDATE pet SET "checkedIn" = true WHERE id ={};""".format(id))
    print(id)
    conn.commit()

    return Response('', status=201, mimetype='application/json')
  except Exception as e:
    print(e)
    return []
  finally:
    if conn is not None:
      conn.close()

    #   This is how it looks in js
  #   pool.query("""SELECT * FROM movies ORDER BY title ASC""")
  #     .then( (results) => 
  #     rows = results
  #   [
  #     {id: 7, petname: 'spike', animal: 'dog'}
  #   ]

  # y ->      0     1         2         3
  # x
  # 0    [7,     spike,    dog,      attribute]
  
  # 1    [8,     fido,     dog,      attribute]

  #   [ id, petname, animal, columnTitle]
  #   [
  #     [each, row, gets, it's own', array],
  #     [next, row]
  #   ]

  # [
  #   { id: 7, }
  # ]



# module.exports = router;


# @app.route('/details/<id>', methods=['GET'])
# def detailRouter(id):
#   try:
#     cur.execute('''SELECT
#       "movies"."title",
#       "movies"."poster",
#       "movies"."description",
#       ARRAY_AGG("name") "genres"
#     FROM "movies"
#     JOIN "movies_genres" ON "movie_id" = "movies"."id"
#     JOIN "genres" ON "genre_id" = "genres"."id"
#     WHERE "movies"."id" = {}
#     GROUP BY "movies"."id"
#     ORDER BY "movies"."title" ASC'''.format(id))
#     rows = cur.fetchall()
#     colnames = [desc[0] for desc in cur.description]
#     cur.close()
#     print(colnames)
#     response = []
#     for x in range( 0, len(rows) ):
#       response.append({'id':id })
#       for y in range(0, len(colnames)):
#         response[x].update({colnames[y]:rows[x][y]})
#     print(response)
#     return jsonify(response)
#   except Exception as e:
#     print(e)
#     return []

# @app.route('/genres', methods=['GET'])
# def genreRouter():
#   try:
#     cur.execute("""SELECT * FROM genres ORDER BY id ASC""")
#     rows = cur.fetchall()
#     colnames = [desc[0] for desc in cur.description]
#     cur.close()
#     print(colnames)
#     response = []
#     for x in range( 0, len(rows) ):
#       response.append({'id':rows[x][0]})
#       for y in range(1, len(colnames)):
#         response[x].update({colnames[y]:rows[x][y]})

#     return jsonify(response)
#   except Exception as e:
#     print(e)
#     return []


if __name__ == "__main__":
  app.run(debug=True)


# const express = require('express');
# const app = express();
# const bodyParser = require('body-parser');
# const port = process.env.PORT || 5000;

# // require routers
# const detailsRouter = require('./routes/details.router');
# const genresRouter = require('./routes/genres.router');
# const moviesRouter = require('./routes/movies.router');

# /** ---------- MIDDLEWARE ---------- **/
# app.use(bodyParser.json()); // needed for angular requests
# app.use(express.static('build'));

# /** ---------- ROUTES ---------- **/
# app.use('/details', detailsRouter);
# app.use('/genres', genresRouter);
# app.use('/movies', moviesRouter);


# /** ---------- START SERVER ---------- **/
# app.listen(port, function () {
#     console.log('Listening on port: ', port);
# });
