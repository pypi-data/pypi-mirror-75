class StringUtils:

    @staticmethod
    def find_strings_in_list(strings, string_list):
        return [string for string in strings if string in string_list]
