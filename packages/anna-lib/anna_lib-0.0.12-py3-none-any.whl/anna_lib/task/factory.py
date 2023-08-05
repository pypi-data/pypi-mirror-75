import types
import inspect
import string
from importlib import import_module


def parse_namespace_config(config: object) -> tuple:
	return getattr(config, 'url'), getattr(config, 'sequence')


def get_tasks(namespace: str) -> tuple:
	if isinstance(namespace, (list, tuple)) and len(namespace) == 1:
		return get_tasks(namespace[0])
	elif not isinstance(namespace, str):
		raise TypeError
	url, sequence = parse_namespace_config(import_module(namespace + '.config'))
	tasks = []
	for task in sequence:
		tasks.append(get_task(namespace, task))
	return url, tasks


def get_task(namespace: str, task: str) -> tuple:
	module = import_module(namespace + '.' + task)
	return task, inspect.getsource(module)


def load_task(driver: object, task: tuple) -> tuple:
	module = types.ModuleType(task[0])
	exec(task[1], module.__dict__)
	task_class = string.capwords(task[0].split('.')[-1].replace('_', ' ')).replace(' ', '')
	task = module.__dict__[task_class](driver)
	return module.__dict__['__name__'], task


def create(driver: object, namespace: str, task: str) -> object:
	task = get_task(namespace, task)
	return load_task(driver, task)
