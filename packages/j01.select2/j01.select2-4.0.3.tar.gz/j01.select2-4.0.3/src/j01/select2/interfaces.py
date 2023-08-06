##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
$Id: interfaces.py 5006 2020-04-19 14:50:48Z roger.ineichen $
"""
__docformat__ = "reStructuredText"

import zope.interface
import zope.schema.interfaces

import z3c.form.interfaces
import z3c.jsonrpc.interfaces



################################################################################
#
# shared schema

class ISelect2WidgetSchema(z3c.form.interfaces.ISequenceWidget):
    """Select2 widget for ISequence of IChoice."""


################################################################################
#
# select

class ISelect2Widget(ISelect2WidgetSchema):
    """Select widget for IList of IChoice fields

    All values must be a part of the choice vocabulary/source. No extra input
    is allowed. The widget will render the result as select input like design.
    """


class ISingleSelect2Widget(ISelect2WidgetSchema):
    """Select widget for IChoice fields

    The value must be a part of the choice vocabulary/source. No extra input
    is allowed. The widget will render the result with tokens.
    """


class ISelect2ResultAware(zope.interface.Interface):
    """Offering result setup used for JSON-RPC call"""

    def getSelect2Result(searchString, page):
        """Returns the select2 jsonrpc call result

        {
            "results": [
                {"id": "mytag", text: "mytag" },
                { "id": "another", text: "another" }
            ],
            "pagination": {
                "more": false
            }
        }

        or if you like to support select widget optgroup option grouping:

        {
            results: [{
                text: "Western",
                "children": [
                    {"id": "CA", text: "California" },
                    {"id": "AZ", text: "Arizona", "selected": true}
                ]},{
                "text": "Eastern",
                "children": [
                    {"id": "FL", text: "Florida"}
                ]}
            ],
            "pagination": {
                "more": false
            }
        }

        """


################################################################################
#
# tagging

# single tag
class ISingleTagSelect2Widget(ISelect2ResultAware,
    ISelect2WidgetSchema):
    """Select2 widget for ITextLine"""


# tag list
class ITagListSelect2Widget(ISelect2ResultAware,
    ISelect2WidgetSchema):
    """Select2 widget for IList of ITextLine"""


################################################################################
#
# live lookup terms

class ILiveListTerms(zope.interface.Interface):
    """Simple LiveListTerm list supporting total result size etc."""

    total = zope.schema.Int(
        title=u'Total terms (not only in this list)',
        description=u'Total terms (not only in this list)',
        required=True)

    more = zope.schema.Bool(
        title=u'Marker for more available data',
        description=u'Marker for more available data',
        default=False,
        required=True)

    def append(item):
        """Append an item to the list."""

    def insert(i, item):
        """Insert an item at the given position."""

    def pop(i=-1):
        """Pop an item from the list."""

    def remove(item):
        """Remove an item from the list."""

    def sort(*args, **kwargs):
        """Sort the list"""

    def __len__():
        """Returns the lenght."""

    def __contains__(item):
        """Returns True if the list contains the given item otherwise False."""

    def __getitem__(i):
        """Get an item from the list."""

    def __setitem__(i, item):
        """Add an item to the list."""

    def __delitem__(i):
        """Remove an item from the list."""

    def __cmp__(other):
        """compare"""

    def __repr__():
        """representation"""


class ILiveListTerm(zope.schema.interfaces.ITitledTokenizedTerm):
    """Group name aware term."""

    def getTitle(request):
        """Return translated title if needed."""


class ILiveListSource(zope.schema.interfaces.IBaseVocabulary,
    zope.schema.interfaces.IContextSourceBinder):
    """A set of values from which to choose

    This vocabulary is not iterable and provides getTermByToken and knows it's
    context.
    """

    def search(searchString, start=None, size=None):
        """Search for terms by given query string and return a list of terms."""

    def __contains__(value):
        """Return whether the value is available in this source. Return True if
        the context didn't get bind to the field. This means we can't probably
        lookup our terms.
        """

    def getTerm(value):
        """Return the ITerm object for the term 'value'.

        If 'value' is not a valid term, this method raises LookupError.
        """

    def getTermByToken(token):
        """Return an ITokenizedTerm for the passed-in token.

        If `token` is not represented in the vocabulary, `LookupError`
        is raised.
        """


class ILiveTagSelect2Widget(ISelect2ResultAware, ISelect2WidgetSchema):
    """Select2 widget for IChoice offering live autosuggest"""


class ILiveListSelect2Widget(ISelect2ResultAware, ISelect2WidgetSchema):
    """Select2 widget for IList of IChoice offering live autosuggest"""


################################################################################
#
# helper

class ISelect2Result(z3c.jsonrpc.interfaces.IJSONRPCRequest):
    """JSON-RPC select2 result search method."""

    def j01Select2Result(self, fieldName, searchString, page):
        """Returns the select2 search result as JSON data.

        The returned value provides the following data structure:

        {
            "results": [
                {"id": "mytag", text: "mytag" },
                { "id": "another", text: "another" }
            ],
            "pagination": {
                "more": false
            }
        }

        or if you like to support select widget optgroup option grouping:

        {
            results: [{
                text: "Western",
                "children": [
                    {"id": "CA", text: "California" },
                    {"id": "AZ", text: "Arizona", "selected": true}
                ]},{
                "text": "Eastern",
                "children": [
                    {"id": "FL", text: "Florida"}
                ]}
            ],
            "pagination": {
                "more": false
            }
        }

        """
