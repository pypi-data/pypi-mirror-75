# -*- coding: utf-8 -*-

import os

from mutagen._senf import fsnative as fsn

from tests.test_tools import _TTools
from tests import DATA_DIR, get_temp_copy


class TMOggSPlit(_TTools):

    TOOL_NAME = u"moggsplit"

    def setUp(self):
        super(TMOggSPlit, self).setUp()
        self.filename = get_temp_copy(
            os.path.join(DATA_DIR, fsn(u'multipagecomment.ogg')))

        # append the second file
        with open(self.filename, "ab") as first:
            to_append = os.path.join(
                DATA_DIR, fsn(u'multipage-setup.ogg'))
            with open(to_append, "rb") as second:
                first.write(second.read())

    def tearDown(self):
        super(TMOggSPlit, self).tearDown()
        os.unlink(self.filename)

    def test_basic(self):
        d = os.path.dirname(self.filename)
        p = os.path.join(d, fsn(u"%(stream)d.%(ext)s"))
        res, out = self.call(fsn(u"--pattern"), p, self.filename)
        self.failIf(res)
        self.failIf(out)

        for stream in [1002429366, 1806412655]:
            stream_path = os.path.join(
                d, fsn(str(stream)) + fsn(u".ogg"))
            self.failUnless(os.path.exists(stream_path))
            os.unlink(stream_path)
