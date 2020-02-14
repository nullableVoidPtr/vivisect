import io
import unittest

import cobra


class NewObjectReturn:

    @cobra.newobj
    def open(self):
        return io.BytesIO('asdf')


class CobraNewObjTest(unittest.TestCase):

    def test_cobra_newobj(self):

        daemon = cobra.CobraDaemon(port=60500, msgpack=True)
        objname = daemon.shareObject(NewObjectReturn())
        daemon.fireThread()

        t = cobra.CobraProxy('cobra://localhost:60500/%s?msgpack=1' % objname)

        with t.open() as fd:
            self.assertEqual(fd.read(), 'asdf')

        self.assertEqual(len(daemon.shared.keys()), 1)
        daemon.stopServer()
