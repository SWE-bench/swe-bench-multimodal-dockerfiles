I did a pass of looking at Data table in all sizes per story that we have in React. Maybe solving one of these things will solve it for multiple stories.

--------------------------------------------------------------------------------------------------

#### default
- [x] everything looks good

--------------------------------------------------------------------------------------------------

#### with batch actions
- [x] everything looks good

--------------------------------------------------------------------------------------------------

#### with batch expansion
- [x] The chevron with the `tall` size prop is misaligned in the header.
<img width="549" alt="Screen Shot 2020-06-02 at 1 38 33 PM" src="https://user-images.githubusercontent.com/43969356/83557026-89cb9a80-a4d6-11ea-8c5d-f75f7c5b7563.png">

- [x] The chevrons are misaligned and the cells are not adapting the right heights when the `short` and `compact` size props are applied.
<img width="493" alt="Screen Shot 2020-06-02 at 1 41 08 PM" src="https://user-images.githubusercontent.com/43969356/83557219-e29b3300-a4d6-11ea-968f-1240267d840a.png">

- [x] The text inside the expanded row needs to match the story for `with expansion`. I know this is just a demo, but we should be taking a stance on what we would suggest.

--------------------------------------------------------------------------------------------------

#### with boolean column
- [x] The cell heights are wrong for `none` `short` and `compact`.

--------------------------------------------------------------------------------------------------

#### with dynamic content
- [x] The header checkbox is too far to the right.
<img width="388" alt="Screen Shot 2020-06-02 at 1 48 21 PM" src="https://user-images.githubusercontent.com/43969356/83557773-d2d01e80-a4d7-11ea-9d3f-ea7b02e0c604.png">

- [x] The cell heights are wrong for `short` and `compact` and the chevrons and checkboxes are misaligned.
- [x] The text inside the expanded row needs to match the story for `with expansion`. 

--------------------------------------------------------------------------------------------------

#### with expansion
- [x] The cell heights are wrong for `short` and `compact` and the chevrons are misaligned.

--------------------------------------------------------------------------------------------------

#### with options
- [x] The header checkbox is too far to the right.
<img width="547" alt="Screen Shot 2020-06-02 at 1 53 24 PM" src="https://user-images.githubusercontent.com/43969356/83558331-7cafab00-a4d8-11ea-99c3-67e9e7fda624.png">

- [x] The text inside the expanded row needs to match the story for `with expansion`. 
- [x] The cell heights are wrong for `short` and `compact` and the chevrons and checkboxes are misaligned.

--------------------------------------------------------------------------------------------------

#### with overflow menu
- [x] everything looks good

--------------------------------------------------------------------------------------------------

#### with radio button selection
- [x] radio buttons are riding a little high in each row. Could come down a pixel. It is more noticeable in the short and compact sizes.
<img width="400" alt="Screen Shot 2020-06-02 at 1 58 53 PM" src="https://user-images.githubusercontent.com/43969356/83558862-44f53300-a4d9-11ea-9d38-0f95c2d43993.png">

--------------------------------------------------------------------------------------------------

#### with selection
- [x] everything looks good

--------------------------------------------------------------------------------------------------

#### with sorting
- [x] the column header text with `tall` size prop applied is too high. There should be 16px padding above the text.
<img width="395" alt="Screen Shot 2020-06-02 at 2 31 58 PM" src="https://user-images.githubusercontent.com/43969356/83562441-301b9e00-a4df-11ea-8740-82985b8c7133.png">


--------------------------------------------------------------------------------------------------

#### with toolbar
- [x] everything looks good
