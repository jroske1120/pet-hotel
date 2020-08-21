# import os
import psycopg2
import json
from flask_cors import CORS
# from os.path import exists
# from os import makedirs
from flask import Flask, jsonify, render_template, Response, request
app = Flask(__name__)
CORS(app)
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


@app.route('/api/owner/', methods=['GET'])
def ownerRouter():
      cur.execute("""SELECT * FROM owner
      WHERE deleted=FALSE
      ORDER BY id ASC""")
      rows = cur.fetchall()
      colnames = [desc[0] for desc in cur.description]
      # cur.close()
      # conn.commit()

      print(colnames)
      response = []
      for x in range( 0, len(rows) ):
        response.append({'id':rows[x][0]})
        for y in range(1, len(colnames)):
          response[x].update({colnames[y]:rows[x][y]})

      return jsonify(response)

# Get the pets
@app.route('/api/pet/', methods=['GET', 'POST'])
def petRouter():
  try:
    if(request.method =='GET'):
      cur.execute("""SELECT * FROM "pet"
      JOIN "owner" on "owner"."id" = "pet"."owner_id"
      WHERE deleted=FALSE
      ORDER BY "pet"."id" ASC
      """)
      rows = cur.fetchall()
      colnames = [desc[0] for desc in cur.description]
      # cur.close()
      # conn.commit()

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

      cur.execute("""INSERT INTO "pet" ("pets_name", "breed", "color", "owner_id")
                  VALUES
                  ('{}', '{}', '{}', '{}');""".format(data['pets_name'], data['breed'], data['color'], data['owner_id']))
      # petId = cur.fetchone()[0]
      # print("petID is:", petId)
      # cur.execute("""INSERT INTO "pet_owner" ("pet_id", "owner_id")
      #             VALUES ({}, {})""".format( petId, data['owner'] ))
      conn.commit()
      # conn.close()
      return Response('', status=201, mimetype='application/json')

  except Exception as e:
    print(e)
    return Response(e)
  # finally:
  #   # if conn is not None:
  #   print('inside finally')
  #   conn.close()


# add an owner
@app.route('/api/owner/<name>', methods=['POST'])
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
  # finally:
  #   if conn is not None:
  #     conn.close()


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

# DELETE pets
@app.route('/api/pet/<id>', methods=['DELETE'])
def deletePetRouter(id):
  try:
    cur.execute("""DELETE FROM pet WHERE id ={};""".format(id))
    print(id)
    conn.commit()

    return Response('', status=201, mimetype='application/json')
  except Exception as e:
    print(e)
    return []
  # finally:
  #   if conn is not None:
  #     conn.close()

########PUT##########
@app.route('/api/pet/checkin/<id>', methods=['PUT'])
def checkInPetRouter(id):
  try:

    data = request.get_json()

    cur.execute("""UPDATE pet SET "checkedIn" = {} WHERE id ={};""".format(data['checked_in'], id))
    print(id)
    conn.commit()

    return Response('', status=201, mimetype='application/json')
  except Exception as e:
    print(e)
    return []
  # finally:
  #   if conn is not None:
  #     conn.close()

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



if __name__ == "__main__":
  app.run(debug=True)