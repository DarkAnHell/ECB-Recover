# ECB-Recover
Script to recover AES-ECB encrypted plain text files from known encrypted-plain pairs of files

<hr>

This script will load pair values (encrypted block - plaintext block) from a range of provided files, then use those known pairs and try to decrypt blocks on the target files.

All those files *must* have been encrypted with the same key and key length for this attack to be of any assistance.

# Example

./ecb_recover.py enc plain target out

Where:
  * enc == Folder containing the encrypted files with a known plain text counterpart
  * plain == Folder containing the plain counterparts of the previous encrypted files
  * target == Folder containing the encrypted files to be attacked
  * out == Optional folder on which the recovered data will be stored

*Note*: This script takes files from the "enc" and "plain" folders in the same order that they appear in the folder. Try naming the pairs with the same name to ensure a correct match up
