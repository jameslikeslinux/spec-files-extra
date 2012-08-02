#used by at least SFElibvanessa-* and SFEperdition.spec

%define perditionparentversion 1.19-rc4

#              ##NOTE## to version bumpers!
# enter version numbers into the defines below (spec files pick up this include
# file)
#%define libvanessa_adt_version $( wget -q -N -O - http://www.vergenet.net/linux/perdition/download/%{perditionparentversion}/ | grep "vanessa.*tar.bz2" | sed -e 's/.*href="//' -e 's/".*//' | grep _adt- )
%define libvanessa_adt_version 0.0.9
%define libvanessa_logger_version 0.0.10
%define libvanessa_socket_version 0.0.12

# for checking yourself, run this command and read the version numbers
# wget -q -N -O - \
#   http://www.vergenet.net/linux/perdition/download/%{perditionparentversion}/ \
#   | grep "vanessa.*tar.bz2" | sed -e 's/.*href="//' -e 's/".*//'
# vanessa_adt-0.0.9.tar.bz2
# vanessa_logger-0.0.10.tar.bz2
# vanessa_socket-0.0.12.tar.bz2


##TODO## possibly define the lib versions as well (tied to the download-version directory)

%changelog
* Mon Aug 02 2010 - Thomas Wagner
- add library version numbers (must be updated manually for now)
* Fri Jul  9 2010 - Thomas Wagner
- make the base download-directory maintained centrally

