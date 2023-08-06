from osiris.Osiris import Osiris

SYSTEM_NAME = "hydda"
PLUGIN_NAME = "openstack"

osiris = Osiris(SYSTEM_NAME, PLUGIN_NAME)

osiris.systemIntrospect()
