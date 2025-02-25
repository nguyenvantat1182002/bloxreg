# from roblox import Roblox


# rblx = Roblox()


try:
    raise TimeoutError(123)
except (ZeroDivisionError, Exception) as ex:
    print(type(type(ex).__name__))
