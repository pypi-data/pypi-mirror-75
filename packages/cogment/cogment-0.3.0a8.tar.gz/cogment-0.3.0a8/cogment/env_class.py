class EnvClass:
    def __init__(self, id, config_type, message_space):
        self.id = id
        self.config_type = config_type
        self.message_space = message_space


class EnvClassList:
    def __init__(self, *args):
        self._env_classes_list = list(args)

        for a_c in args:
            setattr(self, a_c.id, a_c)

    def __iter__(self):
        return iter(self._env_classes_list)

    def get_env_counts(self, trial_params):
        result = [0] * len(self._env_classes_list)

        index_map = {}
        for index, env_class in enumerate(self._env_classes_list):
            index_map[env_class.id] = index

        for env in trial_params.actors:
            result[index_map[env.env_class]] += 1

        return result
