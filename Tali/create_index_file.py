
class create_index_file (object):

    def __init__(self, tirps, starts_dic, come_before_dic):
        # output index file path
        self.index_file = open("index_file.txt", "w")

        self.tirps = tirps
        self.starts_dic = starts_dic
        self.come_before_dic = come_before_dic

        # self.ends_dic = ends_dic

        # creating the index output file
        self.write_to_index_file()

        self.index_file.close()

    """write to the output index file"""
    def write_to_index_file(self):
        for tirp in self.tirps:
            self.index_file.write("tirp: "+str(tirp)+"\n")

            self.index_file.write("starts_with: ")
            starts_with = self.starts_dic[tirp]
            self.write_to_index_file_tirps(tirps=starts_with)
            self.index_file.write("\n")
            self.index_file.write("\n")

            self.index_file.write("come_before: ")
            come_before = self.come_before_dic[tirp]
            self.write_to_index_file_tirps(tirps=come_before)
            self.index_file.write("\n")
            self.index_file.write("--------------------------------------------------------------------------------")
            self.index_file.write("\n")
            self.index_file.write("\n")

            # self.index_file.write("ends_with: ")
            # ends_with = self.ends_dic[tirp]
            # self.write_to_index_file_tirps(tirps=ends_with)
            # self.index_file.write("\n")
            # self.index_file.write("\n")


    """writes the list of tirps to the index output file"""
    def write_to_index_file_tirps(self,tirps):
        for tirp in tirps:
            self.index_file.write(str(tirp))
