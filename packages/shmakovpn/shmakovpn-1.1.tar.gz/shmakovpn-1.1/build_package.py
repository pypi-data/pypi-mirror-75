import os
SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))


def run_build():
    os.chdir(SCRIPT_DIR)
    os.system('python setup.py test')
    os.system('python setup.py sdist bdist_wheel')
    print('__END__')


if __name__ == '__main__':
    run_build()
