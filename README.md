# mcs-format
Formatter for microchip studio AVR assembly files.  
Watches .asm files in selected microchip studio solution folder for changes, and formats the files.
Backups of .asm files will be saved at "./MCS-Format Backup" before each format.  Saves the most recent 30 versions with a UNIX timestamp.

This is in super beta and I would not trust your mission critical files to it.

There is a "auto reload files when changed outside the editor" feature in microchip studio, unfortunately it does not work.  To see the changes to a file, you have to close and re-open it within microchip studio.

Created by Joe Maloney for ECE 412 Lab1