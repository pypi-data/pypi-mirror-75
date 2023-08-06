import sys

from wardoff import cli
from wardoff import tokenizer as tok
from wardoff import venv


def common_entry_point(func):
    def wrapper():
        func()
        keep_env = False
        for el in sys.argv:
            if "-k" == el or "--keep-env" == el:
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
        if not args.details:
            print("\n".join([str(el) for el in module_analyzer.requirements]))
        else:
            for req in module_analyzer.requirements:
                print("")
                for key in req.__dict__:
                    val = str(req.__dict__[key])
                    if "$$secure_url$$" in val:
                        val = val.replace("$$secure_url$$", "https")
                    if "$$url$$" in val:
                        val = val.replace("$$url$$", "http")
                    if key:
                        print(f"{key}: {val}")


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
