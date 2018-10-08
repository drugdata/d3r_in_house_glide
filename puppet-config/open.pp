class internalglide::open
{
  #epel repo
  exec { 'install_epel':
    command => '/bin/yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm',
    creates => '/etc/yum.repos.d/epel.repo'
  }

  Package { ensure => 'installed' }
  $python_deps    = [ 'python2-pip', 'python-psutil', 'python-virtualenv', 'python-tox', 'pylint', 'python-coverage' ]
  $perl_deps      = [ 'perl-Archive-Tar', 'perl-List-MoreUtils' ]
  $other_packages = [ 'libXft', 'openbabel', 'xorg-x11-xauth', 'screen', 'bzip2', 'which', 'rsync', 'ncftp', 'tk-devel', 'libXScrnSaver' ]
  $pymol_deps     = [ 'subversion', 'gcc', 'gcc-c++', 'kernel-devel', 'python-devel', 'tkinter', 'python-pmw', 'glew-devel', 'freeglut-devel', 'libpng-devel', 'freetype-devel', 'libxml2-devel', 'popt', 'popt-devel', 'cppunit', 'cppunit-devel', 'tcsh']
  $mesa_packages  = [ 'mesa-libGL-devel','mesa-libEGL-devel','mesa-libGLES-devel' ]
  $pip_packages   = [ 'argparse','psutil','biopython','xlsxwriter','ftpretty','wheel','flake8','lockfile','easywebdav','d3r', 'numpy' ]
  package { $python_deps: }
  package { $perl_deps: }
  package { $other_packages: }
  package { $mesa_packages: }
  package { $pymol_deps: }

  package { $pip_packages:
    ensure   => 'installed',
    provider => 'pip',
    require  => Package['python2-pip'],
  }

  # manual INSTALL Schrodinger
  exec { 'install_schrodinger':
    path => [ '/usr/bin', '/usr/sbin', '/bin', '/usr/local/bin'],
    command => 'cd /tmp;
                tar -xf Schrodinger_Suites*;
                cd Schrodinger_Suites*;
                ./INSTALL -d `pwd` -b -s /opt/schrodinger -k /tmp -t /opt/schrodinger/thirdparty *.gz;
                cd /tmp',
#    onlyif => '/bin/test -e /tmp/Schrod*.tar',
    creates => '/opt/schrodinger'
  }
}
# Run the class
class { 'internalglide::open': }
