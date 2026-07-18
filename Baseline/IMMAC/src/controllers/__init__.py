REGISTRY = {}

from .basic_controller import BasicMAC
from .vffac_controller import VffacMAC
from .immac_controller import ImmacMAC

REGISTRY["basic_mac"] = BasicMAC
REGISTRY['vffac_mac'] = VffacMAC
REGISTRY['immac_mac'] = ImmacMAC