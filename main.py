from connectsql import iss_path


def main():
    p1 = iss_path()
    try:
        p1.execute()
    except Exception as e:
        print(e, flush=True)
        del p1


if __name__ == '__main__':
    main()
