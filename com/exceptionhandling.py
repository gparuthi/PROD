'''
Created on Jul 28, 2012

@author: gparuthi
'''
def handle_exception(handler):
    def decorate(func):
        def call_function(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception, e:
                handler(e)
        return call_function
    return decorate

def wssError(e):
    print("Error with SendToWSServer:")
    print(e)