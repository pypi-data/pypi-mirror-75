import logging
from collections import defaultdict
from typing import Callable

from pydantic import BaseModel

logger = logging.getLogger(__name__)

solver = defaultdict(list)


class Solution(BaseModel):
    func: Callable
    solution: int
    time: str
    space: str

    def __init__(self, func: Callable, time: str, space: str, **data):
        super().__init__(
            func=func,
            solution=int(func.__name__.split("_")[-1]),
            time=time,
            space=space,
            **data,
        )


def register(task: str, *, time: str, space: str):
    def decorator(func):
        if len(task.split(".")) != 2:
            logger.info(f"Register task {task} with wrong format name.")
        else:
            solver[task].append(Solution(func=func, time=time, space=space))
        return func

    return decorator
