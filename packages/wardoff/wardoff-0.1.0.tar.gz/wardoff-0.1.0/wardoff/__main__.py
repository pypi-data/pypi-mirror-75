from wardoff import cli
from wardoff import tokenizer as tok


def freeze():
    args = cli.main().parse_args()
    module_analyzer = args.project
    _ = args.output
    module_analyzer.retrieve_requirements()
    if not module_analyzer.requirements:
        print(f"No requirements used by {module_analyzer.project}")
    else:
        print("\n".join([str(el) for el in module_analyzer.requirements]))


def main():
    args = cli.main().parse_args()
    module_analyzer = args.project
    _ = args.output
    module_analyzer.analyze()
    res = module_analyzer.get_results()
    if not res:
        print(f"No deprecations found in {module_analyzer.project}")
    else:
        print(module_analyzer.get_results())


def tokenizer():
    args = cli.tokenizer().parse_args()
    global verbosity
    verbosity = args.verbosity
    for el in tok.tokenizer(args.code, args.trim):
        print(el)


if __name__ == "__main__":
    main()
