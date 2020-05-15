# Solution

## Overview
We are taking multi-line input via stdin. The bash script reads & parses the input line by line and outputs to stdout. 
For parsing and removing the duplicates we are using the GNU/Linux version of sed. Sed is doing a substitute and replace for all duplicates found in a line.

## Regex
The regex used for matching duplicate words is \b\([a-z]\+\)[[:space:]]\1\b
While the regex for replacing these matched words is \1

### Breaking down the match regex

\b :- 
Using this at the start and end of the regexp to match complete blocks of words to avoid false cases. 
If the \b at the start is omitted an input of the form "nowtimes times" will be replaced by "times" as the first word will be partially matched. 
If \b at the end is omitted an input of the form "best bestnow" will be replaced by "best" as the second word will be partially matched.

([a-z]+) :- 
Additional forward slashes have been added in front of special characters in the solution to escape them. We are using a match group to match all combinations of one or more small letters.
(): match group
[a-z]+: matches all combination of one or more small letters from a to z

[[:space:]] :- 
As it implies this is being used to match one space, this is the format of regex to be used for sed. 
Since we are using this space to demarcate the difference between the two identical consecutive words, we don't need /b again at the end of the first word and at start of the second one.

\1 :- Matching the first capture group i.e whatever word is matched by the regex ([a-z]+), should be present again.

### Breaking down the replace regex

\1 :- Matching the first capture group, i.e replace the two identical words separated by a single space with only one of them
