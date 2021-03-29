import Read_KL_Output_File,maps_manager,create_index_file,state_reader,ParseInput,Create_Forward_Index,Creare_Backwards_Index,Create_Vectors_Index
import os



def start_project(dataset_path):
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, dataset_path)
    # states_file = os.path.join(here, "./symbol_names.json")
    # input_path = os.path.join(here, "./ASL.txt")
    # output_path = os.path.join(here, "./ASL_OUT.txt")

    # KLOutput_path="./KL_Output.txt"
    file = Read_KL_Output_File.Read_file(KLOutput_path=filename+"/KL_Output.txt")
    forward_tree = file.get_forward_tree()
    backwards_tree = file.get_backwards_tree()
    relations_vectors = file.get_relations_vectors()

    # tirps = file.get_tirps()
    # manager = maps_manager.maps_manager(tirps=tirps)
    # start_dictionary = manager.get_start_dictionary()
    # come_before = manager.get_come_before_dictionary()
    # tirps_symbols_reader = state_reader.state_reader(states_file=states_file)
    # states_map = tirps_symbols_reader.get_json()

    Create_Forward_Index.Create_Forward_Index(forward_tree=forward_tree,
                                              forward_index_path=filename+"/forward_index_file.txt")
    Creare_Backwards_Index.Create_Backwards_Index(backwards_tree=backwards_tree,
                                                  backwards_index_path=filename+"/backwards_index_file.txt")
    Create_Vectors_Index.Create_Vectors_Index(relations_vectors=relations_vectors,vectors_index_path=filename+"/relations_index_file.txt")
    # creating the index file and print all dictionaries
    # create_index_file.create_index_file(tirps=tirps, starts_dic=start_dictionary, come_before_dic=come_before)
    # ParseInput.parse_kl_input(maps_manager=manager,input_path=input_path,output_path=output_path)
    # raw_data = manager.get_raw_intervals()
    # return [manager,states_map,raw_data]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dataset_path = "Datasets/ASL"
    start_project(dataset_path)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
