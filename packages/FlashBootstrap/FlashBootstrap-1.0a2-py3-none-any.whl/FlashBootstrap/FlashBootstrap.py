###
# Author : Emmanuel Essien
# Author : emmaessiensp@gmail.com
# Maintainer By: Emmanuel Essien
# Maintainer Email: emmaessiensp@gmail.com
# Created by Betacodings on 26 July 2020.
###

from pytonik.Flash import Flash

class FlashBootstrap:

    def __getattr__(self, item):
        return item

    def __call__(self, *args, **kwargs):
        return None
        
    def __init__(self, *args, **kwargs):
        return None

    def message(self, message, showin="", key='flash'):
        return Flash.message(message=message, showin=showin, key=key)

    @staticmethod
    def error(description="", title="",  dismissible=True, key='flash'):
        title = "<strong>{title}</strong>".format(title=title) if title != "" else ""
        dismissible = """<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
	    """if dismissible == True else "" 
        result = """<div class="alert alert-danger">
        {dismissible}
        {title}{description}
        </div>""".format(title=title, description=description, dismissible=dismissible)
        
        return Flash.message(message=result, showin="", key=key)

    @staticmethod
    def warning(description="", title="",  dismissible=True, key='flash'):
        title = "<strong>{title}</strong>".format(title=title) if title != "" else ""
        dismissible = """<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
	    """if dismissible == True else "" 
        result = """<div class="alert alert-warning">
        {dismissible}
        {title}{description}
        </div>""".format(title=title, description=description, dismissible=dismissible)
        return Flash.message(message=result, showin="", key=key)
    
    @staticmethod
    def success(description="", title="",  dismissible=True, key='flash'):
        title = "<strong>{title}</strong>".format(title=title) if title != "" else ""
        dismissible = """<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
	    """if dismissible == True else "" 
        result = """<div class="alert alert-success">
        {dismissible}
        {title}{description}
        </div>""".format(title=title, description=description, dismissible=dismissible)

        return Flash.message(message=result, showin="", key=key)

    @staticmethod
    def info(description="", title="",  dismissible=True, key='flash'):
        title = "<strong>{title}</strong>".format(title=title) if title != "" else ""
        dismissible = """<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
	    """if dismissible == True else "" 
        result = """<div class="alert alert-info">
        {dismissible}
        {title}{description}
        </div>""".format(title=title, description=description, dismissible=dismissible)
        
        return Flash.message(message=result, showin="", key=key)

    @staticmethod
    def display(key='flash'):
        return Flash.display(key)