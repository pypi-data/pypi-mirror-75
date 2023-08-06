class Input:

    def input(t, prompt=None):
        if prompt == None:
            value = input()
        else:
            value = input(prompt)
        try:
            casted = t(value)
        except TypeError as e:
            raise e
        except ValueError as e:
            raise e
        else:
            return casted
