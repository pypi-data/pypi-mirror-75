def replace_multi_substrs_via_dict(given_str: str, replace_map: dict) -> str:
    """
    Replace all substrings given as keys in replace_map by corresponding values
    :param given_str: Target String to manipulate
    :type given_str: str
    :param replace_map: Manipulation Mapping
    :type replace_map:
    :return: the transformed given_str
    :rtype: str
    """

    for sub_str, sub_str_rpl in replace_map.items():
        given_str = given_str.replace(sub_str, sub_str_rpl)
    return given_str


class StringUtility:
    @staticmethod
    def find_longest_prefix_match_index(a: str, b: str) -> int:
        """
        Given two strings find the highest matching index
        """
        i = 0
        while a[i] == b[i]:
            i += 1
            if i == min(len(a), len(b)):
                break
        return i
