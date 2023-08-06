from .identity import Identity
from .identity import _ident
from .identity import compile_namespace
from stevedore import extension


class InstrumentBase:
    def __init__(self, resource_name, resource_manager, identity, timeout):
        self.rsrc_name = resource_name
        self.rsrc_mgr = resource_manager
        self.timeout = timeout
        self._idn = identity

    @property
    def idn(self):
        """A description of the instrument"""
        return self._idn

    @property
    def features(self):
        """A list of supported instrument features"""
        return self._features

    def write(self, *args, **kwargs):
        """Writes a command to the instrument"""
        with self.rsrc_mgr.open_resource(self.rsrc_name) as instr:
            instr.timeout = self.timeout
            instr.write(*args, **kwargs)

    def query(self, *args, **kwargs):
        """Retrieves data from the instrument"""
        with self.rsrc_mgr.open_resource(self.rsrc_name) as instr:
            instr.timeout = self.timeout
            return instr.query(*args, **kwargs)


def instrument_factory(resource_name, resource_manager, identity, timeout):
    """
    Dynamically constructs and returns an instrument object associated with the given
    VISA resource name.

        resource_name (str): A string describing the name of a VISA resource.
        resource_manager (obj or None): An optional pyvisa resource manager object.
        identity (obj or None): An optional Identity named tuple used to
            override the automatic instrument identity detection.
        timeout (int or float): An optional timeout value (in seconds)
    """

    # Automatically create a pyvisa resource manager object, unless one was provided.
    if not resource_manager:
        import pyvisa

        resource_manager = pyvisa.ResourceManager()

    def feature_extractor(ext):
        """
        Returns the feature name and feature method from stevedore extension manager
        """
        return ext.name, ext.obj.get_feature(resource_manager, resource_name)

    # Create a new empty instrument object for the target instrument
    if isinstance(identity, Identity):
        idn = identity
    else:
        idn = _ident(
            resource_name=resource_name,
            resource_manager=resource_manager,
            timeout=timeout,
        )

    namespace = compile_namespace(idn)

    # Each type of instrument needs a unique subclass of InstrumentBase
    # Use the value of namespace to derive the name of the subclass
    cls_name = "".join([t.capitalize() for t in namespace.split(".")[1:]])
    cls = type(cls_name, (InstrumentBase,), dict(InstrumentBase.__dict__))

    # Use the stevedore extension manager to load the available instrument features based on the instrument identity
    mgr = extension.ExtensionManager(
        namespace=namespace, invoke_on_load=True, invoke_args=()
    )

    # Load all available features from the extension manager
    feature_map = mgr.map(feature_extractor)

    # Each available feature is added to the instrument class and the _feature names list.
    features = []
    for feature_name, feature_obj in feature_map:
        setattr(cls, feature_name, feature_obj)
        features.append(feature_name)

    # Add the features list to the Instrument class
    setattr(cls, "_features", features)

    # Return an instantiated class for the new instrument
    return cls(resource_name, resource_manager, identity=idn, timeout=timeout)
