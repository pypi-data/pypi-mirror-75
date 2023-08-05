# encoding: utf-8

u"""
==================================================================================
Replace entire content string
----------------------------------------------------------------------------------
Filter     : A string to match in the request.
             Leave blank to modify for all requests.
Override   : N/A
Parameters : New content string
----------------------------------------------------------------------------------

"""

import logging_helper
from future.utils import iteritems
from pyhttpintercept.intercept.handlers.support import parse_dictionary_parameters

logging = logging_helper.setup_logging()


def modify(request,
           response,
           modifier,
           **_):

    if modifier.passes_filter(value=request,
                              wildcards=u''):

        response._content = modifier.params

    return response
