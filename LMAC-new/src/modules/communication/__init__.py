from .comm_selector import CommSelectorNet
from .message_selector import MessageSelectNet

REGISTRY = {
    "comm_selector": CommSelectorNet,
    "message_selector": MessageSelectNet,
}
