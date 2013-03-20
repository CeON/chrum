chrum - The Apache Oozie Workflow Generator
=====
----

Check  [wiki page](.wiki/)

----

This project is currently UNSTABLE - please wait for full version

----

## For impatients

### General routine
1. Clone this repository into any localization ($CHRUM)
2. Prepare config.chrum, workflow.properties.chrum and workflow.xml.chrum files
3. Launch Chrum (a) python $CHRUM/full_chrum_action.py config.chrum workflow.properties.chrum workflow.xml.chrum
 
 
2. Redefine a stub workflow file
3. Change a configuration file according to your cluster setting as well as a set of properties used
4. Execute locally a script `./chrum-compile.sh` localizated in the folder $PROJECT/src/main/oozie
5. Execute `./chrum-ignit.sh $USER_NAME` localizated in the same folder as above
6. Check the execution status in a favourite web browser. 
7. Get your 
* scripts output in /$USER/workflows/mytask/$COMPILATION_TIME/$EXECUTION_TIME/results 
* scripts code in /$USER/workflows/mytask/$COMPILATION_TIME/$EXECUTION_TIME/scripts 
* libraries used in results in /$USER/workflows/mytask/$COMPILATION_TIME/$EXECUTION_TIME/libs 

### Working example
You can also

1. take a working example from the following github repository (...)
2. Execute locally a script `./chrum-compile.sh` localizated in the folder $PROJECT/src/main/oozie
3. Execute `./chrum-ignit.sh $USER_NAME` localizated in the same folder as above
4. Check the execution status in a favourite web browser. 
5. Get your 
6. scripts output in /$USER/workflows/mytask/$COMPILATION_TIME/$EXECUTION_TIME/results 
7. scripts code in /$USER/workflows/mytask/$COMPILATION_TIME/$EXECUTION_TIME/scripts 
8. libraries used in results in /$USER/workflows/mytask/$COMPILATION_TIME/$EXECUTION_TIME/libs

## About (for patient participants or cooled down impatient ones)
**chrum** has two basic goals:

1. Easy generate and maintain workflows for Apache Oozie.
2. Conveniently manage workflow/properties input as well as result keeping

### Workflow maintance
By using just a few chrum instructions you may make an Apache Oozie workflow.xml description more clear. 
To do so use following command:

* REPLACE -- (a) to define a portion of code and instantiate it in a usable places as well as (b) to extract the very core of each node (parameters and script name) to one, visible on one screen place
* FORK_MERGE -- to briefly describe e.g. executing an Apache Pig script with a combination of parameters from a given lists
* ACTION -- to briefly define a node, i.e. a name of a node, a destination node after success or failure.

### Properties description and results keeping
Furthermore, chrum gives you easy way to handle results of your calculations. 
Over regular Apache Oozie properties you can define dynamicly calculated variables like:

* *TIME_INFIX* - by this variable usage you can conveniently sort versions of submited code (scripts, JARs, configuration properties). As a stack of amendments in code grows, it is essential to keep in one place code and its results just to easily keep track on input-algorithm-output triple
* *OPTS_INFIX* - parallely to Apache Oozie configuration file keeping, options may be saved in a folder path, to see at glance, which set of parameters has been picked

With those dynamically calculated varibles, you can easily construct path to your HDFS store, where you can manage results of calculations, e.g. for a further comparison, which is essential in conducting efficient and convenient research.  

## Prerequirements
To fully levarage chrum and obtain top-quality experience in Apache Hadoop environment, including Apache Pig and Apache Oozie, one is adviced to follow a certain dojo described in the further parts of this section.

### Apache Pig
* use parameters to select localization and pick JAR libraries needed. Put all needed JAR files in one localization to obtain short and clear register section.

```
%DEFAULT commonJarsPath 'lib/*.jar'
REGISTER '$commonJarsPath'
```

* put all your Apache Pig scripts in one folder (do not create subdirectories) to ensure your Apache Pig scripts may be executed in Apache Oozie in the same manner as in the local mode
### Apache Oozie
* use configuration file over a workflow definition. You can use in a Apache Oozie workflow file parameters defined in Apache Oozie configuration file in Bash-wise style (${parameter_name})
* define a path to a libraries and using it as copying destination 
* As code is developed and stored in local file system, if one want to execute it in mapreduce mode copy to HDFS is needed. Gather all libraries, scripts, etc. and put them in one folder structure

## Quick Start

### Apache-Oozie-wise project organization
It is advisable to  following a very easy to apply the pattern of interaction with Apache Oozie. 
In Apache Oozie you can define a workflow, which defines a list of JARs or Pig scripts you want to execute as well as a properties files in which you can define (in a Bash-like manner) parameters’ values.

Assume the following Apache Oozie files location in a project folder:

```
$PROJECT
|--(files)
+-- SRC
     +-- MAIN
          |-- JAVA
          |-- RESOURCES
          |-- PIG
          +-- OOZIE
               |-- submit-to-oozie.sh
               |-- copy-to-oozie.sh
               +-- $TASK
                     |-- cluster.properties
                     |-- local.properties
                     +-- WORKFLOW
                           +-- workflow.xml
```

After selecting in copy-to-oozie.sh libraries needed, one can execute in $PROJECT/SRC/MAIN/OOZIE command

```
./subimt-to-oozie.sh $TASK $USER $OOZIE_SERVER $PROPERTIES_FILE
```

with the following results:
in the $TASK directory a LIB folder is created and indicated in copy-to-oozie.sh JAR files are passed to it
in the $TASK directory a PIG directory is created in which src/main/pig/*.pig files are copied
$TASK directory is copied to HDFS (path /user/${USER}/workflows/${TASK}/)
The workflow defined in $TASK/WORKFLOW/workflow.xml is executed
In time of execution values defined in the $PROPERTIES_FILE are substituted in a workflow
User may follow execution of the workflow in a web browser.

This way of organizing interaction with Apache Oozie is very straight-forward and convenient, but still you have to manage a localization of workflow output and changes in parameters by yourself.

### Tackling multiple parameters
chrum tends to create files and directories as described above. To do so it used file prototypes *.part1 (e.g. workflow.xml.part1, local.properties.part1, copy-to-oozie.sh.part1). First of all, one can state that a property in Apache Oozie configuration file prototype has multiple values, e.g.
```
my_1_value=13 #regular variable declaration
@my_2_value@ 3 5 7 #declaration with multiple values
@my_3_value@ a b c
```
Furthermore, in copy-to-oozie.sh or *.properties file prototypes a few additional variables may be used, like:
@TIME_INFIX@ - time of chrum assembly (./bake-oozie.sh ignition time)
@OPTS_INFIX@ - a combination of variables’ values (sorted in order of appearance in *.properties file)



To gain full benefit out of this product it is recommended to follow the beneath directory structure:
```
$PROJECT
|--(files)
+-- SRC
     +-- MAIN
          |-- JAVA
          |-- RESOURCES
          |-- PIG
          |-- PYTHON
          +-- OOZIE
               |-- (files)
               +-- $TASK
                     |-- $SOME_NAME.properties
                     +-- WORKFLOW
                           +-- workflow.xml
```

First of all, in a main directory holds java folder as well as oozie and python folders (code plugins from this project) and e.g. your Apache Pig pig folder.
The oozie contains:
Bash script bake-oozie.sh
Bash script submit-to-oozie.sh (and its subscript copy-to-oozie.sh)
Directory TASK
The key to interact with Apache Oozie in a convenient way is to extract properties (like a value of a threshold which will be passed via Apache Oozie to Apache Pig script) to the properties file and not hold them in a workflow file. To do so one should in the dedicated to Apache Oozie files oozie folder create a TASK folder.

### Instalation
The instation process may be simply performed by:

1. cloning this repository
```
cd ~
git clone git@github.com:CeON/chrum.git
```
2. and copying files straight to your project folder, e.g.
```
cp chrum/* ~/MYPROJECT/src/main
```
3. next, go to your oozie folder
```
cd ~/MYPROJECT/src/main/oozie
```
you can find there folder TASK
