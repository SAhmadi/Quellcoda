from enum import Enum


class ExecType(Enum):
    """Defines the execution type of the request. Should the incoming java code
    be run or tested with JUnit. It will decide which JDK or Gradle commands to use.
    """
    run = 1
    test = 2
