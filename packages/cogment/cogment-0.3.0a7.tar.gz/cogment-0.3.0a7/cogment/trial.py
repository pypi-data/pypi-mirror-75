from types import SimpleNamespace
from cogment.api.common_pb2 import Feedback, Message


class Actor:

    def __init__(self, actor_class, actor_id, id_in_class, trial):
        self.actor_class = actor_class
        self.actor_id = actor_id
        self.id_in_class = id_in_class

        self._feedback = []
        self._message = []
        self.trial = trial

    def add_feedback(self, value=None, confidence=None, tick_id=None, user_data=None):
        if tick_id is None:
            tick_id = -1

        self._feedback.append((tick_id, value, confidence, user_data))

    def send_message(self, user_data=None):
        self._message.append(user_data)


class Env:

    def __init__(self, actor_id, trial):
        self.actor_id = actor_id

        self._message = []
        self.trial = trial

    def send_message(self, user_data):
        self._message.append((user_data))


class Trial:

    def __init__(self, id, settings, actor_counts, trial_config):
        self.id = id
        self.actor_counts = actor_counts
        self.actors = SimpleNamespace(all=[])
        self.settings = settings
        self.tick_id = 0
        self.trial_config = trial_config

        self.env = SimpleNamespace(all=[])

        actor_id = 0
        for class_index, actor_class in enumerate(self.settings.actor_classes):
            actor_list = []
            id_in_class = 0
            for _ in range(actor_counts[class_index]):
                actor = Actor(actor_class, actor_id, id_in_class, self)
                actor_list.append(actor)
                self.actors.all.append(actor)
                actor_id += 1
                id_in_class += 1

            setattr(self.actors, actor_class.id, actor_list)

        env_list = []
        env = Env(-1, self)
        env_list.append(env)
        self.env.all.append(env)
        env_class = self.settings.env_class

        setattr(self.env, env_class.id, env_list)

    def new_observation_table(self):
        return self.settings.ObservationsTable(self.actor_counts)

    def _get_all_feedback(self):
        for actor in self.actors.all:
            a_fb = actor._feedback
            actor._feedback = []

            for fb in a_fb:
                re = Feedback(
                    actor_id=actor.actor_id,
                    tick_id=fb[0],
                    value=fb[1],
                    confidence=fb[2],
                    agent_id=actor.id_in_class
                )
                if fb[3] is not None:
                    re.content = fb[3].SerializeToString()

                yield re

    def _get_all_messages(self, source_id):

        for actor in self.actors.all:
            a_msg = actor._message
            actor._message = []

            for msg in a_msg:
                re = Message(
                    sender_id=source_id,
                    receiver_id=actor.actor_id
                )
                if msg is not None:
                    re.payload.Pack(msg)
                yield re

        for env in self.env.all:
            e_msg = env._message
            env._message = []

            for msg in e_msg:
                re = Message(
                    sender_id=source_id,
                    receiver_id=-1
                )

                if msg is not None:
                    re.payload.Pack(msg)
                yield re

    def multi_cast(self, user_data=None, send_list=None):

        if send_list is not None:
            possible_targets = [i for i in range(sum(self.actor_counts))]
            possible_targets.append(-1)

            for target in send_list:
                if target in possible_targets:
                    if target == -1:
                        self.env.env[0].send_message(user_data=user_data)
                    elif target == 0:
                        self.actors.human[0].send_message(user_data=user_data)
                    else:
                        self.actors.agent[
                            target - 1].send_message(user_data=user_data)
                else:
                    raise Exception(target, "is not a valid agent!!")
