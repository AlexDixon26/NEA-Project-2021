from UI import GUI
from sys import argv

def usage():   
    print(f"""
Usage: {argv[0]} [g | t]
g : play with the GUI
t : play with the Terminal""")
    quit()

if __name__ == "__main__":
    if len(argv) != 2:
        usage()
    #elif argv[1] == "t":
    #    ui = Terminal()
    elif argv[1] == "g":
        ui = GUI()
    else:
        usage()
    
    ui.run()