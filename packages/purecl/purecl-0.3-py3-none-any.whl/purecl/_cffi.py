"""
Copyright (c) 2014, Samsung Electronics Co.,Ltd.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of Samsung Electronics Co.,Ltd..
"""

"""
Original author: Alexey Kazantsev <a.kazantsev@samsung.com>
Alterations author: Andrey Ivanko <sarck.four@gmail.com>
"""

"""
OpenCL cffi bindings.
"""

import cffi
import threading

from purecl.common.const import *

ffi = None
lib = None
event_callback = None
build_callback = None
runtime_callback = None


lock = threading.Lock()


def _initialize(backends):
    global lib
    if lib is not None:
        return
    # C function definitions

    import purecl.common.src_reader as rd
    src = rd.read("ocl_api.c")

    # Parse
    global ffi
    ffi = cffi.FFI()
    ffi.cdef(src)

    # Load library
    for libnme in backends:
        try:
            lib = ffi.dlopen(libnme)
            break
        except OSError:
            pass
    else:
        ffi = None
        raise OSError("Could not load OpenCL library")


def initialize(backends=("libOpenCL.so", "OpenCL.dll", "OpenCL")):
    global lib
    if lib is not None:
        return
    global lock
    with lock:
        _initialize(backends)
