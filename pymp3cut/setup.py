#! /usr/bin/env python
#
# pymp3cut
# (c) 2002 Jerome Alet <alet@librelogiciel.com>
# You're welcome to redistribute this software under the
# terms of the GNU General Public Licence version 2.0
# or, at your option, any higher version.
#
# You can read the complete GNU GPL in the file COPYING
# which should come along with this software, or visit
# the Free Software Foundation's WEB site http://www.fsf.org
#
# $Id: setup.py,v 1.4 2002/05/24 09:18:36 jalet Exp $

from distutils.core import setup

import pymp3cut

setup(name = "pymp3cut", version = pymp3cut.__version__,
      licence = "GNU GPL",
      description = pymp3cut.__doc__,
      author = "Jerome Alet",
      author_email = "alet@librelogiciel.com",
      url = "http://www.librelogiciel.com/software/",
      packages= [ "" ],
      scripts = [ "bin/pymp3cut", "bin/pmpcmp3" ])
