from src.parser.log_parser import LogParser


def run(logfile, metrics):
    parser = LogParser()
    for event in parser.parse(logfile):
        for metric in metrics:
            metric.consume(event)
    return metrics