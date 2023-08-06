#!/usr/bin/python3

class Error(Exception):
    """
    Base Class for all the Exceptions
    """

    pass

class NotAValidOption(Error):
    """
    Checking for a valid option
    """

    def __init__(self, option, valid_options):
        self.option = option
        self.valid_options = valid_options

        self.message = self.option+" is not a valid option, "+str(self.valid_options)+" are the only valid options"

        super().__init__(self.message)