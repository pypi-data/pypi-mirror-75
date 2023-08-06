# -*- coding: UTF-8 -*-
# Copyright 2017-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""This is the main module of Lino Avanti.

.. autosummary::
   :toctree:

   lib


"""

from .setup_info import SETUP_INFO

__version__ = SETUP_INFO.get('version')

intersphinx_urls = dict(docs="http://avanti.lino-framework.org")
srcref_url = 'https://github.com/lino-framework/avanti/blob/master/%s'
doc_trees = ['docs']
