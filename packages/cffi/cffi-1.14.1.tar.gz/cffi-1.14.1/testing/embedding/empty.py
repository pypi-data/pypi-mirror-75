import cffi

ffi = cffi.FFI()

ffi.embedding_api("")

ffi.set_source("_empty_cffi", "")

fn = ffi.compile(verbose=True)
print('FILENAME: %s' % (fn,))
