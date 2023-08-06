import os

import purecl as cl


def test_api_nonumpy():
    import math
    src_test = (
        """
        #include "test.cl"
        """)
    include_dirs = ("", os.path.dirname(__file__), ".")

    # Create platform, context, program, kernel and queue
    platforms = cl.Platforms()
    ctx = platforms.create_some_context()
    prg = ctx.create_program(src_test, include_dirs)
    krn = prg.get_kernel("test")
    # Create command queue
    queue = ctx.create_queue(ctx.devices[0])

    # Create arrays with some values for testing
    N = 100000
    ffi = cl.get_ffi()
    _a = ffi.new("float[]", N + queue.device.memalign)
    sz = int(ffi.cast("size_t", _a))
    if sz % queue.device.memalign != 0:
        sz += queue.device.memalign - (sz % queue.device.memalign)
        a = ffi.cast("float*", sz)
    else:
        a = _a
    _b = ffi.new("float[]", N + queue.device.memalign)
    sz = int(ffi.cast("size_t", _b))
    if sz % queue.device.memalign != 0:
        sz += queue.device.memalign - (sz % queue.device.memalign)
        b = ffi.cast("float*", sz)
    else:
        b = _b
    c = ffi.new("float[]", 1)
    c[0] = 1.2345
    d = ffi.new("float[]", N)
    sz = ffi.sizeof(d)
    for i, t in enumerate(d):
        a[i] = math.sin(i)
        b[i] = math.cos(i)
        d[i] = a[i] + b[i] * c[0]
    a_copy = ffi.new("float[]", N)
    a_copy[0:N] = a[0:N]

    # Create buffers
    a_ = ctx.create_buffer(cl.CL_MEM_READ_WRITE | cl.CL_MEM_USE_HOST_PTR,
                           a, size=sz)
    b_ = ctx.create_buffer(cl.CL_MEM_READ_WRITE | cl.CL_MEM_USE_HOST_PTR,
                           b, size=sz)

    # Set kernel arguments
    krn.set_arg(0, a_)
    krn.set_arg(1, b_)
    krn.set_arg(2, ffi.cast("const void*", c), ffi.sizeof(c))

    # Execute kernel
    global_size = [N]
    local_size = None
    queue.execute_kernel(krn, global_size, local_size, need_event=False)

    # Get results back from the device by map_buffer
    ev, ptr = queue.map_buffer(a_, cl.CL_MAP_READ, sz)
    del ev
    queue.unmap_buffer(a_, ptr).wait()
    mx = 0
    for i, t in enumerate(d):
        mx = max(mx, math.fabs(a[i] - t))

    # Get results back from the device by read_buffer
    aa = ffi.new("float[]", N)
    queue.read_buffer(a_, aa, size=sz)
    mx = 0
    for i, t in enumerate(d):
        mx = max(mx, math.fabs(aa[i] - t))

    # Refill buffer with stored copy by map_buffer with event
    ev, ptr = queue.map_buffer(
        a_, cl.CL_MAP_WRITE if queue.device.version < 1.1999
        else cl.CL_MAP_WRITE_INVALIDATE_REGION, sz,
        blocking=False, need_event=True)
    ev.wait()
    a[0:N] = a_copy[0:N]
    ev = queue.unmap_buffer(a_, ptr)

    # Execute kernel
    ev = queue.execute_kernel(krn, global_size, local_size, wait_for=(ev,))
    # Get results back from the device by map_buffer
    ev, ptr = queue.map_buffer(a_, cl.CL_MAP_READ, sz,
                               wait_for=(ev,), need_event=True)
    ev.wait()
    queue.unmap_buffer(a_, ptr).wait()
    mx = 0
    for i, t in enumerate(d):
        mx = max(mx, math.fabs(a[i] - t))

    # Refill buffer with stored copy by write_buffer
    ev = queue.write_buffer(a_, a_copy, size=sz,
                            blocking=False, need_event=True)

    # Execute kernel
    ev = queue.execute_kernel(krn, global_size, local_size, wait_for=(ev,))
    # Get results back from the device by map_buffer
    ev, ptr = queue.map_buffer(a_, cl.CL_MAP_READ, sz,
                               wait_for=(ev,), need_event=True)
    ev.wait()
    queue.unmap_buffer(a_, ptr).wait()
    mx = 0
    for i, t in enumerate(d):
        mx = max(mx, math.fabs(a[i] - t))

    del _b
    del _a

    print(a_copy[3])


test_api_nonumpy()
