def init_test(test_name):
    path_json = '../results/' + test_name + '.json'
    path_progress = os.path.splitext(path_json)[0] + "-progress.txt"
    path_txt = os.path.splitext(path_json)[0] + ".txt"
    return path_json, path_progress, path_txt

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
                res_sorted.append(sorted(results[name][res], key = res_sort_key)[:head])
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
            f.write(str(t))