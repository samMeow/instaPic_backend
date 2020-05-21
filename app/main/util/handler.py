from werkzeug.exceptions import HTTPException
import traceback


def handle_500(err):
    """
    handle all exception
    """
    print(traceback.print_exc())
    code = 500
    if isinstance(err, HTTPException):
        code = err.code
    return {'message': str(err)}, code

def global_handler(app):
    """
    init app with handler
    """
    app.register_error_handler(Exception, handle_500)
    return app
