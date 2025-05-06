"""
Writes to Output
"""
# A fájlba írást segítő függvény
def write_to_file(text):
    with open("output.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")

def Writeshort(Solution):
    write_to_file(Solution.split('\n', 1)[0])

def Write(id_value:int, A, b,k,Solution, output_file = "output.txt"):

    write_to_file(f"ID: {id_value}")
    write_to_file(f"A mátrix:\n{A}")
    write_to_file(f"b vektor: {b}")
    write_to_file(f"k érték: {k}")
    write_to_file(" ")
    write_to_file(Solution)
    with open(output_file, "a", encoding="utf-8") as f:
        f.write("\n")




#logging fájl írása legacynak !!NEM MŰKÖDIK!!
class SmartWriter:
    def __init__(self, filename):
        self.filename = filename
        self.lines = self._load_file()
        self.cursor = 0
        self.indent = self._calculate_indent()
        self.last_written_line = None

    def _load_file(self):
        with open(self.filename, 'r', encoding='utf-8') as f:
            return f.readlines()

    def _calculate_indent(self):
        # Legelső sor vezető szóközeinek száma
        for line in self.lines:
            if line.strip() != '':
                return len(line) - len(line.lstrip())
        return 0

    def write_to_file(self, text):
        while self.cursor < len(self.lines):
            line = self.lines[self.cursor].rstrip('\n')

            if line.strip() == 'END':
                # Ha END sor jönne, beszúrunk elé egy új sort
                new_line = ' ' * self.indent + text + '\n'
                self.lines.insert(self.cursor, new_line)
                self.last_written_line = self.cursor
                self.cursor += 1
                self._save()
                return

            # Ha a sor nem END, akkor melléírunk
            if '\t' in line:
                # Már van adat melléírva, nem írunk még egyet
                self.cursor += 1
                continue

            new_line = line + '\t' + text + '\n'
            self.lines[self.cursor] = new_line
            self.last_written_line = self.cursor
            self.cursor += 1
            self._save()
            return

        # Ha elértük a fájl végét, egyszerűen hozzáfűzzük
        new_line = ' ' * self.indent + text + '\n'
        self.lines.append(new_line)
        self.last_written_line = len(self.lines) - 1
        self.cursor += 1
        self._save()

    def write_end(self):
        while self.cursor < len(self.lines):
            if self.lines[self.cursor].strip() == 'END':
                self.cursor += 1
                return
            self.cursor += 1

    def append_to_last_written_line(self, text):
        if self.last_written_line is not None and self.last_written_line < len(self.lines):
            self.lines[self.last_written_line] = self.lines[self.last_written_line].rstrip('\n') + ' ' + text + '\n'
            self._save()
        else:
            raise RuntimeError("Nincs előzőleg írt sor, amihez lehetne fűzni.")

    def _save(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.writelines(self.lines)
