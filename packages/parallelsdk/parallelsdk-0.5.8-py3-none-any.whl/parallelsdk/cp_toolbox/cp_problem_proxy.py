import re
from parallelsdk.cp_toolbox import cp_sat_problem

CP_MODEL_KEY_WORDS = ['name', 'status_to_string', 'to_protobuf', 'upload_proto_solution']


def generate_proxy(model_str, instance_name):
    method_name_list = [f for f in dir(cp_sat_problem.CPSatProblem) if not f.startswith('_')]
    method_name_list = [f for f in method_name_list if f not in CP_MODEL_KEY_WORDS]
    for method_name in method_name_list:
        first_regex = '([^a-zA-Z][ \\t]*)(' + method_name + ')([ ]*\(+)'
        first_sub = '\\1' + instance_name + '.\\2\\3'
        second_regex = '^' + method_name + '([ ]*\()'
        second_sub = instance_name + '.' + method_name + '\\1'
        model_str_pair = re.subn(first_regex, first_sub, model_str)
        if model_str_pair[1] == 0:
            model_str = re.sub(second_regex, second_sub, model_str)
        else:
            model_str = model_str_pair[0]
    return model_str


