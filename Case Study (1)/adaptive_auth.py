import subprocess
import shutil
import sys


# Define the command and its arguments
command = ['z3', '-smt2', '-st', 'test.txt' ]
final_model = ''
z3_model = ''


def do_command(utility):
    shutil.copy(z3_model,'test.txt')
    
    with open('test.txt', 'a') as file:
        file.writelines("(assert (>= Utility "+ utility+" ))\n(check-sat)\n(get-model)\n")
        
    return subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Run the command and capture the output

# Identifies the bottom value of the utility
def find_utility(utility):
        
    result = do_command(utility)
        
    if 'unsat' in result.stdout:
        
        with open('test.txt', 'r+') as file:
            
            file.truncate(0)
            
        return find_utility(str(float(utility)-0.1))
    else:
        return utility
        
        
# Identifies the upper value of the utility
def find_utility_upper(utility):
        
    result = do_command(utility)
        
    if 'unsat' in result.stdout:
            
            return str(float(utility))
    else:
        with open('test.txt', 'r+') as file:
            file.truncate(0)
        return find_utility_upper(str(float(utility)+0.01))
    




# Identifies the bottom value of the utility
def find_utility_bottom(utility):
    global final_model
    result = do_command(utility)
        
    if 'unsat' in result.stdout:
        
        with open('test.txt', 'r+') as file:
            
            file.truncate(0)
            
        return find_utility_bottom(str(float(utility)-0.001))
    else:
        final_model = result.stdout
        
        return utility
        
def get_line_after_string(string):
    lines = final_model.splitlines()
    
    for i, line in enumerate(lines):
        if string in line:
            # If we find 'Utility', return the next line
            if i + 1 < len(lines):  # Ensure there is a next line
                text = lines[i + 1]
                text = text[text.find('(/ ')+3:len(text)]
                if text.startswith('  1.0)'):
                    return 1.0
                if text.startswith('  0.0)'):
                    return 0.0
                n = text[:text.find(' ')]
                d = text[text.find(' ')+1:text.find(')')]
                return round(float(n) / float (d),3)
            else:
                return "No line after '" + string + "'."
    return "'"+string+"' not found in the output."
    

if len(sys.argv) > 1:
    user_input = sys.argv[1]  # First argument passed after the script name
    z3_model ='Scenario'+user_input+'/model-zu-'+user_input+'.txt'
    u = str(round(float(find_utility_upper(str(round(float(find_utility('1.0')),2) +0.01))),2))

    print("Utility: "+ find_utility_bottom(u)+"\n")


    print("Security: "+ str(get_line_after_string("Security"))+"\n")
    print("Usability: "+ str(get_line_after_string("Usability"))+"\n")
    print("Performance: "+ str(get_line_after_string("Performance"))+"\n")
    print("Total Risk: "+ str(get_line_after_string("TotalRisk"))+"\n")


else:
    print("Provide a command line argument (1 | 2 | 3)")



