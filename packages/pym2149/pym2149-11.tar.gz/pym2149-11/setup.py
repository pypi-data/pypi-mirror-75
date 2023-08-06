import setuptools

def long_description():
    with open('README.md') as f:
        return f.read()

# Copyright 2013, 2014, 2015, 2016, 2017, 2020 Andrzej Cichocki

# This file is part of pyven.
#
# pyven is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyven is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyven.  If not, see <http://www.gnu.org/licenses/>.

class SourceInfo:

    class PYXPath:

        dotpyx = '.pyx'

        def __init__(self, package, name, path):
            self.package = package
            self.name = name
            self.path = path

        def make_ext(self):
            g = {}
            with open(self.path + 'bld') as f: # Assume project root.
                exec(f.read(), g)
            return g['make_ext'](self.package + '.' + self.name[:-len(self.dotpyx)], self.path)

    def __init__(self, rootdir):
        import os, setuptools, subprocess
        self.packages = setuptools.find_packages(rootdir)
        def g():
            for package in self.packages:
                dirpath = package.replace('.', os.sep)
                for name in os.listdir(os.path.join(rootdir, dirpath)):
                    if name.endswith(self.PYXPath.dotpyx):
                        yield self.PYXPath(package, name, os.path.join(dirpath, name))
        pyxpaths = list(g())
        if pyxpaths and os.path.isdir(os.path.join(rootdir, '.git')): # We could be an unpacked sdist.
            check_ignore = subprocess.Popen(['git', 'check-ignore'] + [p.path for p in pyxpaths], cwd = rootdir, stdout = subprocess.PIPE)
            ignoredpaths = set(check_ignore.communicate()[0].decode().splitlines())
            assert check_ignore.wait() in [0, 1]
            self.pyxpaths = [path for path in pyxpaths if path.path not in ignoredpaths]
        else:
            self.pyxpaths = pyxpaths

# Copyright 2013, 2014, 2015, 2016, 2017, 2020 Andrzej Cichocki

# This file is part of pyven.
#
# pyven is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyven is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyven.  If not, see <http://www.gnu.org/licenses/>.

def lazy(clazz, init, *initbefore):
    from threading import Lock
    initlock = Lock()
    init = [init]
    def overridefactory(name):
        orig = getattr(clazz, name)
        def override(*args, **kwargs):
            with initlock:
                if init:
                    init[0](obj)
                    del init[:]
            return orig(*args, **kwargs)
        return override
    Lazy = type('Lazy', (clazz, object), {name: overridefactory(name) for name in initbefore})
    obj = Lazy()
    return obj

# FIXME: The idea was to defer anything Cython/numpy to pyximport time, but this doesn't achieve that.
def cythonize(*args, **kwargs):
    def init(ext_modules):
        from Cython.Build import cythonize
        ext_modules[:] = cythonize(*args, **kwargs)
    return lazy(list, init, '__getitem__', '__iter__', '__len__')

def ext_modules():
    extensions = [path.make_ext() for path in sourceinfo.pyxpaths]
    return dict(ext_modules = cythonize(extensions)) if extensions else {}

sourceinfo = SourceInfo('.')
setuptools.setup(
        name = 'pym2149',
        version = '11',
        description = 'YM2149 emulator supporting YM files, OSC, MIDI to JACK, PortAudio, WAV',
        long_description = long_description(),
        long_description_content_type = 'text/markdown',
        url = 'https://github.com/combatopera/pym2149',
        author = 'Andrzej Cichocki',
        packages = sourceinfo.packages,
        py_modules = ['bpmtool', 'lc2txt', 'ym2portaudio', 'lc2wav', 'dosound2jack', 'midi2wav', 'ym2wav', 'dosound2wav', 'ym2txt', 'dosound2txt', 'ym2jack', 'midi2jack', 'dsd2wav', 'lc2jack'],
        install_requires = ['aridity', 'diapyr', 'lagoon', 'Lurlene', 'mynblep', 'outjack', 'Pillow', 'PyAudio', 'pyrbo', 'splut', 'timelyOSC'],
        package_data = {'': ['*.pxd', '*.pyx', '*.pyxbld', '*.arid', '*.aridt']},
        scripts = [],
        entry_points = {'console_scripts': ['bpmtool=bpmtool:main_bpmtool', 'dosound2jack=dosound2jack:main_dosound2jack', 'dosound2txt=dosound2txt:main_dosound2txt', 'dosound2wav=dosound2wav:main_dosound2wav', 'dsd2wav=dsd2wav:main_dsd2wav', 'lc2jack=lc2jack:main_lc2jack', 'lc2txt=lc2txt:main_lc2txt', 'lc2wav=lc2wav:main_lc2wav', 'midi2jack=midi2jack:main_midi2jack', 'midi2wav=midi2wav:main_midi2wav', 'ym2jack=ym2jack:main_ym2jack', 'ym2portaudio=ym2portaudio:main_ym2portaudio', 'ym2txt=ym2txt:main_ym2txt', 'ym2wav=ym2wav:main_ym2wav', 'mkdsd=ymtests.mkdsd:main_mkdsd']},
        **ext_modules())
