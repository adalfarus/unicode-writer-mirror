from dancer import config, start
from argparse import ArgumentParser


if __name__ == "__main__":
    app_info = config.AppInfo(
        False, True,
        "Unicode Writer",
        "unicode_writer",
        100, "b0",
        {"Windows": {"10": ("any",), "11": ("any",)}},
        [(3, 10), (3, 11), (3, 12), (3, 13)],
        {"logs": {}, "config": {}, "media": {}},
        ["./"]
    )
    config.do(app_info)

    from unicode_writer import UnicodeWriterApp

    parser = ArgumentParser(config.PROGRAM_NAME)
    # parser.add_argument("--load-config-path", type=str, default=None)
    start(UnicodeWriterApp, parser)
