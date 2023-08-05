# -*- coding: utf-8 -*-
# Tests of pymongo interface to members and cards

import pytest
from pymongo import MongoClient

# import saltMongDB
# from sbextend import SaltReq
from tests.conftest import TEST_DB_NAME
from tests.example_views.cardView import CardView
from tests.example_views.memberView import MemberView


@pytest.fixture
def memberView():
    return MemberView(dict(sqlid=8))  # ObjDict(memberID='ian')


@pytest.fixture
def membersView():
    return MemberView(dict())  # ObjDict(memberID='ian')


class TestMembers:
    def test_member(self, memberView):
        mv = memberView
        assert len(mv) == 1
        assert mv.memberID == 'ian'

    def test_member_given_name(self, memberView):
        mv = memberView
        assert len(mv) == 1
        assert mv.fields_['name'].src == 0
        assert mv.fields_['name'].raw_src == ''
        assert mv.fields_['name'].src_dicts == []
        assert mv.name.givenNames == 'iann'
        assert mv.fields_['givenNames'].src == 0
        assert mv.fields_['givenNames'].raw_src == '.name'
        assert mv.fields_['givenNames'].src_dicts == ['name']
        assert mv.givenNames == 'iann'

    def test_member_given_name_set(self, memberView):
        mv = memberView
        assert len(mv) == 1
        assert mv.name.givenNames == 'iann'
        assert mv.givenNames == 'iann'
        assert mv.quickName == 'ian3'
        with mv:
            mv.quickName = 'newname'
            mv.givenNames = 'testing'
            changes = mv.changes_[0]['members'].copy()
            assert mv.givenNames == 'testing'
            assert 'name.givenNames' in changes
        # import pdb; pdb.set_trace()
        # pass

    def test_view_form(self, memberView):
        mv = memberView
        names = 'memberID', 'quickName', 'name', 'nameType', 'plan'
        for nm, fld in zip(names, mv.fields_()):
            assert fld.name == nm

        assert fld.label == 'Shaker Type'  # just testing last one

    def test_members_rows(self, membersView):
        mv = membersView
        assert len(mv) == 3
        names = 'ian', 'Michael', ' default'
        for n, m in zip(names, mv.fields_.loopRows()):
            assert m.memberID == n
            assert mv != m

    def test_members_index(self, membersView):
        mv = membersView
        assert mv[1].memberID == 'Michael'

    def test_member_json(self, membersView):
        # import pdb; pdb.set_trace()
        jsmemb = membersView.__json__(True)
        assert len(jsmemb.data) == 3
        jscards = jsmemb.data[0]['cards']
        assert len(jscards) == 3
        assert jscards[0]['label'] == 'card1'


class TestFieldAccess:
    def test_members_fields(self, membersView):
        mv = membersView
        assert len(mv) == 3
        names = 'ian', 'Michael', ' default'
        for n, m in zip(names, mv.fields_.loopRows()):
            its = m.fields_.items()
            key, value = list(its)[2]
            assert value.value == n

    def test_members_fields_row_fields_items(self, membersView):
        mv = membersView
        assert len(mv) == 3
        names = 'ian', 'Michael', ' default'
        for n, m in zip(names, mv):
            its = m.fields_.items()
            key, value = list(its)[2]
            assert value.value == n
            assert value.name == 'memberID'

    def test_members_fields_new(self, membersView):
        mv = membersView
        assert len(mv) == 3
        names = 'ian', 'Michael', ' default'
        for n, m in zip(names, mv):
            its = m.fields_.items()
            key, value = list(its)[2]
            assert value.value == n
            assert value.name == 'memberID'

    def test_members_fields_postID(self, membersView):
        mv = membersView
        assert mv._baseFields['notes'].name == 'notes'
        assert mv._baseFields['notes'].postID == 'fieldnotes'
        assert mv._baseFields['priorRequests'].name == 'prior'
        assert mv._baseFields['priorRequests'].postID == 'fieldpriorRequests'
        assert mv._baseFields['priorPickUps'].name == 'prior'
        assert mv._baseFields['priorPickUps'].postID == 'fieldpriorPickUps'


class TestComplexFieldsUsingCardData:
    def test_access_inside(self):
        cv = CardView({"sqlid": 8})
        c2 = cv[1]
        assert c2.membcard['sqlid'] == 96

    def test_change_inside(self):
        cv = CardView({"sqlid": 8})
        c2 = cv[1]
        with c2:
            vals = c2.membcard
            vals['sqlid'] = 97
            vals.id = c2.id
            c2.membcard = vals
        assert c2.membcard['sqlid'] == 97
        assert c2.membcard['id'] == c2.id


class TestCards:
    def test_view_cards_by_join_table_in_memberview(self, membersView):
        """ cards - members relationship is many to many with join table embedded in members
        view all cards for member is instanced with the embedded table as the parameter
        """
        row = membersView[0]
        cv = CardView(dict(cards=row.cards))
        card0 = cv[0]
        assert isinstance(cv._dbRows, list)
        assert len(cv._dbRows) == 3, "test db has 3 cards for this member with 3 entries"
        row1 = cv._dbRows[0]
        assert isinstance(row1, dict), "each row is a dictionary of the sources"
        assert len(row1) > 0, "each dictionary should have at least one source already"
        assert "members.cards" in row1
        assert isinstance(row1["members.cards"], dict)
        assert card0.label == "card1"  # field from members.card source
        # currently one only source present, other retrieved on demand
        assert len(row1) == 1, 'one source now'
        assert card0.leadings == '00001231'  # field from the cards source
        assert len(row1) == 2, "now second source in the dbRows[0]"

    def test_card_read(self):
        """ test reading cards from from member ID
            note: does not appear to have way of reading card ID at this time
        """
        cv = CardView({"sqlid": 8})
        card1 = cv[1]
        # now change sqlid which is used to for reading card- to show that makes read fail
        assert card1.membcard['sqlid'] == 97
        assert card1.label == 'c1'
        with pytest.raises(AssertionError):
            card1.nameOnCard == 'ian'  # retrieve
        with card1:  # restore id to enable fetch from card
            vals = card1.membcard
            vals['sqlid'] = 96
            card1.membcard = vals
        assert card1.nameOnCard == 'ian'

    def test_card_update(self):
        cv = CardView({"sqlid": 8})
        c2 = cv[1]
        with c2:
            c2.nameOnCard = 'Fred'
        assert cv._dbRows[1]['cards'].nameOnCard == 'Fred'
        # cv.update_()
        cv = CardView({"sqlid": 8})
        assert cv[1].nameOnCard == 'Fred'

    def test_card_labelupdate_to_check_embedded_source_update(self):
        cv = CardView({"sqlid": 8})
        c2 = cv[1]
        with c2:
            c2.nameOnCard = 'Fred'
            c2.label = 'new label'
        assert cv._dbRows[1]['cards'].nameOnCard == 'Fred'
        cv = CardView({"sqlid": 8})
        assert cv[1].nameOnCard == 'Fred'
        assert cv[1].label == 'new label'

    def test_insert_card_and_update_for_both_sources(self):
        cv = CardView({"sqlid": 8})
        cnew = cv.insert_()
        with cnew:
            cnew.nameOnCard = 'Fred'
            cnew.label = 'new card'
        assert cv._dbRows[3]['cards'].nameOnCard == 'Fred'
        assert cv._dbRows[3]['members.cards'].label == 'new card'
        assert '_id' in cv._dbRows[3]['cards']
        memb = cv._dbRows[3]['members.cards']
        assert 'key' in memb

        # testing update of second  id link as used by salt app
        # salt uses second id link to allow legacy links in legacy records
        #
        with cnew:
            cnew.sqlid = cnew.id

        cv = CardView({"sqlid": 8})
        assert cv[3].nameOnCard == 'Fred'
        assert cv[3].label == 'new card'

    def test_Cards_delete_nested(self):
        # Prepare
        before_change = CardView({"sqlid": 8})
        card2 = before_change[1]
        sqlid = card2['sqlid'].value

        # Prepare the date to check
        nested_list_size = len(before_change)

        # Delete the card
        with card2:
            card2.delete_()

        # Retrieve the data again to assert the result
        after_change = CardView({"sqlid": 8})

        # Assert if the nested card has been delete
        assert len(after_change) == nested_list_size - 1
        for card in after_change:
            assert card['sqlid'] != sqlid

    def test_Cards_delete_nested_and_non_nested(self):
        # Prepare
        before_change = CardView({"sqlid": 8})
        card1 = before_change[0]
        CardsCollection = MongoClient()[TEST_DB_NAME].cards
        sqlid = card1['sqlid'].value

        # Prepare the date to check
        nested_list_size = len(before_change)
        list_size = CardsCollection.count_documents({})

        # Delete the card
        with card1:
            card1.delete_()

        # Retrieve the data
        after_change = CardView({"sqlid": 8})

        # Assert if the nested card has been delete
        assert len(after_change) == nested_list_size - 1
        for card in after_change:
            assert card['sqlid'] != sqlid

        # Assert if the non-nested card in cards collection has been deleted
        assert CardsCollection.count_documents({}) == list_size - 1
        assert CardsCollection.find({'sqlid': sqlid}).count() == 0
