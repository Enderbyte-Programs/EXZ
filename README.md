# EXZ
A format to zip executables

How to run an exz file.
If you are on Windows and have installed EXZ, simply double click and it will automatically run.

How to make an exz file:
Put your project in a folder with assets in a correct configuration so that if you run the executable, it will run correctly.
In the TOP LEVEL of your project folder, make a new file called EXZMANIFEST. Inside, put some data in a json structure. Here is an example manifest:

{
    "cwd" : ">EXTRACTDIR",
    "execute" : "HelloWorld.exe",
    "allowargs" : true 
}

cwd is the Current Working Directory your program will be run from. For most projects, >EXTRACTDIR is the best option.

execute is the command that will be run. In this case, just link it to your main executable, preferably also in the top level folder.

allowargs sets whether EXZ will pass arguments on to your software.

Save EXZ manifest, then highlight every file/directory in the top level of your project. Now we will be building the project. For this step, 7-Zip is the best but the Explorer ZIPPER will be fine. Create a zip archive out of your project. (EXZMANIFEST *MUST* be on the top level of the ZIP hierarchy). Rename to .exz and it is ready to run.
