import TIRP

class Read_file(object):

    def __init__(self, KLOutput_path):
        self.KLOutput_path=KLOutput_path
        self.lines = self.get_lines_from_file(KLOutput_path)
        self.TIRP_SIZE = 0
        self.SYMBOLS = 1
        self.RELATIONS = 2
        self.NUM_SUPPORT_ENTITIES = 3
        self.MEAN_HORIZONTAL_SUPPORT = 4
        self.OCCURRENCES = 5

        self.tirps = self.create_tirps()


    """gets path to KL output and returns all lines"""
    def get_lines_from_file(self,KLOutput_path):
        file = open(KLOutput_path, "r")
        # first line is just karma-lego output parameters
        file.readline()
        # actual output lines
        lines = file.readlines()
        file.close()
        return lines

    """for every line from the KL output file, creates a tirp"""
    def create_tirps(self):
        tirps = []
        for line in self.lines:
            line_components = line.split(" ")
            size = int(line_components[self.TIRP_SIZE])
            # take the symbols only(last place is '' after split)
            symbols = line_components[self.SYMBOLS].split("-")[0:-1]
            # take the relations only(last place is '' after split)
            relations = line_components[self.RELATIONS].split('.')[0:-1]
            num_support_entities = line_components[self.NUM_SUPPORT_ENTITIES]
            mean_horizontal_support = line_components[self.MEAN_HORIZONTAL_SUPPORT]
            occurrences = line_components[self.OCCURRENCES:]
            new_tirp = TIRP.TIRP(size=size, symbols=symbols, relations=relations, num_supporting_entities=num_support_entities, mean_horizontal_support=mean_horizontal_support, occurences=occurrences)
            tirps.append(new_tirp)
        return tirps

    def get_tirps(self):
        return self.tirps