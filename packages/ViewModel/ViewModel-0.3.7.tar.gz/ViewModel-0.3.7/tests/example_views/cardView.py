from objdict import ObjDict

from tests.example_views.memberView import Cards, Members
from viewmodel import BaseView, DBMongoEmbedSource
from viewmodel.viewFields import (
    DateField, EnumField, IdField, IntField, ObjDictField, TxtField,
    viewModelDB
)


class CardView(BaseView):
    ''' a view of one or more card documents.  Each view can be a join of
    a parent list of cards (from member table) plus the data from card documents
    '''
    viewName_ = "Cards"
    models_ = Cards, DBMongoEmbedSource(viewModelDB, "members.cards")

    # used in mako fmpage for on screen display of viewname

    id = IdField(cases={})
    # salt        = IntField(cases={}) #no in db for Mongo
    membcard = ObjDictField(cases={}, name='key', src='members.cards')
    membcardk = TxtField(cases={}, name='id', src='members.cards')
    label = TxtField('Label for Card', 8, src='members.cards', rowLabel=True)
    leadLen = IntField(cases={})
    sqlid = TxtField(cases={})
    leadings = TxtField('', 8, cases={})
    trailings = TxtField('', 8, cases={})
    expire = TxtField('', 4, cases={})
    encrypted = TxtField('', 12, cases={})
    owf = TxtField('', 32, cases={})
    cardNumber = TxtField('', 24, cases={})
    nameOnCard = TxtField('Name On Card', 24)
    cardType = EnumField("Card Type",
                         fmt=dict(values=('E', 'V', 'M', 'A'), names=('EftPOS', 'Visa', 'MasterCard', 'Amex')
                                  )
                         )
    accountsOnCard = TxtField('', 8, cases={})
    defaultAcc = TxtField('', 1, cases={})
    allowOverride = TxtField('', 1, cases={})
    securecode = TxtField('', 6, cases={})
    encKey = TxtField('', 8, cases={})
    cardOnSaltSince = DateField()
    activeDate = DateField()
    address = IntField('enum which addr', cases={})
    defaultExpensexx = TxtField('to move to profile', 24, cases={})
    askOverridexx = TxtField('to move to profile', 24, hint='ask which expense?', cases={})

    def getRows_(self, *args, **kwargs):
        def cardreader(idx_):
            self.getJoin_('cards',
                          ObjDict(sqlid=self[idx_].membcard['sqlid']),
                          idx_)
            return {}

        def lazy(rows):
            # lazy_ indicates main row not yet loaded
            return [{'members.cards': row} for row in rows]

        def fromMemb(finddict):
            read = viewModelDB.default(Members).find(finddict)
            assert read.count() == 1, 'Problem finding member for cards'
            member = read[0]
            self.set_source_idx_('members.cards', member)
            return lazy(member['cards'])

        if not args:
            return []

        self._sources['cards'].loader = cardreader

        self._sources.cards.join_links = ['membcardk', 'membcard.id', 'membcard.sqlid']

        target = args[0]

        # if isinstance(target,dict):  # extract list from dict:(cards=[])
        #     target=target.get('cards', None)
        if isinstance(target, list):
            return lazy(target)

        else:
            return fromMemb(args[0])
