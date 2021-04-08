from connectsql import iss_path
p1 = iss_path()
try:
    p1.execute()
except Exception as e:
    print(e, flush=True)
    p1.execute()
finally:
    del p1


