*** Settings ***
Documentation    Suite description

Library    libs/ui/ExtendedSeleniumLibrary.py


*** Variables ***

${url}           https://yahoo.com
${url1}           https://google.com

*** Test Cases ***

Test title
    [Tags]    DEBUG
    Open Browser      ${url}
    Close Browser
    Open Browser    ${url1}
    Close Browser


