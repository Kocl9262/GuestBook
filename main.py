#!/usr/bin/env python
import os
import jinja2
import webapp2

from models import Sporocilo


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        self.render_template("index.html")


class PoslanoHandler(BaseHandler):
    def post(self):
        ime = self.request.get("ime")
        email = self.request.get("email")
        sporocilo = self.request.get("sporocilo")

        if ime == "":
            ime = "Neznanec"
        else:
            ime = ime

        if email == "":
            email = "Neizpolnjen"
        else:
            email = email

        sporocilo1 = Sporocilo(ime=ime, email=email, sporocilo=sporocilo)
        sporocilo1.put()

        self.render_template("poslano.html")


class SporocilaHandler(BaseHandler):
    def get(self):
        sporocila = Sporocilo.query().order(-Sporocilo.created).fetch()

        params = {"sporocila": sporocila}

        self.render_template("sporocila.html", params)


class NoteHandler(BaseHandler):
    def get(self, note_id):
        note = Sporocilo.get_by_id(int(note_id))

        params = {"note": note}

        self.render_template("note.html", params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/poslano', PoslanoHandler),
    webapp2.Route('/sporocila', SporocilaHandler),
    webapp2.Route('/note/<note_id:\d+>', NoteHandler),
], debug=True)
