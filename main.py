import Read_file,maps_manager,create_index_file,state_reader,ParseInput
import os



def start_project():
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, "./KL_Output.txt")
    states_file = os.path.join(here, "./symbol_names.json")
    input_path = os.path.join(here, "./ASL.txt")
    output_path = os.path.join(here, "./ASL_OUT.txt")

    # KLOutput_path="./KL_Output.txt"
    file = Read_file.Read_file(KLOutput_path=filename)
    tirps = file.get_tirps()
    manager = maps_manager.maps_manager(tirps=tirps)
    start_dictionary = manager.get_start_dictionary()
    come_before = manager.get_come_before_dictionary()
    tirps_symbols_reader = state_reader.state_reader(states_file=states_file)
    states_map = tirps_symbols_reader.get_json()

    # creating the index file and print all dictionaries
    create_index_file.create_index_file(tirps=tirps, starts_dic=start_dictionary, come_before_dic=come_before)
    ParseInput.parse_kl_input(maps_manager=manager,input_path=input_path,output_path=output_path)
    raw_data = manager.get_raw_intervals()
    return [manager,states_map,raw_data]


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
    # start_project()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
