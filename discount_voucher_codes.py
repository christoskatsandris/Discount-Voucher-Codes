from enum import Enum
import random
import timeit
import math
import sympy

ascii_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Voucher:
    def __init__(self):
        self.code = str()

    def __str__(self):
        return self.code[0:4] + '-' + self.code[4:8] + '-' + self.code[8:12]

    def generate(self):
        for _ in range(4):
            self.code += random.choice(ascii_letters)
        for _ in range(4):
            self.code += str(random.randint(0,9))
        for _ in range(4):
            self.code += random.choice(ascii_letters) 

    def load(self, code):
        self.code = code
        
    def star_code(self, starred_codes_list):
        chars = list(self.code)
        for index in range(len(chars)):
            original = chars[index]
            chars[index] = "*"
            starred_codes_list.append("".join(chars))
            chars[index] = original 

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def insert(self, starred_code):
        key = hash(starred_code) % self.size

        cell = self.table[key]
        for content in cell:
            if content[0] == starred_code:
                content[1] += 1
                return
        cell.append([starred_code, 1])
    
    def count_duplicates(self):
        counter = 0
        for cell in self.table:
            for content in cell:
                if content[1] > 1:
                    counter += math.comb(content[1], 2)
        return counter

class Algorithm:
    class Mode(Enum):
        GENERATE = 1,
        IMPORT = 2

    def __init__(
        self,
        mode = Mode.GENERATE,
        number_of_vouchers = None,
        import_filename = None,
        export = False,
        export_filename = None
    ):
        """
        Parameters
        ----------
        mode : Algorithm.Mode
            Choose Algorithm.Mode.GENERATE should you want to generate random voucher codes.
            Choose Algorithm.Mode.IMPORT should you want to import voucher codes from a file.
            default: Algorithm.Mode.GENERATE

        number_of_vouchers : int
            Choose how many vouchers should be generated.
            Number should be a positive integer.
            Required argument if GENERATE mode has been selected.
            default: None

        import_filename : str
            Choose the file from which the vouchers should be imported.
            Required argument if IMPORT mode has been selected.
            default: None
            
        export : boolean
            Choose whether the voucher codes should be exported to a file.
            default: False
            
        export_filename : str
            Choose the file to which the vouchers should be exported.
            Required argument if export has been set True.
            default: None
        """

        # Required arguments validation
        if mode == self.Mode.GENERATE and number_of_vouchers == None:
            raise TypeError("Please specify how many vouchers should be generated.")
        if mode == self.Mode.GENERATE and ((not isinstance(number_of_vouchers, int)) or number_of_vouchers < 1):
            raise TypeError("Invalid number of vouchers requested.")
        if mode == self.Mode.IMPORT and import_filename == None:
            raise TypeError("Please specify the file name from which the vouchers should be imported.")
        if export and export_filename == None:
            raise TypeError("Please specify the file name to which the vouchers should be exported.")
        
        # Unused arguments validation
        if mode == self.Mode.GENERATE and import_filename != None:
            print("WARNING: Vouchers will be generated. Import filename will be discarded.")
        if mode == self.Mode.IMPORT and number_of_vouchers != None:
            print("WARNING: Vouchers will be imported. Requested number of vouchers will be discarded.")
        if (not export) and export_filename != None:
            print("WARNING: Vouchers will not be exported. Export filename will be discarded.")
          
        self.mode = mode
        self.export = export
        self.import_filename = import_filename
        self.export_filename = export_filename
        self.number_of_vouchers = number_of_vouchers

        self.vouchers_list = []
        self.starred_codes_list = []

        self.main()

    def generate_vouchers(self):
        for _ in range(self.number_of_vouchers):
            new_voucher = Voucher()
            new_voucher.generate()
            self.vouchers_list.append(new_voucher)
        print(f"Generated {self.number_of_vouchers} vouchers.")

    def import_vouchers(self):
        with open(self.import_filename, "rt") as file:
            while True:
                new_line = file.readline().strip()
                if new_line == "":
                    break
                new_voucher = Voucher()
                new_voucher.load(new_line)
                self.vouchers_list.append(new_voucher)
        self.number_of_vouchers = len(self.vouchers_list)
        print(f"Imported {self.number_of_vouchers} vouchers.")

    def export_vouchers(self):
        with open(self.export_filename, "wt") as file:
            for voucher in self.vouchers_list:
                print(voucher.code, file=file)
        print(f"Exported {self.number_of_vouchers} vouchers.")
    
    def main(self):
        if self.mode == self.Mode.GENERATE:
            self.generate_vouchers()
        else:
            self.import_vouchers()

        initial_timestamp = timeit.default_timer()
        for voucher in self.vouchers_list:
            voucher.star_code(self.starred_codes_list)
        
        hash_table = HashTable(sympy.nextprime(len(self.starred_codes_list)))

        for starred_code in self.starred_codes_list:
            hash_table.insert(starred_code)

        duplicates = hash_table.count_duplicates()

        final_timestamp = timeit.default_timer() - initial_timestamp
        print(f"Found {duplicates} similar codes in {final_timestamp} seconds.")

        if self.export:
            self.export_vouchers()
        
        print("-------------------------------------")

if __name__ == "__main__":
    Algorithm(
        mode = Algorithm.Mode.GENERATE,
        number_of_vouchers = 100000
    )
    Algorithm(
        mode = Algorithm.Mode.IMPORT,
        import_filename = "voucher_list.txt",
    )
    Algorithm(
        mode = Algorithm.Mode.GENERATE,
        number_of_vouchers = 200000,
        export = True,
        export_filename = "exported_vouchers.txt"
    )
