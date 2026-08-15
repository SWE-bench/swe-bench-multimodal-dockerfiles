@halocline I'm trying to understand the desire here. Is this still a valid issue given some of the direction to enforce the toolbar anatomy a bit more?
Promoting "Clear fliters" to top level should allow for clearing "quick filters" in addition to filters contained when `<DataFilters />` has `drop` or `layer`.

"Clear filters" should be available as a smart default and as a composable element.
After diving in to this work, here are some questions/behaviors we should be sure to solve for or file tickets for future enhancements:

The use case driving some of this discovery is when you might have DataSearch + one exposed filter + more filters hidden behind a layer:

![Image](https://github.com/grommet/grommet/assets/12522275/64303f87-1e74-496b-bc9a-b0cf4e786d35)

- [x] To get the label above a DataFilter, you need to wrap DataFilter in DataFilters. So, is it okay to have multiple `DataFilters`? **Yes, see notes below next question.**
- [x] Functionally, you can have a DataFilter outside of DataFilter and the filtering still works. What then is the specific purpose of DataFilters (we should document this)?
   - DataFilters is a means of presenting a group of filters together. If the filters are presented behind a drop or a layer, then DataFilters will also manage the presentation of the "Filter" button and track the badge count for that button via "touched" variable. Ultimately, multiple DataFilters can be used together in a single DataContext because Data relies on the "view" to drive which data should be shown.
- [x] If you have an exposed filter, you likely want the filtering to `updateOn="change"` but if you have the rest of the filters in a drop/layer then you likely would want filtering to `updateOn="submit"`. Should `updateOn` be available at the level of `DataFilters` as well for compositional use cases? **Yes, allow updateOn on individual DataFilters also, but fallback to the one of Data if not present.**
- [x] If caller is using their own `ClearFilters` control, there needs to be a way for them to turn off the ClearFilters that is built into DataFilters. What should this prop be called on DataFilters? `showClearFilters`?
   - **showClearFilters** aligns with other property conventions like Calendar `showAdjacentDays` or SelectMultiple `showSelectedInline`
- [x] If the caller is using their own `ClearFilters` control, should it always render by default and allow the caller to determine their own logic for when to hide it (such as when no filters are applied) or should `ClearFilters` have internal logic to hide itself when no filters are applied (similar to what is already happening in the DataFilters logic)?
   - **We will render by default. In future, we could introduce a property that would allow caller to opt-in to "smart hide" behavior, but this is not necessary for MVP**
- [x] Should `ClearFilters` be wrapped in a Box with flex={false} the way it is in DataFilters? If so, where should the `{...rest}` props spread (seems like the internal button would be ideal, but breaks common conventions)? **We will not wrap in flex false because this breaks common convention for button components. If we want an easy opt-in for Buttons not to flex, this should come from a more comprehensive solution. The caller can wrap the component with a Box with flex false if they want this behavior. (MVP mindset)**
- [x] Need a way for ClearFilters to have access to the `setTouched` handler from DataFilters
- [x] Should DataFilters have `drop` and `layer` as booleans or should those be string values under on prop? I recall some discussion about this early on but don't remember the rationale for leaving as booleans?
   - The reason to leave as booleans was so that they could also accept an object (either of drop or layer props) easily.
- [x] Should the component (since it's a subcomponent) be called `DataClearFilters`? **I'm proposing yes given the other conventions like "DataFilters" "DataFilter" "CardHeader" "CardBody" ...**

