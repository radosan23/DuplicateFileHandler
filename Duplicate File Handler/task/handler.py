import os
import sys


class FileHandler:

    def __init__(self, root_f, f_form, sort):
        self.root_f = root_f
        self.f_form = f_form
        self.sort = sort
        self.file_sizes = {}

    @staticmethod
    def get_sort_opt():
        sort_opt = {'1': True, '2': False}
        print('\nSize sorting options:\n1. Descending\n2. Ascending')
        while True:
            sort = input('\nEnter a sorting option:\n')
            if sort in sort_opt:
                return sort_opt[sort]
            print('\nWrong option')

    def find_files(self):
        for root, dirs, files in os.walk(self.root_f):
            for file in files:
                f_path = os.path.join(root, file)
                if f_path.endswith(self.f_form):
                    self.file_sizes.setdefault(os.path.getsize(f_path), []).append(f_path)
        self.file_sizes = dict(sorted(self.file_sizes.items(), reverse=self.sort))

    def print_files(self):
        for key, value in self.file_sizes.items():
            if len(value) > 1:
                print(f'\n{key} bytes')
                print('\n'.join(value))


def main():
    if len(sys.argv) != 2:
        print('Directory is not specified')
        sys.exit()
    file_format = input('\nEnter file format:\n')
    sort = FileHandler.get_sort_opt()
    handler = FileHandler(sys.argv[1], file_format, sort)
    handler.find_files()
    handler.print_files()


if __name__ == '__main__':
    main()
