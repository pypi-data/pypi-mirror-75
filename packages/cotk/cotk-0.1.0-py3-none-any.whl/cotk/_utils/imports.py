r"""
``cotk._utils.imports`` provides classes that fake a uninstalled module.
"""
import importlib
import sys

class LazyModule(object):
	r'''Lazy loading modules.

	Arguments:
		module_name (str): The path of import. For example: ``cotk``.
		global_dict (str): Override the global dictionary when the module is loaded.

	Examples:
		>>> torch = LazyModule("torch", globals())
		>>> print(torch)
		<cotk._utils.imports.LazyModule object at 0x000001BE147682E8>
		>>> torch.Tensor = LazyObject("torch.Tensor")
		>>> print(torch.Tensor)
		<cotk._utils.imports.LazyObject object at 0x000001BE1339CE80>
		>>> print(torch.LongTensor)
		<class 'torch.LongTensor'>
		>>> print(torch.Tensor)
		<class 'torch.Tensor'>
		>>> print(torch)
		<module 'torch'>
	'''
	def __init__(self, module_name, global_dict):
		super().__init__()
		self._module_name = module_name
		self._global_dict = global_dict

	def _try_load(self):
		if super().__getattribute__("_module_name") in sys.modules:
			return sys.modules[super().__getattribute__("_module_name")]
		else:
			return None

	def _load(self):
		module = importlib.import_module(super().__getattribute__("_module_name"))
		global_dict = super().__getattribute__("_global_dict")
		global_dict[super().__getattribute__("_module_name")] = module
		return module

	def __getattribute__(self, key):
		loaded = super().__getattribute__("_try_load")()
		if loaded is not None:
			return getattr(loaded, key)

		try:
			return super().__getattribute__(key)
		except AttributeError:
			pass

		if key == "__bases__":
			return tuple()
		else:
			return getattr(super().__getattribute__("_load")(), key)

	# def __call__(self, *args, **kwargs):
	# 	return self.__load()(*args, **kwargs)

class LazyObject(object):
	r'''Lazy loading objects.

	Arguments:
		object_name (str): The path of import. For example: ``cotk.dataloader.MSCOCO``.

	Examples:
		>>> dataloader = LazyObject("cotk.dataloader")
		>>> print(dataloader)
		<cotk._utils.imports.LazyObject object at 0x000001BE1339CE48>
		>>> print(dataloader.MSCOCO)
		<class 'cotk.dataloader.language_generation.MSCOCO'>
	'''
	def __init__(self, object_name):
		super().__init__()
		self._object_name = object_name
		self._module_name = object_name.split('.')[0]

	def _try_load_module(self):
		if super().__getattribute__("_module_name") in sys.modules:
			return sys.modules[super().__getattribute__("_module_name")]
		else:
			return None

	def _load_object(self):
		mod = importlib.import_module(super().__getattribute__("_module_name"))
		arr = super().__getattribute__("_object_name").split('.')
		obj = getattr(mod, arr[1])
		for i in range(2, len(arr)):
			try:
				obj = getattr(obj, arr[i])
			except AttributeError:
				raise AttributeError("No attribute %s in %s." % (arr[i], ".".join(arr[:i])))
		return obj

	def _try_getattribute(self, key):
		loaded = super().__getattribute__("_try_load_module")()
		if loaded is not None:
			return getattr(super().__getattribute__("_load_object")(), key)

		try:
			return super().__getattribute__(key)
		except AttributeError:
			pass

		return None


	def __getattribute__(self, key):
		loaded = super().__getattribute__("_try_load_module")()
		if loaded is not None:
			return getattr(super().__getattribute__("_load_object")(), key)

		try:
			return super().__getattribute__(key)
		except AttributeError:
			pass

		if key == "__bases__":
			return tuple()
		else:
			return getattr(super().__getattribute__("_load_object")(), key)

	def __call__(self, *args, **kwargs):
		return self._load_object()(*args, **kwargs)

	@staticmethod
	def peek(obj, key):
		if isinstance(obj, LazyObject):
			loaded = obj._try_load_module()
			if loaded is not None:
				return getattr(obj, key)
			else:
				return obj._try_getattribute(key)
		else:
			return None

class DummyObject(dict):
	r'''Dummy Object for uninstalled modules. [deprecated]

	Examples:
		>>> try:
		...   import torch
		... except ImportError as err:
		...   torch = DummyObject(err)
		...
		>>> torch.Tensor
		ModuleNotFoundError: No module named 'torch'
		>>> torch.Tensor = DummyObject(torch.err)
		>>> torch.Tensor
		>>> torch.Tensor()
		ModuleNotFoundError: No module named 'torch'
	'''
	def __init__(self, err):
		self.err = err
		super().__init__()

	def __getattr__(self, key):
		if key in self:
			return self[key]
		elif key == "__bases__":
			return tuple()
		else:
			raise self["err"]

	def __setattr__(self, key, value):
		self[key] = value

	def __delattr__(self, key):
		del self[key]

	def __call__(self, *args, **kwargs):
		raise self['err']
