def read(filename, ):
    # todo exept FNFE
    import os.path as show
    dir = get_path()
    print(dir)
    f = open(show.realpath("%s/%s" % (dir, filename)))
    out = f.read()
    f.close()
    return out


# todo Cpython only
def get_path(depth=1):
    import sys
    import os
    f_name = sys._getframe(depth).f_code.co_filename
    out = os.path.dirname(os.path.abspath(f_name))
    return out
