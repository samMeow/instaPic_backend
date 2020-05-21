import traceback
from werkzeug.exceptions import HTTPException

def global_handler(err):
    """
    handle all exception
    """
    print(traceback.print_exc())
    code = 500
    if isinstance(err, HTTPException):
        code = err.code
    return {'message': str(err)}, code

def init_error_handler(app):
    """
    init app with handler
    """
    app.register_error_handler(Exception, global_handler)
    return app
