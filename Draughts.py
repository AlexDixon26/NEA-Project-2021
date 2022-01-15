from UI import GUI
from sys import argv

def usage():  
    #prints how to use the game 
    print(f"""
Usage: {argv[0]} [g | t]
g : play with the GUI""")
    quit()

if __name__ == "__main__":
    #Main game runs
    if len(argv) != 2:
        usage()
    elif argv[1] == "g":
        ui = GUI()
    else:
        usage()
    
    ui.run()