from flask import Flask

from app.admin.admin import admin
from app.admin.documents import documents
from app.autocomplete import autocomplete
from app.reception import reception
from app.reports import reports

app = Flask(__name__)

app.register_blueprint(reception, url_prefix="/reception")
app.register_blueprint(autocomplete, url_prefix="/autocomplete")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(documents, url_prefix="/admin/documents")
app.register_blueprint(reports, url_prefix="/reports")

