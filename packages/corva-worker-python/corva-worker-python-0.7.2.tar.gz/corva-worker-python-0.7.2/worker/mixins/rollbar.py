class RollbarMixin(object):
    def __init__(self, *args, **kwargs):
        self.rollbar = kwargs.pop('rollbar', None)
        super().__init__(*args, **kwargs)

    def track_message(self, message: str, level: str):
        # Levels: critical, error, warning, info, debug, and ignored
        if not self.rollbar:
            return

        level = level.lower()

        self.rollbar.report_message(message, level)

    def track_error(self, message: str = None):
        if not self.rollbar:
            return

        self.rollbar.report_exc_info(extra_data=message, level='error')
