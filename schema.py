import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Users as UsersModel, Follows as FollowsModel#, Posts as PostsModel



class UserType(graphene.ObjectType):
	name = "UserType"
	description = '...'

	email = graphene.String()
	firstName = graphene.String()
	id = graphene.Int()
	lastName = graphene.String()
	username = graphene.String(description='Something you forget often')
	followers = graphene.List(lambda:UserType)
	#user_posts = graphene.List(lambda:PostsType)

	def resolve_followers(self, info, **args):
		# print(db_session.query(FollowsModel.follow_by).filter(FollowsModel.follow_to == 4).all())
		followers_list =  db_session.query(FollowsModel.follow_by).filter(FollowsModel.follow_to == self.id).all()
		l = list()

		for follower in followers_list:
			l.append(follower[0])

		l = tuple(l)
		userList = db_session.query(UsersModel).filter(UsersModel.id.in_(l)).all()
		return userList

	#def resolve_posts(self, info, **args):
		#return db_session.query(PostsModel).filter(PostsModel.post_by == self.id).all()


class QueryType(graphene.ObjectType):
	name='query'
	description='...'

	user = graphene.Field(
		UserType,
		id = graphene.Int()
		)

	def resolve_user(self, info, **args):
		id = args.get('id')
		#print(db_session.query(UsersModel.id,UsersModel.firstName,).first())
		requiredUser = db_session.query(UsersModel).filter(UsersModel.id == id)
		print(requiredUser.first())
		return requiredUser.first()

schema = graphene.Schema(query=QueryType)
