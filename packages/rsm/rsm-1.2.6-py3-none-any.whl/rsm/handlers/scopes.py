class AlertScope:
    """
        Validate and set the alert severity according to the given default levels.
    """

    def __init__(self, default_levels: list or dict, scope: str or list) -> None:

        if isinstance(scope, str):
            scope = scope.strip().split(',')

        if isinstance(default_levels, dict):
            default_levels = list(default_levels)
        elif not isinstance(default_levels, list):
            raise TypeError("Invalid type for 'default_levels'.")

        self.scope = scope
        self.default_levels = default_levels

    def is_valid_scope(self) -> bool:
        invalid = []
        try:
            for key in self.default_levels:
                for i in self.scope:
                    i = i.strip()
                    if i != key and i not in self.default_levels:
                        invalid.append(i)
            invalid = self.__remove_dup(invalid)
            if len(invalid) > 0:
                raise AttributeError(
                    f"Invalid scope parameters: {[ i.strip() for i in invalid ]}")
        except AttributeError as err:
            print(err)
            return False
        return True

    @staticmethod
    def __remove_dup(x) -> list:
        return list(dict.fromkeys(x))
