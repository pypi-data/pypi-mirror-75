#!/usr/bin/env python3
"""
Module: viewSources.py
Base class (or abstract class, if you like) definition for all classes i.e. DBSource.
"""


class DBSource:
    """
        consists of an ObjDict keyed by what was 'joins', but with an entry for all tables
        with each entry being an object with 'row_source', and 'row_key' attributes.
        row_source - is the previous default_dbRowSrc_  ...the table object for db operations
            row_source set to none should be used to indicate a memory only source
        row_id - None except when view data is embedded in a list within a single
                document, in which case this is the key for the umbrella document

        loader  -  the method to be used to lazy load the data
        join_links  - list of ViewFlds to be updated with _id
    """
    # __keys__ = "full_name row_source row_id"
    loader = None

    def __init__(self, full_name, row_source, row_id):
        self.full_name = full_name
        self._row_source = row_source
        self.row_id = row_id
        self.join_links = []

    def __repr__(self):
        return ('DBSource: {full_name} from {_row_source} id:{row_id} j:{join_links}'
                .format(**vars(self)))

    @property
    def row_source(self):
        return None

    def map_src(self, src):
        """ maps a 'src' string to return dictionary names
          currently simply assumes first link is source and correct
          so discards first link"""
        return src.split('.')[1:]

    def apply_changes_to_dbsource(self, view, idx_, change, tbl, action_type=None):
        return  # default is to ignore changes


class DBNoSource(DBSource):
    pass
