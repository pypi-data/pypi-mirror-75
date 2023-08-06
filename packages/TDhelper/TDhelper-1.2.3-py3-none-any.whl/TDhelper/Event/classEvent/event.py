from TDhelper.Event.classEvent.meta import eventMeta
def hook(before= None, complete= None):
    def wrapper(func):
        def deco(*args, **kwargs):
            try:
                m_args= None
                if before:
                    m_args, kwargs= before(*args, **kwargs)
                if m_args:
                    ret= func(*m_args, **kwargs)
                else:
                    ret= func(*args, **kwargs)
                if complete:
                    kwargs['func-result']= ret
                    if m_args:
                        ret= complete(*m_args, **kwargs)
                    else:
                        ret= complete(*args, **kwargs)
                return ret
            except Exception as e:
                raise e
        return deco
    return wrapper

class event(metaclass= eventMeta):

    def _event_register(self, name, func):
        pass

    def _event_remove(self, name):
        pass

    def _event_on(self, name, *args, **kwargs):
        pass
    