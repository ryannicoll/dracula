import re, os

class Parser:

    def __init__(self, stats=None):
        self.chapter_pattern = re.compile(r"^CHAPTER\s+[IVXLCDM]+$")
        self.end_pattern = re.compile(r"^\s+THE\s+END\s+$")
        self.char_pattern = re.compile(r"\w")
        self.word_pattern = re.compile(r"\w+")
        self.chapter_count = 0 
        self.dracula_stats = open(stats, 'w') if stats else None
        if self.dracula_stats is not None:
            self.line_count, self.word_count, self.char_count = 0,0,0
            self.dracula_stats.write(",".join(str(x) for x in ("Chapter #", "Line Count", "Word Count", "Character Count")))
            self.dracula_stats.write(os.linesep)
        
    def _write_stats(self):
        self.dracula_stats.write(",".join(str(x) for x in (self.chapter_count, self.line_count, self.word_count, self.char_count)))
        self.dracula_stats.write(os.linesep)
        self.line_count, self.word_count, self.char_count = 0,0,0
    
    def parse(self, f):
        with open(f, "r", encoding="utf8") as fin:
            for line in fin:
                if re.match(self.chapter_pattern, line):
                    if self.dracula_stats is not None and self.chapter_count > 0:
                        self._write_stats()
                    self.chapter_count += 1
                    current_file = open("Dracula-Chapter-{num}.txt".format(num=str(self.chapter_count)), "w")
                if self.chapter_count > 0:
                    current_file.write(line)
                    if self.dracula_stats is not None:
                        self.line_count += 1
                        self.char_count += len(re.findall(self.char_pattern, line))
                        self.word_count += len(re.findall(self.word_pattern, line))
                if self.dracula_stats is not None and re.match(self.end_pattern, line):
                    self._write_stats()

dracula_parser = Parser("dracula-stats.csv")
dracula_parser.parse("Dracula.txt")
