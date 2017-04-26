
try:
    from .local_settings import *
except:
    DEBUG = False
    pass

# try: 
#     from .production_settings import *
# except:
#     pass