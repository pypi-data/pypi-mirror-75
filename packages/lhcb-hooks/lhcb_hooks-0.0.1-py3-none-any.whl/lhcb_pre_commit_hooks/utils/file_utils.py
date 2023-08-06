import os

class FileUtils:

    @staticmethod
    def get_non_empty_filenames(path):
        file_names = FileUtils.get_filenames(path)

        non_empty_filenames = []
        for file_name in file_names:
            if not FileUtils.is_empty('{}/{}'.format(path, file_name)):
                non_empty_filenames.append(file_name)

        return non_empty_filenames

    @staticmethod
    def get_filenames(path):
        file_names = []

        for (_, _, filenames) in os.walk(path):
            file_names.extend(filenames)
            break

        return file_names

    @staticmethod
    def is_empty(path):
        '''
        Check if file is empty or virtually empty (only spaces).
        '''

        def only_blanks():
            with open(path) as f:
                for l in f:
                    if l.strip():
                        return False
            return True

        zero_size = os.stat(path).st_size == 0
        return zero_size or only_blanks()