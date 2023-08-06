class RepoException(Exception):
    pass


#
class ShapeItException(Exception):
    def __init__(self, *args, **kwargs):
        self.output_method = kwargs.get("output_method")
        self.exit_code = 8
        if args:
            self.message = args[0]
        elif hasattr(self.__class__, "message"):
            self.message = self.__class__.message
        else:
            self.message = ""

    def __str__(self):
        return self.message


class NoAnswersError(ShapeItException):
    exit_code = 8


class NoStandardsError(Exception):
    pass


class AllowedTypesError(Exception):
    def __init__(self):
        self.message = "You have to use the specified types."
        super().__init__(self.message)

class NoRepoAccessError(Exception):
    def __init__(self):
        self.message = "You do not have access to the requested repo."
        super().__init__(self.message)

class NoGitRepo(Exception):
    pass
