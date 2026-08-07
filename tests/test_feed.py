import unittest
from pathlib import Path
import tempfile

import feed


class FeedGenerationTests(unittest.TestCase):
    def test_build_feed_creates_rss_structure(self):
        yaml_data = {"title": "The future is tech"}

        root = feed.build_feed(yaml_data)

        self.assertEqual(root.tag, "rss")
        self.assertEqual(root.attrib["version"], "2.0")
        self.assertEqual(root.find("channel/title").text, "The future is tech")

    def test_write_feed_writes_xml_file(self):
        yaml_data = {"title": "The future is tech"}

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "podcast.xml"
            feed.write_feed(output_path, yaml_data)

            self.assertTrue(output_path.exists())
            self.assertIn("<rss", output_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
