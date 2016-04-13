#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@w4111a.eastus.cloudapp.azure.com/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@w4111a.eastus.cloudapp.azure.com/proj1part2"
#
DATABASEURI = "postgresql://acc2193:W4111project@w4111a.eastus.cloudapp.azure.com/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
# engine.execute("""CREATE TABLE IF NOT EXISTS test (
#   id serial,
#   name text
# );""")
# engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass

@app.route('/')
def index():
	return render_template("index.html")	

@app.route('/chemistry')
def chemistry():
	data_to_send = ["",0]

	context = dict(data = data_to_send)
	
	return render_template("chemistry.html", **context)	

@app.route('/compute_chemistry')
def compute_chemistry():
	
	print request.args

	positions = {}

	positions['lb'] = request.args["LB"]
	positions['cb1'] = request.args["CB1"]
	positions['cb2'] = request.args["CB2"]		
	positions['rb'] = request.args["RB"]	
	positions['cdm'] = request.args["CDM"]
	positions['cm1'] = request.args["CM1"]
	positions['cm2'] = request.args["CM2"]
	positions['lw'] = request.args["LW"]
	positions['rw'] = request.args["RW"]
	positions['st'] = request.args["ST"]

	queried_players = []
	
	team_chemistry = 0
	
	for position in positions:
		query = text("SELECT p.pid, p.pname, p.position, p.overall FROM players p WHERE p.pname ILIKE '%%%s%%' AND p.overall = (SELECT MAX(p2.overall) FROM players p2 WHERE p2.pname ILIKE '%%%s%%')" % (positions[position], positions[position]))
	
		cursor = g.conn.execute(query)

		result = ''
		
		for item in cursor:
			result = item

		cursor.close()
	
		pid = result[0]	
		name = result[1]
		assigned_position = position
		player_preferred_position = result[2]

		query = text("SELECT plays.tid FROM plays_for plays WHERE plays.pid = %s" % pid)

		cursor = g.conn.execute(query)
	
		club_id = ''
		nation_id = ''
	
		for item in cursor:
			if item[0] <= 228:
				club_id = item[0]
			else:
				nation_id = item[0]

		cursor.close()

		club = ''
		league = ''
		nation = ''
	
		query = text("SELECT c.clubname, c.lname FROM clubs c WHERE c.tid = %s" % club_id)
	
		cursor = g.conn.execute(query)

		for item in cursor:
			club = item[0]
			league = item[1]

		cursor.close()

		query = text("SELECT n.nname FROM national_teams n WHERE n.tid = %s" % nation_id)

		cursor = g.conn.execute(query)

		for item in cursor:
			nation = item[0]
			
		cursor.close()

		chemistry = 0
	
		if assigned_position == "lb":
			if player_preferred_position == "LB":
				chemistry = 5
			elif player_preferred_position == "RB":
				chemistry = 4
			elif player_preferred_position == "CB":
				chemistry = 2
			else:
				chemistry = 0	
			assigned_position = "LB"
		elif assigned_position == "cb1" or assigned_position == "cb2":
			if player_preferred_position == "CB":
				chemistry = 5
			elif player_preferred_position == "RB" or player_preferred_position == "LB":
				chemistry = 3
			else:
				chemistry = 0
			assigned_position = "CB"
		elif assigned_position == "rb":
			if player_preferred_position == "RB":
				chemistry = 5
			elif player_preferred_position == "LB":
				chemistry = 4
			elif player_preferred_position == "CB":
				chemistry= 2	
			else:
				chemistry = 0
			assigned_position = "RB"
		elif assigned_position == "cdm":
			if player_preferred_position == "CDM":
				chemistry = 5
			elif player_preferred_position == "CM":
				chemistry = 4
			else:
				chemistry = 0
			assigned_position = "CDM"
		elif assigned_position == "cm1" or assigned_position == "cm2":
			if player_preferred_position == "CM":
				chemistry = 5
			elif player_preferred_position == "CDM":
				chemistry = 4
			elif player_preferred_position == "CAM" or player_preferred_position == "RM" or player_preferred_position == "LM":
				chemistry = 3
			else:
				chemistry = 0
			assigned_position = "CM"
		elif assigned_position == "lw":
			if player_preferred_position == "LW":
				chemistry = 5
			elif player_preferred_position == "RW":
				chemistry = 4
			elif player_preferred_position == "ST" or player_preferred_position == "CF":
				chemistry = 2
			else:
				chemistry = 0
			assigned_position = "LW"
		elif assigned_position == "rw":
			if player_preferred_position == "RW":
				chemistry = 5
			elif player_preferred_position == "LW":
				chemistry = 4
			elif player_preferred_position == "ST" or player_preferred_position == "CF":
				chemistry = 2
			else:
				chemistry = 0
			assigned_position = "RW"
		elif assigned_position == "st":
			if player_preferred_position == "ST" or player_preferred_position == "CF":
				chemistry = 5
			elif player_preferred_position == "LW" or player_preferred_position == "RW":
				chemistry = 3
			else: 
				chemsitry = 0
			assigned_position = "ST"
		else: 
			chemistry = 0 

		queried_players.append([name, assigned_position, player_preferred_position, club, league,  nation, chemistry])

	for player in queried_players:
		player_name = player[0]
		player_club = player[3]
		player_league = player[4]
		player_nation = player[5]
	
		for other_player in queried_players:
			other_player_name = other_player[0]
			other_player_club = other_player[3]
			other_player_league = other_player[4]
			other_player_nation = other_player[5]
			
			if player_name != other_player_name:
				if player_club == other_player_club:
					player[6] += 2
				if player_league == other_player_league:
					player[6] += 1
				if player_nation == other_player_nation:
					player[6] += 1


		if player[6] > 10:
			player[6] = 10

		team_chemistry = team_chemistry + player[6]


	data_to_send = (queried_players, team_chemistry)
	
	context = dict(data = data_to_send)
	
	return render_template("chemistry.html", **context)	

@app.route('/sortbot')
def sortbot():
	return render_template("sortbot.html")

@app.route('/search')
def search():	
	
	print request.args

	# Pagination
	if "page" not in request.args:
		page = 1
	else:
		if int(request.args["page"]) > 0:
			page = int(request.args["page"])	
		else:
			page = 1

	sortby = request.args["sortby"]

	order = request.args["order"]

	if request.args["min_overall"] == '':
		min_overall = 0
	else:
		min_overall = request.args["min_overall"]
	
	if request.args["max_overall"] == '':
		max_overall = 99
	else:
		max_overall = request.args["max_overall"]

	if request.args["position"] == 'null':
		position = text("ANY(ARRAY['GK','CB','LB','RB','CDM','CM','CAM','LM','RM','LW','RW','CF','ST'])")
	elif request.args["position"] == 'DEF':
		position = text("ANY(ARRAY['CB','LB','RB'])")
	elif request.args["position"] == 'MID':
		position = text("ANY(ARRAY['CDM','CM','CAM','LM','RM'])")
	elif request.args["position"] == 'ATT':
		position = text("ANY(ARRAY['LW','RW','CF','ST'])")
	else:
		position = text("'%s'"%request.args["position"])

	# Get table data
	query = text("SELECT p.pname, p.position, p.overall, p.passing, p.pace, p.dribbling, p.shooting, p.defense, p.physical FROM players p WHERE p.overall >= %s AND p.overall <= %s AND p.position = %s AND p.pname ILIKE '%%%s%%' ORDER BY %s %s" % (min_overall, max_overall, position, request.args['name'], sortby, order))
	print query
	cursor = g.conn.execute(query)
	table_data = []
	for row in cursor:
		table_data.append(row)
	cursor.close()

	#data_to_send = table_data[(page-1)*50:(page*50)+1]
	data_to_send = table_data
	
	context = dict(data = data_to_send)
	
	return render_template("index.html", **context)	



@app.route('/sort')
def sort():	
	
	print request.args
	
	attr1 = request.args["attr1"]
	attr2 = request.args["attr2"]
	attr3 = request.args["attr3"]

	sortby = text("(%s*1.0) + (%s*0.8) + (%s*0.6)" % (attr1,attr2,attr3))

	if request.args["min_overall"] == '':
		min_overall = 0
	else:
		min_overall = request.args["min_overall"]
	
	if request.args["max_overall"] == '':
		max_overall = 99
	else:
		max_overall = request.args["max_overall"]

	if request.args["position"] == 'null':
		position = text("ANY(ARRAY['GK','CB','LB','RB','CDM','CM','CAM','LM','RM','LW','RW','CF','ST'])")
	elif request.args["position"] == 'DEF':
		position = text("ANY(ARRAY['CB','LB','RB'])")
	elif request.args["position"] == 'MID':
		position = text("ANY(ARRAY['CDM','CM','CAM','LM','RM'])")
	elif request.args["position"] == 'ATT':
		position = text("ANY(ARRAY['LW','RW','CF','ST'])")
	else:
		position = text("'%s'"%request.args["position"])

	# Get table data
	query = text("SELECT p.pname, p.position, p.overall, p.passing, p.pace, p.dribbling, p.shooting, p.defense, p.physical FROM players p WHERE p.overall >= %s AND p.overall <= %s AND p.position = %s ORDER BY %s DESC" % (min_overall, max_overall, position, sortby))
	print query
	cursor = g.conn.execute(query)
	table_data = []
	for row in cursor:
		table_data.append(row)
	cursor.close()

	data_to_send = table_data
	
	
	
	context = dict(data = data_to_send)
	
	return render_template("sortbot.html", **context)	


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
  return redirect('/')


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
