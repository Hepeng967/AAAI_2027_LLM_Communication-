from .q_learner import QLearner
from .coma_learner import COMALearner
from .qtran_learner import QLearner as QTranLearner
from .vffac_learner import QLearner as VffacLearner
from .immac_learner import QLearner as ImmacLearner

REGISTRY = {}

REGISTRY["q_learner"] = QLearner
REGISTRY["coma_learner"] = COMALearner
REGISTRY["qtran_learner"] = QTranLearner
REGISTRY["vffac_learner"] = VffacLearner
REGISTRY["immac_learner"] = ImmacLearner