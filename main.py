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

        if email == "":
            email = "Neizpolnjen"

        sporocilo1 = Sporocilo(ime=ime, email=email, sporocilo=sporocilo)
        sporocilo1.put()

        self.render_template("poslano.html")


class SporocilaHandler(BaseHandler):
    def get(self):
        sporocila = Sporocilo.query(Sporocilo.izbrisano == False).order(-Sporocilo.created).fetch()

        params = {"sporocila": sporocila}

        self.render_template("sporocila.html", params)


class NoteHandler(BaseHandler):
    def get(self, note_id):
        note = Sporocilo.get_by_id(int(note_id))

        params = {"note": note}

        self.render_template("note.html", params)


class UrediHandler(BaseHandler):
    def get(self, note_id):
        note = Sporocilo.get_by_id(int(note_id))

        params = {"note": note}

        self.render_template("uredi.html", params)

    def post(self, note_id):
        urejen_ime = self.request.get("uredi_ime")
        urejen_email = self.request.get("uredi_email")
        urejen_sporocilo = self.request.get("uredi_sporocilo")

        if urejen_ime == "":
            urejen_ime = "Neznanec"

        if urejen_email == "":
            urejen_email = "Neizpolnjen"

        note = Sporocilo.get_by_id(int(note_id))
        note.ime = urejen_ime
        note.email = urejen_email
        note.sporocilo = urejen_sporocilo
        note.put()

        return self.redirect_to("sporocila")


class IzbrisiHandler(BaseHandler):
    def get(self, note_id):
        note = Sporocilo.get_by_id(int(note_id))

        params = {"note": note}

        self.render_template("izbrisi.html", params)

    def post(self, note_id):
        note = Sporocilo.get_by_id(int(note_id))

        note.izbrisano = True
        note.put()

        return self.redirect_to("sporocila")


class IzbrisanaSporocila(BaseHandler):
    def get(self):
        sporocila = Sporocilo.query(Sporocilo.izbrisano == True).order(-Sporocilo.created).fetch()

        params = {"sporocila": sporocila}

        self.render_template("izbrisana_sporocila.html", params)


class DeletedNote(BaseHandler):
    def get(self, deleted_note_id):
        deleted_note = Sporocilo.get_by_id(int(deleted_note_id))

        params = {"deleted_note": deleted_note}

        self.render_template("deleted_note.html", params)


class PovrniSporocilo(BaseHandler):
    def get(self, deleted_note_id):
        deleted_note = Sporocilo.get_by_id(int(deleted_note_id))

        params = {"deleted_note": deleted_note}

        self.render_template("povrni.html", params)

    def post(self, deleted_note_id):
        deleted_note = Sporocilo.get_by_id(int(deleted_note_id))

        deleted_note.izbrisano = False
        deleted_note.put()

        return self.redirect_to("izbrisana_sporocila")


class TrajnoIzbrisi(BaseHandler):
    def get(self, deleted_note_id):
        deleted_note = Sporocilo.get_by_id(int(deleted_note_id))

        params = {"deleted_note": deleted_note}

        self.render_template("trajno_izbrisi.html", params)

    def post(self, deleted_note_id):
        deleted_note = Sporocilo.get_by_id(int(deleted_note_id))

        deleted_note.key.delete()

        return self.redirect_to("izbrisana_sporocila")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/poslano', PoslanoHandler),
    webapp2.Route('/sporocila', SporocilaHandler, name="sporocila"),
    webapp2.Route('/note/<note_id:\d+>', NoteHandler),
    webapp2.Route('/note/<note_id:\d+>/uredi', UrediHandler),
    webapp2.Route('/note/<note_id:\d+>/izbrisi', IzbrisiHandler),
    webapp2.Route('/izbrisana_sporocila', IzbrisanaSporocila, name="izbrisana_sporocila"),
    webapp2.Route('/deleted_note/<deleted_note_id:\d+>', DeletedNote),
    webapp2.Route('/deleted_note/<deleted_note_id:\d+>/povrni', PovrniSporocilo),
    webapp2.Route('/deleted_note/<deleted_note_id:\d+>/trajno_izbrisi', TrajnoIzbrisi),
], debug=True)
