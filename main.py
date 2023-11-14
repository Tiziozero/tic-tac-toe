from local_pvp import pvp_logic
from local_ai import ai_logic 
from online_code import online_logic

mode = 2
print("Modes:")
print("    [0] local pvp")
print("    [1] local ai")
print("    [2] online pvp")
print("    [3] online ai")
try:
    #mode = int(input("Enter mode: "))
    print(f"mode: {mode}")
except:
    print("Invalid input")
    quit()
# for test purposes
if mode == 0:
    pvp_logic.main()
elif mode == 1:
    ai_logic.main()
elif mode == 2:
    online_logic.main()
