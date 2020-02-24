# Tests for mutations pertaining to entry points.
import os
import unittest

from tests import util
from trompace.mutations.entrypoint import mutation_create_entry_point


class TestEntryPoint(unittest.TestCase):

    def setUp(self) -> None:
        super()
        self.data_dir = os.path.join(os.path.dirname(__file__), "data", "entrypoint")

    def test_create(self):
        expected = util.read_file(self.data_dir, "EXPECTED_ENTRYPOINT.txt")

        created_entrypoint = mutation_create_entry_point(name="Verovio MusicXML Converter",
                                                         contributor="https://www.verovio.org",
                                                         subject="Music notation engraving library for MEI with MusicXML,Humdrum support, toolkits, JavaScript, Python",
                                                         description="Verovio supports conversion from MusicXML to MEI. When converting from this web interface, the resulting MEI data will be displayed directly in the MEI-Viewer. The MEI file can be saved through the MEI  button that will be displayed on the top right.",
                                                         creator="Verovio", source="https://github.com/rism-ch/verovio",
                                                         language="en",
                                                         actionPlatform="TROMPA algorithm proof of concept.",
                                                         contentType=["html/json"],
                                                         encodingType=["html/text"])
        self.assertEqual(created_entrypoint, expected)