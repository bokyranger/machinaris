import datetime as dt

from flask.views import MethodView

from api import app
from api.commands import websvcs
from api.extensions.api import Blueprint, SQLCursorPage
from common.extensions.database import db
from common.models import StatTotalCoins

from .schemas import StatTotalCoinsSchema, StatTotalCoinsQueryArgsSchema, BatchOfStatTotalCoinsSchema, BatchOfStatTotalCoinsQueryArgsSchema


blp = Blueprint(
    'StatTotalCoins',
    __name__,
    url_prefix='/stats/totalcoins',
    description="Operations on stat totalcoins recorded on each worker."
)


@blp.route('/')
class StatTotalCoinss(MethodView):

    @blp.etag
    @blp.arguments(BatchOfStatTotalCoinsQueryArgsSchema, location='query')
    @blp.response(200, StatTotalCoinsSchema(many=True))
    @blp.paginate(SQLCursorPage)
    def get(self, args):
        ret = db.session.query(StatTotalCoins).filter_by(**args)
        return ret

    @blp.etag
    @blp.arguments(BatchOfStatTotalCoinsSchema)
    @blp.response(201, StatTotalCoinsSchema(many=True))
    def post(self, new_items):
        if len(new_items) == 0:
            return "No stats provided.", 400
        items = []
        for new_item in new_items:
            cold_wallet_farmed_balance = websvcs.cold_wallet_farmed_balance(new_item['blockchain'])
            if cold_wallet_farmed_balance is not None: # If none, we got an error from ATB, so don't save a farmed total coins
                if cold_wallet_farmed_balance > 0:
                    app.logger.info("Adding cold farmed balance of {0} for {1}".format(cold_wallet_farmed_balance, new_item['blockchain']))
                new_item['value'] += cold_wallet_farmed_balance
                item = StatTotalCoins(**new_item)
                items.append(item)
                db.session.add(item)
        db.session.commit()
        return items
