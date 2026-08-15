Store: Settings: Email: Undecoded entity in From-Name placeholder
Observed on today's master

#### Steps to reproduce
1. On a site with an encodable character in its Site Title (e.g. Allendav's Store Test)
2. Starting at URL: http://calypso.localhost:3000/store/settings/email/{DOMAIN}
3. Clear the From Name field
4. See the undecoded entity

<img width="993" alt="entity" src="https://user-images.githubusercontent.com/1595739/35405551-58f061cc-01bb-11e8-85bf-e80cf159d485.png">

