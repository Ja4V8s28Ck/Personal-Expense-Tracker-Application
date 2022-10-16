## Assignments 1 - 3 \[All link expires on Nov 12th\]

## - [Assignment - I](https://ferry.s3.jp-tok.cloud-object-storage.appdomain.cloud/index.html)
## - [Assignment - II A](http://159.122.174.143:31837)
## - [Assignment - II B](http://159.122.174.143:32208)
## - [Assignment - II C](http://159.122.174.143:30458)
## - [Assignment - III](https://frustum.s3.jp-tok.cloud-object-storage.appdomain.cloud/index.html)


### Watson Assistant's actions and steps (Assignment III)

#### Flowchart and it's explanation

```mermaid
flowchart TD
	s[/Start Action/] --> greet
	greet(Greeting) --> a
	a(Is Covid really that dangerous?) --> b(Who's more prone to Covid?)
	b ==> c(What're the complications of Covid?)
	c ==> d{{Do you have any of the symptoms listed above??}}
	d ==> |NO| e(Asymptomatic)
	d ===> |YES| f(Based on symptoms)
	f ==> g1(Stage - I)
	f ==> g2(Stage - II)
	f ==> g3(Stage - III)
	e ==> h(Thanking Gesture)
	g1 ==> h
	g2 ==> h
	g3 ==> h
	h ==> j(Link to current Covid statistics)
	j ==> *[/End Action/]
```