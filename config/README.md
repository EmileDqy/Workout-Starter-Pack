A session is a sequence of exerices : ["pushups", "plank"]

EXERCICE_MODE 0 : Each session will take the sequence in the same order.
EXERCICE_MODE 1 : Each session will shuffle the sequence 

For each sequence, you take the first N exercices.

MODE 0 : 1 session every N seconds.
MODE 1 : Given an interval of hours (ie [8, 10, 15, 20] = 8h to 10h and then 15h to 20h), do N sessions with M seconds between each one.

Each exercice is configurated as follow:

(type, f(x), x)

type 0 : This exercice consists of repetitions of a sequence of movements. We need to count those repetitions.
type 1 : This exercice is static, we need to time the user.

f(x) : the function is a mathematical function with x as a variable. It represents the number of repetitions or the number of seconds during which you have to maintain the position during the exercice.
Example : "ln(10+x) + 15"
/!\ : Make sure to put "".

x : THe number of time you have done this exercice. The x in f(x) will take its value.