import hashlib
import os
import sys


class File:
    def __init__(self, n, path, size):
        self.n = n
        self.path = path
        self.size = size


class FileHandler:

    def __init__(self, root_f, f_form, sort):
        self.root_f = root_f
        self.f_form = f_form
        self.sort = sort
        self.file_sizes = {}
        self.file_hashes = {}
        self.to_delete = []

    @staticmethod
    def get_sort_opt():
        sort_opt = {'1': True, '2': False}
        print('\nSize sorting options:\n1. Descending\n2. Ascending')
        while True:
            sort = input('\nEnter a sorting option:\n')
            if sort in sort_opt:
                return sort_opt[sort]
            print('\nWrong option')

    @staticmethod
    def get_input_yesno(msg):
        while True:
            answer = input('\n' + msg + '\n')
            if answer in ('yes', 'no'):
                return True if answer == 'yes' else False
            print('Wrong option')

    def get_f_numbers(self):
        while True:
            answer = input('\nEnter file numbers to delete:\n').split()
            if answer and all(x.isdigit() and int(x) <= len(self.to_delete) for x in answer):
                return [int(n) for n in answer]
            print('\nWrong format')

    def sort_by_size(self):
        for root, dirs, files in os.walk(self.root_f):
            for file in files:
                f_path = os.path.join(root, file)
                if f_path.endswith(self.f_form):
                    self.file_sizes.setdefault(os.path.getsize(f_path), []).append(f_path)
        self.file_sizes = dict(sorted(self.file_sizes.items(), reverse=self.sort))
        self.file_sizes = dict(x for x in self.file_sizes.items() if len(x[1]) > 1)

    def sort_by_hash(self):
        for size, paths in self.file_sizes.items():
            self.file_hashes.setdefault(size, {})
            for file in paths:
                with open(file, 'rb') as f:
                    h = hashlib.md5(f.read()).hexdigest()
                self.file_hashes[size].setdefault(h, []).append(file)
            self.file_hashes[size] = dict(x for x in self.file_hashes[size].items() if len(x[1]) > 1)
        self.file_hashes = dict(x for x in self.file_hashes.items() if x[1])

    def print_same_size(self):
        for size, paths in self.file_sizes.items():
            print(f'\n{size} bytes')
            print('\n'.join(paths))

    def print_same_hash(self):
        n = 1
        for size, hashes in self.file_hashes.items():
            print(f'\n{size} bytes')
            for hash_, paths in hashes.items():
                print('Hash:', hash_)
                for path in paths:
                    print(f'{n}. {path}')
                    self.to_delete.append(File(n, path, size))
                    n += 1

    def delete_files(self, numbers):
        freed_space = 0
        for file in self.to_delete:
            if file.n in numbers:
                os.remove(file.path)
                freed_space += file.size
        print(f'\nTotal freed up space: {freed_space} bytes')


def main():
    if len(sys.argv) != 2:
        print('Directory is not specified')
        sys.exit()
    file_format = input('\nEnter file format:\n')
    sort = FileHandler.get_sort_opt()
    handler = FileHandler(sys.argv[1], file_format, sort)
    handler.sort_by_size()
    handler.print_same_size()
    if FileHandler.get_input_yesno('Check for duplicates?'):
        handler.sort_by_hash()
        handler.print_same_hash()
        if FileHandler.get_input_yesno('Delete files?'):
            handler.delete_files(handler.get_f_numbers())


if __name__ == '__main__':
    main()
