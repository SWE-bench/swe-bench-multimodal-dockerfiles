The flexBasis rule does not work in v2.0.8.
The flexBasis rule does not work since I upgraded to version 2.0.8 from 1.6.14.
I have the following code:

```
<View
  style={{
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
  }}
>
  <Text style={{ flexBasis: "50%" }}>One</Text>
  <Text style={{ flexBasis: "25%" }}>Two</Text>
  <Text style={{ flexBasis: "25%" }}>Three</Text>
</View>
```

Before:
![image](https://user-images.githubusercontent.com/21165322/116717903-ca19ee00-a9af-11eb-89bd-7633c37bd21f.png)

After:
![image](https://user-images.githubusercontent.com/21165322/116718099-01889a80-a9b0-11eb-9d12-a15756b0a819.png)

