# mcs-format
Formatter for microchip studio AVR assembly files.  
Watches .asm files in selected microchip studio solution folder for changes, and formats the files.
Backups of .asm files will be saved at "./MCS-Format Backup" before each format.  Saves the most recent 30 versions with a UNIX timestamp.

This is in super beta and I would not trust your mission critical files to it.

There is a "auto reload files when changed outside the editor" feature in microchip studio, unfortunately it does not work.  To see the changes to a file, you have to close and re-open it within microchip studio.

Only works with the 4 types of input lines described in the AVR assembler manual:
1. [label:] directive [operands] [Comment]
2. [label:] instruction [operands] [Comment]
3. Comment
4. Empty line
Other types of input lines such as [label:] [Comment] are not implemented and may result in lost code.

Created by Joe Maloney for ECE 412 Lab1
