#!/bin/bash

# color output, taken from Fedora init functions!
           BOOTUP=color
          RES_COL=60
      MOVE_TO_COL="echo -en \\033[${RES_COL}G"
 SETCOLOR_SUCCESS="echo -en \\033[1;32m"
 SETCOLOR_FAILURE="echo -en \\033[1;31m"
  SETCOLOR_NORMAL="echo -en \\033[0;39m"

function announce {
        echo
        echo "$1"
        echo
}

function step {
        echo -n "$1"
}

function verify {
        if [ $? -eq 0 ]; then
                [ "$BOOTUP" = "color" ] && $MOVE_TO_COL
                echo -n "["
                [ "$BOOTUP" = "color" ] && $SETCOLOR_SUCCESS
                echo -n $"  OK  "
                [ "$BOOTUP" = "color" ] && $SETCOLOR_NORMAL
                echo -n "]"
                echo -ne "\r"
                echo
                return 0
        else
                [ "$BOOTUP" = "color" ] && $MOVE_TO_COL
                echo -n "["
                [ "$BOOTUP" = "color" ] && $SETCOLOR_FAILURE
                echo -n $"FAILED"
                [ "$BOOTUP" = "color" ] && $SETCOLOR_NORMAL
                echo -n "]"
                echo -ne "\r"
                echo
                announce "Quitting!"
               exit;
                fi
}

function findreplace {
	sed -i "s/$1/$2/g" $3
}
