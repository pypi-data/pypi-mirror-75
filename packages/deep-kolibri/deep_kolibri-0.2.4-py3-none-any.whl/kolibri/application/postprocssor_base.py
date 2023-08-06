class PostProcessorBase(object):
    """
    A superclass for all adapter classes.

    :param application: An App instance.
    """

    def __init__(self, application, **kwargs):
        self.application = application
