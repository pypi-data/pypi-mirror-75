from .. import base


class LocalProductFeature(base.FeatureBase):

	def feature(self, a, b):
		"""Returns the product of two numbers without interacting with the mock instrument."""
		return float(a*b)


class InstrumentProductFeature(base.FeatureBase):

	def feature(self, a, b):
		"""Returns the product of two numbers after storing the values in the mock instrument."""
		with self.resource_manager.open_resource(self.resource_name) as inst:
			inst.write("A {:.2f}".format(a))
			inst.write("B {:.2f}".format(b))
			return float(inst.query("A?")) * float(inst.query("B?"))


class ResourceNameFeature(base.FeatureBase):

	def feature(self):
		"""Returns the resource name of the mock instrument."""
		return self.resource_name
