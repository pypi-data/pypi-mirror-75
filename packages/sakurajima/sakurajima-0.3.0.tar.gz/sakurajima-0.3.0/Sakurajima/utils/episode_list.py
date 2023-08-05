from Sakurajima.models import base_models as bm


class EpisodeList(object):
    def __init__(self, episode_list):
        self.validate_list(episode_list)
        self.__episode_list = episode_list

    def validate_list(self, episode_list):
        for episode in episode_list:
            if isinstance(episode, bm.Episode):
                continue
            else:
                raise ValueError(
                    "EpisodeList only take in lists that contain only Episode objects"
                )

    def get_episode_by_number(self, episode_number):
        result = list(
            filter(
                lambda episode: True if episode.number == episode_number else False,
                self.__episode_list,
            )
        )
        if len(result) == 0:
            return None
        else:
            return result[0]

    def get_episode_by_title(self, title):
        result = list(
            filter(
                lambda episode: True if episode.title == title else False,
                self.__episode_list,
            )
        )
        if len(result) == 0:
            return None
        else:
            return result[0]

    def __getitem__(self, position):
        if isinstance(position, int):
            return self.__episode_list[position]
        elif isinstance(position, slice):
            return EpisodeList(self.__episode_list[position])

    def __len__(self):
        return len(self.__episode_list)

    def __reversed__(self):
        return self[::-1]

    def __repr__(self):
        return f"EpisodeList({self.__episode_list})"
