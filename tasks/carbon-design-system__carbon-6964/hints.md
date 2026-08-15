Couple more notes:
- [The APG pattern for a Tabs component](https://w3c.github.io/aria-practices/#tabpanel) does not use nav or navigation role
- [Bootstrap Navs doc](https://getbootstrap.com/docs/4.0/components/navs/#regarding-accessibility) says not to use tab/tablist/tabpanel for navigation (which also means don't use navigation for tab/tablist/tabpanel)
thank you for reporting! I will hold off on making these changes until #6798 is resolved to avoid changes being overlooked or conflicts in merging the fixes
Ok, that makes sense. Until this is fixed, apparently setting the Tabs component's role to "none" is a (hacky but acceptable) work-around. e.g.

```
<Tabs role="none">
      <Tab label="Tab one">Tab content one</Tab>
      <Tab label="Tab two">Tab content two</Tab>
</Tabs>
```