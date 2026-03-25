import sys
from packaging.version import Version


def ok(msg):
    print(f'[OK] {msg}')

def fail(msg):
    print(f'[FAIL] {msg}')

if Version(sys.version.split()[0]) < Version('3.8'):
    fail(f'Your Python version is {sys.version}, we recommend 3.8 or newer')
else:
    ok(f'Your Python version is {sys.version}')


def get_packages(pkgs):
    versions = []
    for p in pkgs:
        try:
            imported = __import__(p)
            try:
                versions.append(imported.__version__)
            except AttributeError:
                try:
                    versions.append(imported.version)
                except AttributeError:
                    try:
                        versions.append(imported.version_info)
                    except AttributeError:
                        versions.append('0.0')
        except ImportError:
            versions.append('N/A')
    return versions


def check_packages(d):

    versions = get_packages(d.keys())

    for (pkg_name, suggested_ver), actual_ver in zip(d.items(), versions):
        if actual_ver == 'N/A':
            fail(f'{pkg_name} not installed or cannot be imported.')
            continue
        actual_ver, suggested_ver = Version(actual_ver), Version(suggested_ver)
        if pkg_name == "matplotlib" and actual_ver == Version("3.8"):
            fail(f'{pkg_name} {actual_ver}, please upgrade to {suggested_ver} >= matplotlib > 3.8')
        elif actual_ver < suggested_ver:
            fail(f'{pkg_name} {actual_ver}, please upgrade to >= {suggested_ver}')
        else:
            ok(f'{pkg_name} {actual_ver}')


if __name__ == '__main__':
    d = {
        'numpy': '1.21.2',
        'scipy': '1.7.0',
        'matplotlib': '3.4.3',
        'pandas': '1.3.2',
        'sklearn': '1.0',
        'torch': '1.8.0',
        'tensorflow': '2.6.0',
    }
    check_packages(d)
