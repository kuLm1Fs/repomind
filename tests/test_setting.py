import repomind.config.settings as settings_module

import importlib, os, unittest

class TestSettings(unittest.TestCase):
    def setUp(self):
        self.old_env = os.environ.copy()

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.old_env)

    def reload_settings(self):
        return importlib.reload(settings_module).settings

    def test_settings_use_default_values(self):
        os.environ.pop("TOP_K", None)
        os.environ.pop("CHUNK_SIZE", None)
        os.environ.pop("CHUNK_OVERLAP", None)
        os.environ.pop("MAX_RETRY", None)

        settings = self.reload_settings()

        self.assertEqual(settings.TOP_K, 5)
        self.assertEqual(settings.CHUNK_SIZE, 80)
        self.assertEqual(settings.CHUNK_OVERLAP, 10)
        self.assertEqual(settings.MAX_RETRY, 1)

    def test_settings_read_env_values(self):
        os.environ["OPENAI_API_KEY"] = "test-key"
        os.environ["OPENAI_BASE_URL"] = "https://example.com/v1"
        os.environ["OPENAI_MODEL"] = "test-model"
        os.environ["TOP_K"] = "8"
        os.environ["CHUNK_SIZE"] = "100"
        os.environ["CHUNK_OVERLAP"] = "20"
        os.environ["MAX_RETRY"] = "2"

        settings = self.reload_settings()

        self.assertEqual(settings.OPENAI_API_KEY, "test-key")
        self.assertEqual(settings.OPENAI_BASE_URL, "https://example.com/v1")
        self.assertEqual(settings.OPENAI_MODEL, "test-model")
        self.assertEqual(settings.TOP_K, 8)
        self.assertEqual(settings.CHUNK_SIZE, 100)
        self.assertEqual(settings.CHUNK_OVERLAP, 20)
        self.assertEqual(settings.MAX_RETRY, 2)


if __name__ == "__main__":
    unittest.main()