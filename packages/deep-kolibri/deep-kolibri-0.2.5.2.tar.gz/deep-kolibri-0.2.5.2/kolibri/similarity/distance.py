class Distance:

    def __call__(self, text_a, text_b):
        return self.compare(text_a, text_b)

    def compare(self, text_a, text_b):
        return 0
