# Tiny brainfuck experiments

A little while ago, I had an assignment the goal of which was designing an algorithm to solve some problem efficiently. I don't remember what the problem was anymore. What's important is that the problem required a single true/false answer, and that for each test case we knew whether the code failed. The idea to use this as a sidechannel to leak the test cases emerged pretty quickly. Then I joined in, and used the execution time and memory used as extra sidechannels - we had access to those as well. Pretty quickly we knew the index and value of the first unique character in each test case, leading to impossibly fast solutions.

Then, I decided that I want to submit my assignment in brainfuck. Why not? The problem was, for several of the test cases, the first unique character was a couple thousand characters in. So I needed a way to read a precise number of characters. A number into the thousands. In brainfuck. Of course, I could just spam a couple megabytes of the read command. But I wanted to be just a bit more efficient. As in, I wanted the brainfuck program to be as small as I can get it.

So, the solution was generating loops. This is a collection of scripts I very quickly wrote (the assignment was due in a couple hours) that let me accurately input thousands of characters. I'm writing this readme half a year after the assignment, so I don't really remember how it works, and don't have the energy to read it all and try to understand. Iirc, the basic idea is that, for example, by just incrementing a cell, you get a loop of length 255, and within it you can read several characters, and have a nested loop that also reads several characters per iteration.

My brainfuck solution ended up being 950 bytes. If I remember it all right, it was only ever beaten by my own C solution, and the only other solution that came close was one hardcoded in java. Moral of the story: if you have cool teachers and know brainfuck, you actually can get away with hardcoding the testcases.

These scripts were just chilling in my projects directory, so I decided to upload them as is, in case anyone finds them interesting.
