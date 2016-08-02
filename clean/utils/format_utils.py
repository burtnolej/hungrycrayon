
import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/utils")
from misc_utils import enum

color=enum(burgundy="#85144B",
           orange="#FF851B",
           grey="#AAAAAA",
           lightblue="#39CCCC",
           darkblue="#001F3F",
           yellow="#FFDC00",
           green="#2ECC40",
           white="#FFFFFF",
           black="#000000")

ss16=enum(BOLD="false",
          ITALIC="False",
          NAME="SansSerif",
          SIZE="16")

ss14=enum(BOLD="false",
          ITALIC="False",
          NAME="SansSerif",
          SIZE="14")

ss18=enum(BOLD="false",
          ITALIC="False",
          NAME="SansSerif",
          SIZE="18")

ss14i=enum(ITALIC="true",
           BOLD="false",
           NAME="SansSerif",
           SIZE="14")


whiteblack14i = enum(STYLE="bubble",
                       COLOR=color.white,
                       BACKGROUND_COLOR=color.burgundy,
                       FONT=ss14i)

burgundywhite18 = enum(STYLE="bubble",
                       COLOR=color.white,
                       BACKGROUND_COLOR=color.burgundy,
                       FONT=ss18)

greyblack18 = enum(STYLE="bubble",
                   COLOR=color.black,
                   BACKGROUND_COLOR=color.grey,
                   FONT=ss18)


darkbluelightblue16 = enum(STYLE="bubble",
                           COLOR=color.lightblue,
                           BACKGROUND_COLOR=color.darkblue,
                           FONT=ss16)

yellowburgundy14 = enum(STYLE="bubble",
                        COLOR=color.burgundy,
                        BACKGROUND_COLOR=color.yellow,
                        FONT=ss14)

lightblueburgundy16 = enum(STYLE="bubble",
                           COLOR=color.burgundy,
                           BACKGROUND_COLOR=color.lightblue,
                           FONT=ss16)

blackgreen14 = enum(STYLE="bubble",
                    COLOR=color.green,
                    BACKGROUND_COLOR=color.black,
                    FONT=ss14)