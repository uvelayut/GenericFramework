*** Settings ***
Documentation    Suite description



*** Variables ***

${url}           https://yahoo.com
${url1}           https://google.com

*** Test Cases ***

Test title
    [Tags]    DEBUG
    Log    This is a Sample Text


