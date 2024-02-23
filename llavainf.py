import subprocess
import sys

def get_description(filename):
    command = ["ollama", "run", "llava:13b", "What is in this image", filename]
    output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    command_output = output.stdout
    return command_output

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python llavainf.py <filename>")
    else:
        filename = sys.argv[1]
        description = get_description(filename)
        print(description)
