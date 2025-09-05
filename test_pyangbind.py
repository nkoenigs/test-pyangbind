from pathlib import Path
import subprocess


def test_yang(model_path, do_pdb):

    print("testing pyangbind with model " + model_path.as_posix())

    ##########################################################################

    print("making yang tree")

    command = [
        "pyang",
        "--path", model_path.as_posix(),
        '-f', 'tree',
    ] + [yang_file.as_posix() for yang_file in model_path.glob("*.yang")]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    with Path("output/tree.txt").open("w", encoding='utf-8') as f:
        f.write(result.stdout)

    ##########################################################################

    print("running toy yang compiler")

    OUTPUT_PATH = Path("output/bound_yang.py") # is .py right?
    PLUGIN_PATH = Path("venv/lib/python3.10/site-packages/pyangbind/plugin")
    command = [
        "pyang",
        "--path", model_path.as_posix(),
        "--plugindir", PLUGIN_PATH.as_posix(),
        "-f", "pybind",
        "-o", OUTPUT_PATH.as_posix(),
    ] + [path.as_posix() for path in model_path.glob("*.yang")]
    subprocess.run(command, check=True)

    print("running toy injection")
    with OUTPUT_PATH.open('r') as f:
        content = f.read()
    updated_content =  content.replace(
        'from pyangbind.lib.base import PybindBase',
        'from custom_pybind_base import CustomPybindBase as PybindBase')
    with OUTPUT_PATH.open("w") as f:
        f.write(updated_content)


    print("building yang")

    from importlib.util import module_from_spec, spec_from_file_location
    spec = spec_from_file_location(OUTPUT_PATH.stem, str(OUTPUT_PATH))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    print("testing!")

    try:
        instance = module.engineer()
        print("name: " + instance.engineer.name)
        print("age: "+ str(instance.engineer.age))
        print(instance.engineer.__dict__)
        print(str(instance.engineer.reboot))
        print(str(instance.engineer.reboot(20)))
        print(str(instance.engineer.delete_))
        print(str(instance.engineer.delete_()))
    except AttributeError as e:
        print(e)

    if do_pdb:
        import pdb
        from pprint import pprint as pp
        pdb.set_trace()


    print("finsihed!")
    print("")


test_yang(Path("custom-yang-simple"), 0)
test_yang(Path("custom-yang"), 1)