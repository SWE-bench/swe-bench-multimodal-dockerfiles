React code example reproducing the issue: https://codesandbox.io/s/sidenavissues-jtrzb

Result here: https://jtrzb.csb.app/#/
To reproduce:
- Reduce viewport width to less than 40rem, so that the HeaderMenuButton is displayed on the top-left corner.
- Click on the menu button to display the SideNav.
- Click on the different zones (see picture above in section "Additional information") does not close the SideNav, as expected.

Related issues with keyboard navigation:
- pressing the Enter-key when a SideNavLink is selected does not close the side navigation
- pressing the ESC-key does not close the side navigation
@nxn-4-wdf hey man, i ran into this problem too. just change your <Header component to look like this: 

```
<HeaderContainer
        render={({ isSideNavExpanded, onClickSideNavExpand }) => (
          <Fragment>
            <Header
              aria-label="nxn-4-wdf's Totally Tubular Application Worth Millions"
              onClick={
                isSideNavExpanded === true ? onClickSideNavExpand : null
              }>
```

tadaaaaa
@nxn-4-wdf yo. i ran into another problem where the sidenav stays there if you resize the browser so i amended the code to look like this. this fixes both the click out issue you describes as well as a broken ghosted sidenav on resize

```
      <HeaderContainer
        render={({ isSideNavExpanded, onClickSideNavExpand }) => {
          window.addEventListener(
            'resize',
            () => {
              const viewportWidth =
                window.innerWidth || document.documentElement.clientWidth;
              if (viewportWidth > 1056) {
                if (isSideNavExpanded === true) onClickSideNavExpand();
              }
            },
            false
          );
          return (
            <Fragment>
              <Header
                aria-label="Carbon Tutorial"
                onClick={
                  isSideNavExpanded === true ? onClickSideNavExpand : null
                }>
```
@dryhurst Thanks for your code!
I have used it in my code and solves all the use cases except one:
- It calls onClickSideNavExpand on clicking on the sidebar link items, but does not hide the sidenav panel. It is weird because I can see how it removes the overlay background and change the header menu button... I think maybe the nav items is preventing it to be closed when they get the focus.

```
<HeaderContainer
          render={({ isSideNavExpanded, onClickSideNavExpand }) => {
            window.addEventListener(
              'resize',
              () => {
                const viewportWidth =
                  window.innerWidth || document.documentElement.clientWidth;
                if (viewportWidth > 1056) {
                  if (isSideNavExpanded === true) onClickSideNavExpand();
                }
              },
              false
            )

            return (
              <Fragment>
                <Header
                  aria-label="my app"
                  onClick={ isSideNavExpanded === true ? onClickSideNavExpand : null}
                  >
                  <SkipToContent />
                  <HeaderMenuButton
                    aria-label="Open menu"
                    onClick={onClickSideNavExpand}
                    isActive={isSideNavExpanded}
                  />
                  <HeaderName element={NavLink} to="/" prefix="">
                    MyApp
                  </HeaderName>
                  <HeaderNavigation aria-label="Carbon Tutorial">
                    <HeaderMenuItem element={NavLink} to="/about">About</HeaderMenuItem>
                    <HeaderMenuItem element={NavLink} to="/help">Help</HeaderMenuItem>
                    <HeaderMenuItem element={NavLink} to="/contact">Contact</HeaderMenuItem>
                    <HeaderMenuItem element={NavLink} to="/theme">Theme</HeaderMenuItem>
                  </HeaderNavigation>
                  <SideNav
                    aria-label="Side navigation"
                    expanded={isSideNavExpanded}
                    isPersistent={false}>
                    <SideNavItems>
                      <HeaderSideNavItems>
                        <HeaderMenuItem element={NavLink} to="/about">About</HeaderMenuItem>
                        <HeaderMenuItem element={NavLink} to="/help">Help</HeaderMenuItem>
                        <HeaderMenuItem element={NavLink} to="/contact">Contact</HeaderMenuItem>
                        <HeaderMenuItem element={NavLink} to="/theme">Theme</HeaderMenuItem>
                      </HeaderSideNavItems>
                    </SideNavItems>
                  </SideNav>
                </Header>
              </Fragment>
          )}}
        />
```

Thanks!

Hey, I have solved it with a workaround, I have identified that by clicking on the nav items it didn't remove the bx--side-nav--expanded class of the side nav panel.

```
<SideNav
   aria-label="Side navigation"
   expanded={isSideNavExpanded}
   isPersistent={false}
   className="global_sidenav">
      <SideNavItems>
         <HeaderSideNavItems>
            <HeaderMenuItem element={NavLink} to="/about" onClick={hideSideNav}>About</HeaderMenuItem>
            <HeaderMenuItem element={NavLink} to="/help" onClick={hideSideNav}>Help</HeaderMenuItem>
            <HeaderMenuItem element={NavLink} to="/contact" onClick={hideSideNav}>Contact</HeaderMenuItem>
            <HeaderMenuItem element={NavLink} to="/theme" onClick={hideSideNav}>Theme</HeaderMenuItem>
         </HeaderSideNavItems>
      </SideNavItems>
</SideNav>
```

```
const hideSideNav = () => {
    var sidenav = document.getElementsByClassName('global_sidenav');
    sidenav[0].classList.remove('bx--side-nav--expanded');
  };`
> @nxn-4-wdf hey man, i ran into this problem too. just change your <Header component to look like this:
> 
> ```
> <HeaderContainer
>         render={({ isSideNavExpanded, onClickSideNavExpand }) => (
>           <Fragment>
>             <Header
>               aria-label="nxn-4-wdf's Totally Tubular Application Worth Millions"
>               onClick={
>                 isSideNavExpanded === true ? onClickSideNavExpand : null
>               }>
> ```
> 
> tadaaaaa

this will trigger when you try to expand a sidenav menu as well.

```
let onHeaderClick = (evt, hprops) => {
  if(evt.target.className.includes && evt.target.className.includes('nav__overlay')) {
    hprops.onClickSideNavExpand(evt)
  }
}

<HeaderContainer render={hprops => (
  <Header aria-label="example" onClick={(evt) => {onHeaderClick(evt, hprops)}}>
)} />
```
HeaderMenuButton not rendering on Chrome but I can see it when I open the CodeSandBox, any reason for this?
> HeaderMenuButton not rendering on Chrome but I can see it when I open the CodeSandBox, any reason for this?
```
<HeaderMenuButton
    aria-label="Open menu"
    onClick={onClickSideNavExpand}
    isActive={isSideNavExpanded}
/>
```
make sure you have this added. also.. this appears only on low width pages. (max ~1050px)
Is there a way to display the HeaderMenuButton even if the page width is more than 1050px? And when the HeaderMenuButton is expanded the background is not greyed out.
^would like to second this question. Basically, is there a way to turn responsiveness off through props or something? It seems odd it forces you to use responsiveness.
cc @carbon-design-system/design do we have a spec that covers the expand/collapse behavior for the sidenav? also is the expand/collapse behavior only available at smaller screen sizes?
@here So the current Storybook may have a bug issue with it. But this old issue has the correct specified interaction spec in its and should resolve the current issues with the SideNav in Storybook. 

https://github.com/carbon-design-system/carbon/issues/2335#issuecomment-491885393

![](https://user-images.githubusercontent.com/11670886/57636572-00fe5b80-756f-11e9-8d41-8d32108373c3.png)
