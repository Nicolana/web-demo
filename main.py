# encoding: utf-8
import web
import json

web.config.debug = False
urls = (
	'/', 		'index',
	'/index',   'index',
	'/login', 	'login',
	'/reset',	'reset',
	'/post', 	'post',
	'/admin',	'admin',
	'/edit',	'edit'
)
app = web.application(urls, globals())
render = web.template.render('template/')
db = web.database(dbn='postgres', user="postgres", pw="123456", db="webpy", 
	host="192.168.3.20", port=5432)
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'login': 0})

def logged():
	if session.login == 1:
		return True
	else:
		return False

class index:
	def GET(self):
		todos = db.select('todo') # 查询
		return render.main(todos)


class login:
	def GET(self):
		if logged():
			raise web.seeother("/admin")
		else:
			return "%s" % render.login()

	def POST(self):
		username, password = web.input().username, web.input().password
		indent = db.select('blog_users', where='username=$username', vars=locals())[0]
		web.header('Content-Type', 'application/json')
		try:
			if password == indent.pwd:
				session.login = 1
				return json.dumps({'login':1, 'status': 'success'})
			else:
				session.login =0
				return json.dumps({'login':0, 'status': 'failed'})				
		except:
			session.login = 0
			return json.dumps({'login':0, 'status': 'failed'})


class post:
	def POST(self):
		web.header('Content-Type', 'application/json')
		if logged():
			i = web.input()
			method = i.method
			if method == "update":
				pass
			elif  method == "delete":
				pass
			elif method == "add":
				n = db.insert("blog", title=i.title, )
		else:
			return json.dumps({'success':0, 'message': 'Not Login'})


class admin:
	def GET(self):
		if logged():
			entries = db.select("blog")
			return render.admin(entries)
		else:
			raise web.seeother("/login")

class edit:
	def GET(self):
		if logged():
			m = web.input(m=None), p = web.input(p=None)
			if p and m:
				entries = db.select("blog", where="")
		else:
			raise web.seeother("/login")
	def POST(self):
		pass


if __name__ == "__main__":
	app.run()
