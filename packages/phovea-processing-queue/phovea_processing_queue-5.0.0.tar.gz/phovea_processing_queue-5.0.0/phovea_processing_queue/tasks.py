
from phovea_processing_queue.task_definition import task, get_logger


_log = get_logger(__name__)


@task
def add(x, y):
  return float(x) + float(y)


@task
def mul(x, y):
  return float(x) * float(y)


@task
def xsum(numbers):
  return sum(numbers)
