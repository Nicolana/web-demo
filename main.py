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
	'/edit',	'edit',
	'/delete',  'delete'
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


class delete:
	def POST(self):
		if logged():
			web.header('Content-Type', 'application/json')
			i = web.input(p=None)
			if i.p:
				db.delete("blog", where="id="+i.p)
				return json.dumps({"success": 1,"message": "删除成功"})
			return json.dumps({"success": 0, "message": "删除失败"})

class edit:
	def GET(self):
		if logged():
			i = web.input(p=None)
			if i.p:
				print(i)
				entries = db.select("blog", i, where="id=$p")[0]
				return render.edit(entries)
			else:
				return render.edit(entries=None)
		else:
			raise web.seeother("/login")

	def POST(self):
		if logged():
			i = web.input(p=None, title=None, content=None)
			web.header('Content-Type', 'application/json')
			if not i.p:
				title = i.title if i.title != None else " "
				contents = i.contents if i.contents != None else " "
				db.insert("blog", title=title, contents=contents, author=1);
				return json.dumps({'success':1, "message": "add blog success"})
			elif i.p:
				title = i.title if i.title != None else " "
				contents = i.contents if i.contents != None else " "
				db.update("blog", title=title, where="id=" + i.p, contents=contents, author=1, updated="now()");
				return json.dumps({'success':1, "message": "add blog success"})	
		else:
			return "Please Login."


if __name__ == "__main__":
	app.run()
