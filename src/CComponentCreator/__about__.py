# Copyright (c) 2021 Paweł Piskorz
# Licensed under the MIT License
# See attached LICENSE file

__all__ = ('__title__', '__summary__', '__uri__', '__version_info__',
           '__version__', '__author__', '__maintainer__', '__email__',
           '__copyright__', '__license__')

__title__        = "CComponentCreator"
__summary__      = "Python package for creating components in C language"
__uri__          = "https://github.com/zxvcv/CComponentCreator"
__version_info__ = type("version_info", (), dict(major=0, minor=0, micro=1,
                        releaselevel="final", serial=0))
__version__      = "{0.major}.{0.minor}.{0.micro}{1}{2}".format(__version_info__,
                   dict(alpha="a", beta="b", candidate="rc", final="",
                        post=".post", dev=".dev")[__version_info__.releaselevel],
                   __version_info__.serial
                   if __version_info__.releaselevel != "final" else "")
__author__       = "Pawel Piskorz"
__maintainer__   = "Pawel Piskorz"
__email__        = "ppiskorz0@gmail.com"
__copyright__    = "Copyright (c) 2021 {0}".format(__author__)
__license__      = "MIT License ; {0}".format(
                   "https://opensource.org/licenses/MIT")