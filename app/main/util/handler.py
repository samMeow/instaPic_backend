import traceback

def handle_500(err):
    """
    handle all exception
    """
    print(traceback.print_exc())
    return {'message': str(err)}, 500

def global_handler(app):
    """
    init app with handler
    """
    app.register_error_handler(Exception, handle_500)
    return app
