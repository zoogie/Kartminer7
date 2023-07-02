# Kartminer BETA

## Thanks 
- wwylele for [save3ds](https://github.com/wwylele/save3ds) Installing the exploit to extdata from just seedminer and a PC would be impossible without this tool.
- PabloMK7 for [3dsropxploitinjector](https://github.com/PabloMK7/3dsropxploitinjector) which makes tricky exploits like this much less of a hassle. Do you know he is also the author of a different mk7 exploit [kartdlphax](https://github.com/PabloMK7/kartdlphax), and ALSO the famous mk7 plugin [CTGP-7](https://ctgp-7.github.io/)?
- Yellows8 for this enduringly useful tool: [3ds_ropkit](https://github.com/yellows8/3ds_ropkit)

## What is this?
This is a BETA stage exploit for Mario Kart 7. This is the 3rd public exploit of this extremely popular game, this time targeting the extdata savegame on the sd card. It works with both the digital and cartridge version of the game on app version 1.2.

## Bugs, how?
The flaw was found by simply fuzzing the entire 1MB+ of extdata save file, creatively named "data.dat", with continuous, indexed u32s. This resulted in multiple crashes, with some contexts having my fuzzed data showing up in various registers, and near branch instructions. The wide scope of this fuzzing naturally crashed multiple threads, but those were pretty easily handled by spraying their stacks with sleeping gas :p The US version 1.2 of the source code has comments if you need more precise (and messy) info.

## Directions
-- Prereqs: 
* UNHACKED USA, EUR, or JPN new3ds or old3ds.
* An eShop, pack-in, or cartridge version of Mario Kart 7 (pack-in means it came with your system out of the box)
* Mario Kart 7 needs to be updated to game version 1.2. If you've played online recently, this should already be the case.
* Windows PC with sd reader

-- Prep:<br>
a. Update your 3DS to 11.17 <br>
b. Do https://3ds.hacks.guide/seedminer.html but STOP it and continue here when you get your system's movable.sed file. Place movable.sed inside the resources folder.<br>
c. Boot up your 3ds and start mk7 and tap "Mario Kart Channel" at the bottom and then "Streetpass List" also at the bottom. Then agree to all the prompts to get sd extdata, spotpass, streetpass, etc. initialized. 
Skip this if you've already done it of course.<br>
d. Turn off Wifi on your 3DS. The reason is spotpass could download and erase the exploit payload with it on.<br>

-- Optional (but highly recommended)
Backing up your extdata save<br>
a. Place your 3DS sd card into your PC and make note of the Drive Letter. (Usually E-I, but could be higher letter)<br>
b. Go inside the "backup" folder and double click the backup_???.bat script where ??? is your 3DS's region.<br>
If it errors, open up the .bat script you clicked with notepad and check that the drive letter  ' --sd "F:"  ' matches yours. Change it and save if it's different.<br>
c. A folder like 306, 307, or 308 should appear in the backup folder if the backup worked. <br>
After the exploit is finished and you've installed cfw, you may run the restore_???.bat to restore your old unhacked save.<br>

Instructions:

1. Place your 3DS sd card into your PC and make note of the Drive Letter. (Usually E-I, but could be higher letter)

2. In the Release folder, double click on the .bat that matches your 3DS's model type and region. 
If it errors, open up the .bat script you clicked with notepad and check that the drive letter  ' --sd "F:"  ' matches yours. Change it and save if it's different.

3. Your hax upload worked if there is no red text and it says "finished" at the end.

4. Turn your 3ds on, boot mk7, and go to Mario Kart Channel -> Streetpass List -> Press A repeatedly (but slowly) to get past all the menu screens until the hax launches.

5. If successful, you should arrive at a black and white screen titled "3DS ROP xPloit Injector". You now have a choice of further exploits to install, unsafe_mode or menuhax67, but that's the subject of another tutorial!
Enjoy!

## Q&A

Q: Omg, online cheaters will thrive! How could you?<br>
A: The user has to knowingly install the exploit to their sdmc extdata using seedminer and a PC tool, it's not RCE in any way.<br>
Q: This could mess up my save!<br>
A: While I offer backup procedures in the instructions, I can make no guarantees this exploit can't mess up the overall savegame state somehow. I have no idea how the extdata save (or spotpass/streetpass) interacts with the normal savegame, for instance. This is why I need testers, and why I am calling this a BETA! Let's find out!<br>
Q: Why can't I just run kartdlphax?<br>
A: Well you certainly can, it's a great exploit. In fact, I'd recommend kartdlphax over Kartminer7, but you do need a 2nd hacked 3ds for it. If you don't have a 2nd hacked 3ds, I think kartminer7 could work well for you (after the beta phase, of course).<br>
Q: Hi, I'm a famous youtube content creator and I'd like to make a video tutorial out of this exploit and not mention or attribute you in any way!<br>
A: That's not a question, and no, you DO need to give me a shoutout for the work I put into writing these exploits while voluntarily refusing pay for it. It's just common courtesy.<br>