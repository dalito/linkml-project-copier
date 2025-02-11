def on_pre_build():
    import os
    os.system('just gendoc')
