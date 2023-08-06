# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.
#

import ecmwfapi
import os

from climetlab.core.caching import temp_file
from .base import FileSource


class MARSRetriever(FileSource):

    def __init__(self, **req):
        self.path = temp_file('MARSRetriever', req)
        if not os.path.exists(self.path):
            ecmwfapi.ECMWFService('mars').execute(req, self.path + '.tmp')
            os.rename(self.path + '.tmp', self.path)


source = MARSRetriever
