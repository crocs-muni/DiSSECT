#!/usr/bin/env python3
import difflib
from pathlib import Path

import ipywidgets as widgets
from IPython.core.display import display

from curve_analyzer.definitions import STD_SOURCES, STD_BITLENGTHS, ALL_COFACTORS
from curve_analyzer.utils.json_handler import load_from_json
from curve_analyzer.utils.data_processing import filter_df
from curve_analyzer.definitions import TRAIT_PATH
from sage.all import sage_eval


def multi_checkbox_widget(name, preselected, others):
    """ Inspired by from https://gist.github.com/pbugnion/5bb7878ff212a0116f0f1fbc9f431a5c """
    """ Widget with a search field and lots of checkboxes """

    # Get rid of overlapping elements and convert everything to strings, but sort numerically when possible
    others_strings = list(map(str, set(others) - set(preselected)))
    try:
        others = sorted(others_strings, key=int)
    except ValueError:
        others = sorted(others_strings)
    preselected = list(map(str, preselected))

    style = {'description_width': 'initial'}
    layout = widgets.Layout(width="100px")
    widget_outer_width = "120px"

    description_widget = widgets.Label(value=f"{name}:", layout=widgets.Layout(position="top"))
    search_widget = widgets.Text(layout=widgets.Layout(width="auto"))
    select_all_widget = widgets.Checkbox(description="(un)select all", value=False, style=style)
    select_preselected_widget = widgets.Checkbox(value=True)
    options_dict = {**{option: widgets.Checkbox(description=option, value=True,
                                                layout=layout, style=style) for option in preselected},
                    **{option: widgets.Checkbox(description=option, value=False,
                                                layout=layout, style=style) for option in others}}
    all_options = preselected + others
    options = [options_dict[option] for option in all_options]
    options_widget = widgets.VBox(options)
    # link all options to the select_all_widget, but also make sure this doesn't unselect preselected ones:
    for option in options:
        widgets.jsdlink((select_all_widget, 'value'), (option, 'value'))
        if option.value:
            widgets.jsdlink((select_preselected_widget, 'value'), (option, 'value'))
    multi_select = widgets.VBox([description_widget, search_widget, select_all_widget, options_widget],
                                layout=widgets.Layout(width=widget_outer_width))
    multi_select.name = name

    # Wire the search field to the checkboxes
    def on_text_change(change):
        search_input = change['new']
        if search_input == '':
            # Reset search field
            new_options = [options_dict[option] for option in all_options]
        else:
            # Filter by search field using difflib.
            close_matches = difflib.get_close_matches(search_input, all_options, cutoff=0.0)
            new_options = [options_dict[option] for option in close_matches]
        options_widget.children = new_options

    search_widget.observe(on_text_change, names='value')
    return multi_select


def common_filtering_widgets():
    source_choice = multi_checkbox_widget("source", preselected=["std", "sim"], others=STD_SOURCES)
    bitlength_choice = multi_checkbox_widget("bitlength", preselected=[128, 160, 192, 224, 256], others=STD_BITLENGTHS)
    cofactor_choice = multi_checkbox_widget("cofactor", preselected=[1], others=ALL_COFACTORS)
    return [source_choice, bitlength_choice, cofactor_choice]


def trait_filtering_widgets(trait_name):
    params_dict = get_trait_params_dict(trait_name)
    param_choice = []
    for param_name in params_dict.keys():
        param_values = params_dict[param_name]
        param_choice.append(multi_checkbox_widget(param_name, preselected=[param_values[0]], others=param_values))
    return param_choice


def get_filtering_widgets(trait_name):
    filtering_widgets = [*common_filtering_widgets(), *trait_filtering_widgets(trait_name)]
    hbox = widgets.HBox(filtering_widgets,
                        layout=widgets.Layout(justify_content='space-around', flex_flow='row wrap', height='250px'))
    display(hbox)
    return filtering_widgets


def get_trait_params_dict(trait_name):
    params_file = load_from_json(Path(TRAIT_PATH, trait_name, trait_name + ".params"))
    params_names = params_file["params_local_names"]
    params_dict = {}
    for param_name in params_names:
        param_values = sage_eval(params_file["params_global"][param_name + "_range"])
        params_dict[param_name] = param_values
    params_dict_sorted = {key: params_dict[key] for key in sorted(params_dict)}
    return params_dict_sorted


def get_choices(filtering_widgets):
    result = {}
    for subwidget in filtering_widgets:
        result[subwidget.name] = [w.description for w in subwidget.children[-1].children if w.value]
    return result
