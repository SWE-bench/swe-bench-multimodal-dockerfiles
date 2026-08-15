Editor: Categories Accordion closes when autosave takes place


#### Steps to reproduce
1. Starting at URL: wordpress.com/post
2. Write some post content (before it saves)
3. Open the sidebar and add a category (before it saves) - leave it open
4. Wait for autosave

#### What I expected

Accordion to remain open

#### What happened instead

Accordion closes automatically on save

#### Browser / OS version

Chrome macOS

#### Screenshot / Video

![editor cat](https://user-images.githubusercontent.com/128826/43183813-c8289eb8-9029-11e8-9f76-f7671c63554e.gif)

#### Context / Source

Found by failing automated e2e tests which expect the categories accordion to remain open to add a tag

