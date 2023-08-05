import pytest

from viewmodel import BaseView, DBMongoEmbedSource, ObjListField, viewMongoDB


class EmbeddedView(BaseView):
    models_ = DBMongoEmbedSource(viewMongoDB, "edgeCases.listNotThere")
    embedded_list_not_there = ObjListField(src="edgeCases.listNotThere")

    def getRows_(self, *args, **kwargs):
        return self.embeded_rows({}, "edgeCases.listNotThere", "fieldNotThere", viewMongoDB.default("edgeCases"))


class TestEmbeddedSources:

    @pytest.fixture
    def embedView(self):
        return EmbeddedView()

    def test_read_from_ObjListField_not_there(self, embedView):
        assert embedView.embedded_list_not_there == []  # default value
