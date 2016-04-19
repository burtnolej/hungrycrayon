

# shell command to get directories created and files copied by 'make install'
make install -n | egrep "^cp|^mkdir|^list"



if cmd_str.startswith("list"):
    splits = cmd_str.split(";")
    
elif cmd_str.startswith("mkdir):
elif(cmd_str.startswith("cp"):
     
     
     
'''

list

list, test = split
list='electricsheep'; test -n "/usr/local/bin" || list=; \
list='electricsheep-preferences'; test -n "/usr/local/bin" || list=; \
mkdir -p /usr/local/bin
mkdir -p /usr/local/share/electricsheep/Scripts
mkdir -p /usr/local/share/applications
mkdir -p /usr/local/share/pixmaps
mkdir -p /usr/local/share/electricsheep/icons
mkdir -p /usr/lib/gnome-screensaver
cp -rf ./Runtime/Scripts /usr/local/share/electricsheep
mkdir -p /usr/local/share/applications/
cp -f ./menu-entries/ElectricSheep.desktop.kde /usr/local/share/applications/ElectricSheep.desktop
mkdir -p /usr/local/share/pixmaps/
cp -f ./menu-entries/electricsheep.xpm /usr/local/share/pixmaps/
cp -f ./Runtime/electricsheep-attr.png /usr/local/share/electricsheep/
cp -f ./Runtime/electricsheep-frown.png /usr/local/share/electricsheep/
cp -f ./Runtime/electricsheep-smile.png /usr/local/share/electricsheep/
cp -f ./Runtime/TrebuchetMS-20.glf /usr/local/share/electricsheep/
cp -f ./Runtime/TrebuchetMS-24.glf /usr/local/share/electricsheep/
mkdir -p /usr/local/bin
cp -f ./electricsheep-saver /usr/local/bin && chmod a+rx /usr/local/bin/electricsheep-saver
mkdir -p /usr/share/applications/screensavers/
cp -f ./menu-entries/electricsheep-saver.desktop /usr/share/applications/screensavers/electricsheep.desktop
mkdir -p /usr/lib/gnome-screensaver
cp -f ./electricsheep-saver-gnome /usr/lib/gnome-screensaver/electricsheep-saver && chmod a+rx /usr/lib/gnome-screensaver/electricsheep-saver
list='AUTHORS README NEWS ChangeLog Runtime/Instructions.rtf Runtime/License.rtf'; test -n "/usr/local/share/doc/electricsheep-2.7b33-svn" || list=; \
'''
