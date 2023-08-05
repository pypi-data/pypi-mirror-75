from testing.embedding.test_basic import EmbeddingTests


class TestThreadLocal(EmbeddingTests):
    def test_thread_local(self):
        tlocal_cffi = self.prepare_module('tlocal')
        self.compile('tlocal-test', [tlocal_cffi], threads=True)
        for i in range(10):
            output = self.execute('tlocal-test')
            assert output == "done\n"
