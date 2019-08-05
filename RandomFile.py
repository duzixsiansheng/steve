import shutil, random, os
types = ['lsqxz', 'xcxjlybz', 'lslmqk', 'lsqbm', 'lsqdp', 'lsqlm', 'wtxztc' , 'xcxjlybz', 'xcxjqlm', 'xjjqls', 'xjjsd', 'xztc']
for names in types:
    dirpath = names
    destDirectory = names + '_sample'

    filenames = random.sample(os.listdir(dirpath), int(len(os.listdir(dirpath)) * 0.2))
    print(len(os.listdir(dirpath)))
    print(filenames)
    for fname in filenames:
        srcpath = os.path.join(dirpath, fname)
        shutil.copy(srcpath, destDirectory)

