from dissect.definitions import TRAIT_DESCRIPTIONS, TRAIT_PATH, ROOT_DIR
import dissect.traits.gen_unittest as unittest
import dissect.traits.gen_trait_structures as structures
import os
import dissect.utils.json_handler as json_handler
import consolemenu
from consolemenu.items import *


def create_directory(name):
    path = os.path.join(TRAIT_PATH, name)
    os.mkdir(path)
    with open(os.path.join(path, "__init__.py"), "w"):
        pass
    print("Directory", name, "created")


def check_files(name):
    path = os.path.join(TRAIT_PATH, name)
    message = (
            "Please put the files "
            + name
            + ".py and "
            + name
            + ".params"
            + " in the directory "
            + name
            + " and press enter"
    )
    while True:
        input(message)
        if not os.path.isfile(os.path.join(path, name + ".py")):
            print("File", name + ".py", "not found")
            continue
        if not os.path.isfile(os.path.join(path, name + ".params")):
            print("File", name + ".params", "not found")
            continue
        break


def update_default_params(name, delete=False):
    dp_path = os.path.join(TRAIT_PATH, "default.params")
    dp = json_handler.load_from_json(dp_path)
    if delete:
        del dp[name]
    else:
        dp[name] = json_handler.load_from_json(os.path.join(TRAIT_PATH, name, name + ".params"))
    json_handler.save_into_json(dp, dp_path, mode="w")


def update_descriptions(name, desc=None, delete=False):
    descs_path = os.path.join(TRAIT_PATH, "trait_descriptions")
    descs = json_handler.load_from_json(descs_path)
    if delete:
        del descs[name]
        del TRAIT_DESCRIPTIONS[name]
    else:
        descs[name] = desc
        TRAIT_DESCRIPTIONS[name] = desc
    json_handler.save_into_json(descs, descs_path, mode="w")


def create_trait():
    name = input("Oh yeah, new trait! Type the name: ")
    create_directory(name)
    check_files(name)
    update_default_params(name)

    if not 'm' == input(
            "We need to create structure file. Do you wish to create one automatically (you trust your implementation) or manually (slower)? [A/m]").lower():
        structures.compute_results(name)
    else:
        unittest.main(name, False, True)
    if input("Do you  wish to auto-generate unittest?[Y/n]").lower() != "n":
        unittest.main(trait_name=name, u=True, s=False)
    desc = input("Please write a short description for your trait: ")
    update_descriptions(name, desc)
    input("Awesome! Trait " + name + " is ready to go! Don't forget to update trait_info.py")


def modify_description(name):
    desc = input("Write a short description for your trait: ")
    update_descriptions(name, desc)


def change_feature(name, feature, new_feature, file):
    print("Changing", file)
    structure_path = os.path.join(TRAIT_PATH, name, file)
    try:
        structure = json_handler.load_from_json(structure_path)
    except FileNotFoundError:
        print("File", file, "not found, moving on.")
        return
    for curve, result in structure.items():
        for param, values in result.items():
            values[new_feature] = values.pop(feature)
    json_handler.save_into_json(structure, structure_path, mode="w")


def modify_features_name(name):
    close = "All done. Don't forget to change the file " + name + ".py and the unittest (you can autogenerate)."
    structure = json_handler.load_from_json(os.path.join(TRAIT_PATH, name, name + "_structure.json"))
    features_names = list(list(list(structure.values())[0].values())[0].keys())
    options = {}
    for i, feature in enumerate(features_names):
        options[i + 1] = feature
        print("(" + str(i + 1) + ")", feature)
    choice = int(input("Which feature do you want to change? "))
    feature = options[choice]
    if input("Do you really want to change the name of the feature \'" + feature + "\'? [y/N]:").lower() != "y":
        input("OK, nevermind")
        return
    new_feature_name = input("Type the new name of the feature: ")

    change_feature(name, options[choice], new_feature_name, name + "_structure.json")

    result_file = name + ".json"
    if input(
            "Do you also wish to modify the result file " + result_file + " (might take a while)? [y/N]:").lower() != "y":
        input(close)
        return
    change_feature(name, options[choice], new_feature_name, result_file)
    input(close)


def modify_trait(menu):
    name = input("Type the name of the trait: ")
    modify_menu = consolemenu.ConsoleMenu("Trait " + name, TRAIT_DESCRIPTIONS[name])
    modify_menu.parent = menu

    modify_menu.append_item(FunctionItem("Generate a trait structure", structures.compute_results, [name]))
    modify_menu.append_item(FunctionItem("Manually create new trait structure", unittest.main, [name, False, True]))
    modify_menu.append_item(FunctionItem("Generate a unittest", unittest.main, [name, True, False]))
    modify_menu.append_item(FunctionItem("Modify the description", modify_description, [name]))
    modify_menu.append_item(FunctionItem("Modify the features' names", modify_features_name, [name]))

    modify_menu.show()


def delete_trait():
    name = input("Type the name of the trait: ")
    if not input("Are you sure you want to delete trait " + name + "?[Y/n]: ").lower() == 'y':
        return
    update_default_params(name, delete=True)
    update_descriptions(name, delete=True)
    input('You can remove the trait folder and the unittest. Dont forget to update trait_info.py')


def main():
    menu = consolemenu.ConsoleMenu("DiSSECT", "Welcome to DiSSECT! You can create or modify traits.")
    function_item = FunctionItem("Create a trait", create_trait)
    menu.append_item(function_item)
    function_item2 = FunctionItem("Modify existing trait", modify_trait, [menu])
    menu.append_item(function_item2)
    function_item3 = FunctionItem("Delete existing trait", delete_trait)
    menu.append_item(function_item3)
    menu.show()


if __name__ == "__main__":
    main()
