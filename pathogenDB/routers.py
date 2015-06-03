class PathogenRouter(object):
	def db_for_read(self, model, **hints):
		if model._meta.app_label == 'pathogenSite':
			return 'pathogen'
		return None

	def db_for_write(self, model, **hints):
		if model._meta.app_label == 'pathogenSite':
			return 'pathogen'
		return None

	def allow_relation(self, obj1, obj2, **hints):
		if obj1._meta.app_label == 'pathogenSite' or \
			obj2._meta.app_label == 'pathogenSite':
			return True
		return None

	def allow_migrate(self, db, app_label, model=None, **hints):
		if app_label == 'pathogenSite':
			return db == 'pathogen'
		return None


class SsuProkRouter(object):
	def db_for_read(self, model, **hints):
		if model._meta.app_label == 'ssuProkSite':
			return 'ssuProk'
		return None

	def db_for_write(self, model, **hints):
		if model._meta.app_label == 'ssuProkSite':
			return 'ssuProk'
		return None

	def allow_relation(self, obj1, obj2, **hints):
		if obj1._meta.app_label == 'ssuProkSite' or \
			obj2._meta.app_label == 'ssuProkSite':
			return True
		return None

	def allow_migrate(self, db, app_label, model=None, **hints):
		if app_label == 'ssuProkSite':
			return db == 'ssuProkSite'
		return None
