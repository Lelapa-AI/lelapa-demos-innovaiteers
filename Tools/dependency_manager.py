import os
#DO NOT IMPORT MODULE ANYWHERE JUST RUN THE SCRIPT

def install_dependencies():
    os.system('pip install google-cloud-vision')
    os.system('pip install google-generativeai')
    os.system('pip install -r requirements.txt')

def update_dependencies():
    os.system('pip install --upgrade google-cloud-vision')
    os.system('pip install --upgrade google-generativeai')
    os.system('pip install --upgrade -r requirements.txt')

def save_dependencies():
    os.system('pip install pipreqs')
    os.system('pipreqs .')


if __name__ == '__main__':
    install_dependencies()
    update_dependencies()
    save_dependencies()

#DO NOT IMPORT MODULE ANYWHERE JUST RUN THE SCRIPT