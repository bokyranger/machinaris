import datetime as dt

from flask.views import MethodView

from api import app
from api.extensions.api import Blueprint, SQLCursorPage
from common.extensions.database import db
from common.models import Key

from .schemas import KeySchema, KeyQueryArgsSchema


blp = Blueprint(
    'Keys',
    __name__,
    url_prefix='/keys',
    description="Operations on keys"
)


@blp.route('/')
class Keys(MethodView):

    @blp.etag
    @blp.arguments(KeyQueryArgsSchema, location='query')
    @blp.response(200, KeySchema(many=True))
    @blp.paginate(SQLCursorPage)
    def get(self, args):
        return db.session.query(Key).filter_by(**args)

    @blp.etag
    @blp.arguments(KeySchema)
    @blp.response(201, KeySchema)
    def post(self, new_item):
        item = db.session.query(Key).filter(Key.hostname==new_item['hostname'], \
            Key.blockchain==new_item['blockchain']).first()
        if item: # upsert
            new_item['created_at'] = item.created_at
            new_item['updated_at'] = dt.datetime.now()
            KeySchema().update(item, new_item)
        else: # insert
            item = Key(**new_item)
        db.session.add(item)
        db.session.commit()
        return item


@blp.route('/<hostname>/<blockchain>')
class KeysByHostnameBlockchain(MethodView):

    @blp.etag
    @blp.response(200, KeySchema)
    def get(self, hostname, blockchain):
        return db.session.query(Key).filter(Key.hostname==hostname, \
            Key.blockchain==blockchain).first()

    @blp.etag
    @blp.arguments(KeySchema)
    @blp.response(200, KeySchema)
    def put(self, new_item, hostname, blockchain):
        item = db.session.query(Key).filter(Key.hostname==hostname, \
            Key.blockchain==blockchain).first()
        new_item['hostname'] = item.hostname
        new_item['created_at'] = item.created_at
        new_item['updated_at'] = dt.datetime.now()
        blp.check_etag(item, KeySchema)
        KeySchema().update(item, new_item)
        db.session.add(item)
        db.session.commit()
        return item

    @blp.etag
    @blp.response(204)
    def delete(self, hostname, blockchain):
        item = db.session.query(Key).filter(Key.hostname==hostname, \
            Key.blockchain==blockchain).first()
        blp.check_etag(item, KeySchema)
        db.session.delete(item)
        db.session.commit()