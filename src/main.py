from src.parser.log_parser import LogParser

def main():
    parser = LogParser()
    for event in parser.parse("sample_logs/access.log"):
        print(event)

if __name__ == "__main__":
    main()