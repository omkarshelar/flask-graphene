from flask import Flask, request, jsonify
from flask_graphql import GraphQLView
from models import db_session, Users as UsersModel, Follows as FollowsModel
import json
from schema import schema

app = Flask(__name__)
#app.debug = True

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)

@app.route('/rest/user/', methods=["GET"])
def rest_endpoint_handler():
	id = request.args.get('id')
	if id is not None:
		user = db_session.query(UsersModel).filter(UsersModel.id == id).first()
		followers = db_session.query(FollowsModel.follow_by).filter(FollowsModel.follow_to == id).all()
		d = dict()
		d['firstName'] = user.firstName
		d['lastName'] = user.lastName
		d['username'] = user.username
		d['email'] = user.email
		l = list()
		for follower in followers:
			l.append('/rest/user/?id='+str(follower[0]))

		d['followers'] = l
		return jsonify(resultSet = d)
	else:
		users = db_session.query(UsersModel).filter().all()
		l1 = list()
		for user in users:
			followers = db_session.query(FollowsModel.follow_by).filter(FollowsModel.follow_to == user.id).all()
			d = dict()
			d['firstName'] = user.firstName
			d['lastName'] = user.lastName
			d['username'] = user.username
			d['email'] = user.email
			l = list()
			for follower in followers:
				l.append('/rest/user/?id='+str(follower[0]))
			d['followers'] = l
			l1.append(d)
		return jsonify(resultSet = l1)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run()
