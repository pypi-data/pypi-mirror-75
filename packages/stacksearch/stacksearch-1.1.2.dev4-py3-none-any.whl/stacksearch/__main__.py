#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Bryan Hu .

@Bryan Hu .

Made with love by Bryan Hu .


Version: See __init__.py

Desc: The main file to use/execute when trying to search StackOverflow.

"""


def custom_main(args_: list) -> None:
    """For simulating the command line with custom arguments in your program.

    Parameters
    ----------
    args_ : list
        The list of arguments.

    Returns
    -------
    None

    """

    import sys
    import argparse
    from blessings import Terminal
    from pprint import pprint
    from . import __version__
    from .Search import Search

    parser = argparse.ArgumentParser(
        prog="StackSearch",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
    For searching StackOverflow and getting results that you can use.

    There are many other libraries/modules available that do the same
    thing. The reason you should use this is because this returns results that you can
    use. If ran from the command line, it'll return human readable results. If ran from
    another python script, it'll return some parsable JSON. Assuming you are utilizing
    this script's wonderful functions and objects.""",
        epilog=' \n Judge a man by his questions rather than by his answers" - Voltaire \n ',
    )
    try:
        parser.add_argument(  # Query
            "query", help="The query to search.", nargs="*", action="extend",
        )
    except ValueError:
        parser.add_argument(  # Python <3.8
            "query", help="The query to search.", nargs="*", action="append",
        )
    parser.add_argument(  # JSON
        "-j",
        "--json",
        "--raw-data",
        "-r",
        "--raw",
        help="For outputting JSON data that you can use.",
        action="store_true",
        default=False,
        dest="json",
    )
    parser.add_argument(  # Output
        "-o",
        "--output",
        help="The output file.",
        nargs="?",
        default=sys.stdout,
        action="store",
        dest="OUTPUT",
    )
    parser.add_argument(  # Silent
        "-s",
        "--silent",
        action="store_true",
        default=False,
        help="Don't print the progress.",
        dest="s",
    )
    try:
        parser.add_argument(  # Sites
            "--sites",
            action="extend",
            default=["stackoverflow"],
            nargs="+",
            help="The StackExchange sites to search.",
        )
    except ValueError:
        parser.add_argument(  # Python <3.8
            "--sites",
            action="append",
            default=["stackoverflow"],
            nargs="+",
            help="The StackExchange sites to search.",
        )
    parser.add_argument(  # Version
        "-v",
        "-V",
        "--version",
        action="store_true",
        default=False,
        help="Print the version number and exit.",
        dest="version",
    )

    args = parser.parse_args(args_)
    t = Terminal()
    if args.version:
        print(f"stacksearch version: {__version__}", file=args.OUTPUT)  # noqa
    elif not args.query:
        parser.print_help(file=args.OUTPUT)
    else:
        PRINT_PROGRESS = not args.s
        SITES_TO_SEARCH = set(args.sites)
        FILE = args.OUTPUT
        if PRINT_PROGRESS:
            print(f"Searching {', '.join(SITES_TO_SEARCH)}...")
        ANSWERS = []
        for site in map(str, SITES_TO_SEARCH):
            try:
                ANSWERS.append(
                    Search(
                        " ".join(args.query),
                        print_prog=PRINT_PROGRESS,
                        search_on_site=site,
                    )
                )
            except TypeError:
                ANSWERS.append(
                    Search(
                        " ".join(args.query[0]),
                        print_prog=PRINT_PROGRESS,
                        search_on_site=site,
                    )
                )

        if args.json:
            pprint(ANSWERS, stream=FILE, width=79)  # You will get unprocessed, raw JSON
        else:  # We got some parsing to do
            if PRINT_PROGRESS:
                print("Outputting results...")
            question_number = 0
            for answer in ANSWERS:
                question_number += 10
                print(t.bold("Answers from {}"))
                for question, answers in answer.items():
                    print(
                        f"{t.bold}{t.bright_green}Question #{question_number / 10}: {question}{t.normal}",
                        file=FILE,
                    )
                    print("\n")
                    try:
                        print(
                            f"{t.bright_yellow}{t.bold} Best Answer: {answers[0]}{t.normal}",
                            file=FILE,
                        )
                        print("\n\n\n", file=FILE)
                        try:
                            for question_answer in answers[1:]:
                                print(
                                    f"{t.green}Answer: {question_answer}{t.normal}",
                                    file=FILE,
                                )
                                print("\n\n\n", file=FILE)
                        except IndexError:
                            print(
                                f"{t.red}{t.bold}This is the only answer.{t.normal}",
                                file=FILE,
                            )
                    except IndexError:
                        print(
                            f"{t.bright_red}There were no answers for this question{t.normal}\n",
                            file=FILE,
                        )
                    else:
                        print("\n\n\n", file=FILE)
                    finally:
                        question_number += 1


async def fcustom_main(args_: list) -> None:
    """For simulating the command line with custom arguments in your program using the expiramental fSearch.

    Parameters
    ----------
    args_ : list
        The list of arguments.

    Returns
    -------
    None

    """

    import sys
    import argparse
    from blessings import Terminal
    from pprint import pprint
    from . import __version__
    from .Search import fSearch

    parser = argparse.ArgumentParser(
        prog="StackSearch",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
    For searching StackOverflow and getting results that you can use.

    There are many other libraries/modules available that do the same
    thing. The reason you should use this is because this returns results that you can
    use. If ran from the command line, it'll return human readable results. If ran from
    another python script, it'll return some parsable JSON. Assuming you are utilizing
    this script's wonderful functions and objects.""",
        epilog=' \n Judge a man by his questions rather than by his answers" - Voltaire \n ',
    )
    try:
        parser.add_argument(  # Query
            "query", help="The query to search.", nargs="*", action="extend",
        )
    except ValueError:
        parser.add_argument(  # Python <3.8
            "query", help="The query to search.", nargs="*", action="append",
        )
    parser.add_argument(  # JSON
        "-j",
        "--json",
        "--raw-data",
        "-r",
        "--raw",
        help="For outputting JSON data that you can use.",
        action="store_true",
        default=False,
        dest="json",
    )
    parser.add_argument(  # Output
        "-o",
        "--output",
        help="The output file.",
        nargs="?",
        default=sys.stdout,
        action="store",
        dest="OUTPUT",
    )
    parser.add_argument(  # Silent
        "-s",
        "--silent",
        action="store_true",
        default=False,
        help="Don't print the progress.",
        dest="s",
    )
    try:
        parser.add_argument(  # Sites
            "--sites",
            action="extend",
            default=["stackoverflow"],
            nargs="+",
            help="The StackExchange sites to search.",
        )
    except ValueError:
        parser.add_argument(  # Python <3.8
            "--sites",
            action="append",
            default=["stackoverflow"],
            nargs="+",
            help="The StackExchange sites to search.",
        )
    parser.add_argument(  # Version
        "-v",
        "-V",
        "--version",
        action="store_true",
        default=False,
        help="Print the version number and exit.",
        dest="version",
    )

    args = parser.parse_args(args_)
    t = Terminal()
    if args.version:
        print(f"stacksearch version: {__version__}", file=args.OUTPUT)  # noqa
    elif not args.query:
        parser.print_help(file=args.OUTPUT)
    else:
        PRINT_PROGRESS = not args.s
        SITES_TO_SEARCH = set(args.sites)
        FILE = args.OUTPUT
        if PRINT_PROGRESS:
            print(f"Searching {', '.join(SITES_TO_SEARCH)}...")
        ANSWERS = []
        for site in map(str, SITES_TO_SEARCH):
            try:
                ANSWERS.append(
                    await fSearch(
                        " ".join(args.query),
                        print_prog=PRINT_PROGRESS,
                        search_on_site=site,
                    )
                )
            except TypeError:
                ANSWERS.append(
                    await fSearch(
                        " ".join(args.query[0]),
                        print_prog=PRINT_PROGRESS,
                        search_on_site=site,
                    )
                )

        if args.json:
            pprint(ANSWERS, stream=FILE, width=79)  # You will get unprocessed, raw JSON
        else:  # We got some parsing to do
            if PRINT_PROGRESS:
                print("Outputting results")
            question_number = 0
            for answer in ANSWERS:
                question_number += 10
                print(t.bold("Answers from {}"))
                for question, answers in answer.items():
                    print(
                        f"{t.bold}{t.bright_green}Question #{question_number / 10}: {question}{t.normal}",
                        file=FILE,
                    )
                    print("\n")
                    try:
                        print(
                            f"{t.bright_yellow}{t.bold} Best Answer: {answers[0]}{t.normal}",
                            file=FILE,
                        )
                        print("\n\n\n", file=FILE)
                        try:
                            for question_answer in answers[1:]:
                                print(
                                    f"{t.green}Answer: {question_answer}{t.normal}",
                                    file=FILE,
                                )
                                print("\n\n\n", file=FILE)
                        except IndexError:
                            print(
                                f"{t.red}{t.bold}This is the only answer.{t.normal}",
                                file=FILE,
                            )
                    except IndexError:
                        print(
                            f"{t.bright_red}There were no answers for this question{t.normal}\n",
                            file=FILE,
                        )
                    else:
                        print("\n\n\n", file=FILE)
                    finally:
                        question_number += 1


def main() -> None:
    """This is the main function for the command-line interface.

    Parameters
    ----------
    None.

    Returns
    -------
    None
        None

    """
    import sys

    custom_main(sys.argv[1:])


if __name__ == "__main__":
    main()
