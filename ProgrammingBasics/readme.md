# Programming For Non-Programmers From a Non-Programmer

Hey there, my name's Brant. I work in the cybersecurity field and would consider myself a professional in security-related areas of Information Technology (IT). Now, before you completely discredit me as someone who is actually a "programmer" only because I work in IT, let me explain why I don't think I am.

I'll start by clearing up something: Not all "tech" people know how to do all "tech" stuff. Funnily enough, most IT people will get fairly irritated if you ask them "Oh, you're a computer person?" It's just not fair to broaden their specific skillset(s) that much. Just like someone who works in the theater field doesn't always know how to "act", or someone in the business field may not know every facet of business, people in the IT field often don't know how to "program."

With that in mind, I graduated college with a cybersecurity degree. I am qualified to analyze a company's cyber defenses and do my best to keep the bad guys out and sensitive information safe. I do NOT "program" in the slightest. It's actually laughable how bad I am at it. I have enough experience in a bunch of different languages to talk about them here, but that's it.

At this point you're probably thinking, "Well there goes my small understanding of programming. What is "programming" then?" In my opinion, "programming" is a term used to describe someone who knows a certain computer language at an expert level and can develop applications that would take you and I decades to make if we started now. They spend 8+ hours at a keyboard every day writing code because they enjoy it and are Subject Matter Experts (SMEs) in it. Now, take that a step further: Not all programmers are SMEs in all languages. Just like not all spoken language interpreters can interpret every language on the planet, not all computer programmers can write in all computer languages.

If you've peeked into the programming headlines just long enough before you got overwhelmed, you might've seen "Python, Java, SQL, or HTML" in there somewhere. These are some very big name languages and are used A LOT in the tech industry just like how English, Spanish, and Chinese are big name spoken languages.

My goal here is to split up programming into digestable categories and explain what some of their languages are used for and how YOU could actually start using some of them in your own life as well.

#### Web Development

This category encapsulates languages like HTML, PHP, Swift, JavaScript, and others. They're used for creating the websites you see every day as you browse the internet. Each of them has their own unique pros and cons, and some can even be used together, but they're all focused on the same endgoal.

A good beginner language here is HTML. It is probably one of the most basic languages across all categories. Is that to say you'll get it right away? No! HTML takes some time to get used to, but you don't need any special software to make it or see it work. You'll need a text editor like Notepad (or Text Edit on Mac) and a web browser like Chrome, Firefox, etc... that's it! HTML code can be as simple as this:

```html
<html>
<p> Hello there! </p>
</html>
```

If we take a closer look at that code, we can see a pattern pop up where one "tag" opens without a slash (`<html>`) and another tag closes it (`</html>`) with a slash. These tags can be like a Russian Nesting Doll, where one may open and then a new one may open before the first one closes. You see this happen with the HTML and P tags. The HTML tag lets the browser know that whatever is inside of it is HTML code. The P tag tells the browser to display the text as "paragraph" text. It's that simple!

If web development sounds interesting as a hobby to you, try creating a personal "website" on your computer using HTML and these other languages. If it becomes fun enough, pursue hosting a real website online and using your code to build it.

#### Application Development

This cateogry is HUGE and gets big names like "Java, C, C++, and C#" to create many pieces of software the world uses on their computers every day. While these languages are much more complex than HTML, they are rewarding to learn at a basic level.

The best beginner language here is Java. Thankfully Java is one of, if not the most, popular languages on the planet. Tutorials and Q&A forums are found as far as the eye can see. Java is also the most important language to learn in my opinion because it teaches basic data structures like no other. What are those? Simply put, they're how computers interpret the English language into "computer understandable" words I guess. Here's an example:

```java
int mynumber = 10;
String myname = "Brant";
System.out.println(myname + " " + mynumber);
```

Now you might think this got way more complicated after reading that. To a certain extent, it did, but you can understand this I promise. The first line we "declare" a variable called `mynumber` as an integer (`int`). Hopefully you remember from middle school math that an integer is any whole number. In this case we assigned the value `10` to `mynumber`. The semicolon says we're done with that line. The next line we declared a variable `myname` and assigned the string value `"Brant"`. A string is simply a sequence of any number of characters, but they're interpreted differently than integers and other data types, which is why they get the quotes.

The next line is probably the most confusing. `System.out.println` is what we tell Java when we want it to display something on the screen. What we put inside of the parantheses is what we want it to display. In this case, I told it to put the `myname` variable plus a space (`" "`) plus the `mynumber` variable. This will end up displaying `Brant 10` when we run it.

Of course there is MUCH MUCH more to Java, but the best way to learn it is through baby steps that gradually build into more complex applications. If this sounds interesting to you, think of a small game or puzzle idea you've wanted to make and try to take that to Java. Emphasis on small though. You shouldn't need graphics or anything to play/solve it. You don't want to burn out just because the idea was too complex to start out with.

You'll need to download what's called an IDE (Integrated Development Environment) and the Java SDK. I recommend Netbeans as the IDE. It's free and straightforward. The Java SDK is located on their website.

#### Database Management

This category is focused on storing large amounts of data efficiently to make it quickly accessible by companies. The biggest name in this area is SQL (Structured Query Language, although nobody ever says the whole name). You'll hear it pronounced "See-quill" or "S-Q-L", but they're the same thing. SQL is known as a "relational database" language, which means that it connects different tables of data by creating relationships between certain areas. These relationships are often defined by the database "administrator" (the person in charge of it).

If you've used Microsoft Excel or another spreadsheet program, it can often be helpful to look at SQL through that lense where there are rows and columns and cells to track data. Here's an example:

```sql
CREATE TABLE Team (Name VARCHAR(15), Wins INT(2), Losses INT(2));
INSERT INTO Team (Name, Wins, Losses) VALUES ('Patriots', 10, 9), ('Eagles', 5, 14), ('Seahawks', 12, 7);
```

Again, it may look confusing at first, but let's look closer. The first line we're creating a table, kind of like when we create a new sheet inside Excel. We're calling this sheet `Team` and giving it three "columns": Name (which can vary in length up to 15 characters), Wins (which is a two digit integer), and Losses (which is a two digit integer). The semicolon tells SQL that we're done with the command. The next line we're inserting data into the `Team` table. We're telling it which columns we want to add the data to and giving it sets of values in that order.

So now we've added three rows of data for the table `Team`. You can see how these tables can grow to be MASSIVE for companies like Amazon or sports stats tracking websites and so on.

If this sounds interesting to you, try creating a SQL database on your own and adding data from a hobby or area of interest until there's enough of it where you can run some analysis on it. You'll need to download an application such as MySQL to create the database. Again, there are tutorials all over the internet to do this.

#### Scripting

What on Earth is "scripting!?" It gets lumped into the programming scope, but I like to think of it as a "brother" of sorts to programming. It is a way of automating one or more tasks. Think of the Ford assembly line. Back in the day, one person did one job over and over again which made the production process MUCH faster. Today, machines can do those tasks because they're very good at doing simple tasks very quickly.

What if there isn't just one thing to do, though? What if there are a whole slew of things to do and different places to go to get it? Also, what if all of those things need to happen within a computer not in the real world?

Enter Python! Full disclosure: this is my favorite language. It is very versatile and extremely good at automating tasks. Whenever I enounter a task, I look to see if whatever I'm doing is repetitive in some shape or form. If it is, I immediately look for a way to automate it: How is it repetitive? What steps are being repeated? Is it consistently repeated or is it just coincidence?

The most simple example of a task that can be automated is counting to high numbers. You could ask somebody to type into a computer the numbers 1 - 100, hitting Enter after each number OR you could automate it. How do I know it could be automated? The only thing changing throughout the whole process is the number being typed. Each iteration the person has to press the current number, press enter, then increase the number by one. Here's how you'd do it:

```py
number = 1
while number <= 100:
  print(number)
  number = number + 1
print("Counted to 100!")
```

Let's examine again.

1. The first line we're declaring an integer like we did in Java. The syntax is a little different because it's a different language, but we're declaring `number` with the value `1` since that's the number we were told to start with.

2. Then we enter what's called a "while loop". A while loop attempts to compare two values and conclude whether the comparison is true or false. In this case, we're comparing the `number` variable to the integer `100`. We know that the current value of `number` is `1` since that's what we declared it as. Hopefully you remember from middle school that `<=` means less than or equal to. So our current comparison would look something like "while 1 is less than or equal to 100", which is a TRUE statement; 1 is less than or equal to 100 the last time I checked! Since that statement is true, Python is allowed to evaluate the logic within the while loop. If it were false (which we'll get to soon), it would simply skip the logic inside the loop.

3. Now, within the loop, we're told to display the `number` variable (`print` is Python's version of `System.out.println` in Java) which is `1` right now. We then take the current value of `number` variable, which is `1`, and reassign it a value of `number + 1`. So now we have `number` equal to `2`.

4. Now we go back to the while loop comparison. 2 is still less than or equal to 100 so we run the logic again. This continues until `number` is equal to `101`. When the while loop comparison happens, it looks something like "while 101 is less than or equal to 100", which is FALSE because 101 is GREATER than 100. At this point, the loop is not run and we move on to print `Counted to 100!`.

So if we were to look at everything that got printed, we would see the numbers 1 through 100 then "Counted to 100!" printed out, just like what would've happened if a person were to do it... only this time it happened in nanoseconds rather than a minute.

Of course that is a VERY simple example, but you can look around in my GitHub for more complex examples such as NBAStatFinder or GroupMe or AutomatedWeather.

If Python sounds interesting to you, think about some very repetitive things that you've done on the computer for who knows how long and have probably started to annoy you by this point. What is repetitive about it? Could a dumb computer that works very quickly do this? Try writing out the logic without worrying about the code syntax to see how you would automate it, then go for it!

The great thing about Python is you don't need anything special to make it. All you really need is Notepad and a Powershell/Terminal prompt.

#### Conclusion

I've been around computers all my life and have always had an interest in them. Most of the IT world is interesting to me EXCEPT for hardcore programming where you spend 8+ hours a day at the keyboard writing code and finding miniscule mistakes that cause collosal problems. I would much rather examine cybersecurity postures within a company and sometimes write Python scripts to help me fix issues. The difference is I'm not spending 8+ hours to make a picture perfect script.

At the beginning of this whole file I mentioned that you could use something in here and apply it to your life. I think you'd most likely be able to use Python in some shape or form to make your life a bit easier, regardless of what industry you work in. I challenge you to find that area and learn this new skill along the way!

Until next time,

Brant
