*** Settings ***
Documentation    A test suite covering all smoke tests for windows plugin
Library    ../Lib/BaseTest.py
Resource   ../TestData/TestData.robot # When required



*** Test Cases ***
Test Notepad
    Log    Testing open notepad
    Start Application    notepad.exe
    sleep    1s
    Get Dialog    Untitled - NotepadNotepad
    Type    Edit    Test
    Menu Select    File->Save As...
    Get Dialog    Save As
    Type    edit1    test.txt
    Click    Save
    Close Application