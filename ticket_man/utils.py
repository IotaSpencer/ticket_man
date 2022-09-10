from sqlalchemy.orm import declarative_base


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, d):
        super().__init__()
        for k, v in d.items():
            if isinstance(v, dict):
                self[k] = dotdict(v)
            else:
                self[k] = v


Base = declarative_base()
