from dissect.definitions import TRAIT_DESCRIPTIONS, TRAIT_PATH, ROOT_DIR
import dissect.traits.gen_unittest as unittest
import dissect.traits.gen_trait_structures as structures
import os
import dissect.utils.json_handler as json_handler


def create_directory(name):
    path = os.path.join(TRAIT_PATH, name)
    os.mkdir(path)
    with open(os.path.join(path, '__init__.py'), 'w'):
        pass
    print('Directory', name, 'created')


def check_files(name):
    path = os.path.join(TRAIT_PATH, name)
    message = 'Please put the files ' + name + '.py and ' + name + '.params' + ' in the directory ' + name + ' and press enter'
    while True:
        input(message)
        if not os.path.isfile(os.path.join(path, name + '.py')):
            print('File', name + '.py', 'not found')
            continue
        if not os.path.isfile(os.path.join(path, name + '.params')):
            print('File', name + '.params', 'not found')
            continue
        break


def update_default_params(name):
    dp_path = os.path.join(TRAIT_PATH, 'default.params')
    dp = json_handler.load_from_json(dp_path)
    p = json_handler.load_from_json(os.path.join(TRAIT_PATH, name, name + '.params'))
    dp[name] = p
    json_handler.save_into_json(dp, dp_path, mode='w')


def update_descriptions(name, desc):
    descs_path = os.path.join(TRAIT_PATH, 'trait_descriptions')
    descs = json_handler.load_from_json(descs_path)
    descs[name] = desc
    json_handler.save_into_json(descs, descs_path, mode='w')


def main():
    welcome = 'Welcome to Curve analyzer! You can create or modify traits. Please input a name of trait: '
    name = input(welcome)
    if name in TRAIT_DESCRIPTIONS:
        print('There is a trait', name, '(' + TRAIT_DESCRIPTIONS[name] + ')')
        choice = input(
            'Do you want to:\n' + '[1] Generate a trait structure\n' + '[2] Manually create new trait structure\n' + '[3] Generate a unittest\n')
        if choice == '1':
            structures.compute_results(trait_name=name)
        if choice == '2':
            unittest.main(trait_name=name, u=False, s=True)
        if choice == '3':
            unittest.main(trait_name=name, u=True, s=False)
        return
    print("Oh yeah, new trait!")
    create_directory(name)
    check_files(name)
    update_default_params(name)
    print('We need to create structure file. Do you with to create one:\n',
          '[1] manually (you trust your implementation) \n', '[2] automatically (quicker)')
    if input() == '1':
        unittest.main(trait_name=name, u=False, s=True)
    else:
        structures.compute_results(trait_name=name)
    if input('Do you wish to auto-generate unittest?[Y/n]').lower() != 'n':
        unittest.main(trait_name=name, u=True, s=False)
    desc = input('Please write a short description for your trait: ')
    update_descriptions(name, desc)


if __name__ == '__main__':
    main()
