Hi @aagonzales , As I understand the issue, you want a dev to impliment the `xl` varient to the current button based on the spec provided. If that is the task, then please assign me this issue as I would love to work on it.
Hi @aagonzales , I've taken some time to setup the project locally and familiarize myself with different parts of this monorepo. I noticed that the button is implimented as both an SCSS partial (under [carbon/packages/components/src/components/button/](https://github.com/carbon-design-system/carbon/tree/master/packages/components/src/components/button) ) and a react component under [carbon/packages/react/src/components/Button](https://github.com/carbon-design-system/carbon/tree/master/packages/react/src/components/Button). 

Does this issue encompass implementing this feature to both react button and vanilla JS button separately? Sorry if this is an ignorant question 😅
@Abdul-Sen Hello! Thanks for picking this up. We only require the React version to be built but the Vanilla JS would be extra credit. 

And yes adding the `xl` variant is the task. There is also a task of adding the `large` variant as well at 64px.