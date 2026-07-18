REGISTRY = {}

from .rnn_agent import RNNAgent
from .rnn_msg_agent import RnnMsgAgent
from .immac_agent import ImmacAgent

REGISTRY["rnn"] = RNNAgent
REGISTRY['rnn_msg'] = RnnMsgAgent
REGISTRY['immac_agent'] = ImmacAgent