
import os
def abs_path(filepath:str):
    components = filepath.split('/') if ('/' in filepath) else filepath.split('\\')
    dir_path = os.path.dirname(os.path.realpath(__file__))
    components.insert(0,dir_path)
    final_path = os.path.join(*components)
    os.makedirs(os.path.join(*components[:-1]),exist_ok=True)
    return(final_path)
def main():
    print(abs_path('src\\abc\\def.txt'))
if __name__ == '__main__':
    main()