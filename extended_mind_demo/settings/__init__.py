
try:
    from .local_settings import *
except:
    DEBUG = True
    pass

# try: 
#     from .production_settings import *
# except:
#     pass