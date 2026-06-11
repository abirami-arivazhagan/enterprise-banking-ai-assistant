class LoggingCallback:

    def on_chain_start(
        self,
        *args,
        **kwargs
    ):

        print("Chain started")

    def on_chain_end(
        self,
        *args,
        **kwargs
    ):

        print("Chain ended")