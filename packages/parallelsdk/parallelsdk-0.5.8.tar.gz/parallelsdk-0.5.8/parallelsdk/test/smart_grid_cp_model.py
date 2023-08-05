def create_int_var_array(model, len_array, min_dom, max_dom, name='v_'):
    var_array = []
    for idx in range(len_array):
        var_name = name + str(idx)
        var = model.IntVar(min_dom, max_dom, var_name)
        var_array.append(var)
    return var_array


def create_int_var_2d_array(model, num_rows, num_cols, min_dom, max_dom, name='v_'):
    var_array = []
    for r_idx in range(num_rows):
        row_array = []
        for c_idx in range(num_cols):
            var_name = name + str(r_idx) + "_" + str(c_idx)
            var = model.IntVar(min_dom, max_dom, var_name)
            row_array.append(var)
        var_array.append(row_array)
    return var_array


def get_domain_neg_inf(self):
    return -2147483646


def get_domain_pos_inf(self):
    return -2147483647


def createSmartGridCPModel(model):
    num_actuators = 6
    predictive_model_size = 6
    max_neighbors_power_consumption = 0
    min_neighbors_power_consumption = 0
    max_background_load = 2
    min_background_load = 0
    horizon = 12
    aggregated_power_bounds = [0, 364]
    lb_obj_price = 0
    ub_obj_price = 30572
    lb_obj_power_diff = 0
    ub_obj_power_diff = 1589952
    x = []
    var_predictive_model = create_int_var_2d_array(model,
                                                   predictive_model_size, horizon,
                                                   model.get_infinity(False),
                                                   model.get_infinity(True),
                                                   'predModel_')
    var_aggr_power = create_int_var_array(model,
                                          horizon,
                                          aggregated_power_bounds[0] + min_background_load,
                                          aggregated_power_bounds[1] + max_background_load,
                                          'aggrPower_')
    x.append(create_int_var_array(model, horizon, 0, 1, 'x_GE_WSM2420D3WW'))
    x.append(create_int_var_array(model, horizon, 0, 1, 'x_Tesla_S'))
    x.append(create_int_var_array(model, horizon, 0, 1, 'x_Kenmore_665.13242K900'))
    x.append(create_int_var_array(model, horizon, 0, 1, 'x_E52-50R-045DV'))
    x.append(create_int_var_array(model, horizon, 0, 2, 'x_Kenmore_790.91312013'))
    x.append(create_int_var_array(model, horizon, 0, 1, 'x_LG_WM2016CW'))
    obj_price = model.IntVar(lb_obj_price, ub_obj_price, 'price')
    obj_power_diff = model.IntVar(lb_obj_power_diff, ub_obj_power_diff, 'pwDiff')

    # Constraints

