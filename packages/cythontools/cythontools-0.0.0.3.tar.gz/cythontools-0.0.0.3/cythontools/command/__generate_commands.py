import pkgutil, importlib
import os.path


def __save_derivative_file(filename, parent_name, text):
    with open(filename, "w") as file:
        file.write("# AUTOMATICALLY GENERATED AS DERIVATIVE OF %s PACKAGE (cythontools)\n" % parent_name)
        file.write(text)


def __generate_derivatives(parent_name):
    base = parent_name.rsplit(".")[-1]
    prefix = "_" + parent_name.replace(".", "_") + "_"
    parent_mod = importlib.import_module(parent_name)

    children = []
    for entry in pkgutil.iter_modules(parent_mod.__path__):
        name, is_pkg = entry[1:]
        if is_pkg:
            print("%s is subpackage; skippping." % name)
        else:
            __generate_skbuild_derivative_file(parent_name, parent_mod, name)
            children.append(name)

    text = "".join(["from . import %s.%s as %s\n" % (name, name, name) for name in children])
    __save_derivative_file(parent_name.rsplit(".")[-1] + ".py", parent_name, text)


def __generate_skbuild_derivative_file(parent_name, parent_mod, name):
    mod = parent_mod.__dict__[name]
    prefix = "_" + parent_name.replace(".", "_") + "_" + name + "_"
    keys = [key for key in mod.__dict__.keys() if not key.startswith("_")]

    # Add the imports
    import_text = ["from %s.%s import %s as %s" % (parent_name, name, key, prefix + key) for key in keys]
    import_text = "\n".join(import_text) + "\n\n\n"

    # Create a derived class for class types
    class_text = ["class %s(%s):" % (key, prefix + key) for key in keys if type(mod.__dict__[key]) is type]
    class_text = "\n    pass\n\n".join(class_text) + "\n    pass\n\n\n"

    # For others, add a direct variable reference
    attr_text = ["%s = %s\n" % (key, prefix + key) for key in keys if not type(mod.__dict__[key]) is type]
    attr_text = "".join(attr_text)

#    with open(name + ".py", "w") as file:
#    "".join(["from . import %s.%s as %s\n" % (name, name, name) for name in children])
    __save_derivative_file(name + ".py", parent_name, import_text + class_text + attr_text)


if __name__ == "__main__":
    __generate_derivatives("skbuild.command")
