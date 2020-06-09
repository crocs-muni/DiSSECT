def init_test(test_name):
    path_json = '../results/' + test_name + '.json'
    path_progress = os.path.splitext(path_json)[0] + "-progress.txt"
    path_txt = os.path.splitext(path_json)[0] + ".txt"
    return path_json, path_progress, path_txt

#https://ask.sagemath.org/question/10112/kill-the-thread-in-a-long-computation/
def timeout(func, args=(), kwargs={}, timeout_duration = 10):
    @fork(timeout=timeout_duration, verbose=False)
    def my_new_func():
        return func(*args, **kwargs)
    return my_new_func()

# parameters = {'l_max': 100}
def compute_results(test_name, parameters, curve_list = curves, order_bound = 256):
    jsonfile, progressfile, _ = init_test(test_name)
    def feedback(text, outfile = progressfile):
        print(text)
        with open(outfile, 'a') as f:
            f.write(text)

    total = {'parameters': {}, 'results': {}}
    total['parameters'] = parameters
    # parameters = {'l_max': 100}
    param_list = list(parameters.values())
    results = {}
    for curve in curve_list:
        feedback("Processing curve " + curve.name + ":\t")
        
        if curve.order.nbits() > order_bound:
            feedback("Too large order\n")
            continue
        # TODO: add timeout support

        results[curve.name] = get_curve_results(curve, *param_list)
        feedback("Done\n")
        
        total['results'] = results
        save_into_json(total, jsonfile, 'w')

def pretty_print_results(test_name, result_names, captions, head = 2^100, curve_list = curves, res_sort_key = lambda x: x, curve_sort_key = "bits", save_to_txt = True):
    infile, _, outfile = init_test(test_name)
    total = load_from_json(infile)
    params = total['parameters']
    param_table = PrettyTable(['parameter', 'value'])
    for param in params.keys():
        param_table.add_row([param, params[param]])
    print(param_table, '\n\n')
    
    assert len(result_names) == len(captions)
    cols = len(result_names)
    results = total['results']
    names_computed = results.keys()
    headlines = ['name', 'bits']
    for caption in captions:
        headlines.append(caption)
    t = PrettyTable(headlines)
    
    for curve in curve_list:
        name = curve.name
        order_bits = curve.order.nbits()
        if name in names_computed:
            res_sorted = []
            for res in result_names:
                data = results[name]
                for r in res:
                    data = data[r]
                res_sorted.append(sorted(data, key = res_sort_key)[:head])
        else:
            res_sorted = ["Not computed"] * cols
        row = [name, order_bits]
        for res in res_sorted:
            row.append(res)
        t.add_row(row)
    t.sortby = curve_sort_key
    print(t)
    
    if save_to_txt:
        with open(outfile, "w") as f:
            f.write(str(param_table))
            f.write('\n\n')
            f.write(str(t))

def ints_before_strings(x):
    try:
        return ZZ(x)
    except:
        return oo