import sys

from wardoff import cli
from wardoff import tokenizer as tok
from wardoff import venv


def common_entry_point(func):
    def wrapper():
        func()
        keep_env = False
        if "-k" in sys.argv or "--keep-env" in sys.argv:
            keep_env = True
        if not keep_env:
            venv.destroy()

    return wrapper


@common_entry_point
def freeze():
    args = cli.freeze().parse_args()
    module_analyzer = args.project
    module_analyzer.retrieve_requirements()
    if not module_analyzer.requirements:
        print(f"No requirements used by {module_analyzer.project}")
    else:
        print("\n".join([str(el) for el in module_analyzer.requirements]))


@common_entry_point
def infos():
    args = cli.infos().parse_args()
    module_analyzer = args.project
    module_analyzer.retrieve_requirements()
    if not module_analyzer.requirements:
        print(f"No requirements used by {module_analyzer.project}")
    else:
        output = []
        for req in module_analyzer.requirements:
            # are we looking for specific python supported versions?
            if args.support:
                sup_ver = set(req.supported_python_versions())
                # are we support all searched versions?
                if not set(args.support).issubset(sup_ver):
                    # not, then ignore this project
                    continue
            if not args.no_separator:
                output.append("-----")
            for key in req.__dict__:
                if key == "metadata":
                    continue
                if args.filter and key not in args.filter:
                    continue
                val = str(req.__dict__[key])
                if "$$secure_url$$" in val:
                    val = val.replace("$$secure_url$$", "https")
                if "$$url$$" in val:
                    val = val.replace("$$url$$", "http")
                if key:
                    if args.no_key:
                        output.append(val)
                    else:
                        output.append(f"{key}: {val}")
            if not args.no_classifiers:
                if not args.filter:
                    output.extend(req.metadata)
        print("\n".join(output))


@common_entry_point
def main():
    args = cli.main().parse_args()
    module_analyzer = args.project
    module_analyzer.analyze()
    res = module_analyzer.get_results()
    if not res:
        print(f"No deprecations found in {module_analyzer.project}")
    else:
        print(module_analyzer.get_results())


@common_entry_point
def tokenizer():
    args = cli.tokenizer().parse_args()
    global verbosity
    verbosity = args.verbosity
    for el in tok.tokenizer(args.code, args.trim):
        print(el)


if __name__ == "__main__":
    main()
