Intermediate Events lose their properties when copied and pasted as Boundary Events
__Describe the Bug__

When an Intermediate Event is copied and pasted as a Boundary Event, it loses its properties. See the GIF: 

![bug2](https://user-images.githubusercontent.com/15003836/65767709-eba95880-e12e-11e9-836f-917776cc029e.gif)

__Steps to Reproduce__

1. Crete an Intermediate Event
2. Fill Async Continuations and/or Job Configurations fields
3. Copy it
4. Paste it onto a Task as a Boundary Event
5. Previously filled fields are now gone for the pasted Boundary Event.

__Expected Behavior__

As the properties are kept while pasting normally, they should not be gone when pasting as a BoundaryEvent as well.

__Environment__

 - OS: Mac OS Mojave 10.14.5
 - Library version: v5.0.5

