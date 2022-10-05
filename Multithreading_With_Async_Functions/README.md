**Multithreading with async functions** in Python 3.9




In this demo case, a tester will run for a random period of time.

The main function will hold at max concurrently three testers.

A new tester will be run in a new thread after an old one has finished.

```
>py main.py

        starting tester : 1
        starting tester : 2
        starting tester : 3
tester.1 waiting .... 0
tester.2 waiting .... 0
tester.3 waiting .... 0
tester.3 has stopped after 1 seconds.
tester.2 waiting .... 1
tester.1 waiting .... 1
        starting tester : 4
tester.4 waiting .... 0
tester.1 waiting .... 2
tester.2 waiting .... 2
tester.4 has stopped after 1 seconds.
        starting tester : 5
tester.1 waiting .... 3
tester.2 waiting .... 3
tester.5 waiting .... 0
tester.1 waiting .... 4
tester.2 waiting .... 4
tester.5 has stopped after 1 seconds.
tester.2 waiting .... 5
        starting tester : 6
tester.1 waiting .... 5
tester.6 waiting .... 0
tester.2 waiting .... 6
tester.6 waiting .... 1
tester.1 waiting .... 6
tester.2 waiting .... 7
tester.6 has stopped after 2 seconds.
tester.1 waiting .... 7
tester.2 has stopped after 8 seconds.
        starting tester : 7
tester.1 has stopped after 8 seconds.
        starting tester : 8
        starting tester : 9
tester.7 waiting .... 0
tester.9 waiting .... 0
tester.8 waiting .... 0
tester.9 waiting .... 1
tester.7 waiting .... 1
tester.8 has stopped after 1 seconds.
        starting tester : 10
tester.9 waiting .... 2
tester.10 waiting .... 0
tester.7 has stopped after 2 seconds.
tester.9 waiting .... 3
tester.10 waiting .... 1
tester.9 waiting .... 4
tester.10 waiting .... 2
tester.9 waiting .... 5
tester.10 waiting .... 3
tester.9 waiting .... 6
tester.10 has stopped after 4 seconds.
tester.9 waiting .... 7
tester.9 has stopped after 8 seconds.
All Done.
```
