try:
    from App.ImageFile import ImageFile
    misc_ = {'method.gif': ImageFile('www/method.gif', globals())}
except ImportError:
    pass

def initialize(context):
    from AccessControl.Permissions import view_management_screens
    from Products.ZSPARQLMethod.Method import ZSPARQLMethod
    from Products.ZSPARQLMethod.Method import manage_addZSPARQLMethod_html
    from Products.ZSPARQLMethod.Method import manage_addZSPARQLMethod
    context.registerClass(
        ZSPARQLMethod,
        permission=view_management_screens,
        constructors=(manage_addZSPARQLMethod_html,
                      manage_addZSPARQLMethod),
    )
