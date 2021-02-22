import Read_file,maps_manager,create_index_file
import os



def start_project():
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, "./KL_Output.txt")

    # KLOutput_path="./KL_Output.txt"
    file = Read_file.Read_file(KLOutput_path=filename)
    tirps = file.get_tirps()
    manager = maps_manager.maps_manager(tirps=tirps)
    start_dictionary = manager.get_start_dictionary()
    come_before = manager.get_come_before_dictionary()
    # end_dictionary = manager.get_end_dictionary()

    # creating the index file and print all dictionaries
    create_index_file.create_index_file(tirps=tirps, starts_dic=start_dictionary, come_before_dic=come_before)
    return manager


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
    # start_project()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
