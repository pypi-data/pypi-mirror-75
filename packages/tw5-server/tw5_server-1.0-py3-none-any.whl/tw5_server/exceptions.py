class ProjectError(Exception):
    pass


class OperationError(ProjectError):
    pass


class PathError(ProjectError):
    pass


class DirNotExist(PathError):
    pass


class NotDir(PathError):
    pass


class DirAlreadyExist(PathError):
    pass
