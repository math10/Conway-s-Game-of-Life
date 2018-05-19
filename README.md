# Conway-s-Game-of-Life
Let assume this is a grid,
oxoo
oxox
xoxo
xxxo

where 'x' means live cell and 'o' means dead cell.

In api this grid considered as a single string and the single string is constructed by appending row order. For given grid, its database version should be this,
oxoooxoxxoxoxxxo

you can see that,
 Row0  Row1  Row2  Row3
(oxoo)(oxox)(xoxo)(xxxo)

Sample api for post grid with payload is,
```
http://127.0.0.1:8000/grids/
{
 "x" : 4,
 "y" : 4,
 "data": "oxoooxoxxoxoxxxo"
}
```
Query URL:
```
http://127.0.0.1:8000/grids/3/?after=1,2,3

{
    "id": 3,
    "x": 4,
    "y": 4,
    "data": [
        {
            "age": 1,
            "grid": "ooxoxxooxooxxoxo"
        },
        {
            "age": 2,
            "grid": "oxooxxxoxoxooxoo"
        },
        {
            "age": 3,
            "grid": "xxxoxoxoxoxooxoo"
        }
    ]
}
```
