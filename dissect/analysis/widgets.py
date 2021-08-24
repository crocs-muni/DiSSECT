import difflib
from pathlib import Path

import ipywidgets as widgets
from IPython.core.display import display
from sage.all import sage_eval, RR, ZZ

from dissect.definitions import (
    ALL_BITLENGTHS,
    ALL_COFACTORS,
    TRAIT_DESCRIPTIONS,
)
from dissect.definitions import TRAIT_PATH, TRAIT_NAMES
from dissect.utils.json_handler import load_from_json
from dissect.analysis.data_processing import Modifier, get_curve_categories
import dissect.traits.trait_info as trait_info


def trait_selection_widget():
    trait_selection = widgets.Dropdown(
        options=["{} ({})".format(tn, TRAIT_DESCRIPTIONS[tn]) for tn in TRAIT_NAMES],
        value="a03 (factorization of the quadratic twist cardinality)",
        description="Trait name:",
        layout=widgets.Layout(width="auto"),
    )
    display(trait_selection)
    return trait_selection


def multi_checkbox_widget(name, preselected, others):
    """Widget with a search field and lots of checkboxes;
    inspired by https://gist.github.com/pbugnion/5bb7878ff212a0116f0f1fbc9f431a5c"""

    # Get rid of overlapping elements and convert everything to strings, but sort numerically when possible
    others_strings = list(map(str, set(others) - set(preselected)))
    try:
        others = sorted(others_strings, key=lambda x: 999 if x == "all" else int(x))
    except ValueError:
        others = sorted(others_strings)
    preselected = list(map(str, preselected))

    style = {"description_width": "initial"}
    layout = widgets.Layout(width="100px")
    widget_outer_width = "120px"

    description_widget = widgets.Label(
        value=f"{name}:", layout=widgets.Layout(position="top")
    )
    search_widget = widgets.Text(layout=widgets.Layout(width="auto"))
    select_preselected_widget = widgets.Checkbox(value=True)
    options_dict = {
        **{
            option: widgets.Checkbox(
                description=option, value=True, layout=layout, style=style
            )
            for option in preselected
        },
        **{
            option: widgets.Checkbox(
                description=option, value=False, layout=layout, style=style
            )
            for option in others
        },
    }
    all_options = preselected + others
    options = [options_dict[option] for option in all_options]
    options_widget = widgets.VBox(options, layout=widgets.Layout(width="auto"))
    multi_select = widgets.VBox(
        [description_widget, search_widget, options_widget],
        layout=widgets.Layout(width=widget_outer_width),
    )
    multi_select.name = name

    # Wire the search field to the checkboxes
    def on_text_change(change):
        search_input = change["new"]
        if search_input == "":
            # Reset search field
            new_options = [options_dict[option] for option in all_options]
        else:
            # Filter by search field using difflib.
            close_matches = difflib.get_close_matches(
                search_input, all_options, cutoff=0.0
            )
            new_options = [options_dict[option] for option in close_matches]
        options_widget.children = new_options

    search_widget.observe(on_text_change, names="value")
    return multi_select


def curve_widgets(source):
    categories = get_curve_categories(source)
    source_choice = multi_checkbox_widget(
        "category", preselected=["all"], others=categories
    )
    bits_choice = multi_checkbox_widget(
        "bits", preselected=["all"], others=ALL_BITLENGTHS
    )
    cofactor_choice = multi_checkbox_widget(
        "cofactor", preselected=["all"], others=ALL_COFACTORS
    )
    field_choice = multi_checkbox_widget(
        "field_type", preselected=["all"], others=["Prime", "Binary", "Extension"]
    )
    return [source_choice, bits_choice, cofactor_choice, field_choice]


def trait_filtering_widgets(trait_name):
    params_dict = get_trait_params_dict(trait_name)
    param_choice = []
    for param_name in params_dict.keys():
        param_values = params_dict[param_name]
        param_choice.append(
            multi_checkbox_widget(
                param_name, preselected=[param_values[0]], others=param_values
            )
        )
    return param_choice


def features_filtering_widgets(trait_name):
    features = trait_info.outputs(trait_name)
    features_widgets = widgets.RadioButtons(
        options=features,
        value=features[0],
        description="Feature:",
    )

    modifiers_widgets = widgets.RadioButtons(
        options=[method for method in dir(Modifier) if "__" not in method],
        value="identity",
        description="Modifier:",
    )

    return [features_widgets, modifiers_widgets]


def get_filtering_widgets(source, trait_name):
    curves_widgets = [*curve_widgets(source)]
    curves_hbox = widgets.HBox(
        curves_widgets,
        layout=widgets.Layout(
            justify_content="space-around", flex_flow="row wrap", height="250px"
        ),
    )
    params_widgets = [*trait_filtering_widgets(trait_name)]
    params_hbox = widgets.HBox(
        params_widgets,
        layout=widgets.Layout(
            justify_content="space-around", flex_flow="row wrap", height="250px"
        ),
    )
    features_widgets = features_filtering_widgets(trait_name)
    features_hbox = widgets.HBox(
        features_widgets,
        layout=widgets.Layout(
            justify_content="space-around", flex_flow="row wrap", height="250px"
        ),
    )
    tab = widgets.Tab()
    tab.children = [curves_hbox, params_hbox, features_hbox]
    tab.set_title(0, "Curves")
    tab.set_title(1, "Trait parameters")
    tab.set_title(2, "Features & modifiers")
    display(tab)
    return curves_widgets, params_widgets, features_widgets


def get_trait_params_dict(trait_name):
    params_file = load_from_json(Path(TRAIT_PATH, trait_name, trait_name + ".params"))
    params_names = params_file["params_local_names"]
    params_dict = {}
    for param_name in params_names:
        param_values = sage_eval(params_file["params_global"][param_name + "_range"])
        params_dict[param_name] = param_values
    params_dict_sorted = {key: params_dict[key] for key in sorted(params_dict)}
    return params_dict_sorted


def get_choices(filtering_widgets_tabs):
    result = {}
    for tab_widget in filtering_widgets_tabs:
        for subwidget in tab_widget:
            try:
                result[subwidget.name] = [
                    w.description for w in subwidget.children[-1].children if w.value
                ]
            except AttributeError:
                result[subwidget.description] = subwidget.value
    return result
