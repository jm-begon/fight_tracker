def get_stream(out=None):
    if out is None:
        import sys

        out = sys.stdout
    return out
